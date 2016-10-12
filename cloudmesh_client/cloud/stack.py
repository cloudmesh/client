# this is where the stack class is implemented

from __future__ import print_function

import glob
import os
import stat
import shutil
import subprocess
import sys
import time
from collections import defaultdict

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


def get_virtualenv_environment(venvpath):
    """Figures out the environment variables that are set when activating a virtualenv

    :param venvpath: path to the virtual environment
    :returns: dictionary of environment variables
    :rtype: :class:`dict`
    """

    script_lines = [
        'source {venvpath}/bin/activate >/dev/null 2>&1',
        '{command}'
    ]
    script = ';'.join(script_lines).format(**locals())
    output = subprocess.check_output(['bash', '-c', script])

    env = dict()
    for line in output.split('\n'):
        if '=' not in line: continue
        k, v = line.strip().split('=', 1)
        env[k] = v

    return env



class SubprocessError(Exception):
    def __init__(self, cmd, returncode, stderr, stdout):
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout


class Subprocess(object):

    def __init__(self, cmd, cwd=None, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=None):

        proc = subprocess.Popen(cmd, stderr=stderr, stdout=stdout, cwd=cwd, env=env)
        stdout, stderr = proc.communicate()

        self.returncode = proc.returncode
        self.stderr = stderr
        self.stdout = stdout

        if self.returncode != 0:
            raise SubprocessError(cmd, self.returncode, self.stderr, self.stdout)


class ProjectDB(object):

    filename = '.cloudmesh_projectdb.yml'
    default_name = 'p-'

    def __init__(self, prefix=None):
        assert prefix is not None

        if os.path.isfile(prefix):
            raise OSError('`{}` is a file, should be a directory'.format(prefix))

        if not os.path.isdir(prefix):
            os.makedirs(prefix)

        self.path = path
        self.active = None
        self.generated_pid = 0


    def __iter__(self):
        for name in os.listdir(self.path):
            projdir = os.path.join(self.path, name)
            projfile = os.path.join(projdir, Project.filename)
            if os.path.isdir(projdir) and os.path.isfile(projfile):
                project = Project.load(projdir)
                yield project


    def __getitem__(self, projname):
        return Project.load(os.path.join(self.path, Project.filename))


    def __setitem__(self, name, project):
        projdir = self.projectdir()
        if os.path.exists(projdir):
            raise ValueError('Project {} already exists: {}'.format(name, projdir))

        project.init()
        project.sync_metadata(projdir)


    def lookup(self, projname):
        return self[projname]


    def add(self, project):
        self[project.name] = project


    def sync_metadata(self, projects=True):
        if projects:
            for project in self:
                path = os.path.join(self.path, project.name)
                project.sync_metadata(path)

        prop = self.__dict__
        prop.pop('path')
        y = yaml.dump(prop, default_flow_style=False)
        with open(os.path.join(self.path, ProjectList.filename), 'w') as fd:
            fd.write(y)

    @classmethod
    def load(cls, prefix):
        ypath = os.path.join(prefix, cls.filename)

        plist = cls(prefix=prefix)

        if not os.path.exists(ypath):
            return plist

        with open(ypath) as fd:
            y = yaml.load(fd)

        plist.__dict__.update(y)
        return plist


    def projectdir(self, name):
        return os.path.join(self.path, name)


    def new_project_name(self):
        """Automatically generate a new project name

        :returns: a project name
        :rtype: :class:`str`
        """

        pid = self.generated_pid
        self.generated_pid += 1

        name = '{}{}'.format(self.default_name, pid)
        assert not os.path.exists(os.path.join(self.path, name))
        self.sync_metadata(projects=False)
        return name


    def activate(self, project):
        assert project.pid >= 0, 'Project has not been added yet'
        self.active = project.pid
        self.sync_metadata(projects=False)


    def isactive(self, project):
        """Predicate indicating activation status of the project
        """

        return self.active == project.pid


    def getactive(self):
        """Returns the currently active project.

        :returns: the currently active project
        :rtype: subclass of :class:`Project`
        :raises: :class:`KeyError` if no project is currently active
        """

        return self[self.active]



class ProjectFactory(object):
    def __init__(self, prefix='~/.cloudmesh/projects'):
        path = os.path.abspath(os.path.expanduser(os.path.expandvars(prefix)))
        self.db = ProjectDB(path)
        self.stacktype = 'bds'
        self.project_name = None
        self.repo = None
        self.branch = None


    def __call__(self):
        name = self.project_name or self.db.new_project_name()
        projdir = self.db.projectdir(name)

        if self.stacktype == 'bds':
            kwargs = dict()
            if self.repo:
                kwargs['repo'] = self.repo
            if self.branch:
                kwargs['branch'] = self.branch
            stack = BigDataStack(projdir, **kwargs)
        else:
            raise NotImplementedError('Unknown stack type {}'.format(self.stacktype))


        deployparams = dict()

        if self.username:
            deployparams['user'] = self.username

        if self.ips:
            deployparams['ips'] = self.ips

        if self.overrides:
            deployparams['overrides'] = self.overrides

        if self.playbooks:
            deployparams['playbooks'] = self.playbooks


        project = Project(name, stack, deployparams)
        self.db.add(project)

        if self.activate:
            self.db.activate(project)

        return project


    def use_bds(self):
        self.is_bds = True
        return self


    def set_user_name(self, username):
        self.username = username
        return self


    def set_project_name(self, name):
        self.project_name = name
        return self


    def set_ips(self, ips):
        assert len(ips) >= 0
        self.ips = ips
        return self

    def set_repo(self, repo):
        self.repo = repo
        return self


    def set_branch(self, branch='master'):
        self.branch = branch
        return self


    def set_overrides(self, overrides=None):
        overrides = overrides or defaultdict(lambda: defaultdict(list))
        self.overrides = overrides
        return self


    def activate(self, make_active=True):
        self.make_active = make_active
        return self



class Project(object):

    filename = '.cloudmesh_project.yml'

    def __init__(self, name, stack, deployparams=None):
        assert initparams   is not None
        assert deployparams is not None

        self.name = name
        self.ctime = time.gmtime()
        self.stack = stack
        self.deployparams = deployparams
        self.deployparams['name'] = name


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
    def metadata(self):
        m = dict(type=self.__class__.__name__)
        m.update(self.__dict__)
        return m


    def sync_metadata(self, path):
        y = yaml.dump(self.metadata, default_flow_style=False)
        with open(os.path.join(path, Project.filename), 'w') as fd:
            fd.write(y)


    def init(self):
        self.stack.init()


    def deploy(self):
        self.stack.deploy(**self.deployparams)


class KWArgs(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


    def __getitem__(self, key):
        return self.kwargs[key]


    def __setitem__(self, key, value):
        self.kwargs[key] = value


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


    def in_venv(self, cmd, **kwargs):
        name = cmd.pop(0)
        path = os.path.join('venv', 'bin', name)
        real_cmd = [path] + cmd
        return Subprocess(real_cmd, **kwargs)


    def sync(self, path):


        if not os.path.isdir(os.path.join(path, '.git')):
            # clone BDS from the local cache
            cmd = ['git', 'clone', '--recursive', '--branch', self.branch]
            if self.repo_is_local:
                cmd.append('--local')
            cmd.extend([self.repo, path])
            Subprocess(cmd)

        if not os.path.isdir(os.path.join('path', 'venv')):
            Subprocess(['virtualenv', 'venv'], cwd=path)

        self.in_venv(['pip', 'install', '-r', 'requirements.txt'], cwd=path)

        # generate the inventory file
        local_user = os.getenv('USER')
        cmd = ['python', 'mk-inventory', '-n', '{}-{}'.format(local_user, self.name)]
        cmd.extend(self.ips)
        inventory = self.in_venv(cmd, cwd=path)
        with open(os.path.join(path, 'inventory.txt'), 'w') as fd:
            fd.write(inventory.stdout)

        # write the metadata file
        metadata = yaml.dump(self.metadata, default_flow_style=False)
        with open(os.path.join(path, self.metadata_file), 'w') as fd:
            fd.write(metadata)


    def deploy(self, path, plays=None, defines=None, ping_sleep=5, ping_max=500):

        plays = plays or []
        defines0 = defines or []

        # cleanup defines to dict[play name] ->  list("key=value")
        defines0 = map(lambda s: s.split(':'), defines)
        defines = defaultdict(list)
        for playname, keyvalue in defines0:
            defines[playname].append(keyvalue)


        for play in plays:
            cmd = ['ansible-playbook', play, '-u', self.user]
            if play in defines:
                cmd.extend(['-e', ' '.join(defines[play])])

            self.in_venv(cmd, cwd=path, stdout=None, stderr=None)



class BigDataStack(object):
    def __init__(self, dest, repo='git://github.com/futuresystems/big-data-stack.git', branch='master'):
        self.path = os.path.abspath(dest)
        self.repo = repo
        self.branch = branch
        self.local = os.path.isdir(repo)
        self._env = dict()


    def init(self, force=False):
        if not os.path.isdir(os.path.join(self.path, '.git')):
            Subprocess(['git', 'clone', '--recursive', '--branch', self.branch, self.path])

        venvname = 'venv'
        venvdir = os.path.join(self.path, venvname)

        if force and os.path.isdir(venvdir):
            shutil.rmtree(venvdir)

        if not os.path.isdir(venvdir):
            Subprocess(['virtualenv', venvdir])

        self._env = get_virtualenv_environment(venvdir)
        cmd = ['pip', 'install', '-r', 'requirements.txt'] + (['-U'] if force else [])
        Subprocess(cmd, cwd=self.path)


    def update(self):
        Subprocess(['git', 'fetch', '--recurse-submodules', 'origin', self.branch], cwd=self.path)
        Subprocess(['git', 'checkout', self.branch], cwd=self.path)
        Subprocess(['git', 'merge' 'origin/{}'.format(self.branch)], cwd=self.path)
        self.init(force=True)


    def deploy(self, ips=None, name=None, user=None, playbooks=None, overrides=None):
        assert ips is not None

        name = name or os.getenv('USER') + '-' + os.path.basename(self.path)
        user = user or 'defaultuser'
        playbooks = playbooks or list()
        overrides = overrides or dict()


        Subprocess(['python', 'mk-inventory', '-n', name] + ips, cwd=self.path, env=self._env)


        # wait for the cluster to be accessible
        for _ in xrange(ping_max):
            try:
                Subprocess(['ansible', 'all', '-m', 'ping', '-u', self.user],
                           cwd=path, env=self._env, stdout=None, stderr=None)
                break
            except SubprocessError as e:
                time.sleep(ping_sleep)


        basic_command = ['ansible-playbook', '-u', user]
        for play in playbooks:
            define = ['{}={}'.format(k, v) for k, v in defines[play]]
            cmd = basic_command + [play, '-e', ','.join(define)]
            Subprocess(cmd, cwd=self.path, env=self._env, stdout=None, stderr=None)



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

def sanity_check():
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
