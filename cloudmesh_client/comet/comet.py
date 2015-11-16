from __future__ import print_function
import os
import signal
import json
import time
from pprint import pprint
import webbrowser
import getpass

from cloudmesh_client.shell.console import Console
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.ConfigDict import ConfigDict
import requests
from cloudmesh_base.util import banner

requests.packages.urllib3.disable_warnings()


class Comet(object):
    rest_version = "/v1"
    base_uri = "https://localhost:8443/nucleus"
    auth_uri = "https://localhost:8443/nucleus/rest-auth"
    token = None
    HEADER = {'content-type': 'application/json'}
    AUTH_HEADER = {'content-type': 'application/json'}

    # in case of https endpoint
    verify = False

    @staticmethod
    def set_base_uri(uri):
        Comet.base_uri = uri
        Comet.auth_uri = Comet.base_uri + "/rest-auth"

    @staticmethod
    def url(endpoint):
        return Comet.base_uri + Comet.rest_version + "/" + endpoint

    def __init__(self):
        #
        # TODO: in future set global uris
        #
        pass

    @staticmethod
    def docs():

        webbrowser.open("https://localhost:8443/nucleus/docs/#!/v1")

    # #####################
    # TUNNEL
    # #####################

    @staticmethod
    def tunnel(start):
        if start:
            command =  "ssh -L 8443:localhost:443 nucleus"
            os.system(command)
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
        Console.ok("Comet tunnel: {:}".format(pid))

    @staticmethod
    def is_tunnel():
        pid = Comet.find_tunnel()
        return pid is not None

    @staticmethod
    def find_tunnel():
        r = Shell.execute("ps", ["-ax"]).split("\n")
        pid = None
        info = None
        for line in r:
            if ("localhost" in line and "nucleus" in line) \
                    or ("comet" in line and "tunnel" in line) \
                    and not 'status' in line:
                info = line.strip()
                print(info)
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
            if password.lower() == "readline":
                password = getpass.getpass()
            elif password.lower() == "env":
                password = os.environ.get("COMET_PASSWORD", getpass.getpass())

        ret = False
        if cls.token is None:
            if cls.auth_uri:
                authuri = "%s/login/" % cls.auth_uri
                data = {"username": username, "password": password}
                r = requests.post(authuri,
                                  data=json.dumps(data),
                                  headers=cls.HEADER,
                                  verify=cls.verify)
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
                                  headers=header,
                                  verify=cls.verify)
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
    def old_get(url, headers=None):
        print(Comet.AUTH_HEADER)
        print(url)
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
            # However not sure if the delay is large, what the behaviour
            # would be
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
        else:
            ret = r
        return ret

    @staticmethod
    def get(url, headers=None):
        return Comet.http(url, action="get", headers=headers, data=None)

    @staticmethod
    def post(url, headers=None, data=None):
        return Comet.http(url, action="post", headers=headers, data=data)

    @staticmethod
    def put(url, headers=None, data=None):
        return Comet.http(url, action="put", headers=headers)

    # To make GET calls for synchronous or asynchronous API
    @staticmethod
    def http(url, action="get", headers=None, data=None, cacert=False):
        if headers is None:
            headers = Comet.AUTH_HEADER
        if 'post' == action:
            r = requests.post(url, headers=headers, data=json.dumps(data),
                              verify=cacert)
        elif 'put' == action:
            r = requests.put(url, headers=headers, verify=cacert)
        else:
            r = requests.get(url, headers=headers, verify=cacert)

        # banner("DEBUGGING HTTP CALL")
        # print (r)

        ret = None

        # responded immediately
        if r.status_code == 200:
            try:
                ret = r.json()
            except:
                ret = r.text
        # code 202, accepted call and processing
        elif r.status_code == 202:
            # now automatically redirect to result page
            # thus no need to check status periodically.
            # Currently it works well for cluster listing
            # However not sure if the delay is large, what the behaviour
            # would be
            finished = False
            newurl = r.headers["Location"]
            while not finished:
                ret = requests.get(newurl, headers=headers)
                try:
                    ret = ret.json()
                except:
                    pass
                # in some occasions, when the result is not ready,
                # the result still has 'status' in it (value as '0')
                # otherwise it's the correct value after redirection
                if 'status' not in ret:
                    finished = True
                else:
                    time.sleep(1)
        elif r.status_code == 401:
            ret = {"error": "Not Authenticated"}
        elif r.status_code == 403:
            ret = {"error": "Permission denied"}
        elif r.status_code == 400:
            ret = {"error": "%s" % r.text}

        return ret

    @staticmethod
    def get_computeset(id=None):
        geturl = Comet.url("computeset/")
        if id:
            geturl = Comet.url("computeset/{}/".format(id))
        r = Comet.get(geturl)
        return r


def main():
    comet = Comet()

    # change user, password to proper value as set in django
    # in shell, we may ask user input

    print(comet.status())
    print(comet.logon())
    print(comet.status())
    print(comet.logoff())
    print(comet.status())
    print(comet.logoff())


def test_get_cluster_list():
    token = ''
    banner("TEST 1: Get without logon")
    authheader = {'content-type': 'application/json',
                  "Authorization": 'Token %s' % token}
    geturl = "https://localhost:8443/nucleus/v1/cluster/"
    r = requests.get(geturl, headers=authheader, verify=False)
    # pprint (r)
    pprint(r.json())

    banner("TEST 2: Auth and then get cluster list")
    # authurl = "https://localhost:8443/nucleus/rest-auth"
    # auth = Authenticator(authurl)
    # change user, password to proper value as set in django
    # in shell, we may ask user input
    comet = Comet()
    token = comet.logon()

    # construct a header with auth token after login
    # for all the following calls before log out
    authheader = {'content-type': 'application/json',
                  "Authorization": 'Token %s' % token}
    geturl = "https://localhost:8443/nucleus/v1/"
    geturl1 = "{}cluster/".format(geturl)
    r = Comet.get(geturl1, headers=authheader)
    pprint(r)

    # as of 2:40pm ET Oct 15, this is changed to 'not implemented'
    # as of 5:30pm ET this is now fixed and working
    # Getting only cluster details for those owned by the caller.
    banner("TEST 3a: Get cluster 'OSG'")
    geturl1 = "%scluster/%s" % (geturl, "osg/")
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)

    banner("\nTEST 3b: Get cluster 'vc2'")
    geturl1 = "%scluster/%s" % (geturl, "vc2/")
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)

    banner("TEST 4: Get compute nodes sets")
    r1 = Comet.get_computeset()
    pprint(r1)

    banner("TEST 4a: Get compute nodes set with id")
    r1 = Comet.get_computeset(46)
    pprint(r1)

    banner("TEST 10: logoff and get cluster list again")
    comet.logoff()
    authheader = {'content-type': 'application/json',
                  "Authorization": 'Token %s' % token}
    geturl = "https://localhost:8443/nucleus/v1/cluster/"
    r = requests.get(geturl, headers=authheader, verify=False)
    pprint(r.json())


def test_power_nodes(action='on'):
    banner("TEST: power on/off a list of nodes")

    banner("Authenticating...")
    # always logon first
    comet = Comet()
    token = comet.logon()

    authheader = {'content-type': 'application/json',
                  "Authorization": 'Token %s' % token}

    url = "https://localhost:8443/nucleus/v1/"
    vcname = "vc2"
    vmnames = ["vm-vc2-0", "vm-vc2-1"]
    vmhosts = {
        vmnames[0]: "comet-01-05",
        vmnames[1]: "comet-01-06"
    }
    data = {"computes": [{"name": vm, "host": vmhosts[vm]} for vm in vmnames],
            "cluster": "%s" % vcname}

    if 'on' == action:
        banner("Issuing request to poweron nodes...")
        posturl = "{}/computeset/".format(url)
        # posturl = "%s%s/compute/poweron" % (url, vcname)
        r = Comet.http(posturl, action="post", headers=authheader, data=data)
        banner("RETURNED RESULTS:")
        print(r)
    elif 'off' == action:
        computesetid = 33
        banner("Issuing request to poweroff nodes...")
        puturl = "%s/computeset/%s/poweroff" % (url, computesetid)
        # posturl = "%s%s/compute/poweron" % (url, vcname)
        r = Comet.http(puturl, action="put", headers=authheader)
        banner("RETURNED RESULTS:")
        print(r)
    else:
        print("The Specified Power Action NOT Supported!")


if __name__ == "__main__":
    test_get_cluster_list()
    # main()
    test_power_nodes("off")
    test_power_nodes()
