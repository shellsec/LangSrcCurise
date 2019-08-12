# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:43
@file: Subdomain_Baidu.py
"""
import requests
import re
import requests
import re
import time
import random
from urllib.parse import quote,urlparse
requests.packages.urllib3.disable_warnings()
timeout = 15



headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
def Get_Resp(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'BAIDUID=832CF61CDAEF34C68E7CA06F591DF82A:FG=1; BIDUPSID=832CF61CDAEF34C68E7CA06F591DF82A; PSTM=1544962484; BD_UPN=12314753; BDUSS=RWclRJUURtR25qZWxKZWZiN0JuSlJVTWpKRjhvb3ROdmIyNnB0eEwwY2FVOWxjSVFBQUFBJCQAAAAAAAAAAAEAAADS9fNj0-~PxM600esAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrGsVwaxrFcck; cflag=13%3A3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; delPer=0; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_PS_PSSID=1453_21088_20692_28774_28720_28558_28832_28584; B64_BOT=1; BD_CK_SAM=1; PSINO=1; sug=3; sugstore=1; ORIGIN=2; bdime=0; H_PS_645EC=87ecpN5CzJjR5UwprsIowJPhqh6m9t1xGvxRkjeNmvcXBhI86ytKIjXLMhQ',
        'Host': 'www.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

    }

    try:
        r = requests.get(url,headers=headers,timeout=20,verify=False)
        #print(r.content)
        return r.content
    except Exception as e:
        #print(e)
        return None

def Baidu(domainkey):
    '''
    传递参数为子域名
    返回的是存在存在子域名的完整网址
    '''
    result = []
    if '//' in domainkey:
        domain = domainkey.split('//')[1].replace('www.','')
    else:
        domain = domainkey.replace('www.','')
        domain = domain.split('.')[0].encode()

    for page in range(0,100,10):
        url = 'http://www.baidu.com/s?wd=site%3A{}&pn={}'.format(quote(domainkey),page)
        #print(url)
        try:
            resp = Get_Resp(url)
            if not resp:
                resp = Get_Resp(url)
            if resp:
                subdomain = re.findall(b'-decoration:none;">(.*?)/&nbsp',resp)
                for x in subdomain:
                    # print(b'1111111:'+x)
                    if domain in x:
                        if b'http' in x:
                            if b'..' in x:
                                result.append(x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.append(x.decode().rstrip('/'))
                            if b'&' in x:
                                result.append(x.decode().split('&')[0].rstrip('/'))
                            else:
                                result.append(x.decode().rstrip('/'))

                        else:
                            if b'..' in x:
                                result.append('http://'+x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.append('http://'+x.decode().rstrip('/'))
                            if b'&' in x:
                                result.append('http://'+x.decode().split('&')[0].rstrip('/'))
                            else:
                                result.append('http://'+x.decode().rstrip('/'))

                subdomain = re.findall(b'style="text-decoration:none;">(.*?)/.*?class="c-tools',resp)
                for x in subdomain:
                    # print(b'2222222:'+x)
                    if domain in x:
                        if b'http' in x:
                            if b'..' in x:
                                result.append(x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.append(x.decode().rstrip('/'))
                        else:
                            if b'..' in x:
                                result.append('http://' + x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.append('http://' + x.decode().rstrip('/'))
        except Exception as e:
            print(e)
    returl_result = []
    res = (list(set(result)))
    print('首次捕获子域名:'+str(res))
    for real in res:
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA, 'Connection': 'close'}
            r = requests.get(url=real, headers=headers, verify=False, timeout=timeout)
            time.sleep(0.1)
            if b'Service Unavailable' not in r.content and b'The requested URL was not found on' not in r.content and b'The server encountered an internal error or miscon' not in r.content and '.show.jj.cn' not in real and 'en.alibaba.com ' not in real:
                if r.status_code == 200 or r.status_code == 301 or r.status_code==302:
                # 这里读取验证码即可
                    real_url = r.url.rstrip('/')
                    returl_result.append(urlparse(real_url).scheme + '://' + urlparse(real_url).netloc)
        except Exception as e:
            # print(e)
            pass
    return list(set(returl_result))
    # 返回数据是完整的url，进过存活检测
if __name__ == '__main__':
    print(Baidu('baidu.com'))