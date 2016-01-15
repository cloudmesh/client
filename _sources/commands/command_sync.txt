Sync Command
======================================================================

The sync command provides an API that allows users to sync
a local directory with a directory on any remote machine on the cloud.
Sync command can be used to pull in data from the remote host, or
send data from local machine to remote host.

The manual page of the network command can be found at: `sync <../man/man.html#sync>`



Sync file on local machine with remote machine on cloud
--------------------------------------------------------

To sync a file from local machine to remote use::

  $ cm sync put ubuntu_file.txt sync_dir
    Please enter putty private key(ppk) file path: ~/.ssh/id_rsa_ppk.ppk
    Passphrase for key "imported-openssh-key":
    ubuntu_file.txt           | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%
    Successuly synced local and remote directories.

Sync file from remote machine on cloud to local machine
--------------------------------------------------------

To sync a file from remote machine to local use::

  $ cm sync get sync_dir/* ./cm_sync/
    Please enter putty private key(ppk) file path: ~/.ssh/id_rsa_ppk.ppk
    Passphrase for key "imported-openssh-key":
    my_text.txt               | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%
    my_text_2.txt             | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%
    ex1.txt                   | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%
    ubuntu_file.txt           | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%
    Successuly synced local and remote directories.