from fabric.api import task, local
import sys
import os

from cloudmesh_base.util import banner
from fabfile.security import check

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

debug = True    

@task
def view():
    """view the documentation in a browser"""
    local("{browser} docs/build/html/index.html".format(browser=browser))


@task
def html():
    # disable Flask RSTPAGES due to sphins incompatibility
    # os.environ['RSTPAGES'] = 'FALSE'
    # banner("API Generation")
    # api()
    # banner("Manual Pages")
    # man()
    # build the docs locally and view
    banner("Make the sphinx documentation")
    local("cd docs; make html")
    check()

@task
def publish():
    """deploy the documentation on gh-pages"""
    banner("publish doc to github")
    local("ghp-import -n -p docs/build/html")
    #html()
    #local('cd docs/build/html && git add .  && git commit -m "site generated" && git push origin gh-pages')
    #local('git commit -a -m "build site"')
    #local("git push origin master")


@task
def man():
    """deploy the documentation on gh-pages"""
    # TODO: match on "Commands"
    local('cm debug off')
    local('cm man | grep -A10000 \"Commands\"  |'
          ' sed \$d  > docs/source/man/man.rst')


@task
def api():
    for modulename in ["cloudmesh_base",
                       "cmd3",
                       "cloudmesh_client"]:
        print 70 * "="
        print "Building API Docs:", modulename
        print 70 * "="
        local("sphinx-apidoc -f -o docs/source/api/{0} {0}".format(modulename))
        print "done"
