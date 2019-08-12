# coding:utf-8
# from celery import Celery,platforms

import time
from core.Subdomain_Baidu import Baidu
from core.Subdomain_Brute import Brute
from core.Subdomain_Crawl import Crawl
from core.Url_Info import Get_Url_Info
from core.Host_Info import Get_Ip_Info,Get_Alive_Url
from core.Cor import Cor

import random
import socket
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url,IP,URL,Show_Data,Error_Log,Cpu_Min,Domains,Setting,Content

from concurrent.futures import ProcessPoolExecutor


Set = Setting.objects.all()[0]
pool_count = int(Set.Pool)
Alive_Status = eval(Set.Alive_Code)

def Run_Cpu_Min():
    while 1:
        try:
            c = Cor()
            cpu, men, new_send, new_recv = c[0], c[1], c[2], c[3]
            Cpu_Min.objects.create(cpu=cpu,menory=men,network_send=new_send,network_recv=new_recv)
        except Exception as e:
            print('错误代码 [16] {}'.format(str(e)))
            Error_Log.objects.create(url='监控资源消耗', error='错误代码 [16] {}'.format(str(e)))
            return '获取失败'



def get_host(url):
    url = url.split('//')[1]
    if ':' in url:
        url = url.split(':')[0]
    try:
        s = socket.gethostbyname(url)
        return s
    except Exception as e:
        print('错误代码 [25] {}'.format(str(e)))
        Error_Log.objects.create(url=url,error='错误代码 [25] {}'.format(str(e)))
        return '获取失败'


def Add_Data_To_Url(url):
        try:
            ip = get_host(url)
            if ip == '获取失败':
                return
            # print('[+ Domain UrlIP] IP解析 --> {}  IP --> {}'.format(url, ip))
            test_url = list(URL.objects.filter(url=url))
            if test_url != []:
                return
            try:
                Test_Other_Url = Other_Url.objects.filter(url=url)
                if list(Test_Other_Url) == []:
                    res = Get_Url_Info(url).get_info()
                    res_url = res.get('url')
                    res_title = res.get('title')
                    res_power = res.get('power')
                    res_server = res.get('server')
                    res_status = res.get('status')
                    res_ip = ip
                    if int(res_status) in Alive_Status:
                        Other_Url.objects.create(url=res_url, title=res_title, power=res_power, server=res_server,
                                                 status=res_status,ip=res_ip)
            except Exception as e:
                print('错误代码 [29] {}'.format(str(e)))
                Error_Log.objects.create(url=url, error='错误代码 [29] {}'.format(str(e)))

            try:
                URL.objects.create(url=url,ip=ip)
                try:
                    Show_contents = Get_Url_Info(url).Requests()[0]
                    Cont = Content()
                    Cont.url = url
                    Cont.content = Show_contents
                    Cont.save()
                    Show_Data.objects.create(url=url, ip=ip, content=Cont)
                except Exception as e:
                    print('错误代码 [08] {}'.format(str(e)))
                    Error_Log.objects.create(url='外键添加错误', error='错误代码 [08] {}'.format(str(e)))



                BA = Domains.objects.all()
                ALL_DOMAINS = [x.get('url') for x in BA.values()]

                # print('所有域名：{}'.format(ALL_DOMAINS))
                This_Sub = [x for x in ALL_DOMAINS if x in url]
                # # 获取到当前子域名属于的主域名
                # print('传入域名:{}'.format(url))
                # print('获取域名:{}'.format(This_Sub))

                try:
                    if This_Sub != []:
                        Domain_Count = Domains.objects.filter(url=This_Sub[0])[0]
                        counts = int(Domain_Count.counts)+1
                        Domain_Count.counts = counts
                        Domain_Count.save()
                except Exception as e:
                    print('错误代码 [15] {}'.format(str(e)))
                    Error_Log.objects.create(url=url+'|'+This_Sub, error='错误代码 [15] {}'.format(str(e)))
            except Exception as e:
                print('错误代码 [22] {}'.format(str(e)))
                Error_Log.objects.create(url=url, error='错误代码 [22] {}'.format(str(e)))

            test_ip = list(IP.objects.filter(ip=ip))
            # 这里开始判断数据库中是否有这个ip，并且先添加然后修改(防止重复浪费资源)
            if test_ip != []:
                test_ip_0 = IP.objects.filter(ip=ip)[0]
                # 这里判断数据中IP时候存在，如果存在并且有扫描状态，就直接中断操作
                if test_ip_0.get == '是' or test_ip_0.get == '中':
                    return
            else:
                try:
                    IP_Res = Get_Ip_Info(ip)
                    area = IP_Res.get_ip_address(ip)
                    IP.objects.create(ip=ip, servers='None', host_type='None', alive_urls='None', area=area)
                    # 这里先添加数据，异步执行获取到的数据作为结果给下个进程使用
                except Exception as e:
                    print('错误代码 [21] {}'.format(str(e)))
                    Error_Log.objects.create(url=url, error='错误代码 [21] {}'.format(str(e)))
        except Exception as e:
            print('错误代码 [30] {}'.format(str(e)))
            Error_Log.objects.create(url=url, error='错误代码 [30] {}'.format(str(e)))



def Change_IP_Info():
    while 1:
        time.sleep(random.randint(1,20))
        time.sleep(random.randint(1,20))
        try:
            target_ip = IP.objects.filter(get='否')[0]
            ip = target_ip.ip
            target_ip.get = '中'
            # 为了防止重复获取同一个数值，这里进行修改
            # 但是有时候 数据没有正常跑出来 设置成 【是】 会导致偏差
            target_ip.save()
        except Exception as e:
            time.sleep(600)
            # 等待并充实一次
            try:
                target_ip = IP.objects.filter(get='否')[0]
                ip = target_ip.ip
                target_ip.get = '中'
                target_ip.save()
            except Exception as e:
                print('错误代码 [39] {}'.format(str(e)))
                Error_Log.objects.create(url='获取 IP 失败', error='错误代码 [39] {}'.format(str(e)))
                return

        print('[+ Host Scaner] 当前扫描主机 : {}'.format(ip))
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

        IP_Obj = IP.objects.filter(ip=ip)[0]
        IP_Obj.ip = ip
        IP_Obj.servers = str(servers)
        IP_Obj.host_type = host_type
        IP_Obj.alive_urls = str(alive_url)
        IP_Obj.area = area
        IP_Obj.get = '是'
        try:
            IP_Obj.save()
        except Exception as e:
            print('错误代码 [38] {}'.format(str(e)))
            Error_Log.objects.create(url='获取 IP 失败', error='错误代码 [38] {}'.format(str(e)))


def Change_ShowData_Info(Sub_Domains):
    while 1:
        time.sleep(random.randint(1, 20))
        time.sleep(random.randint(1, 20))
        time.sleep(random.randint(1, 20))
        time.sleep(random.randint(1, 20))
        time.sleep(random.randint(1, 20))
        # 线程同步
        try:
            target_info = Show_Data.objects.filter(success='否')[0]
            ip = target_info.ip
            url = target_info.url
            Data_IP = IP.objects.filter(ip=ip)[0]
            if Data_IP.get == '否' or Data_IP.get == '中':
                # 如果收集整理的数据还没有获取完成
                time.sleep(360)
                return
            else:
                target_info.get = '中'
                # 这里就不要设置检查状态了，等到最后再设置
                target_info.save()
        except Exception as e:
            time.sleep(600)
            # 等待并充实一次
            try:
                target_info = Show_Data.objects.filter(success='否')[0]
                ip = target_info.ip
                url = target_info.url
                Data_IP = IP.objects.filter(ip=ip)[0]
                if Data_IP.get == '否' or Data_IP.get == '中':
                    # 如果收集整理的数据还没有获取完成
                    time.sleep(360)
                    return
                else:
                    target_info.get = '中'
                    # 这里就不要设置检查状态了，等到最后再设置
                    target_info.save()
            except Exception as e:
                print('错误代码 [41] {}'.format(str(e)))
                Error_Log.objects.create(url='清洗数据流程获取数据失败', error='错误代码 [41] {}'.format(str(e)))
                return
        print('[+ DataInfo Collection] 数据整理清洗 : {} --> {}'.format(url,ip))
        try:
            Data_IP = IP.objects.filter(ip=ip)[0]
            Data_URL = Other_Url.objects.filter(url=url)[0]
            Show_title = Data_URL.title
            Show_power = Data_URL.power
            Show_server = Data_URL.server
            # 该网站使用的web容器
            Show_status = Data_URL.status

            Show_servers = Data_IP.servers
            # 开放的端口和服务，字典类型
            Show_alive_urls = Data_IP.alive_urls
            # 旁站
            Show_host_type = Data_IP.host_type
            Show_area = Data_IP.area
            Show_belong_domain = [x for x in Sub_Domains if x in url]
            if Show_belong_domain == []:
                Show_belong_domain = 'None'
            else:
                Show_belong_domain = Show_belong_domain[0]
            Show_success = '是'
            # 可以设置为获取成功

            ShowS_DataD = Show_Data.objects.filter(url=url)[0]
            ShowS_DataD.title = Show_title
            ShowS_DataD.power = Show_power
            ShowS_DataD.server = Show_server
            ShowS_DataD.status = Show_status
            # ShowS_DataD.content = Cont
            ShowS_DataD.servers = Show_servers
            ShowS_DataD.alive_urls = Show_alive_urls
            ShowS_DataD.host_type = Show_host_type
            ShowS_DataD.area = Show_area
            ShowS_DataD.belong_domain = Show_belong_domain
            ShowS_DataD.success = Show_success
            ShowS_DataD.save()
        except Exception as e:
            print('错误代码 [43] {}'.format(str(e)))
            Error_Log.objects.create(url='清洗数据URL:{} IP:{}失败'.format(url,ip), error='错误代码 [43] {}'.format(str(e)))

def Sub_Baidu(Sub_Domains):
    while 1:
        res = []
        with ProcessPoolExecutor(max_workers=pool_count) as pool:
            res = list(pool.map(Baidu,Sub_Domains))
        if res != []:
            res = list(set([y for x in res for y in x]))
            with ProcessPoolExecutor(max_workers=pool_count) as pool:
                result = pool.map(Add_Data_To_Url, res)
        # 每次跑完休息一阵子
        time.sleep(3600*12)


def Sub_Brute(Sub_Domains):
    for domain in Sub_Domains:
        res = []
        res = Brute(domain).start()
        res = list(set(res))
        if res != []:
            with ProcessPoolExecutor(max_workers=pool_count) as pool:
                result = pool.map(Add_Data_To_Url, res)
        time.sleep(60)


def Run_Crawl(Domains):
    while 1:
        try:
            target_url = URL.objects.filter(get='否')[0]
            url = target_url.url
            target_url.get = '是'
            target_url.save()
            # 这里需要提前设置的原因是，防止下一个进程启动重复 使用 同一个数据
        except Exception as e:
            time.sleep(600)
            # 在获取失败（数据库没数据存入），重试一次
            try:
                target_url = URL.objects.filter(get='否')[0]
                url = target_url.url
                target_url.get = '是'
                target_url.save()
            except Exception as e:
                print('错误代码 [31] {}'.format(str(e)))
                Error_Log.objects.create(url='获取URL失败', error='错误代码 [31] {}'.format(str(e)))
                return
        try:
            All_Urls = Crawl(url)
            if All_Urls:
                Sub_Domains1 = list(set([y for x in Domains for y in All_Urls if x in y]))
                if Sub_Domains1 != []:
                    with ProcessPoolExecutor(max_workers=pool_count) as pool:
                        result = pool.map(Add_Data_To_Url, Sub_Domains1)
                Other_Domains = list(set([y for x in Domains for y in All_Urls if x not in y]))
                if Other_Domains:
                    for url in Other_Domains:
                        try:
                            Test_Other_Url = Other_Url.objects.filter(url=url)
                            if list(Test_Other_Url) == []:
                                ip = get_host(url)
                                res = Get_Url_Info(url).get_info()
                                res_url = res.get('url')
                                res_title = res.get('title')
                                res_power = res.get('power')
                                res_server = res.get('server')
                                status = res.get('status')
                                res_ip = ip
                                if int(status) in Alive_Status:
                                    Other_Url.objects.create(url=res_url, title=res_title, power=res_power, server=res_server,status=status,ip=res_ip)
                        except Exception as e:
                            print('错误代码 [33] {}'.format(str(e)))
                            Error_Log.objects.create(url=url, error='错误代码 [33] {}'.format(str(e)))
        except Exception as e:
            print('错误代码 [32] {}'.format(str(e)))
            Error_Log.objects.create(url=url, error='错误代码 [32] {}'.format(str(e)))


def Sub_Crawl(pax,Sub_Domains):
    p = ProcessPoolExecutor(max_workers=pool_count)
    for i in pax:
        #p.submit(Run_Crawl,Sub_Domains)
        p.submit(Change_IP_Info)
        p.submit(Change_ShowData_Info,Sub_Domains)

if __name__ == '__main__':
    pass
    #Domains = list(set([x.strip() for x in open('domains.list', 'r', encoding='utf-8').readlines()]))
    #Domains = ['baidu.com','qq.com','jd.com','iqiyi.com','kuaishou.com','sina.com']
    # Sub_Baidu(Domains)
    # Sub_Brute(Domains)
    # Sub_Crawl(range(20),Domains)