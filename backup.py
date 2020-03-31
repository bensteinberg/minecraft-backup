import click
import socket
import tarfile
from pathlib import Path
from mcrcon import MCRcon
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
CONTEXT_SETTINGS = dict(auto_envvar_prefix='RCON',
                        help_option_names=['-h', '--help'])


class MinecraftBackupException(Exception):
    pass


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--password', required=True)
@click.option('--port', default=25575)
@click.option('--world', default='world',
              help='Directory to back up')
@click.option('--directory', default='backups',
              help='Directory for storing backups')
@click.option('--if-empty/--no-if-empty', default=False,
              help='Back up only when no players are present')
@click.option('--source', help='Source, e.g. server name',
              default=lambda: socket.gethostname())
@click.option('--keep-only', type=int,
              help='Number of backup files to keep')
@click.option('--sync', help='Server to sync to, not yet implemented')
def cli(password, port, world, directory, if_empty, source, keep_only, sync):
    """
    This program backs up a local Minecraft server instance
    """
    p = Path(directory)
    p.mkdir(exist_ok=True)
    with MCRcon('localhost', password, port=port) as mcr:
        try:
            if if_empty:
                r = mcr.command('/list')
                count = int(r.split()[2])
                if count != 0:
                    raise MinecraftBackupException
        except MinecraftBackupException:
            are, s = ('is', '') if count == 1 else ('are', 's')
            print(f'There {are} {count} player{s} online, stopping')
        else:
            print('Saving world...')
            r = mcr.command('/save-all')
            print('Turning save off...')
            r = mcr.command('/save-off')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'world-{source}-{timestamp}.tar.xz'
            with tarfile.open(p / filename, 'w:xz') as tar:
                tar.add(world)
            print(f'Wrote world to {filename}')
            print('Turning save back on.')
            r = mcr.command('/save-on')
        finally:
            if keep_only:
                backup_files = sorted([f for f in p.glob('*.tar.xz')],
                                      key=lambda x: x.stat().st_ctime)
                deleted = [(f.name, f.unlink()) for f in
                           backup_files[:-keep_only]]
                for d in deleted:
                    print(f'Deleted {d[0]}')
