# -*- encoding: utf-8 -*- 
import socket
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Domains
import requests,re,sys,io,time,queue,threading
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

def Get_Content(domain):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
                   'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
                   'Cookie': 'Hm_lvt_de25093e6a5cdf8483c90fc9a2e2c61b=1553260543; _csrf=fb33ebded8b9efc940bdf6a20996f570283a8eb5299ea6956e8673a8b2f021f1a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22GcFvhvYi7zUi4yBbOJN7kkA26ochnfCs%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1565279531,1565326170; allSites=baidu.com%7Cle.com%7Cdouyu.com%7Cly.com%7Cbugx.io%7Cmogujie.com%2C0; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1565327289',
                   'Host': 'icp.aizhan.com', 'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        try:
            url = 'https://icp.aizhan.com/'+domain
            print(url)
            r = requests.get(url=url,headers=headers,timeout=15)
            content = r.content.decode()
            return content
        except Exception as e:
            return None

def run(domain):
    content = Get_Content(domain)
    try:
        pattern = re.compile('<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td><span>(.*?)</span></td>', re.S | re.I)
        name = re.search(pattern, content).group(1)
        types = re.search(pattern, content).group(2)
        uid = re.search(pattern, content).group(3)
        return (name,types,uid)
    except Exception as e:
        print(e)
        return ('获取失败','获取失败','获取失败')

if __name__ == '__main__':

    tasks = [x.strip() for x in open('domains.list','r').readlines()]
    for task in tasks:
        time.sleep(5)
        try:
            print('当前检测URL：{}'.format(task))
            res = run(task)
            if res[1] == '获取失败':
                print('第1次获取失败')
                res = run(task)
                if res[1] == '获取失败':
                    print('第2次获取失败')
                    res = run(task)
                    if res[1] == '获取失败':
                        print('第3次获取失败')
                        res = run(task)
                        if res[1] == '获取失败':
                            print('第4次获取失败')
                            res = run(task)

            bid = str(res[2])
            bsex = str(res[1])
            bname = str(res[0])

            print(bid,bname,bsex)
            BA = Domains.objects.filter(url=task)[0]
            if BA.BA_id == '暂无信息' or BA.BA_id == '获取失败':
                BA.url = task
                BA.BA_sex = bsex
                BA.BA_name = bname
                BA.BA_id = bid
                BA.save()
            else:
                print('{} 该站点信息齐全'.format(task))
        except Exception as e:
            print(e)
