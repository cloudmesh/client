from __future__ import print_function
from string import Template
import inspect
import glob
import os
import shutil
import collections
# import pip
import sys
import re

from builtins import input
from past.builtins import basestring

def search(lines, pattern):
    p = pattern.replace("*", ".*")
    test = re.compile(p)
    result = []
    for l in lines:
        if test.search(l):
            result.append(l)
    return result

def grep(pattern, filename):
    """Very simple grep that returns the first matching line in a file.
    String matching only, does not do REs as currently implemented.
    """
    try:
        # for line in file
        # if line matches pattern:
        #    return line
        return next((L for L in open(filename) if L.find(pattern) >= 0))
    except StopIteration:
        return ''


def path_expand(text):
    """ returns a string with expanded variable.

    :param text: the path to be expanded, which can include ~ and $ variables
    :param text: string

    """
    template = Template(text)
    result = template.substitute(os.environ)
    result = os.path.expanduser(result)
    return result


def convert_from_unicode(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_from_unicode, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_from_unicode, data))
    else:
        return data


def yn_choice(message, default='y', tries=None):
    """asks for a yes/no question.
    :param message: the message containing the question
    :param default: the default answer
    """
    # http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input"""
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    if tries is None:
        choice = input("%s (%s) " % (message, choices))
        values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
        return True if choice.strip().lower() in values else False
    else:
        while tries > 0:
            choice = input("%s (%s) (%s)" % (message, choices, "'q' to discard"))
            choice = choice.strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no', 'q']:
                return False
            else:
                print("Invalid input...")
                tries -= 1


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
        print("#", 70 * c)
        if txt is not None:
            print("#", txt)
            print("#", 70 * c)


def str_banner(txt=None, c="#", debug=True):
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
    str = ""
    if debug:
        str += "\n"
        str += "# " + 70 * c
        if txt is not None:
            str += "# " + txt
            str += "# " + 70 * c
    return str


# noinspection PyPep8Naming
def HEADING(txt=None):
    """
    Prints a message to stdout with #### surrounding it. This is useful for
    nosetests to better distinguish them.

    :param txt: a text message to be printed
    :type txt: string
    """
    frame = inspect.getouterframes(inspect.currentframe())

    filename = frame[1][1].replace(os.getcwd(), "")
    line = frame[1][2] - 1
    method = frame[1][3]
    msg = "{}\n# {} {} {}".format(txt, method, filename, line)

    print()
    banner(msg)


def backup_name(filename):
    """
    :param filename: given a filename creates a backup name of the form
                     filename.bak.1. If the filename already exists
                     the number will be increased as  much as needed so
                     the file does not exist in the given location.
                     The filename can consists a path and is expanded
                     with ~ and environment variables.
    :type filename: string
    :rtype: string
    """
    location = path_expand(filename)
    n = 0
    found = True
    backup = None
    while found:
        n += 1
        backup = "{0}.bak.{1}".format(location, n)
        found = os.path.isfile(backup)
    return backup


def auto_create_version(class_name, version, filename="__init__.py"):
    version_filename = "{0}/{1}".format(class_name, filename)
    with open(version_filename, "r") as f:
        content = f.read()

    if content != '__version__ = "{0}"'.format(version):
        banner("Updating version to {0}".format(version))
        with open(version_filename, "w") as text_file:
            text_file.write('__version__ = "{0:s}"'.format(version))


def auto_create_requirements(requirements):
    """
    creates a requirement.txt file form the requirements in the list. If the file exists, it get changed only if the
    requirements in the list are different from the existing file

    :param requirements: the requirements in a list
    """
    banner("Creating requirements.txt file")
    try:
        with open("requirements.txt", "r") as f:
            file_content = f.read()
    except:
        file_content = ""

    setup_requirements = '\n'.join(requirements)

    if setup_requirements != file_content:
        with open("requirements.txt", "w") as text_file:
            text_file.write(setup_requirements)


def copy_files(files_glob, source_dir, dest_dir):
    """

    :param files_glob: *.yaml
    :param source_dir: source directiry
    :param dest_dir: destination directory
    :return:
    """
    files = glob.iglob(os.path.join(source_dir, files_glob))
    for filename in files:
        if os.path.isfile(filename):
            shutil.copy2(filename, dest_dir)


def dict_replace(content, replacements=None):
    if replacements is None:
        replacements = {}
    for key in replacements:
        content = content.replace("\{key\}".format(replacements[key]))

    return content


def readfile(filename):
    with open(path_expand(filename), 'r') as f:
        content = f.read()
    return content


def writefile(filename, content):
    outfile = open(path_expand(filename), 'w')
    outfile.write(content)
    outfile.close()


def get_python():
    python_version = sys.version_info[:3]
    v_string = [str(i) for i in python_version]
    python_version_s = '.'.join(v_string)

    # pip_version = pip.__version__
    pip_version = "8.1.2"
    return python_version_s, pip_version


def check_python():
    python_version = sys.version_info[:3]

    v_string = [str(i) for i in python_version]

    python_version_s = '.'.join(v_string)
    if (python_version[0] == 2) and (python_version[1] >= 7) and (python_version[2] >= 9):

        print("You are running a supported version of python: {:}".format(python_version_s))
    else:
        print("WARNING: You are running an unsupported version of python: {:}".format(python_version_s))
        print("         We recommend you update your python")

    # pip_version = pip.__version__
    pip_version = "8.1.2"

    if int(pip_version.split(".")[0]) >= 7:
        print("You are running a supported version of pip: " + str(pip_version))
    else:
        print("WARNING: You are running an old version of pip: " + str(pip_version))
        print("         We recommend you update your pip  with \n")
        print("             pip install -U pip\n")
