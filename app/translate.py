#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""

"""
import requests 
import hashlib
import random 

def translate(text): 
    appid = '20190531000303862'
    secretKey = 'rbFYX5EeBLecYBWqRuaG'
    q = text
    salt = random.randint(32768,65535)
    sign = appid+q+str(salt)+secretKey
    md5 = hashlib.md5() 
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()

    myurl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    url  = myurl+"?q="+q+"&from=en&to=zh&appid="+appid+"&salt="+str(salt)+"&sign="+sign

    reponse = requests.get(url)
    return reponse.json()['trans_result'][0]['dst']
