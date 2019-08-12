# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 8:03
@file: models.py
"""
from django.db import models

class IP(models.Model):
    uid = models.AutoField()
    ip = models.CharField(max_length=15,primary_key=True)
    servers = models.TextField()
    host_type = models.CharField(max_length=10)
    alive_urls = models.TextField()# 字典类型，存活网址+标题
    area = models.CharField(max_length=10)
    change_time = models.TimeField(auto_now_add=True)
models.ForeignKey
class URL(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=18,unique=True)
    ip = models.ForeignKey(IP,on_delete=models.DO_NOTHING())
    change_time = models.TimeField(auto_now_add=True)

class Other_Url(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=18,unique=True)
    title = models.CharField(max_length=60, default='获取失败')
    power = models.CharField(max_length=10, default='获取失败')
    server = models.CharField(max_length=10, default='获取失败')

class Show_Date(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=18,unique=True)
    title = models.CharField(max_length=60,default='获取失败')
    power = models.CharField(max_length=10,default='获取失败')
    server = models.CharField(max_length=10,default='获取失败')
    content = models.TextField()
    ip = models.CharField(max_length=15)
    servers = models.TextField()
    host_type = models.CharField(max_length=10)
    baidu_url = models.TextField()
    belong_domain = models.CharField(max_length=10,db_index=True)
    change_time = models.TimeField(auto_now_add=True)


