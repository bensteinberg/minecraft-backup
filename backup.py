import click
import tarfile
from mcrcon import MCRcon
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
CONTEXT_SETTINGS = dict(auto_envvar_prefix='RCON',
                        help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--server', default='localhost')
@click.option('--password', required=True)
@click.option('--world', default='/home/minecraft/world',
              help='Directory to back up')
@click.option('--sync', help='Server to sync to')
def cli(server, password, world, sync):
    """
    This program backs up a local Minecraft server instance
    """
    with MCRcon(server, password) as mcr:
        r = mcr.command('/list')
        count = int(r.split()[2])
        if count != 0:
            print(f'There are {count} players online, stopping')
        else:
            print('Saving...')
            r = mcr.command('/save-all')
            print('Turning save off...')
            r = mcr.command('/save-off')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            with tarfile.open(f'world-{server}-{timestamp}.tar.xz',
                              'w:xz') as tar:
                tar.add(world)
            print('Turning save back on.')
            r = mcr.command('/save-on')
