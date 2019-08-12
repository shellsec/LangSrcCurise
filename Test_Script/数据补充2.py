# -*- encoding: utf-8 -*- 
import socket
# import django
# import os
# import sys
# pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0,pathname)
# sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
# django.setup()
# from app.models import Domains
import requests,re,sys,io,time,queue,threading
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

IP_66_headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Cookie': '__jsluid_h=d26e11a062ae566f576fd73c1cd582be; __jsl_clearance=1563459072.346|0|lMwNkWbcOEZhV8NGTNIpXgDvE8U%3D',
'Host': 'www.66ip.cn',
'Referer': 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=2',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

IP_XC_HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTBmOWM5NDc1OWY4NjljM2ZjMzU3OTM1MGMxOTEwMjNhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWVGT0Z1dVpKUXdTMVFEN1JHTnJ3VVhYS05WWlIzUlFEcncvM1daVER2blk9BjsARg%3D%3D--66057a30315f0a34734318d2e6963e608017f79e; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1563458856; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1563460669',
'Host': 'www.xicidaili.com',
'If-None-Match': 'W/"b7acf7140e4247040788777914f600e1"',
'Referer': 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=2',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

IP_66_URL = 'http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
IP_XC_URL = 'http://www.xicidaili.com/nn/'

def Get_Url_Content(url,headers):
    try:
        r = requests.get(url,headers=headers,timeout=20)
        return r.content
    except:
        return None


q = queue.Queue()
Q = queue.Queue()

def Get_IP_LIST():
    for i in range(1,10):
        content = Get_Url_Content(IP_66_URL+str(i),IP_66_headers)
        if content != None:
            try:
                ips = re.findall(b'\t(\d.*?:\d.*\d)<br />',content)
                for ip in ips:
                    #print('抓到IP:{}'.format(ip.decode()))
                    q.put(ip.decode())
            except:
                pass
        content = Get_Url_Content(IP_XC_URL+str(i),IP_XC_HEADERS)
        if content:
            try:
                ips = re.findall(b'<td>(\d.*\.\d.*)</td>\n.*?<td>(\d.*)</td>\n', content)
                for i in ips:
                    ip = (i[0].decode() + ':' + i[1].decode())
                    #print('抓到IP:{}'.format(ip))
                    q.put(ip)
            except:
                pass

def Get_Alive_IP():
    while 1:
        proxies={}
        ip = q.get()
        print('检测IP:{}'.format(ip))
        proxies['http'] = str(ip)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        try:
            url = 'https://www.baidu.com/link?url=wa0u02Xzbi6o8gZ9prRGLlHFpbSvyuVgN0Yf5RfJwP7&amp;wd=&amp;eqid=8cee35f300000518000000025c94e4a0'
            req2 = requests.get(url=url, proxies=proxies, headers=headers, timeout=5)
            if req2.status_code == 200:
                print('网址：{} 代理IP：{} 访问成功'.format(req2.url,ip))
                Q.put(ip)
        except Exception as e:
            #print(e)
            pass


def Get_Content(domain):
    while 1:
        if not Q.empty():
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
                       'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
                       'Cookie': 'Hm_lvt_de25093e6a5cdf8483c90fc9a2e2c61b=1553260543; _csrf=fb33ebded8b9efc940bdf6a20996f570283a8eb5299ea6956e8673a8b2f021f1a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22GcFvhvYi7zUi4yBbOJN7kkA26ochnfCs%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1565279531,1565326170; allSites=baidu.com%7Cle.com%7Cdouyu.com%7Cly.com%7Cbugx.io%7Cmogujie.com%2C0; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1565327289',
                       'Host': 'icp.aizhan.com', 'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            proxies = {'http': Q.get()}
            try:
                url = 'https://icp.aizhan.com/'+domain
                print(url)
                r = requests.get(url=url,headers=headers,timeout=15,proxies=proxies)
                content = r.content.decode()
                return content
            except Exception as e:
                return None
        else:
            time.sleep(3)
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
    for i in range(20):
        t1 = threading.Thread(target=Get_IP_LIST)
        t2 = threading.Thread(target=Get_Alive_IP)
        t1.start()
        t2.start()
    #
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
            # BA = Domains.objects.filter(url=task)[0]
            # if BA.BA_id == '暂无信息' or BA.BA_id == '获取失败':
            #     BA.url = task
            #     BA.BA_sex = bsex
            #     BA.BA_name = bname
            #     BA.BA_id = bid
            #     BA.save()
            # else:
            #     print('{} 该站点信息齐全'.format(task))
        except Exception as e:
            print(e)
