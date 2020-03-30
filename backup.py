import click
import socket
import os
import tarfile
from mcrcon import MCRcon
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
CONTEXT_SETTINGS = dict(auto_envvar_prefix='RCON',
                        help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--password', required=True)
@click.option('--port', default=25575)
@click.option('--world', default='world',
              help='Directory to back up')
@click.option('--directory', default='backups',
              help='Directory for storing backups')
@click.option('--if-empty/--not-if-empty', default=False,
              help='Back up only when no players are present')
@click.option('--source', help='Source, e.g. server name',
              default=lambda: socket.gethostname())
@click.option('--sync', help='Server to sync to, not yet implemented')
def cli(password, port, world, directory, if_empty, source, sync):
    """
    This program backs up a local Minecraft server instance
    """
    with MCRcon('localhost', password, port=port) as mcr:
        if if_empty:
            r = mcr.command('/list')
            count = int(r.split()[2])
            if count != 0:
                are = 'is' if count == 1 else 'are'
                s = '' if count == 1 else 's'
                print(f'There {are} {count} player{s} online, stopping')
                return
        print('Saving world...')
        r = mcr.command('/save-all')
        print('Turning save off...')
        r = mcr.command('/save-off')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'world-{source}-{timestamp}.tar.xz'
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with tarfile.open(os.path.join(directory, filename), 'w:xz') as tar:
            tar.add(world)
        print(f'Wrote world to {filename}')
        print('Turning save back on.')
        r = mcr.command('/save-on')
