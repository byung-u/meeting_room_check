from django.shortcuts import render
from functools import reduce
from redis import StrictRedis
from redis_collections import List

import os


def index(request):
    ip = os.environ.get('RS_HOST')  # RS: raspberry pi
    port = os.environ.get('RS_PORT')
    pw = os.environ.get('RS_PASSWORD')
    redis_connection = StrictRedis(host=ip, port=port, db=0, password=pw)
    r = List(redis=redis_connection, key='rp3:00000000448f5428')
    lv = r[-100:-1]  # light value, latest 100 items
    lv.sort()
    cv = lv[40:60]  # calc value, middle 20 items
    cv_avg = reduce(lambda x, y: x + y, cv) / len(cv)
    is_empty = True if cv_avg < 1500 else False
    # print(cv_avg, is_empty)

    context = {
        'is_empty': is_empty,
    }
    return render(request, 'index.html', context)
