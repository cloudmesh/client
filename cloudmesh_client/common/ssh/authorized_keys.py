
import itertools
import os.path
from cStringIO import StringIO

from cloudmesh_client.common.util import tempdir
from cloudmesh_client.common.Shell import Subprocess


def fingerprint_public_key(pubkey):
    """Generate the fingerprint of a public key

    :param str pubkey: the value of the public key
    :returns: fingerprint
    :rtype: str
    """

    with tempdir() as workdir:

        key = os.path.join(workdir, 'key.pub')
        with open(key, 'w') as fd:
            fd.write(pubkey)

        cmd = [
            'ssh-keygen',
            '-l',
            '-f', key,
        ]

        p = Subprocess(cmd)
        output = p.stdout.strip()
        bits, fingerprint, _ = output.split(' ', 2)
        return fingerprint


class AuthorizedKeys(object):

    def __init__(self):
        self._order = dict()
        self._keys = dict()

    @classmethod
    def from_authorized_keys(cls, path):

        auth = cls()

        with open(path) as fd:

            for pubkey in itertools.imap(str.strip, fd):

                # skip empty lines
                if not pubkey:
                    continue

                auth.add(pubkey)

        return auth

    def add(self, pubkey):
        f = fingerprint_public_key(pubkey)
        if f not in self._keys:
            self._order[len(self._keys)] = f
            self._keys[f] = pubkey

    def remove(self, pubkey):
        raise NotImplementedError()

    def text(self):

        sio = StringIO()

        for fingerprint in self._order.itervalues():
            key = self._keys[fingerprint]
            sio.write(key)
            sio.write('\n')

        text = sio.getvalue()
        sio.close()

        return text.strip()


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    auth = AuthorizedKeys.from_authorized_keys(path)
    print(auth.text())
