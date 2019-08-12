# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:07
@file: celery.py
"""
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

app = Celery('CeleryPro',
             broker='redis://192.168.1.103:6379/1',
             backend='redis://192.168.1.103:6379/1',
             include=['CeleryPro.tasks'])


app.conf.CELERYBEAT_SCHEDULE = {
    'add every 10 seconds': {
        'task': 'CeleryPro.tasks.add',
        'schedule': timedelta(seconds=10),
        # 可以用timedelta对象
        # 'schedule': 10,  # 也支持直接用数字表示秒数
        'args': (1, 2)
    },
    'upper every 2 minutes': {
        'task': 'CeleryPro.tasks.upper',
        'schedule': crontab(minute='*/2'),
        'args': ('abc', ),
    },
}

app.conf.CELERY_TIMEZONE = 'Asia/Shanghai'

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
