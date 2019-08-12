# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:14
@file: Brute.py
"""
import asyncio
import aiodns
import aiomultiprocess
import aiohttp
from urllib.parse import urlparse
import multiprocessing
import os
import random
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

Alive_Status = [200,301,302,404]

class Brute:
    def __init__(self,domain):
        self.domain = domain
        self.dicts = list(set([subdoma.strip() + '.' + self.domain for subdoma in open('SubDomainDict.txt', 'r').readlines()]))

    async def check_url_alive(self,url):
        print('Scan:'+url)
        async with asyncio.Semaphore(1000):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                try:
                    async with session.get('http://'+url,timeout=15) as resp:
                        if resp.status in Alive_Status:
                            content = await resp.read()
                            #print(content)
                            if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                                u = urlparse(str(resp.url))
                                return u.scheme+'://'+u.netloc
                except Exception as e:
                    #print(e)
                    pass
                try:
                    async with session.get('https://' + url,timeout=15) as resp:
                        if resp.status in Alive_Status:
                            content = await resp.read()
                            #print(content)
                            if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                                u = urlparse(str(resp.url))
                                return u.scheme+'://'+u.netloc
                except Exception as e:
                    #print(e)
                    pass

    async def Aio_Subdomain(self,subdomain):
        # 传入参数为 xx.xx.com 返回结果为 xx.xx.com [解析结果]
        # 不存在则返回 NONE NOEN
        resolver = aiodns.DNSResolver(timeout=1)
        try:
            result = await resolver.query(subdomain, 'A')
            return subdomain, result
        except Exception as e:
            return None, None

    async def get_result_from_dns(self,subhosts):
        res = set()
        async with aiomultiprocess.Pool(processes=8,childconcurrency=8) as pool:
            # 如果你想跑满CPU 修改上面的线程和协程数量即可
            results = await pool.map(self.Aio_Subdomain, subhosts)
        for result in results:
            subdomain, answers = result
            if answers != None and subdomain != None:
                res.add(subdomain)
                print((subdomain,answers))
        return list(res)

    def get_result_from_dns_result(self,loop):
        # 返回结果是通过DNS查询获取的子域名
        result = loop.run_until_complete(self.get_result_from_dns(self.dicts))
        if len(result) > 1000: # 泛解析
            return random.sample(result,10)
        else:
            return result

    async def main(self,urls):
        async with aiomultiprocess.Pool(processes=8,childconcurrency=8) as pool:
            result = await pool.map(self.check_url_alive,urls)
        return [x for x in result if x is not None]


    def start(self):
        multiprocessing.freeze_support()
        loop = asyncio.get_event_loop()
        brute_domains = self.get_result_from_dns_result(loop)
        print('爆破获取总子域名数量:{}'.format(len(brute_domains)))
        alive_urls = loop.run_until_complete(self.main(brute_domains))
        print('爆破获取总存货网址数量:{}'.format(len(alive_urls)))
        return alive_urls




if __name__ == '__main__':
    r = Brute('baidu.com')
    res = r.start()
    print(res)