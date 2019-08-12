# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:07
@file: celery.py
"""

from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta

app = Celery('CeleryPro',
             broker='redis://192.168.1.103:6379/1',
             backend='redis://192.168.1.103:6379/1',
             include=['CeleryPro.tasks'])


app.conf.CELERYBEAT_SCHEDULE = {
    'Baidu Every Day': {
        'task': 'CeleryPro.tasks.Sub_Baidu',
        'schedule': timedelta(hours=12),

    },
    'Brute Every Day': {
        'task': 'CeleryPro.tasks.Sub_Brute',
        'schedule': timedelta(hours=24),

    },
    'Crawl Every 2 Days': {
        'task': 'CeleryPro.tasks.Sub_Crawl',
        'schedule': timedelta(hours=48),

    },

}

app.conf.CELERY_TIMEZONE = 'Asia/Shanghai'

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)
# 这里设置会在1天后靠一个内置的周期性任务把超过时限的任务结果给清除的。

if __name__ == '__main__':
    app.start()
