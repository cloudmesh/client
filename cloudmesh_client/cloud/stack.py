# this is where the stack class is implemented

from __future__ import print_function

import glob
import os
import stat
import subprocess
import sys

import yaml

import requests

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.LibcloudDict import LibcloudDict
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.default import Default

requests.packages.urllib3.disable_warnings()


class SubprocessError(Exception):
    def __init__(self, cmd, returncode, stderr, stdout):
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout


class Subprocess(object):

    def __init__(self, cmd, shell=False, cwdir=None):
        proc = subprocess.Popen(cmd, shell=shell, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwdir=cwdir)
        proc.communicate()

        self.returncode = proc.returncode
        self.stderr = proc.stderr
        self.stdout = proc.stdout

        if proc.returncode != 0:
            raise SubprocessError(cmd, proc.returncode, proc.stderr, proc.stdout)


class Project(Object):

    @staticmethod
    def projectsprefix():

        cfgpath = Config.find_file('cloudmesh.yaml')
        dotcloudmesh = os.path.dirname(cfgpath)
        projectsdir = os.path.join(dotcloudmesh, 'projects')

        return projectsdir


    @staticmethod
    def projectdir(name):
        prefix = Project.projectsprefix()
        path = os.path.join(prefix, name)


    @staticmethod
    def new_project_name():
        """Automatically generate a new project name

        :returns: a project name
        :rtype: :class:`str`
        """

        projects = glob.glob(os.path.join(Project.projectsprefix(), 'p-[0-9]*'))
        pids = map(lambda s: int(s.split('-')[-1]), projects)
        newpid = max(pids) + 1

        return 'p-{}'.format(newpid)


    @staticmethod
    def project_exists(name):
        path = Project.projectdir(name)
        return os.path.exists(path)



class Stack(ListResource):
    """
    Not intended to be directly instantiated. Instead use one of the subclasses.
    """

    # should be overridden by subclasses
    __name = 'undefined-stack-name-this-is-a-bug'

    cm = CloudmeshDatabase()


    @property
    def cachedir(self):
        cfgpath = Config.find_file('cloudmesh.yaml')
        dotcloudmesh = os.path.dirname(cfgpath)
        return os.path.join(dotcloudmesh, 'stack', self.__name, 'cache')


    @classmethod
    def refresh(cls, cloud):
        print ("TBD")

    @classmethod
    def list(cls,
             kind,
             cloud,
             user=None,
             tenant=None,
             order=None,
             header=None,
             output="table"):
        print ("TBD")



class SanityCheckError(Exception):

    def __init__(self, message, reason):
        self.message = message
        self.reason  = reason



class SanityChecker(object):

    def check_program(self, program):
        """Verify that the named program is available and executable by the user.

        :param program: commands that must be present by checking in the PATH
        :type programs: :class:`str`
        :returns: None
        :raises: :class:`SanityCheckError` on failure

        """

        PATH = os.getenv('PATH').split(':')

        for prefix in PATH:
            if os.path.exists(os.path.join(prefix, program)):
                return

        raise SanityCheckError('{} not installed correctly'.format(prog),
                               '`{}` not found in $PATH'.format(prog))


    def check_sshkey(self):
        """Ensure that the default ssh key exists with correct permissions

        :returns: None
        :raises: :class:`SanityCheckError`

        """

         valid_key_types = [
            'dsa',
            'ecdsa',
            'ed25519',
            'rsa',
            'rsa1'
        ]

         msg = 'SSH incorrectly configured'

        dotssh = os.path.expanduser('~/.ssh')

        if not os.path.exists(dotssh):
            raise SanityCheckError(msg, 'directory `{}` does not exist, please run ssh-keygen'.format(dotssh))
        
        if not os.path.isdir(dotssh):
            raise SanityCheckError(msg, 'path `{}` exists but is not a directory'.format(dotssh))

        s = os.stat(dotssh)
        if not bool(s.st_mode & stat.S_IRWXU):
            raise SanityCheckError(msg, 'incorrect permissions, run: chmod 0700 "{}"'.format(dotssh))
            
        found = 0
        for typ in valid_key_types:
            private = os.path.join(dotssh, typ)
            public  = private + '.pub'

            if os.path.exists(private) and os.path.exists(public):
                found += 1
                for p in [private, public]:
                    s = os.stat(p)
                    if bool(s.st_mode & (stat.S_IRGRP | stat.S_IROTH)):
                        raise SanityCheckError(msg, 'Permissions on {} are too open')

        if found < 1:
            raise SanityCheckError(msg, 'No id_<type> ssh keys found in {}'.format(dotssh))


    def check_github(self):
        """Ensure that the default ssh key has been uploaded to github.com

        :returns: None
        :raises: :class:`SanityCheckError` on failure
        """

        cmd = ['ssh', '-T', 'git@github.com']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        if "You've successfully authenticated" not in proc.stderr:
            raise SanityCheckError('SSH authentication to github.com failed',
                                   'did you add your public key to https://github.com/settings/ssh ?')



class BigDataStack(Stack):

    __name = 'bds'


    @property
    def cached_repo(self):
        return os.path.join(self.cachedir, 'bds.git')


    def sanity_check(self):
        """Verifies that the environment is set up correctly for BDS usage:

        :returns: boolean indicating pass or fail of the sanity check
        :rtype: :class:`bool`

        """

        def pprint_check(msg, maxchar=20, filler='.', stream=sys.stdout):
            """fancy way for printing out aligned messages

            :param msg: the message
            :param maxchar: maximum number of characters to elide
            :param filler: the filler character
            :param stream: the output stream
            """
            nfiller = maxchar - len(msg)
            nfiller = max(nfiller, 2)

            stream.write(msg)
            stream.write(nfiller * filler)


        checker = SanityChecker()

        # so all errors can be reported at once
        errors = []

        def check(fn, *args, **kws):
            try:
                fn(*args, **kws)
                print('OK')
            except SanityChecker as e:
                print('FAILED')
                errors.append(e)


        ################################################## programs

        # these should be available
        programs = [
            'python',
            'virtualenv',
            'pip',
            'ansible',
            'ansible-playbook',
            'ansible-vault',
            'git',
            'ssh',
        ]

        for prog in programs:
            pprint_check(prog)
            check(checker.check_program, prog)

        ################################################## ssh key

        pprint_check('ssh key')
        check(checker.check_sshkey)

        ################################################## ssh to github

        pprint_check('github')
        check(checker.check_github)


        ################################################## errors

        if len(errors) > 0:
            sys.stderr.write('The following errors were detected:\n\n')

            for e in errors:
                sys.stderr.write('* {}\n'.format(e.message))
                sys.stderr.write('  >{}\n'.format(e.reason))

            return False

        else:
            return True


    def initialize(self, ips, user=None, branch='master', name=None,
                   repo='git://github.com/futuresystems/big-data-stack.git'):
        """Initialize a BDS stack-based project

        :param ips: list of ip addresses
        :param user: the ssh-login username on the nodes with admin privileges
        :param branch: the branch of BDS to use
        :param name: the project name
        :param repo: the upstream git repository to clone
        """

        if not os.path.exists(self.cached_repo):
            Subprocess(['git', 'clone', '--recursive', repo, self.cached_repo], shell=True)

        if not os.path.isdir(prefix):
            raise OSError('{} is not a directory'.format(prefix))


        name = name or Project.new_project_name()
        projectdir = Project.projectdir(name)

        if Project.project_exists(name):
            raise ValueError('Project {} already exists, please choose another'.format(name))

        Subprocess(['git', 'clone', '--recursive', '--branch', branch, '--local', self.cached_repo, projectdir])

        proc_user = os.getenv('USER')
        p = Subprocess(['./mk-inventory', '-n', '{}-{}'.format(proc_user, name)] + ips, cwd=projectdir)
        inventory = p.stdout
        with open(os.path.join(projectdir, 'inventory.txt'), 'w') as fd:
            fd.write(inventory)


        properties = {
            'ips': ips,
            'user': user
        }
        y = yaml.dump(properties, default_flow_style=False)
        with open(projectdir, '.project.yml'), 'w') as fd:
            fd.write(y)


    def update(self, user=None, branch='master', name=None):
        """Updated a previous initialized/cloned stack

        :param user: 
        :param branch: 
        :param name: 
        :returns: 
        :rtype: 

        """

        assert os.path.isdir(self.cachedir)
        assert os.path.isdir(os.path.join(self.cachedir, '.git'))

        current_branch = Subprocess(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwdir=self.cached_repo)\
                        .stdout.strip()

        if current_branch == branch:
            Subprocess(['git', 'pull', '--recurse-submodules', 'origin', branch], cwdir=self.cached_repo)
            Subprocess(['git', 'submodule', 'update'], cwdir=self.cached_repo)

        else:
            Subprocess(['git', 'fetch'], cwdir=self.cached_repo)
            Subprocess(['git', 'pull', 'origin', branch], cwdir=self.cached_repo)


    def list(self, sort=None, fields=None, json=False):
        """List the deployment stacks and projects

        :param sort: 
        :param fields: 
        :param json: 
        :returns: 
        :rtype: 

        """

        
    
    def project(self, projectname=None):
        """View or set the current active project

        :param projectname: If None, return the current project. Otherwise switch to the named project.
        """

        raise NotImplementedError


    def deploy(self):
        """Deploy the currently active project

        :returns: 
        :rtype: 

        """

        raise NotImplementedError
    

