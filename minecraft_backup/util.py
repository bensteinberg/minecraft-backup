from contextlib import contextmanager
from mcrcon import MCRcon


CONTEXT_SETTINGS = dict(auto_envvar_prefix='RCON',
                        help_option_names=['-h', '--help'])


class MinecraftBackupException(Exception):
    pass


@contextmanager
def safe_MCRcon(host, password, port):
    try:
        mcr = MCRcon(host, password, port=port)
        mcr.connect()
    except ConnectionResetError as err:
        yield None, err
    else:
        try:
            yield mcr, None
        finally:
            mcr.disconnect()
