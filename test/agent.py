# -*- coding: UTF-8 -*-
import random

agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

def get_user_agents():
    return random.choice(agent)

def hash33(t):
    e = 0
    for i in range(len(t)):
        e += (e << 5) + ord(t[i])
    return 2147483647 & e

def getToken(p_skey):
    str_ = p_skey or ''
    hash_ = 5381
    for i in range(len(str_)):
        hash_ += (hash_ << 5) + ord(str_[i])
    return hash_ & 0x7fffffff

def guid():
    import uuid
    return str(uuid.uuid4()).upper()

def S():
    import time,re
    e = int(time.time() * 1000)
    return re.sub('[xy]', lambda c: '%x' % (random.randint(0, 15) if c.group() == 'x' else (e + random.randint(0, 16)) % 16 | 8), 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx')

def a(a):
    import random
    b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    c = ""
    for _ in range(a):
        e = int(random.random() * len(b))
        c += b[e]
    return c