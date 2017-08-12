#!/usr/bin/env python3

import os
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
    counter = 0
    for file in file_list:
        info = os.stat(file)
        counter += 1
        my_time = time.strftime('%b %d, %Y %H:%M', time.localtime(info.st_mtime))
        print(str(counter) + '.  ' + str(my_time) + '  ' + file)

def meta_tags(my_file):
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
