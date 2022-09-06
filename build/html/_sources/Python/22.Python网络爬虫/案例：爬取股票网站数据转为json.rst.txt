.. contents::
   :depth: 3
..

案例：爬取股票网站数据转为json
==============================

::

   #!/usr/bin/env python
   # -*- coding:utf8 -*-
   # auther; 18793
   # Date：2019/6/27 14:11
   # filename: 获取json数据.py

   """ 获得动态数据"""
   import re
   import urllib.request

   url = "http://hq.stock.sohu.com/cn/063/cn_000063-1.html?_=1561615833994"

   req = urllib.request.Request(url)

   with urllib.request.urlopen(req) as response:
       data = response.read()
       htmlstr = data.decode("gbk")
       # print(htmlstr)
       htmlstr = htmlstr.replace("fortune_hq(", "")
       htmlstr = htmlstr.replace(")", "")
       print("替换后的：", htmlstr)
