#!/usr/local/bin/python3
from redis import StrictRedis
from redis_collections import List

import matplotlib.pyplot as pp
import os


def redis_init():
    ip = os.environ.get('RS_HOST')  # RS: raspberry pi
    port = os.environ.get('RS_PORT')
    pw = os.environ.get('RS_PASSWORD')

    redis_connection = StrictRedis(host=ip, port=port, db=0, password=pw)
    # TODO: support multi keys
    r = List(redis=redis_connection, key='rp3:00000000448f5428')
    return r


def main():
    r = redis_init()
    print(r[:-1])  # get value.. what a great
    pp.plot(r)
    pp.show()


if __name__ == '__main__':
    main()
