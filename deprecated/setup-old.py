#!/usr/bin/env python
# ----------------------------------------------------------------------- #
# Copyright 2008-2010, Gregor von Laszewski                               #
# Copyright 2010-2013, Indiana University                                 #
# #
# Licensed under the Apache License, Version 2.0 (the "License"); you may #
# not use this file except in compliance with the License. You may obtain #
# a copy of the License at                                                #
#                                                                         #
# http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                         #
# Unless required by applicable law or agreed to in writing, software     #
# distributed under the License is distributed on an "AS IS" BASIS,       #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.#
# See the License for the specific language governing permissions and     #
# limitations under the License.                                          #
# ------------------------------------------------------------------------#
from __future__ import print_function
import platform
import os

from setuptools.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages
import yaml

from cloudmesh_client import __version__


make = """
    test:
    - echo "hallo world"
    github:
    - git commit -a
    - git push
    clean:
    - rm -rf *.egg-info *.eggs
    - rm -rf docs/build
    - rm -rf build
    - rm -rf dist
    doc:
    - sphinx-apidoc -o docs/source cloudmesh_client
    - cd docs; make -f Makefile html
    view:
    - open docs/build/html/index.html
    pypi:
    - python setup.py install
    - python setup.py sdist bdist_wheel
    - python setup.py bdist_wheel upload -r {repo}
    - python setup.py sdist upload -r {repo}
    register:
    - python setup.py register -r {repo}
    tag:
    - bin/new_version.sh
    rmtag:
    - git tag
    - echo "rm Tag?"; read TAG; git tag -d $$TAG; git push origin :refs/tags/$$TAG
    install:
    - python setup.py install
"""

clean_python = '''
        find . -name "*~" -exec rm \{\} \;
	    find . -name "*.pyc" -exec rm \{\} \;
'''

def banner(txt=None, c="#", debug=True):
    """prints a banner of the form with a frame of # arround the txt::

      ############################
      # txt
      ############################

    .

    :param txt: a text message to be printed
    :type txt: string
    :param c: the character used instead of c
    :type c: character
    """
    if debug:
        print
        print ("#", 70 * c)
        if txt is not None:
            print ("#", txt)
            print ("#", 70 * c)



def os_execute(commands):
    for command in commands.split("\n"):
        command = command.strip()
        print(command)
        os.system(command)


def makefile(tag, **kwargs):
    script = "\n".join(yaml.load(make)[tag])
    commands = "\n".join(yaml.load(make)[tag]).format(**kwargs)

    banner("RUNNING")
    os_execute(commands)


def Make(action, **kwargs):

    class InstallAction(install):
        def run(self):
            makefile(action, **kwargs)
            if action == "clean":
                os.system(clean_python)

    return InstallAction

banner("Installing Cloudmesh_client {:}".format(__version__))

requirements = [#'builtins',
                'pyreadline<=1.7.1.dev-r0',
                'colorama',
                'cloudmesh_base',
                'future',
                'docopt',
                'pyaml',
                'simplejson',
                'python-hostlist',
                'prettytable',
                'sqlalchemy',
                'urllib3',
                'requests',
                'pycrypto',
                'httpsig',
                'sandman',
                'gitchangelog',
                'six',
                'python-novaclient',
                'python-keystoneclient',
                'cloudmesh_timestring',
                'wheel',
                'tox',
                'nose',
                'pytest',
                'pytimeparse',
                'pyyaml']

class UploadToPypitest(install):
    """Upload the package to pypi. -- only for Maintainers."""

    description = __doc__

    def run(self):
        os.system("make clean")
        commands = """
            python setup.py install
            python setup.py bdist_wheel            
            python setup.py sdist --format=bztar,zip upload -r pypitest
            python setup.py bdist_wheel upload -r pypitest
            """
        os_execute(commands)    

    
class UploadToPypi(install):
    """Upload the package to pypi. -- only for Maintainers."""

    description = __doc__

    def run(self):
        os.system("make clean")
        commands = """
            python setup.py install
            python setup.py bdist_wheel            
            python setup.py sdist --format=bztar,zip upload
            python setup.py bdist_wheel upload
            """
        os_execute(commands)    

class InstallBase(install):
    """Install the cloudmesh_client package."""

    description = __doc__

    def run(self):
        banner("Install readline")
        commands = None
        this_platform = platform.system().lower()
        if  this_platform in ['darwin']:
            commands = """
                easy_install readline
                """
        elif this_platform in ['windows']:
            commands = """
                pip install pyreadline
                """
        if commands:
            os_execute(commands)
        banner("Install Cloudmesh_client {:}".format(__version__))
        install.run(self)
        os_execute("cm help")


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


home = os.path.expanduser("~")

data_files= [ (os.path.join(home, '.cloudmesh'),
               [os.path.join(d, f) for f in files]) for d, folders, files in os.walk(
                    os.path.join('cloudmesh_client', 'etc'))]

package_data={
   'cloudmesh_client.etc': ['*.yaml', '*.py'],
},


# Hack because for some reason requirements does not work
#
# os.system("pip install -r requirements.txt")


    
class CreateAPI(install):
    """Create the API documentation. -- only for Maintainers."""

    description = __doc__

    def run(self):
        commands = "sphinx-apidoc -f -o docs/source/api/cloudmesh_client cloudmesh_client\n"
        os_execute(commands)
        commands = "sphinx-apidoc -f -o docs/source/api/cloudmesh_base ../base/cloudmesh_base\n"
        os_execute(commands)



class CheckForPasswords(install):
    """Check if a password is somewhere set in cleartext"""

    description = __doc__

    from cloudmesh_client.common.Shell import Shell
    
    def check(self, search=""):
      check_list = [("openstack", "'OS_PASSWORD': '[a-zA-Z0-9]+'"),
                    ("aws", "'EC2_SECRET_KEY': '[a-zA-Z0-9]+'")]
      for pair in check_list:
          platform = pair[0]
          _search = pair[1]
          self._grep(_search, platform)
      if search:
          self._grep(search, 'CUSTOMIZED_SEARCH')


    def _grep(self, search, platform):
      if not search:
          search = "'OS_PASSWORD': '[a-zA-Z0-9]+'"
      cmd = "egrep -ri \"{0}\" * | cut -d\":\" -f1 > a.tmp".format(search)
      print("[{0}]:{1}".format(platform, cmd))
      os.system(cmd)
      res = Shell.cat("a.tmp")
      if res:
          print ('[{0}]: [ERROR] PASSWORD(OR SECRET KEY) DETECTED, SEE FILES '
                 'BELOW'.format(platform))
          print ("")
          print (res)
      else:
          print ("[{0}]: NO PASSWORD DETECTED".format(platform))
      Shell.rm("a.tmp")
      print ("")


    def run(self):
        self.check()
    

        

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    version=__version__,
    name="cloudmesh_client",
    description="cloudmesh_client - A heterogeneous multi cloud command "
                "client and shell",
    long_description=read('README.rst'),
    license="Apache License, Version 2.0",
    author="Gregor von Laszewski",
    author_email="laszewski@gmail.com",
    url="https://github.com/cloudmesh/cloudmesh_client",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console"
    ],
    keywords="cloud cmd commandshell plugins",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    data_files= data_files,
    package_data={
        'cloudmesh_client.etc': ['*.yaml', '*.py'],
    },
    entry_points={
        'console_scripts': [
            'cm = cloudmesh_client.shell.cm:main',
            # 'ghost = cloudmesh_client.shell.ghost:main',
        ],
    },
    tests_require=['tox'],
    cmdclass={
        #'install': InstallBase,
        'docapi': CreateAPI,
        'check': CheckForPasswords,       
        'pypi': Make("pypi", repo='pypi'),
        'pypifinal': Make("pypi", repo='final'),
        'registerpypi': Make("pypi", repo='pypi'),
        'registerfinal': Make("pypi", repo='final'),
        'rmtag': Make('rmtag'),
        'tag': Make("tag"),
        'doc': Make("doc"),
        'view': Make("view"),
        'clean': Make("clean"),
        'test': Tox,
        },

    dependency_links = []
)


