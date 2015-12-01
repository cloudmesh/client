from __future__ import print_function
import os
import sys
import signal
import json
import time
from pprint import pprint
import webbrowser
import getpass
import requests
from httpsig.requests_auth import HTTPSignatureAuth
import random
import string

from cloudmesh_client.shell.console import Console
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.util import banner
from cloudmesh_client.comet.authenticate import AuthenticationException

requests.packages.urllib3.disable_warnings()


class Comet(object):
    rest_version = "/v1"
    base_uri = "https://comet-nucleus.sdsc.edu/nucleus"
    local_base_uri = "https://localhost:8443/nucleus"
    auth_uri = "{}/rest-auth".format(base_uri)
    local_auth_uri = "{}/rest-auth".format(local_base_uri)
    tunnelled = False
    # "USERPASS", "APIKEY"
    auth_provider = None
    token = None
    api_key = None
    api_secret = None
    api_auth = None
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
        if Comet.tunnelled:
            url = Comet.local_base_uri + Comet.rest_version + "/" + endpoint
        else:
            url = Comet.base_uri + Comet.rest_version + "/" + endpoint
        return url

    def __init__(self):
        #
        # TODO: in future set global uris
        #
        pass

    @staticmethod
    def docs():

        webbrowser.open("{}/docs/#!/v1".format(Comet.base_uri) )

    # #####################
    # TUNNEL
    # #####################

    @staticmethod
    def tunnel(start):
        if start:
            Comet.tunnelled = True
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
                break
        if info:
            pid = int(info.split(" ", 1)[0])

        return pid

    # ##############################
    # AUTHENTICATE
    # ##############################
    '''
    import json
    import requests
    from httpsig.requests_auth import HTTPSignatureAuth
    import time, random, string

    secret = "REALAPISECRET"

    auth = HTTPSignatureAuth(secret=secret, headers=["nonce", "timestamp"])

    nonce = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    nodes2op = {"computes":"vm-vc2-[6-7]","cluster":"vc2"}
    z = requests.post('https://comet-nucleus.sdsc.edu/nucleus/v1/computeset/',data=json.dumps(nodes2op), auth=auth, headers={"timestamp": int(time.time()), "nonce":nonce, "X-Api-Key":"Fugang"})
    print z.status_code
    print z.headers
    print z.text

    '''
    @staticmethod
    def get_nonce():
        nonce = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return nonce

    @classmethod
    def set_auth_provider(cls, auth_provider=None):
        # try to load from yaml file if not specified
        if not auth_provider:
            config = ConfigDict("cloudmesh.yaml")
            auth_provider = config["cloudmesh.comet.auth_provider"].upper()
            # value not set in yaml file, use USERPASS as default
            if not auth_provider:
                auth_provider = "USERPASS"
        cls.auth_provider = auth_provider

    @classmethod
    def logon(cls, username=None, password=None):
        cls.set_auth_provider()
        # print (cls.auth_provider)
        ret = False
        if "USERPASS" == cls.auth_provider:
            config = ConfigDict("cloudmesh.yaml")
            # for unit testing only.
            if username is None:
                username = config["cloudmesh.comet.userpass.username"]
            if password is None:
                password = config["cloudmesh.comet.userpass.password"]
                if password.lower() == "readline":
                    password = getpass.getpass()
                elif password.lower() == "env":
                    password = os.environ.get("COMET_PASSWORD", getpass.getpass())

            if cls.token is None:
                if cls.auth_uri:
                    if cls.tunnelled:
                        authuri = "%s/login/" % cls.local_auth_uri
                    else:
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
        elif "APIKEY" == cls.auth_provider:
            # print ("API KEY based auth goes here")
            config = ConfigDict("cloudmesh.yaml")
            cls.api_key = config["cloudmesh.comet.apikey.api_key"]
            cls.api_secret = config["cloudmesh.comet.apikey.api_secret"]
            cls.api_auth = HTTPSignatureAuth(secret=cls.api_secret, headers=["nonce", "timestamp"])
            #
            # api key based auth does not maintain a session
            # once values specified, considered as AuthNed.
            if  cls.api_key and cls.api_secret and cls.api_auth:
                ret = True
        else:
            print ("The specified AUTH Provider Not Currently Supported")
            pass
        return ret

    @classmethod
    def logoff(cls):
        ret = True
        if "USERPASS" == cls.auth_provider:
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
        ret = True
        if "USERPASS" == cls.auth_provider and cls.token is None:
            ret = False
        return ret

    # #############################
    # GET FROM REST
    # #############################

    # To make GET calls for synchronous or asynchronous API

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
    def http(url, action="get", headers=None, data=None, cacert=True):
        # print ("KKK", url)
        # print ("KKK", action)
        # print ("KKK", Comet.auth_provider)
        ret = None
        if Comet.tunnelled:
            cacert = False
        if "USERPASS" == Comet.auth_provider:
            if headers is None:
                headers = Comet.AUTH_HEADER
            if 'post' == action:
                r = requests.post(url, headers=headers, data=json.dumps(data),
                                  verify=cacert)
            elif 'put' == action:
                r = requests.put(url, headers=headers, verify=cacert)
            else:
                r = requests.get(url, headers=headers, verify=cacert)

            # print ("KKK --- DEBUGGING HTTP CALL")
            # pprint (r)

            # responded immediately
            if r.status_code == 200:
                try:
                    ret = r.json()
                except:
                    ret = r.text
            # processed successfully, but returned empty
            elif r.status_code == 204:
                ret = ''
            # code 201, created for the post request
            elif r.status_code == 201:
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
        elif "APIKEY" == Comet.auth_provider:
            headers = {'content-type': 'application/json'}
            headers["timestamp"] = int(time.time())
            headers["nonce"] = Comet.get_nonce()
            headers["X-Api-Key"] = Comet.api_key
            # print ("KKK", headers)
            # print ("KKK", Comet.api_auth)
            # print ("KKK", data)
            # print ("KKK", cacert)
            if 'post' == action:
                r = requests.post(url, auth=Comet.api_auth, headers=headers, data=json.dumps(data), verify=cacert)
            elif 'put' == action:
                r = requests.put(url, auth=Comet.api_auth, headers=headers, verify=cacert)
            else:
                r = requests.get(url, auth=Comet.api_auth, headers=headers, verify=cacert)
                
            ret = None
            
            # print ("KKK", r.status_code)
            # print ("KKK", r.text)

            # responded immediately
            if r.status_code == 200:
                try:
                    ret = r.json()
                except:
                    ret = r.text
            # processed successfully, but returned empty
            elif r.status_code == 204:
                ret = ''
            # code 201, created for the post request
            elif r.status_code == 201:
                finished = False
                newurl = r.headers["Location"]
                headers["timestamp"] = int(time.time())
                headers["nonce"] = Comet.get_nonce()
                while not finished:
                    ret = requests.get(newurl, auth=Comet.api_auth, headers=headers)
                    try:
                        ret = ret.json()
                    except:
                        pass
                    if 'status' not in ret:
                        finished = True
                    else:
                        time.sleep(1)
            elif r.status_code == 401:
                try:
                    ret = r.json()
                    ret = {"error": ret}
                except:
                    pass
                if not ret:
                    ret = {"error": "Not Authenticated"}
            elif r.status_code == 403:
                try:
                    ret = r.json()
                    ret = {"error": ret}
                except:
                    pass
                if not ret:
                    ret = {"error": "Permission denied"}
            elif r.status_code == 400:
                try:
                    ret = r.json()
                    ret = {"error": ret}
                except:
                    pass
                if not ret:
                    ret = {"error": "%s" % r.text}
        # print ("KKKKK", ret)
        return ret

    @staticmethod
    def get_computeset(id=None):
        geturl = Comet.url("computeset/")
        if id:
            geturl = Comet.url("computeset/{}/".format(id))
        r = Comet.get(geturl)
        return r

    @staticmethod
    def console(clusterid, nodeid):
        if not nodeid:
            url = Comet.url("cluster/{}/frontend/console/".format(clusterid))
        else:
            url = Comet.url("cluster/{}/compute/{}/console/".format(clusterid, nodeid))
        if "USERPASS" == Comet.auth_provider:
            r = requests.get(url,
                             headers=Comet.AUTH_HEADER,
                             allow_redirects=False,
                             verify=True)
        elif "APIKEY" == Comet.auth_provider:
            headers = {'content-type': 'application/json'}
            headers["timestamp"] = int(time.time())
            headers["nonce"] = Comet.get_nonce()
            headers["X-Api-Key"] = Comet.api_key
            r = requests.get(url,
                             auth=Comet.api_auth,
                             headers=headers,
                             allow_redirects=False,
                             verify=True)
        # print (url)
        # print (r.status_code)
        # print (r.headers)
        # print (r.text)
        if 303 == r.status_code:
            newurl = r.headers["Location"]
            newurl_esc = newurl.replace("&","\&")
        # print (newurl)
        # for OSX
        if 'darwin' == sys.platform:
            os.system("open {}".format(newurl_esc))
        # for linux - tested on Ubuntu 14.04 and CentOS 7.1
        elif 'linux2' == sys.platform:
            os.system("firefox {}".format(newurl_esc))
        else:
            print ("OS not supported!"\
                   "Use the following url manually in your brower:\n{}".format(newurl) )

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
    Comet.tunnelled = True
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

    banner("\nTEST 3b: Get cluster 'vc2' via tunnel")
    geturl1 = "%scluster/%s" % (geturl, "vc2/")
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)

    banner("\nTEST 3c: Get cluster 'vc2' directly")
    Comet.tunnelled = False
    geturl1 = Comet.url("cluster/vc2/")
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)

    banner("TEST 4: Get compute nodes sets")
    Comet.tunnelled = True
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
    Comet.tunnelled = True
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
