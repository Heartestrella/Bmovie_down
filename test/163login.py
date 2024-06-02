import base64
import codecs
import pickle
from Crypto.Cipher import AES  
import qrcode
import agent
import time
import requests
import os

class CloudMusicLogin:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.headers = {'User-Agent': agent.get_user_agents(),'Referer':'https://music.163.com/'}
        self.iv = "0102030405060708"
        self.e = "010001"
        self.f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.g = "0CoJUm6Qyw8W8jud" # (["爱心", "女孩", "惊恐", "大笑"])的值
        self.i = agent.a(16) 
        self.key = agent.S() 

    def keys(self, key):
        while len(key) % 16 != 0:
            key += '\0'
        return str.encode(key)

    def AES_aes(self, t, key, iv):
        p = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
        encrypt = str(base64.encodebytes(AES.new(self.keys(key), AES.MODE_CBC,self.keys(iv)).encrypt(str.encode(p(t)))), encoding='utf-8')
        return encrypt

    def RSA_rsa(self, i, e, f):
        return format(int(codecs.encode(i[::-1].encode('utf-8'), 'hex_codec'), 16) ** int(e, 16) % int(f, 16), 'x').zfill(256)

    def params(self):
        d = str({'key': self.key, 'type': "1", 'csrf_token': ""})
        return self.AES_aes(self.AES_aes(d, self.g, self.iv), self.i, self.iv)

    def encSecKey(self):
        return self.RSA_rsa(self.i, self.e, self.f)

    #判断cookie是否有效
    def islogin(self, session):
        try:
            session.cookies.load(ignore_discard=True)
        except Exception:
            pass
        csrf_token = session.cookies.get('__csrf')
        c = str({'csrf_token': csrf_token})
        try:
            loginurl = session.post('https://music.163.com/weapi/w/nuser/account/get?csrf_token={}'.format(csrf_token), data={'params': self.AES_aes(self.AES_aes(c, self.g, self.iv), self.i, self.iv), 'encSecKey': self.encSecKey()}, headers=self.headers).json()
            if '200' in str(loginurl['code']):
                print('Cookies值有效：',loginurl['profile']['nickname'],'，已登录！')
                return session, True
            else:
                print('Cookies值已经失效，请重新扫码登录！')
                return session, False
        except:
            print('Cookies值已经失效，请重新扫码登录！')
            return session, False

    #登录扫码保存cookie
    def login(self):
        session = requests.session()
        if not os.path.exists('163.cookie'):
            with open('163.cookie', 'wb') as f:
                pickle.dump(session.cookies, f)
        session.cookies = pickle.load(open('163.cookie', 'rb'))
        session, status = self.islogin(session)
        if not status:
            getlogin = session.post('https://music.163.com/weapi/login/qrcode/unikey?csrf_token=', data={'params': self.params(), 'encSecKey': self.encSecKey()}, headers=self.headers).json()
            pngurl = 'https://music.163.com/login?codekey=' + getlogin['unikey'] + '&refer=scan'
            qr = qrcode.QRCode()
            qr.add_data(pngurl)
            qr.print_ascii(invert=True)
            tokenurl = 'https://music.163.com/weapi/login/qrcode/client/login?csrf_token='
            while 1:
                u = str({'key': getlogin['unikey'], 'type': "1", 'csrf_token': ""})
                qrcodedata = session.post(tokenurl, data={'params': self.AES_aes(self.AES_aes(u, self.g, self.iv), self.i, self.iv), 'encSecKey': self.encSecKey()}, headers=self.headers).json()
                if '801' in str(qrcodedata['code']):
                    print('二维码未失效，请扫码！')
                elif '802' in str(qrcodedata['code']):
                    print('已扫码，请确认！')
                elif '803' in str(qrcodedata['code']):
                    print('已确认，登入成功！')
                    break
                else:
                    print('其他：', qrcodedata)
                time.sleep(2)
            with open('163.cookie', 'wb') as f:
                pickle.dump(session.cookies, f)
        return session

if __name__ == '__main__':
    cloud_music_login = CloudMusicLogin()
    cloud_music_login.login()
