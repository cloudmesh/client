from __future__ import print_function
from cloudmesh_client.shell.console import Console
import os
import signal
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.ConfigDict import ConfigDict
import requests
import json
import time
from pprint import pprint
from cloudmesh_base.util import banner

class Comet(object):


    rest_version = "v1"
    base_uri = "http://localhost:8080/"
    auth_uri = "http://localhost:8080/rest-auth"
    token = None
    HEADER = {'content-type': 'application/json'}
    AUTH_HEADER = {'content-type': 'application/json'}

    # in case of https endpoint
    verify = False


    @staticmethod
    def url(endpoint):
        return Comet.base_uri + Comet.rest_version + "/" + endpoint

    def __init__(self):
        #
        # TODO: in future set global uris
        #
        pass

    # #####################
    # TUNNEL
    # #####################

    @staticmethod
    def tunnel(start):
        if start:
            os.system("ssh -L 8080:localhost:80 gregor@nucleus")
        else:
            Comet.kill_tunnel()

    @staticmethod
    def kill_tunnel():
        pid = Comet.find_tunnel()
        if pid is None:
            Console.error("No tunnel to comet found")
        else:
            Console.ok("Killing the tunnel to comet")
            os.kill(pid, signal.SIGTERM)

    @staticmethod
    def state():
        pid = Comet.find_tunnel()
        Console.ok ("Comet tunnel: {:}".format(pid))

    @staticmethod
    def find_tunnel():
        r = Shell.execute("ps", ["-ax"]).split("\n")
        pid = None
        info = None
        for line in r:
            if "localhost" in line and "nucleus" in line:
                info = line
                break
        if info:
            pid = int(info.split(" ", 1)[0])
        return pid

    # ##############################
    # AUTHENTICATE
    # ##############################

    @classmethod
    def logon(cls, username=None, password=None):

        config = ConfigDict("cloudmesh.yaml")
        # for unit testing only.
        if username is None:
            username = config["cloudmesh.comet.username"]
        if password is None:
            password = config["cloudmesh.comet.password"]

        ret = False
        if cls.token is None:
            if cls.auth_uri:
                authuri = "%s/login/" % cls.auth_uri
                data = {"username": username, "password": password}
                r = requests.post(authuri,
                                  data=json.dumps(data),
                                  headers = cls.HEADER,
                                  verify = cls.verify)
                try:
                    cls.token = r.json()["key"]
                    cls.AUTH_HEADER['Authorization'] = "Token {:}".format(
                        cls.token)
                except:
                    ret = False
                ret = cls.token
        else:
            ret = cls.token

        return ret

    @classmethod
    def logoff(cls):
        ret = True
        if cls.token:
            if cls.auth_uri:
                authuri = "%s/logout/" % cls.auth_uri
                header = dict(cls.HEADER)
                header['Authorization'] = "Token %s" % cls.token
                r = requests.post(authuri,
                                  headers = header,
                                  verify = cls.verify)
                cls.token = None
                cls.AUTH_HEADER = cls.HEADER
            else:
                ret = False
        return ret

    @classmethod
    def status(cls):
        ret = False
        if cls.token:
            ret = True
        return ret

    # #############################
    # GET FROM REST
    # #############################

    # To make GET calls for synchronous or asynchronous API
    @staticmethod
    def get(url, headers=None):
        print (Comet.AUTH_HEADER)
        print (url)
        if headers is None:
            headers = Comet.AUTH_HEADER
        r = requests.get(url, headers=headers)
        ret = None

        # responded immediately
        if r.status_code == 200:
            ret = r.json()
        # code 202, accepted call and processing
        elif r.status_code == 202:
            # now automatically redirect to result page
            # thus no need to check status periodically.
            # Currently it works well for cluster listing
            # However not sure if the delay is large, what the behaviour would be
            finished = False
            newurl = r.headers["Location"]
            while not finished:
                ret = requests.get(newurl, headers=headers).json()
                # in some occasions, when the result is not ready,
                # the result still has 'status' in it (value as '0')
                # otherwise it's the correct value after redirection
                if 'status' not in ret:
                    finished = True
                else:
                    time.sleep(1)
        elif r.status_code == 401:
            ret = {"error": "Not Authenticated"}

        return ret

def main():
    comet = Comet()

    # change user, password to proper value as set in django
    # in shell, we may ask user input

    print (comet.status())
    print (comet.logon())
    print (comet.status())
    print (comet.logoff())
    print (comet.status())
    print (comet.logoff())

def test_get_cluster_list():

    token = ''
    banner ("TEST 1: Get without logon")
    authheader = {'content-type': 'application/json', "Authorization":
        'Token %s' % token}
    geturl = "http://localhost:8080/v1/cluster/"
    r = requests.get(geturl, headers = authheader)
    pprint (r.json())

    banner("TEST 2: Auth and then get cluster list")
    authurl = "http://localhost:8080/rest-auth"
    comet = Comet(authurl)
    # change user, password to proper value as set in django
    # in shell, we may ask user input
    token = comet.logon()

    # construct a header with auth token after login
    # for all the following calls before log out
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "http://localhost:8080/v1/cluster/"
    r = Comet.get(geturl, headers=authheader)
    pprint (r)

    # as of 2:40pm ET Oct 15, this is changed to 'not implemented'
    # as of 5:30pm ET this is now fixed and working
    banner("TEST 3: Get cluster 'OSG'")
    geturl1 = "%s%s" % (geturl, "osg/")
    r1 = Comet.get(geturl1, headers=authheader)
    pprint (r1)

    banner("TEST 4: logoff and get cluster list again")
    comet.logoff()
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "http://localhost:8080/v1/cluster/"
    r = requests.get(geturl, headers = authheader)
    pprint (r.json())

if __name__ == "__main__":
    test_get_cluster_list()
    #main()

