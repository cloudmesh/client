# this is where the stack class is implemented

from __future__ import print_function

import os
import stat
import subprocess
import sys


import requests

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.LibcloudDict import LibcloudDict
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default

requests.packages.urllib3.disable_warnings()


class Stack(ListResource):

    cm = CloudmeshDatabase()


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


    def initialize(self, user=None, branch='master', name=None):
        """Initialize a BDS stack-based project

        :param user: the ssh-login username on the nodes with admin privileges
        :param branch: the branch of BDS to use
        :param name: the project name
        """

        raise NotImplementedError


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
    

