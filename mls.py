#!/usr/bin/env python3

import os
from pymediainfo import MediaInfo
import json

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"


def main():
    file_list = os.listdir('/Users/brysont')
    my_file = "test.m4a"
    print(file_list)
    media_info = MediaInfo.parse(my_file)
    foo = media_info.to_json()
    parsed = json.loads(foo)
    print(json.dumps(parsed, indent=4))

if __name__ == '__main__':
    try:
        main()
    except TypeError as err:
        print('Not sure what shit the bed (you probably fucked up), but the error is below:')
        print(err)
    else:
        pass