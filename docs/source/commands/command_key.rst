Key Command
======================================================================

Manual
--------
The manual page of the key command can be found at: `key <../man/man.html#key>`_


Examples
--------

Adding a key to the database
^^^^^^^^^^^^^

Add a key to the key database from a file::

    PS> cm key add --name=demokey /home/albert/key_expt/id_rsa.pub
        {'--all': False,
         '--dir': '~/.ssh',
         '--format': 'table',
         '--git': False,
         '--help': False,
         '--name': 'demokey',
         '--select': False,
         '--source': 'db',
         '--ssh': False,
         '--username': 'none',
         '-f': False,
         '-h': False,
         'FILENAME': '/home/key_expt/id_rsa.pub',
         'KEYNAME': None,
         'NAME': None,
         'add': True,
         'default': False,
         'delete': False,
         'get': False,
         'list': False}
        ssh dd
        {'comment': 'albert@Zweistein',
         'fingerprint': '4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39',
         'key': 'AAAAB3NzaC1yc2EAAAADAQABAAABAQCzWWw1hY3u2PIQVjE8VvmpN68FFdFZZhkp0VDZyc4a9Ujby73FA5PTE6dZwdGvknjiVX3xBwGhlBzIzvXkHiD2I2EGkR99Y4xOcEZGvZZyA+ktPPiKlfsC9cPH9PBCf6rD84vLeUb57t1Y7dPuH18gRy/ZqzOZPkgk28ZKT0YX2+b8BRjg9lK88ciL4qIoaoOeDjGaXDAa2Y8JAc1AMU4hL/ZXGb3EsiIIsUf9mjjGwnTk44OZghJvmo6e9teBKoZFQdi7WfzPFMUaMui6+KROBrJmep+E2FEBf7UMu4gl5Ib4GNkk+NN5wKS2QYlEvradkwgclzeK5EUsPtnr1wAx',
         'name': 'rsa',
         'source': 'ssh',
         'string': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzWWw1hY3u2PIQVjE8VvmpN68FFdFZZhkp0VDZyc4a9Ujby73FA5PTE6dZwdGvknjiVX3xBwGhlBzIzvXkHiD2I2EGkR99Y4xOcEZGvZZyA+ktPPiKlfsC9cPH9PBCf6rD84vLeUb57t1Y7dPuH18gRy/ZqzOZPkgk28ZKT0YX2+b8BRjg9lK88ciL4qIoaoOeDjGaXDAa2Y8JAc1AMU4hL/ZXGb3EsiIIsUf9mjjGwnTk44OZghJvmo6e9teBKoZFQdi7WfzPFMUaMui6+KROBrJmep+E2FEBf7UMu4gl5Ib4GNkk+NN5wKS2QYlEvradkwgclzeK5EUsPtnr1wAx albert@Zweistein',
         'type': 'ssh-rsa',
         'uri': 'file:///home/albert/key_expt/id_rsa.pub'}
        {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x3766dd0>,
         'cloud': 'general',
         'comment': 'albert@Zweistein',
         'fingerprint': '4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39',
         'is_default': 'False',
         'kind': 'key',
         'label': 'demokey',
         'name': 'demokey',
         'source': 'ssh',
         'type': 'sshkey',
         'uri': 'file:///home/key_expt/id_rsa.pub',
         'user': None}
        info. OK.


List Keys
^^^^^^^^^^^^^

List keys from the database::

      PS> cm key list
        {'--all': False,
         '--dir': '~/.ssh',
         '--format': 'table',
         '--git': False,
         '--help': False,
         '--name': None,
         '--select': False,
         '--source': 'db',
         '--ssh': False,
         '--username': 'none',
         '-f': False,
         '-h': False,
         'FILENAME': None,
         'KEYNAME': None,
         'NAME': None,
         'add': False,
         'default': False,
         'delete': False,
         'get': False,
         'list': True}
        +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
        | name    | comment            | uri                                        | fingerprint                                     | source |
        +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
        | demokey | albert@Zweistein | file:///home/key_expt/id_rsa.pub           | 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39 | ssh    |
        +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
        info. OK.

 OR::

  PS> cm key list --source=db
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': False,
     'delete': False,
     'get': False,
     'list': True}
    +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
    | name    | comment            | uri                                        | fingerprint                                     | source |
    +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
    | demokey | albert@Zweistein | file:///home/key_expt/id_rsa.pub           | 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39 | ssh    |
    +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
    info. OK.

List keys from git::

 PS> cm key list --source=git
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'git',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': False,
     'delete': False,
     'get': False,
     'list': True}
    none
    +------+----------+----------------------------------------+-------------------------------------------------+--------+
    | name | comment  | uri                                    | fingerprint                                     | source |
    +------+----------+----------------------------------------+-------------------------------------------------+--------+
    |      | github-0 | https://github.com/vagloalbert.keys | 2d:18:a8:03:1e:e1:7e:fe:b3:fa:59:49:c7:c2:cf:01 |        |
    +------+----------+----------------------------------------+-------------------------------------------------+--------+
    info. OK.
List keys in different format like json::

 PS> cm key list --source=git --format=json
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'json',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'git',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': False,
     'delete': False,
     'get': False,
     'list': True}
    none
    {
        "github-0": {
            "comment": "github-0",
            "string": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCkVjT+1eWJjiL2gHKXKzlxakD+HP25y+nqTuUKOoIJteYisERJrrJS+LRTUElYpxG7oULajHOTPcQN5UaBfKtCVINLc6WYDultovXvP0gH/W3HljppNGjzxK+T2tC8ZpFr3K0hu4TBKrTQYztA2wi0sytOI2b1NiBz5GogwOEb9LAmESpz1PAhvXpEks7W7EMT9CZ9wC5WIDvfI91Bosgon7JWFECK/VMHI3CUfR0AnOt9Mqcxa0ySubI6ZPsTt72ESMTlrEJuzih7GBe5YG2tSimVpwhjGF1+Dt2Zlgf4P+WVxZm1WrDpXapynOCyr+FScLi8KK2RPzpsmcEwZTFV",
            "uri": "https://github.com/vagloalbert.keys",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQCkVjT+1eWJjiL2gHKXKzlxakD+HP25y+nqTuUKOoIJteYisERJrrJS+LRTUElYpxG7oULajHOTPcQN5UaBfKtCVINLc6WYDultovXvP0gH/W3HljppNGjzxK+T2tC8ZpFr3K0hu4TBKrTQYztA2wi0sytOI2b1NiBz5GogwOEb9LAmESpz1PAhvXpEks7W7EMT9CZ9wC5WIDvfI91Bosgon7JWFECK/VMHI3CUfR0AnOt9Mqcxa0ySubI6ZPsTt72ESMTlrEJuzih7GBe5YG2tSimVpwhjGF1+Dt2Zlgf4P+WVxZm1WrDpXapynOCyr+FScLi8KK2RPzpsmcEwZTFV",
            "fingerprint": "2d:18:a8:03:1e:e1:7e:fe:b3:fa:59:49:c7:c2:cf:01",
            "type": "ssh-rsa",
            "Id": "github-0"
        }
    }
    info. OK.

Get Keys
^^^^^^^^^^^^^

Get a key by name::

 PS> cm key get demokey
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': 'demokey',
     'add': False,
     'default': False,
     'delete': False,
     'get': True,
     'list': False}
    demokey: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39
    info. OK.

Default Keys
^^^^^^^^^^^^^

Mark key as default by name::

 PS> cm key default demokey
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': 'demokey',
     'NAME': None,
     'add': False,
     'default': True,
     'delete': False,
     'get': False,
     'list': False}
    default
    info. OK.

You can verify by::

 PS> cm key list --format=json
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'json',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': False,
     'delete': False,
     'get': False,
     'list': True}
    {
        "1": {
            "comment": "albert@Zweistein",
            "is_default": "True",  <<--Set to True
            "kind": "key",
            "name": "demokey",
            "created_at": "2015-09-23 15:58:32",
            "uri": "file:///home/key_expt/id_rsa.pub",
            "value": null,
            "updated_at": "2015-09-23 16:14:41",
            "project": "undefined",
            "source": "ssh",
            "user": "undefined",
            "fingerprint": "4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39",
            "label": "demokey",
            "id": 1,
            "cloud": "general"
        }
    }
    info. OK.

Select key to be marked as default::

 PS> (ENV)[albert@Zweistein client]$ cm key default --select
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': True,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': True,
     'delete': False,
     'get': False,
     'list': False}
    default
    ('i:', 1)
    ('i:', 2)

    KEYS
    ====

        1 - demokey: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39
        2 - rsa: 2d:18:a8:03:1e:e1:7e:fe:b3:fa:59:49:c7:c2:cf:01
        q - quit


    Select between 1 - 2: 2
    choice 2 selected.
    Setting key: rsa as default.
    info. OK.

Delete Keys
^^^^^^^^^^^^^

Delete key by name::

 PS> cm key delete demokey
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': 'demokey',
     'NAME': None,
     'add': False,
     'default': False,
     'delete': True,
     'get': False,
     'list': False}
    delete
    info. OK.

Select key to be deleted::

 PS> cm key delete --select
    {'--all': False,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': True,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': False,
     'delete': True,
     'get': False,
     'list': False}
    delete
    ('i:', 3)
    ('i:', 4)

    KEYS
    ====

        1 - rsa: 2d:18:a8:03:1e:e1:7e:fe:b3:fa:59:49:c7:c2:cf:01
        2 - demokey: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39
        q - quit


    Select between 1 - 2: 1
    choice 1 selected.
    Deleting key: rsa...
    info. OK.

Delete all keys from database::

 PS> cm key delete --all
    {'--all': True,
     '--dir': '~/.ssh',
     '--format': 'table',
     '--git': False,
     '--help': False,
     '--name': None,
     '--select': False,
     '--source': 'db',
     '--ssh': False,
     '--username': 'none',
     '-f': False,
     '-h': False,
     'FILENAME': None,
     'KEYNAME': None,
     'NAME': None,
     'add': False,
     'default': False,
     'delete': True,
     'get': False,
     'list': False}
    delete
    info. OK.