# this is where the stack class is implemented

from __future__ import print_function

import glob
import os
import stat
import shutil
import subprocess
import sys
import time

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

    def __init__(self, cmd, cwd=None):

        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
        stdout, stderr = proc.communicate()

        self.returncode = proc.returncode
        self.stderr = stderr
        self.stdout = stdout

        if self.returncode != 0:
            raise SubprocessError(cmd, self.returncode, self.stderr, self.stdout)


class ProjectList(object):

    filename = '.projectlist.yml'
    default_name = 'p-'

    def __init__(self):
        self.projects = dict()
        self.active = None
        self.max_pid = 0
        self.generated_name_pid = 0


    def __iter__(self):
        return iter(self.projects.values())


    def sync(self):
        prefix = ProjectList.prefix()

        for project in self.projects.itervalues():
            path = os.path.join(prefix, project.name)
            project.sync(path)

        prop = self.__dict__
        y = yaml.dump(prop, default_flow_style=False)
        with open(os.path.join(prefix, ProjectList.filename), 'w') as fd:
            fd.write(y)

    @classmethod
    def load(cls):
        prefix = ProjectList.prefix()
        ypath = os.path.join(prefix, cls.filename)

        plist = cls()

        if not os.path.exists(ypath):
            return plist

        with open(ypath) as fd:
            y = yaml.load(fd)

        plist.__dict__.update(y)
        return plist


    @classmethod
    def prefix(cls):

        cfgpath = Config.find_file('cloudmesh.yaml')
        dotcloudmesh = os.path.dirname(cfgpath)
        projectsdir = os.path.join(dotcloudmesh, 'projects')

        return projectsdir


    @classmethod
    def projectdir(cls, name):
        prefix = cls.prefix()
        path = os.path.join(prefix, name)
        return path


    @classmethod
    def project_exists(cls, project):
        return project.pid in self.projects


    def new_project_name(self):
        """Automatically generate a new project name

        :returns: a project name
        :rtype: :class:`str`
        """

        if self.generated_name_pid <= self.max_pid:
            self.generated_name_pid = self.max_pid

        pid = self.generated_name_pid
        self.generated_name_pid += 1

        name = '{}{}'.format(self.default_name, pid)
        assert self.max_pid not in self.projects
        assert not os.path.exists(self.projectdir(name))
        return name


    def add(self, project):
        assert project.pid < 0, project.pid
        project.name = project.name or self.new_project_name()
        project._pid = self.max_pid
        self.max_pid += 1
        self.projects[project.pid] = project


    def new(self, name=None, activate=False):
        p = Project(name=name)
        self.add(p)
        if activate:
            self.activate(p)


    def activate(self, project):
        assert project.pid >= 0, 'Project has not been added yet'
        self.active = project.pid


    def isactive(self, project):
        """Predicate indicating activation status of the project
        """

        return self.active == project.pid


    def lookup(self, name):
        """Lookup a project by name.

        :param name: the project name
        :returns: the project
        :rtype: subclass of :class:`Project`
        :raises: :class:`Value Error` if the project is not found
        """

        for project in self:
            if project.name == name:
                return project

        raise ValueError('Could not find project {}'.format(name))



class Project(object):

    metadata_file = '.properties.yml'

    def __init__(self, name=None):
        self.ctime = time.gmtime()
        self.name = name  # this is set by ProjectList if None
        self._pid = -1 # this is set by ProjectList

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, self.metadata_file), 'r') as fd:
            y = yaml.load(fd)

        # pop keys that do not appear in the __dict__
        # see 'sync()' implementation for the ones to remove
        y.pop('type', None)

        project = cls()
        project.__dict__.update(y)


    @property
    def pid(self): return self._pid


    @property
    def metadata(self):
        m = dict(type=self.__class__.__name__)
        m.update(self.__dict__)
        return m


    def sync(self, path):
        """Implemented by subclasses
        """
        raise NotImplementedError



class BDSProject(Project):
    def __init__(self, ips=None, user=None, branch='master', **kwargs):
        super(BDSProject, self).__init__(**kwargs)

        assert ips is not None, ips
        assert type(ips) is list, type(ips)
        assert user is not None, user
        assert type(user) is str, type(user)

        self.ips = ips
        self.user = user
        self.branch = branch
        self.repo = kwargs.pop('repo', 'git://github.com/futuresystems/big-data-stack.git')
        self.repo_is_local = kwargs.pop('repo_is_local', False)


    def sync(self, path):

        print ('Syncing {} to {}'.format(self.name, path))


        if not os.path.isdir(os.path.join(path, '.git')):
            # clone BDS from the local cache
            cmd = ['git', 'clone', '--recursive', '--branch', self.branch]
            if self.repo_is_local:
                cmd.append('--local')
            cmd.extend([self.repo, path])
            Subprocess(cmd)

        # generate the inventory file
        local_user = os.getenv('USER')
        cmd = ['python', 'mk-inventory', '-n', '{}-{}'.format(local_user, self.name)]
        cmd.extend(self.ips)
        inventory = Subprocess(cmd, cwd=path)
        with open(os.path.join(path, 'inventory.txt'), 'w') as fd:
            fd.write(inventory.stdout)

        # write the metadata file
        metadata = yaml.dump(self.metadata, default_flow_style=False)
        with open(os.path.join(path, self.metadata_file), 'w') as fd:
            fd.write(metadata)


class Stack(object):
    """
    Not intended to be directly instantiated. Instead use one of the subclasses.
    """

    def __init__(self, name=None):
        assert name is not None
        self.name = name


    @property
    def cachedir(self):
        cfgpath = Config.find_file('cloudmesh.yaml')
        dotcloudmesh = os.path.dirname(cfgpath)
        return os.path.join(dotcloudmesh, 'stack', self.name, 'cache')


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

        if found > 0:
            raise SanityCheckError(msg, 'No id_<type> ssh keys found in {}'.format(dotssh))


    def check_github(self):
        """Ensure that the default ssh key has been uploaded to github.com

        :returns: None
        :raises: :class:`SanityCheckError` on failure
        """

        try:
            Subprocess(['ssh', '-T', 'git@github.com'])
        except SubprocessError as e:
            if "You've successfully authenticated" not in e.stderr:
                raise SanityCheckError('SSH authentication to github.com failed',
                                       'did you add your public key to https://github.com/settings/ssh ?')



class BigDataStack(Stack):

    def __init__(self):
        super(BigDataStack, self).__init__(name='bds')


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


    def initialize(self, ips, user=None, branch='master',
                   repo='git://github.com/futuresystems/big-data-stack.git'):
        """Initialize a BDS stack-based project

        :param ips: list of ip addresses
        :param user: the ssh-login username on the nodes with admin privileges
        :param branch: the branch of BDS to use
        :param repo: the upstream git repository to clone
        """

        print ('Initializing {}'.format(self.name))

        if not os.path.exists(self.cached_repo):
            Subprocess(['git', 'clone', '--recursive', repo, self.cached_repo])

        if not os.path.isdir(self.cached_repo):
            raise OSError('{} is not a directory'.format(prefix))


    def update(self, user=None, branch='master', name=None):
        """Updated a previous initialized/cloned stack

        :param user: 
        :param branch: 
        :param name: 
        :returns: 
        :rtype: 

        """

        print ('Updating {}'.format(self.name))

        assert os.path.isdir(self.cachedir)
        assert os.path.isdir(os.path.join(self.cachedir, '.git'))

        current_branch = Subprocess(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=self.cached_repo)\
                        .stdout.strip()

        if current_branch == branch:
            Subprocess(['git', 'pull', '--recurse-submodules', 'origin', branch], cwd=self.cached_repo)
            Subprocess(['git', 'submodule', 'update'], cwd=self.cached_repo)

        else:
            Subprocess(['git', 'fetch'], cwd=self.cached_repo)
            Subprocess(['git', 'pull', 'origin', branch], cwd=self.cached_repo)


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
    

