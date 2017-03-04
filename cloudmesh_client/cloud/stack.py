# this is where the stack class is implemented

from __future__ import print_function

import copy
import os
import stat
import shutil
import subprocess
import sys
import time
from collections import defaultdict

import yaml

import requests

from cloudmesh_client.common.util import exponential_backoff
from cloudmesh_client.common.Shell import Subprocess, SubprocessError
from cloudmesh_client.shell.console import Console
from cloudmesh_client.db import CloudmeshDatabase
from pprint import pprint
from cloudmesh_client.default import Default

requests.packages.urllib3.disable_warnings()


def get_virtualenv_environment(venvpath):
    """Figures out the environment variables that are set when activating
    a virtualenv

    Example:
    >>> os.system('virtualenv /tmp/venv')
    >>> get_virtualenv_environment('/tmp/venv')


    :param venvpath: path to the virtual environment
    :returns: dictionary of environment variables
    :rtype: :class:`dict`

    """

    command = 'source %s/bin/activate' % venvpath
    script_lines = [
        'source {venvpath}/bin/activate >/dev/null 2>&1',
        '{command} >/dev/null 2>&1',
        'env',
    ]
    script = ';'.join(script_lines).format(**locals())
    output = subprocess.check_output(['bash', '-c', script])

    env = dict()
    for line in output.split('\n'):
        if '=' not in line:
            continue
        k, v = line.strip().split('=', 1)
        env[k] = v

    return env


class ProjectDB(object):

    filename = '.cloudmesh_projectdb.yml'
    default_name = 'p-'

    def __init__(self, prefix='~/.cloudmesh/projects'):
        prefix = os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(
                    prefix
                )
            )
        )

        if os.path.exists(os.path.join(prefix, self.filename)):
            yp = os.path.join(prefix, self.filename)
            with open(yp) as fd:
                y = yaml.load(fd)
            self.__dict__.update(y)
            self.path = prefix

        else:

            if os.path.isfile(prefix):
                raise OSError('`{}` is a file, should be a directory'
                              .format(prefix))

            if not os.path.isdir(prefix):
                os.makedirs(prefix)

            self.path = prefix
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
        return Project.load(os.path.join(self.path, projname))

    def lookup(self, projname):
        """Lookup the project with the given name.

        If `projname` is None, this returns the currently active project.

        :param projname: Project name
        :returns: the project
        :rtype: :class:`Project`
        """
        if projname is None:
            return self.getactive()
        else:
            return self[projname]

    def add(self, project, force=False, update=False):
        """Add a project to the database

        :param project: the project to add_from_path
        :type project: :class:`Project`
        :param force: whether or not to force initialiation
        :type force: :class:`bool`
        :param update: whether or not to update a previous initialied project
        :type update: :class:`bool`
        """
        projdir = self.projectdir(project.name)
        if os.path.exists(projdir) and not force:
            raise ValueError('Project {} already exists: {}'
                             .format(project.name, projdir))

        project.init(force=force, update=update)
        project.sync_metadata(projdir)

    def sync_metadata(self, projects=True):
        """Synchronize the metadata to the backend store

        :param bool projects: project metadata should be saved as well.
        :type projects: :class:`bool`
        """
        if projects:
            for project in self:
                self.update(project)

        prop = copy.copy(self.__dict__)
        prop.pop('path')
        y = yaml.dump(prop, default_flow_style=False)
        with open(os.path.join(self.path, ProjectDB.filename), 'w') as fd:
            fd.write(y)

    def update(self, project):
        """Update the database with the given project

        :param project: the project
        :type project: :class:`Project`
        """
        path = os.path.join(self.path, project.name)
        project.sync_metadata(path)

    def projectdir(self, name):
        """Get the project directory.

        :param name: the name of a project
        :type name: :class:`str`
        :returns: the path to the project
        :rtype: :class:`str`
        """
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
        """Activate the given project

        :param project: the project to make active
        :type project: :class:`Project`
        """
        self.active = project.name
        self.sync_metadata(projects=False)

    def isactive(self, project):
        """Predicate indicating activation status of the project

        :param project: the project to check
        :type project: :class:`Project`
        :rtype: :class:`bool`
        """
        return self.active == project.name

    def getactive(self):
        """Returns the currently active project.

        :returns: the currently active project
        :rtype: subclass of :class:`Project`
        :raises: :class:`KeyError` if no project is currently active
        """

        if self.active:
            return self[self.active]
        else:
            raise ValueError('No active project')


class ProjectFactory(object):
    """Outer API used to create projects.

    This factory should be used rather than directly constructing
    :class:`Project` instances.

    """

    def __init__(self, prefix='~/.cloudmesh/projects'):
        path = os.path.abspath(os.path.expanduser(os.path.expandvars(prefix)))
        self.db = ProjectDB(path)
        self.stacktype = 'bds'
        self.project_name = None
        self.repo = None
        self.branch = None
        self.overrides = None
        self.playbooks = None
        self.force = False
        self.udpate = False

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
            raise NotImplementedError('Unknown stack type {}'
                                      .format(self.stacktype))

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
        self.db.add(project, force=self.force, update=self.udpate)

        if self.activate:
            self.db.activate(project)

        return project

    def use_bds(self):
        """Use the BigDataStack backend"""
        Console.debug_msg('Factory use_bds')
        self.is_bds = True
        return self

    def set_user_name(self, username):
        """Set the cluster login user name"""
        Console.debug_msg('Factory set_user_name: {}'.format(username))
        self.username = username
        return self

    def set_project_name(self, name):
        """Set the project name"""
        Console.debug_msg('Factory set_project_name: {}'.format(name))
        self.project_name = name
        return self

    def set_ips(self, ips):
        """Set the cluster IP addresses"""
        Console.debug_msg('Factory set_ips: {}'.format(ips))
        assert len(ips) >= 0
        self.ips = ips
        return self

    def set_repo(self, repo):
        """Set the repository to get the stack from"""
        Console.debug_msg('Factory set_repo: {}'.format(repo))
        self.repo = repo
        return self

    def set_branch(self, branch='master'):
        """Set the branch of the repository to use"""
        Console.debug_msg('Factory set_branch: {}'.format(branch))
        self.branch = branch
        return self

    def set_overrides(self, overrides=None):
        """Set the overrides for deployment"""
        Console.debug_msg('Factory set_overrides: {}'.format(overrides))
        overrides = overrides or defaultdict(lambda: defaultdict(list))
        self.overrides = overrides
        return self

    def set_playbooks(self, playbooks=None):
        """Set the playbooks to deploy"""
        Console.debug_msg('Factory set_playbooks: {}'.format(playbooks))
        playbooks = playbooks or list()
        self.playbooks = playbooks
        return self

    def set_force(self, force=False):
        """Set the `force` parameter"""
        Console.debug_msg('Factory set_force: {}'.format(force))
        self.force = force
        return self

    def set_update(self, update=False):
        """Set the `update` parameter"""
        Console.debug_msg('Factory set_update: {}'.format(update))
        self.update = update
        return self

    def activate(self, make_active=True):
        """Set whether or not the created project should be activated"""
        Console.debug_msg('Factory activate: {}'.format(make_active))
        self.make_active = make_active
        return self


class Project(object):
    """Captures the parameters and stack for a deployment.  Note: this is
    a lower-level API that should be predominantly be constructed
    using the :class:`ProjectFactory`.
    """

    filename = '.cloudmesh_project.yml'

    def __init__(self, name, stack, deployparams=None):
        assert deployparams is not None

        self.name = name
        self.ctime = time.gmtime()
        self.stack = stack
        self.is_deployed = False
        self.deployparams = deployparams
        self.deployparams['name'] = name

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, cls.filename), 'r') as fd:
            y = yaml.load(fd)

        project = cls(y['name'], y['stack'], deployparams=y['deployparams'])
        project.__dict__.update(y)
        return project

    @property
    def metadata(self):
        m = dict(type=self.__class__.__name__)
        m.update(self.__dict__)
        return m

    def sync_metadata(self, path):
        y = yaml.dump(self.metadata, default_flow_style=False)
        with open(os.path.join(path, Project.filename), 'w') as fd:
            fd.write(y)

    def init(self, force=False, update=False):
        self.stack.init(force=force, update=update)

    def deploy(self, force=False):

        if not self.is_deployed or force:
            self.stack.deploy(**self.deployparams)
        else:
            Console.info('Already deployed')

        self.is_deployed = True


class KWArgs(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getitem__(self, key):
        return self.kwargs[key]

    def __setitem__(self, key, value):
        self.kwargs[key] = value


class BigDataStack(object):
    def __init__(self, dest,
                 repo='git://github.com/futuresystems/big-data-stack.git',
                 branch='master',
                 **kwargs
    ):
        self.path = os.path.abspath(dest)
        self.repo = repo
        self.branch = branch
        self.local = os.path.isdir(repo)
        self._env = dict()

    @classmethod
    def load(cls, path):
        filename = os.path.join(path, '.cloudmesh_metadata')
        Console.debug_msg('Loading {} to {}'.format(cls.__name__, filename))
        with open(filename) as fd:
            d = yaml.load(fd)
        stack = cls(dest=path, **d)
        stack._env = d['_env']
        return stack

    def sync_metadata(self):
        path = os.path.join(self.path, '.cloudmesh_metadata')
        Console.debug_msg('Saving {} to {}'.format(self.__class__.__name__, path))
        y = yaml.dump(self.__dict__, default_flow_style=False)
        with open(path, 'w') as fd:
            fd.write(y)

    def init(self, force=False, update=False):
        """Initialize by cloning (or updating if requested) a local copy of
        the Big Data Stack repository.

        :param bool force: setup previously setup project
        :type force: :class:`bool`
        :param bool update: update the local repository from the origin
        :type update: :class:`bool`

        """

        if not os.path.isdir(os.path.join(self.path, '.git')):
            Console.debug_msg('Cloning branch {} of {} to {}'
                              .format(self.branch, self.repo, self.path))
            Subprocess(['git', 'clone', '--recursive', '--branch',
                        self.branch, self.repo, self.path])

        elif update:
            Console.debug_msg('Updating to branch {} for {}'
                              .format(self.branch, self.path))
            Subprocess(['git', 'fetch', '--recurse-submodules', 'origin',
                        self.branch],
                       cwd=self.path)
            Subprocess(['git', 'checkout', self.branch], cwd=self.path)
            Subprocess(['git', 'merge', 'origin/{}'.format(self.branch)],
                       cwd=self.path)

        venvname = 'venv'
        venvdir = os.path.join(self.path, venvname)

        if force and os.path.isfile(os.path.join(venvdir, 'bin', 'activate')):
            Console.debug_msg('Removing {}'.format(venvdir))
            shutil.rmtree(venvdir)

        if not os.path.isdir(venvdir):
            Console.debug_msg('Creating virtualenv {}'.format(venvdir))
            Subprocess(['virtualenv', venvdir])

        self._env = get_virtualenv_environment(venvdir)
        cmd = ['pip', 'install', '-r', 'requirements.txt'] + (['-U']
                                                              if force
                                                              else [])
        Console.debug_msg('Installing requirements to {}'.format(venvdir))
        Subprocess(cmd, cwd=self.path, env=self._env)

    def deploy(self, ips=None, name=None, user=None, playbooks=None,
               defines=None):
        """Deploy the big-data-stack to a previously stood up cluster located
        at `ips` with login user `user`.

        :param ips: the ip addresses of the cluster to deploy to
        :type ips: :class:`list` of :class:`str` IP addresses
        :param name: the name of the cluster
        :type name: :class:`str`
        :param user: the login username of the cluster
        :type user: :class:`str`
        :param playbooks: the list of playbooks to deploy. These are paths relative to the root directory of the BDS repository.
        :type playbooks: :class:`list` of :class:`str`
        :param defines: the overridden variables defined for each playbook
        :type defines: :class:`dict` from playbook name to :class:`dict` of variable name to value
        :param ping_max: the maximum number of time to attempt to ping the cluster during the verification step.
        :type ping_max: :class:`int`
        :param ping_sleep: the number of seconds to wait between each attempt to ping
        :type ping_sleep: :class:`int`
        """
        assert ips is not None

        name = name or os.getenv('USER') + '-' + os.path.basename(self.path)
        user = user or 'defaultuser'
        playbooks = playbooks or list()
        defines = defines or defaultdict(list)

        Console.debug_msg('Calling mk-inventory in {}'.format(self.path))
        cmd = ['python', 'mk-inventory', '-n', name] + ips
        inventory = Subprocess(cmd, cwd=self.path, env=self._env)
        Console.debug_msg('Writing inventory file')
        Console.debug_msg('\n    ' + ('\n' + 4*' ').join(inventory.stdout.split('\n')))
        with open(os.path.join(self.path, 'inventory.txt'), 'w') as fd:
            fd.write(inventory.stdout)

        Console.info('Waiting for cluster to be accessible')

        def ping():
            try:
                Subprocess(['ansible', 'all', '-m', 'ping', '-u', user],
                           cwd=self.path, env=self._env,
                           stdout=None, stderr=None)
                return True
            except SubprocessError:
                return False

        exponential_backoff(ping)

        basic_command = ['ansible-playbook', '-u', user]
        Console.debug_msg('Running playbooks {}'.format(playbooks))
        for play in playbooks:
            donefile = os.path.join(self.path, play) + '.done'
            if os.path.exists(donefile):
                Console.ok('Skipping completed play %s' % play)
                continue

            cmd = basic_command + [play]
            define = ['{}={}'.format(k, v) for k, v in defines[play]]
            if define:
                cmd.extend(['-e', ','.join(define)])
            Console.info('Running playbook {} with overrides {}'
                         .format(play, define))
            Subprocess(cmd, cwd=self.path, env=self._env,
                       stdout=None, stderr=None)
            with open(donefile, 'w') as fd:
                fd.write('')


class SanityCheckError(Exception):

    def __init__(self, message, reason):
        self.message = message
        self.reason = reason


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

        raise SanityCheckError('{} not installed correctly'.format(program),
                               '`{}` not found in $PATH'.format(program))

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
            raise SanityCheckError(
                msg,
                'directory `{}` does not exist, please run ssh-keygen'
                .format(dotssh))

        if not os.path.isdir(dotssh):
            raise SanityCheckError(msg,
                                   'path `{}` exists but is not a directory'
                                   .format(dotssh))

        s = os.stat(dotssh)
        if not bool(s.st_mode & stat.S_IRWXU):
            raise SanityCheckError(msg,
                                   'incorrect permissions, run: chmod 0700 "{}"'
                                   .format(dotssh))

        found = 0
        for typ in valid_key_types:
            private = os.path.join(dotssh, typ)
            public = private + '.pub'

            if os.path.exists(private) and os.path.exists(public):
                found += 1
                for p in [private, public]:
                    s = os.stat(p)
                    if bool(s.st_mode & (stat.S_IRGRP | stat.S_IROTH)):
                        raise SanityCheckError(
                            msg,
                            'Permissions on {} are too open')

        if found > 0:
            raise SanityCheckError(msg,
                                   'No id_<type> ssh keys found in {}'
                                   .format(dotssh))

    def check_github(self):
        """Ensure that the default ssh key has been uploaded to github.com

        :returns: None
        :raises: :class:`SanityCheckError` on failure
        """

        try:
            Subprocess(['ssh', '-T', 'git@github.com'])
        except SubprocessError as e:
            if "You've successfully authenticated" not in e.stderr:
                raise SanityCheckError(
                    'SSH authentication to github.com failed',
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
