import click
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
@click.option('--world', default='/home/minecraft/world',
              help='Directory to back up')
@click.option('--directory', default='backups',
              help='Directory for storing backups')
@click.option('--sync', help='Server to sync to, not yet implemented')
def cli(password, world, directory, sync):
    """
    This program backs up a local Minecraft server instance
    """
    with MCRcon('localhost', password) as mcr:
        r = mcr.command('/list')
        count = int(r.split()[2])
        if count != 0:
            are = 'is' if count == 1 else 'are'
            s = '' if count == 1 else 's'
            print(f'There {are} {count} player{s} online, stopping')
        else:
            print('Saving world...')
            r = mcr.command('/save-all')
            print('Turning save off...')
            r = mcr.command('/save-off')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'world-{timestamp}.tar.xz'
            if not os.path.isdir(directory):
                os.makedirs(directory)
            with tarfile.open(os.path.join(directory, filename),
                              'w:xz') as tar:
                tar.add(world)
            print(f'Wrote world to {filename}')
            print('Turning save back on.')
            r = mcr.command('/save-on')
