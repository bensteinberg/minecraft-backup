minecraft-backup
================

This program backs up a local Minecraft server instance. You must have
enabled RCON on the server.

Install `python3-venv` if necessary, then run

    python3 -m venv env
    . env/bin/activate
    pip install -r requirements.txt
    pip install --editable .
    mcbackup --help
