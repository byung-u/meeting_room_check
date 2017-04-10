#!/usr/local/bin/python3
from redis import StrictRedis
from redis_collections import List
from functools import reduce

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
    pp.plot(r)
    pp.show()
"""
    light = r[-100:-1]
    light.sort()
    print(light)
    cl = light[40:60]
    print(cl)
    sum_cl = 0
    print(reduce(lambda x, y: x + y, cl) / len(cl))
"""
    #print(r[:-1])  # get value.. what a great


if __name__ == '__main__':
    main()
