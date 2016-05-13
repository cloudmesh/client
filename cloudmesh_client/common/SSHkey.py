from __future__ import print_function
import base64
import hashlib
import struct
from os.path import basename

from cloudmesh_client.common.ConfigDict import Config


# noinspection PyBroadException
class SSHkey(object):
    def __init__(self, file_path=None, keyname=None):
        self.__key__ = None
        self.read(file_path, keyname)

    def get(self):
        return self.__key__

    def __str__(self):
        return self.__key__['key']

    def __repr__(self):
        return self.__key__['key']

    def read(self, file_path, keyname=None):
        self.__key__ = {}
        if file_path is not None:
            orig_path = file_path
            file_path = Config.path_expand(file_path)
            uri = 'file://{}'.format(file_path)
            self.__key__ = {
                'uri': uri,
                'path': orig_path,
                'string': open(file_path, "r").read().rstrip()
            }

            (self.__key__['type'],
             self.__key__['key'],
             self.__key__['comment']) = self._parse(self.__key__['string'])
            self.__key__['fingerprint'] = self._fingerprint(self.__key__['string'])
            # Workaround for multiple file entries in cloudmesh.yaml getting same name derived from file name (like id_rsa).
            # This caused the dict to have just 1 entry as the name is the key.
            # Change tracked in git issue #8
            if keyname is None:
                name = basename(file_path).replace(".pub", "").replace("id_", "")
            else:
                name = keyname

            self.__key__['name'] = name
            self.__key__['comment'] = self.__key__['comment']
            self.__key__['source'] = 'ssh'
        return self.__key__

    @property
    def fingerprint(self):
        return self.__key__['fingerprint']

    @property
    def key(self):
        return self.__key__['string']

    @property
    def type(self):
        return self.__key__['type']

    @property
    def comment(self):
        return self.__key__['comment']

    @classmethod
    def _fingerprint(cls, entirekey):
        """returns the fingerprint of a key.
        :param entirekey: the key
        :type entirekey: string
        """
        t, keystring, comment = cls._parse(entirekey)
        if keystring is not None:
            return cls._key_fingerprint(keystring)
        else:
            return ''

    @classmethod
    def _key_fingerprint(cls, key_string):
        """create the fingerprint form just the key.

        :param key_string: the key
        :type key_string: string
        """
        # key = base64.decodestring(key_string)
        # fp_plain = hashlib.md5(key).hexdigest()
        key = base64.b64decode(key_string.strip().encode('ascii'))
        fp_plain = hashlib.md5(key).hexdigest()

        return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))

    @classmethod
    def _parse(cls, keystring):
        """
        parse the keystring/keycontent into type,key,comment
        :param keystring: the content of a key in string format
        """
        # comment section could have a space too
        keysegments = keystring.split(" ", 2)
        keytype = keysegments[0]
        key = None
        comment = None
        if len(keysegments) > 1:
            key = keysegments[1]
            if len(keysegments) > 2:
                comment = keysegments[2]
        return keytype, key, comment

    def _validate(self, keytype, key):
        """reads the key string from a file. THIS FUNCTION HAS A BUG.

        :param key: either the name of  a file that contains the key, or the entire contents of such a file
        :param keytype: if 'file' the key is read form the file specified in key.
                        if 'string' the key is passed as a string in key
        """
        keystring = None
        if keytype.lower() == "file":
            try:
                keystring = open(key, "r").read()
            except:
                return False
        elif keytype.lower() == "string":
            keystring = key

        try:

            keytype, key_string, comment = self._parse(keystring)
            data = base64.decodestring(key_string)
            int_len = 4
            str_len = struct.unpack('>I', data[:int_len])[0]
            # this should return 7

            if data[int_len:int_len + str_len] == keytype:
                return True
        except Exception as e:
            # print(e)
            return False

    def _keyname_sanitation(self, username, keyname):
        keynamenew = "%s_%s" % (
            username, keyname.replace('.', '_').replace('@', '_'))
        return keynamenew


# unit testing


def main():
    from pprint import pprint

    sshkey = SSHkey("~/.ssh/id_rsa.pub")
    pprint(sshkey.key)
    print("Fingerprint:", sshkey.fingerprint)
    pprint(sshkey.__key__)
    print("sshkey", sshkey)
    print("str", str(sshkey))
    print(sshkey.type)
    print(sshkey.__key__['key'])
    print(sshkey.key)
    print(sshkey.comment)
    """
    key1 = "ssh-rsa abcdefg comment"
    key2 = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDD+NswLi/zjz" + \
            "7Vf575eo9iWWku5m4nVSPMgP13JbKCTVKtavAXt8UPZTkYVWi" + \
            "USeXRqlf+EZM11U8Mq6C/P/ECJS868rn2KSwFosNPF0OOz8zm" + \
            "TvBQShtvBBBVd1kmZePxFGviZbKwe3z3iATLKE8h7pwcupqTi" + \
            "n9m3FhQRsGSF7YTFcGXv0ZqxFA2j9+Ix7SVbN5IYxxgwc+mxO" + \
            "zYIy1SKEAOPJQFXKkiXxNdLSzGgjkurhPAIns8MNYL9usKMGz" + \
            "hgp656onGkSbQHZR3ZHsSsTXWP3SV5ih4QTTFunwB6C0TMQVs" + \
            "EGw1P49hhFktb3md+RC4DFP7ZOzfkd9nne2B mycomment"
    print(key_validate("string", key1))
    print(key_validate("string", key2))
    print(key_parse(key1))
    print(key_parse("abcdedfg"))
    print(key_parse("ssh-rsa somestringhere")[2])
    """


if __name__ == "__main__":
    main()
