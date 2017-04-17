from django.shortcuts import render
from django.conf import settings
from functools import reduce
from redis import StrictRedis
from redis_collections import List

import os


def index(request):
    ip = getattr(settings, 'RS_HOST', 'localhost')
    port = getattr(settings, 'RS_PORT', 'def_port')
    pw = getattr(settings, 'RS_PASSWORD', 'def_password')
    redis_connection = StrictRedis(host=ip, port=port, db=0, password=pw)
    r = List(redis=redis_connection, key='rp3:00000000448f5428')

    lv = r[-61:-1]  # light value, latest 60 items
    lv.sort()
    cv = lv[20:40]  # calc value, middle 20 items
    cv_avg = reduce(lambda x, y: x + y, cv) / len(cv)
    # TODO : curr time check
    is_empty = False if cv_avg < 1800 else True
    # True : empty
    # False: be in use
    print(cv_avg, is_empty)
 
    context = {
        'is_empty': is_empty,
    }
    return render(request, 'index.html', context)
