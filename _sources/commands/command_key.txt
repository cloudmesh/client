Key Command
============

In clouds and distributed environments security keys are used for
authentication. We like to be able to register specific keys with
clouds or vms and easily use them. To do so we upload them into a key
registry in which each key is uniquely named. We use these named keys
when we start up virtual machines or log into remote machines.

The manual page of the key command can be found at: `key
<../man/man.html#key>`_


Adding a key to the database
-----------------------------

To add a key to the key registry from a file we use the command::

    $ cm key add --name=demokey /home/albert/key_expt/id_rsa.pub
    Key demokey successfully added to the database
    info. OK.


List Keys
^^^^^^^^^^

To list the keys in the registry you can use the command::

      $ cm key list
        +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
        | name    | comment            | uri                                        | fingerprint                                     | source |
        +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
        | demokey | albert@Zweistein | file:///home/key_expt/id_rsa.pub             | 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39 | ssh    |
        +---------+--------------------+--------------------------------------------+-------------------------------------------------+--------+
        info. OK.


The key command takes a number of additional options. Instead of using
the cloudmesh registry, keys can also be read from git hub with the option::

    $ cm key list --source=git
    +------+----------+-----------------------------+-------------------------------------------------+--------+
    | name | comment  | uri                         | fingerprint                                     | source |
    +------+----------+-----------------------------+-------------------------------------------------+--------+
    |      | github-0 | https://github.com/TBD.keys | 6e:95:48:8d:af:20:75:2a:52:6b:c5:29:d3:71:0a:8b |        |
    |      | github-1 | https://github.com/TBD.keys | 8a:4f:fe:80:be:e5:ec:c8:c1:1d:e9:74:28:41:c5:a3 |        |
    +------+----------+-----------------------------+-------------------------------------------------+--------+
    info. OK.


To change the output format you can specify it with the --format
option::

  
    $ cm key list --source=git --format=json
    {
        "github-0": {
            "comment": "github-0",
            "string": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/4dvq0KG++Tieu4vhqL4WptgsSUIq+vqLi4PiR6N+UBwEcYWzX33O0gyHsQIJ4dgZRPzTf/kxGPFGtHCrKd0aAUL4uFWFZwuMmJqOvAp+6UDOan/XU9O59Ou0y2vnIxv7+QYb2AHJpHrxjWJ2TjBH7LlTN+jqZBpKUxWQpy4ooyJaN87vpJMbyOEk1LVNpBZHGexF4WRPI6XQUf4PshBRHgqJ9cmiEZUhFWQgeCiyknm8Zx7rGrRhIDnXRw/FOzCyQhnjSS4nJddWzfjNfv9Y0KzRz1KFWUQT9eLaO/j3Q3TleG0zzbZxCBgHv5Jhjm6lmUBcKD0pKU2uhwlD+Ki9",
            "uri": "https://github.com/TBD.keys",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQC/4dvq0KG++Tieu4vhqL4WptgsSUIq+vqLi4PiR6N+UBwEcYWzX33O0gyHsQIJ4dgZRPzTf/kxGPFGtHCrKd0aAUL4uFWFZwuMmJqOvAp+6UDOan/XU9O59Ou0y2vnIxv7+QYb2AHJpHrxjWJ2TjBH7LlTN+jqZBpKUxWQpy4ooyJaN87vpJMbyOEk1LVNpBZHGexF4WRPI6XQUf4PshBRHgqJ9cmiEZUhFWQgeCiyknm8Zx7rGrRhIDnXRw/FOzCyQhnjSS4nJddWzfjNfv9Y0KzRz1KFWUQT9eLaO/j3Q3TleG0zzbZxCBgHv5Jhjm6lmUBcKD0pKU2uhwlD+Ki9",
            "fingerprint": "6e:95:48:8d:af:20:75:2a:52:6b:c5:29:d3:71:0a:8b",
            "type": "ssh-rsa",
            "Id": "github-0"
        },
        "github-1": {
            "comment": "github-1",
            "string": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNTRjYstjHaZyS+vOssLOxYv57z1YEndk5VI34PFb6zb9JI3kTZ0wvhqeO38yAxkjowyrM5MFsMnJnecu9iNKtwb9VPKZRNHLfS3lftELFEEPQC3YaddjX/1ztr4xZqKKvZ6hXH5cRPHKfu5T+r8k2tvtUJlZhz4YeeSah76AL1OxJelHpCrRsiAyywlNLy55kSuG6LNNim6QELDCTRVHeuKMEAuOBL/0nF4NJx2FSYNnyKlSyESwOq5YFDi8tnB9t93zG6Ki0f3j9EtZVXr/4W+Cp9J/I8dX5tV/AJVTeuGrGvOZUjtv1+Na4XfbTOvB4WCJIbczxPlnORt3Qg3R1",
            "uri": "https://github.com/TBD.keys",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDNTRjYstjHaZyS+vOssLOxYv57z1YEndk5VI34PFb6zb9JI3kTZ0wvhqeO38yAxkjowyrM5MFsMnJnecu9iNKtwb9VPKZRNHLfS3lftELFEEPQC3YaddjX/1ztr4xZqKKvZ6hXH5cRPHKfu5T+r8k2tvtUJlZhz4YeeSah76AL1OxJelHpCrRsiAyywlNLy55kSuG6LNNim6QELDCTRVHeuKMEAuOBL/0nF4NJx2FSYNnyKlSyESwOq5YFDi8tnB9t93zG6Ki0f3j9EtZVXr/4W+Cp9J/I8dX5tV/AJVTeuGrGvOZUjtv1+Na4XfbTOvB4WCJIbczxPlnORt3Qg3R1",
            "fingerprint": "8a:4f:fe:80:be:e5:ec:c8:c1:1d:e9:74:28:41:c5:a3",
            "type": "ssh-rsa",
            "Id": "github-1"
        }
    }
    info. OK.


Get Keys
^^^^^^^^^

To get the fingerprint of a key you can obtain it with::

 $ cm key get demokey
    demokey: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39
    info. OK.

Default Keys
^^^^^^^^^^^^^

In many cases it is convenient to just use a default key that is
set. To mark key as default by name you can use the command::

    $ cm key default demokey
    Key demokey set as default
    info. OK.


You can verify that a key is set as default while looking at the
'is_default' attribute::

 $ cm key list --format=json

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

To make it easy for the user, we can set the default key also
interactively with the select option::

  
    $ cm key default --select

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
^^^^^^^^^^^^

A named key can be deleted from the registry with the command, where
'demokey' is the name of the key::

    $ cm key delete demokey
    Key demokey deleted successfully from database.
    info. OK.

Alternatively you can also interactively select it::

    $ cm key delete --select

    KEYS
    ====

        1 - rsa: 2d:18:a8:03:1e:e1:7e:fe:b3:fa:59:49:c7:c2:cf:01
        2 - demokey: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39
        q - quit


    Select between 1 - 2: 2
    choice 2 selected.
    Deleting key: demokey...
    info. OK.

To delete all keys from database use::

    $ cm key delete --all
    All keys from the database deleted successfully.
    info. OK.


Adding Key to Cloud
^^^^^^^^^^^^^^^^^^^^

This functionality is required for key management with VMs. We can add the key from database to the target cloud.::

    $ cm key add_to_cloud albertkey
    Adding key albertkey to cloud kilo as albert-kilo-albertkey
    Key albertkey added successfully to cloud kilo as albert-kilo-albertkey.
    info. OK.

By default the target cloud key name format is <username>-<cloud>-<key-name>.
However, you may choose to override it with '--name_on_cloud' argument.::


    $ cm key add_to_cloud albertkey --name_on_cloud=someothername
    key add_to_cloud albertkey --name_on_cloud=someothername
    Adding key albertkey to cloud kilo as someothername
    Key albertkey added successfully to cloud kilo as someothername.
    info. OK.

List Key Cloud Mapings
^^^^^^^^^^^^^^^^^^^^^^^

You may check out the mappings of database key names with the cloud key names.::

    $ cm key list_cloud_mappings
    +-----------+-----------+------------+-------------------------+
    | user      | key_name  | cloud_name | key_name_on_cloud       |
    +-----------+-----------+------------+-------------------------+
    | albert    | albertkey | kilo       | albert-kilo-albertkey   |
    +-----------+-----------+------------+-------------------------+
