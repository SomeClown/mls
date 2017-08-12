#!/usr/bin/env python3

import os
import pwd
import grp
import stat
import magic
import json
import time
from pymediainfo import MediaInfo
import click

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EPILOG = 'Media-specific unix ls command'

color_black2 = "\033[1;30m{0}\033[00m"
color_red2_on = "\033[01;31m"
color_red2_off = "\33[00m"
color_green2 = "\033[1;32m{0}\033[00m"
color_yellow2 = "\033[1;33m{0}\033[00m"
color_blue2 = "\033[1;34m{0}\033[00m"
color_purple2 = "\033[1;35m{0}\033[00m"
color_cyan2 = "\033[1;36m{0}\033[00m"
color_white2 = "\033[1;37m{0}\033[00m"


@click.group(epilog=EPILOG, context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Still building, not ready for public use
    :return: 
    """
    pass


@click.command()
@click.argument('directory')
def file_info(directory):
    if directory:
        file_list = os.listdir(directory)
    else:
        file_list = os.listdir('.')
    for file in file_list:
        try:
            info = os.stat(directory + '/' + file)
        except FileNotFoundError as e:
            print(e)
            break
        my_size = humanize_bytes(info.st_size)
        my_time = time.strftime('%b %d, %Y %H:%M', time.localtime(info.st_mtime))
        my_mode = stat.filemode(info.st_mode)
        my_user = pwd.getpwuid(info.st_uid)[0]
        my_group = grp.getgrgid(info.st_gid)[0]
        mime_type = magic.Magic(mime=True)
        try:
            my_type = mime_type.from_file(file)
        except IsADirectoryError:
            my_type = 'Directory'

        print('{:15}'.format(my_mode) + '{:12}'.format(my_user) + '{:10}'.format(my_group)
              + '{:>15}'.format(my_size) + '{:>25}'.format(my_time) + '{:>20}'.format(directory + '/' + file)
              + '{:>20}'.format(my_type))


def meta_tags(my_file):
    media_info = MediaInfo.parse(my_file)
    foo = media_info.to_json()
    parsed = json.loads(foo)
    print(json.dumps(parsed, indent=4))


def humanize_bytes(file_bytes, precision=1):
    """Return a humanized string representation of a number of bytes.

    Cribbed from https://github.com/ActiveState/code

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if file_bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if file_bytes >= factor:
            break
    return '%.*f %s' % (precision, file_bytes / factor, suffix)

cli.add_command(file_info, 'list')

if __name__ == '__main__':
    try:
        cli()
    except TypeError as err:
        print('Not sure what shit the bed (you probably fucked up), but the error is below:')
        print(err)
    else:
        pass
