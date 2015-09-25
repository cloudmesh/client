List Command
======================================================================

Manual
-------
The manual page of the list command can be found at: `list <../man/man.html#list>`_


Examples
---------

List Default
^^^^^^^^^^^^^

List the default values set in a particular cloud::

  PS> cm list --cloud general default
    +-----------+---------+--------+----------+----------------------------+----------------------------+
    | user      | cloud   | name   | value    | created_at                 | updated_at                 |
    +-----------+---------+--------+----------+----------------------------+----------------------------+
    | albert    | general | tenant | fg478    | 2015-09-21 02:24:31.978000 | 2015-09-21 02:24:31.978000 |
    | albert    | general | cloud  | india    | 2015-09-21 02:25:00.781000 | 2015-09-21 02:25:00.781000 |
    | albert    | general | group  | group001 | 2015-09-23 21:53:04        | 2015-09-23 21:53:04        |
    | albert    | general | format | table    | 2015-09-23 21:53:16        | 2015-09-23 21:53:16        |
    +-----------+---------+--------+----------+----------------------------+----------------------------+

List Default (JSON Format)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the default values in (JSON format) set in a particular cloud::

  PS> cm list --cloud general --format json default
  {
        "1": {
            "cloud": "general",
            "created_at": "2015-09-21 02:24:31.978000",
            "id": "1",
            "kind": "default",
            "label": "tenant",
            "name": "tenant",
            "project": "undefined",
            "type": "string",
            "updated_at": "2015-09-21 02:24:31.978000",
            "user": "albert",
            "value": "fg478"
        },
        "2": {
            "cloud": "general",
            "created_at": "2015-09-21 02:25:00.781000",
            "id": "2",
            "kind": "default",
            "label": "cloud",
            "name": "cloud",
            "project": "undefined",
            "type": "string",
            "updated_at": "2015-09-21 02:25:00.781000",
            "user": "albert",
            "value": "india"
        },
        "3": {
            "cloud": "general",
            "created_at": "2015-09-23 21:53:04",
            "id": "3",
            "kind": "default",
            "label": "group",
            "name": "group",
            "project": "undefined",
            "type": "string",
            "updated_at": "2015-09-23 21:53:04",
            "user": "albert",
            "value": "group001"
        },
        "4": {
            "cloud": "general",
            "created_at": "2015-09-23 21:53:16",
            "id": "4",
            "kind": "default",
            "label": "format",
            "name": "format",
            "project": "undefined",
            "type": "string",
            "updated_at": "2015-09-23 21:53:16",
            "user": "albert",
            "value": "table"
        }
  }
