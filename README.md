mcbackup
================

This program backs up a local Minecraft server instance. You must have
enabled RCON on the server.

Installation
------------

Run `pip install mcbackup`.

Usage
-----

```
$ mcbackup --help
Usage: mcbackup [OPTIONS]

  This program backs up a local Minecraft server instance

Options:
  --password TEXT         [required]
  --port INTEGER
  --world TEXT            Directory to back up
  --directory TEXT        Directory for storing backups
  --careful / --careless  Back up only when no players are present
  --source TEXT           Source, e.g. server name
  --keep-only INTEGER     Number of backup files to keep
  --sync TEXT             Server to sync to, not yet implemented
  -h, --help              Show this message and exit.
```
