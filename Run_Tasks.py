# coding:utf-8
from core.main import Sub_Crawl,Sub_Baidu,Sub_Brute,Run_Cpu_Min

import threading
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Domains,Setting
import time



import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'ExtrApps'))





if __name__ == '__main__':
    print('''

             _                           _
            | |                         (_)
            | |     __ _ _ __   __ _ _____
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      
                               |___/       

    ''')
    print('Main Console Start Running....')
    try:
        print('\n开始自检数据库配置文件数据')
        Set = Setting.objects.all()[0]
        pool_count = int(Set.Pool)
        Alive_Status = eval(Set.Alive_Code)
        pax = range(int(Set.Thread))

        BA = Domains.objects.all()
        Sub_Domains = [x.get('url') for x in BA.values()]
        print('\n[成功] 数据库配置文件加载成功 请耐心等待数据持续收集整理\n\n')

    except Exception as e:
        print('\n[警告] 数据库配置文件加载失败 请在后台管理系统检查是否正确配置相关数据\n\n')
        time.sleep(60)
        time.sleep(60)

    t2 = threading.Thread(target=Sub_Baidu,args=(Sub_Domains,))
    t3 = threading.Thread(target=Sub_Crawl,args=(pax,Sub_Domains))
    t4 = threading.Thread(target=Run_Cpu_Min)

    t2.start()
    t3.start()
    t4.start()

    while 1:
        Sub_Brute(Sub_Domains)
        time.sleep(3600*24)
