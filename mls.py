#!/usr/bin/env python3

import os
import pwd
import grp
import stat
from pymediainfo import MediaInfo
import json
import time

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"


def main():
    file_info()


def file_info():
    file_list = os.listdir('.')
    for file in file_list:
        info = os.stat(file)
        my_size = humanize_bytes(info.st_size)
        my_time = time.strftime('%b %d, %Y %H:%M', time.localtime(info.st_mtime))
        my_mode = stat.filemode(info.st_mode)
        my_user = pwd.getpwuid(info.st_uid)[0]
        my_group = grp.getgrgid(info.st_gid)[0]

        print('{:15}'.format(my_mode) + '{:12}'.format(my_user) + '{:10}'.format(my_group)
              + '{:15}'.format(my_size) + '{:20}'.format(my_time) + '{:10}'.format(file))


def meta_tags(my_file):
    media_info = MediaInfo.parse(my_file)
    foo = media_info.to_json()
    parsed = json.loads(foo)
    print(json.dumps(parsed, indent=4))


def humanize_bytes(bytes, precision=1):
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
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


if __name__ == '__main__':
    try:
        main()
    except TypeError as err:
        print('Not sure what shit the bed (you probably fucked up), but the error is below:')
        print(err)
    else:
        pass
