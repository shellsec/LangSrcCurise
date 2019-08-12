# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:07
@file: tasks.py
"""
from __future__ import absolute_import, unicode_literals
from .celery import app
import time












    domains = list(set([x.strip() for x in open('domains.txt', 'r', encoding='utf-8').readlines()]))
    # 要扫描的保存在domains.txt
    for domain in domains:
        print('当前检测域名为:{}'.format(domain))
        dicdic = 'Sub_Big_Dict.txt'
        t1 = time.time()

        result_0 = get_result(inp=domain, loop=loop,dicdic=dicdic)
        print(result_0)
        print('二级域名获取数量为 : {} '.format(len(result_0)))
        print('耗时 : {}'.format(time.time()-t1))

        if result_0 != []:
            for url in result_0:
                with open('domain_log', 'a+', encoding='utf-8')as a:
                    a.write(url + '\n')
            res = loop.run_until_complete(main(result_0))
            http_result = list(set([x for x in res if x != None]))
            print(http_result)
            if len(http_result)>1000:
                # 泛解析  浪费本菜感情
                http_result = random.sample(http_result,10)
            if http_result != []:
                print('二级域名存活数量为 : {} '.format(len(http_result)))
                Write_Database(domain,http_result)

            # 从这开始爆破三级域名，不过我直接注释掉了，感觉有些浪费时间


@app
def