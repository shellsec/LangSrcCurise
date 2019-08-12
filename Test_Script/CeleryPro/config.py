# coding:utf-8
from __future__ import absolute_import          #如果没有这一行，下一行可能会出错
from datetime import timedelta

BROKER_URL = 'redis://127.0.0.1:6379/0'

Domains = list(set([x.strip() for x in open('domains.list','r',encoding='utf-8').readlines()]))

CELERYBEAT_SCHEDULE = {
    'Baidu-1-day': {
        'task': 'tasks.Sub_Baidu',
        'schedule': timedelta(minutes=10),
        'args': (Domains,),
    },
    'Brute-1-day': {
        'task': 'tasks.Sub_Brute',
        'schedule': timedelta(minutes=10),
        'args': (Domains,),
    },
    'Crawl-1-day': {
        'task': 'tasks.Sub_Crawl',
        'schedule': timedelta(minutes=10),
        'args': (range(10),Domains,),
    },

}

CELERY_TIMEZONE = 'Asia/Shanghai'
