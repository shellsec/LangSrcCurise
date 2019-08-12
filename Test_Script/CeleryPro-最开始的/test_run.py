# coding:utf-8
# from celery import Celery,platforms

import time
from core.Subdomain_Baidu import Baidu
from core.Subdomain_Brute import Brute
from core.Subdomain_Crawl import Crawl
from core.Url_Info import Get_Url_Info
from core.Host_Info import Get_Ip_Info,Get_Alive_Url

import socket
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url,IP,URL,Show_Data,Error_Log
Domains = list(set([x.strip() for x in open('domains.list','r',encoding='utf-8').readlines()]))

from concurrent.futures import ProcessPoolExecutor

#app = Celery('tasks')
#app.config_from_object('config')    #以config.py作为配置文件导入参数
#platforms.C_FORCE_ROOT = True

def get_host(url):
    url = url.split('//')[1]
    try:
        s = socket.gethostbyname(url)
        return s
    except Exception as e:
        print('错误代码 [25] {}'.format(str(e)))
        Error_Log.objects.create(url=url,error='错误代码 [25] {}'.format(str(e)))
        return '获取失败'


def Add_Data_To_Url(url):
        try:
            res = Get_Url_Info(url).get_info()
            res_url = res.get('url')
            res_title = res.get('title')
            res_power = res.get('power')
            res_server = res.get('server')
            Other_Url.objects.create(url=res_url, title=res_title, power=res_power, server=res_server)
        except Exception as e:
            print('错误代码 [29] {}'.format(str(e)))
            Error_Log.objects.create(url=url, error='错误代码 [29] {}'.format(str(e)))
        try:
            ip = get_host(url)
            if ip == '获取失败':
                return
            print('URL --> {}  IP --> {}'.format(url, ip))
            URL.objects.create(url=url,ip=ip)

            test_ip = list(IP.objects.filter(ip=ip))
            if test_ip != []:
                return
            IP_Res = Get_Ip_Info(ip)
            servers = IP_Res.get_server_from_nmap(ip)
            # 服务与端口  字典类型
            open_port = servers.keys()
            check_alive_url = []
            for port in open_port:
                check_alive_url.append('http://{}:{}'.format(ip, port))
                check_alive_url.append('https://{}:{}'.format(ip, port))
            alive_url = Get_Alive_Url(check_alive_url)
            # 该IP上存活WEB，类型为列表，内容为多个字典
            host_type = IP_Res.get_host_type(ip)
            # windows/linux
            area = IP_Res.get_ip_address(ip)
            # 返回地址

            IP_Obj = IP()
            IP_Obj.ip = ip
            IP_Obj.servers = str(servers)
            IP_Obj.host_type = host_type
            IP_Obj.alive_urls = str(alive_url)
            IP_Obj.area = area
            try:
                print(ip,servers,host_type,area)
            except Exception as e:
                print('错误代码 [34] {}'.format(str(e)))
                Error_Log.objects.create(url=url, error='错误代码 [34] {}'.format(str(e)))
            IP_Obj.save()
        except Exception as e:
            print('错误代码 [30] {}'.format(str(e)))
            Error_Log.objects.create(url=url, error='错误代码 [30] {}'.format(str(e)))

def Sub_Baidu(Domains):
    with ProcessPoolExecutor() as pool:
        res = pool.map(Baidu,Domains)
    if res:
        with ProcessPoolExecutor() as pool:
            res = pool.map(Add_Data_To_Url, res)


def Sub_Brute(Domains):
    for domain in Domains:
        res = Brute(domain).start()
        print(res)
        if res:
            with ProcessPoolExecutor() as pool:
                result = pool.map(Add_Data_To_Url, res)


def Run_Crawl(pax,Domains):
    print('运行爬行次数:{}'.format(pax))
    time.sleep(20)
    try:
        target_url = URL.objects.filter(get='否')[0]
        url = target_url.url
        target_url.get = '是'
        target_url.save()
    except Exception as e:
        time.sleep(200)
        try:
            target_url = URL.objects.filter(get='否')[0]
            url = target_url.url
            target_url.get = '是'
            target_url.save()
        except Exception as e:
            print('错误代码 [31] {}'.format(str(e)))
            Error_Log.objects.create(url='获取URL失败', error='错误代码 [31] {}'.format(str(e)))
        return
    print(url)
    try:
        All_Urls = Crawl(url)
        print(All_Urls)
        if All_Urls:
            Sub_Domains = list(set([y for x in Domains for y in All_Urls if x in y]))
            if Sub_Domains != []:
                Add_Data_To_Url(Sub_Domains)
            Other_Domains = list(set([y for x in Domains for y in All_Urls if x not in y]))
            if Other_Domains:
                for url in Other_Domains:
                    print(url)
                    try:
                        res = Get_Url_Info(url).get_info()
                        res_url = res.get('url')
                        res_title = res.get('title')
                        res_power = res.get('power')
                        res_server = res.get('server')
                        Other_Url.objects.create(url=res_url, title=res_title, power=res_power, server=res_server)
                    except Exception as e:
                        print('错误代码 [33] {}'.format(str(e)))
                        Error_Log.objects.create(url=url, error='错误代码 [33] {}'.format(str(e)))
    except Exception as e:
        print('错误代码 [32] {}'.format(str(e)))
        Error_Log.objects.create(url=url, error='错误代码 [32] {}'.format(str(e)))


def Sub_Crawl(pax,Domains):
    with ProcessPoolExecutor() as p:
        future_tasks = [p.submit(Run_Crawl, i,Domains) for i in pax]
if __name__ == '__main__':
    #Sub_Baidu(Domains)
    Sub_Brute(Domains)
    Sub_Crawl(range(20),Domains)