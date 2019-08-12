# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()
import re

import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url


from concurrent.futures import ThreadPoolExecutor

import socket,re
def get_host(url):
    url = url.split('//')[1]
    s = socket.gethostbyname(url)
    return s
def Run(url):
    try:
        r = requests.get(url=url,headers={'User-Agent':'langzi'})
        url = r.url.rstrip('/')
        try:
            content = r.content.decode(requests.utils.get_encodings_from_content(r.text)[0],'replace')
        except:
            content = '获取失败'
        try:
            title = re.search('<title>(.*?)</title>',content,re.S|re.I).group(1)
        except:
            title = '获取失败'
        power = str(r.headers.get('X-Powered-By'))
        server = str(r.headers.get('Server'))
    except:
        pass
    print('开始插入数据 : \n{}\n{}\n{}\n{}\n----------------------'.format(url,title,power,server))
    try:
        Other_Url.objects.create(url=url,title=title,power=power,server=server)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    tasks = [x.strip() for x in open('test_data.txt','r',encoding='utf-8').readlines()]
    with ThreadPoolExecutor() as pool:
        pool.map(Run,tasks)
