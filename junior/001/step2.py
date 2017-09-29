#!/usr/bin/python
# -*- coding: utf-8 -*-

import cookielib
import requests, os, time, re
from bs4 import BeautifulSoup

# 当前项目路径
cur_path = os.getcwd() + '/'

class ZhiHuSpider(object):
    '''
    模拟知乎登陆

    Attribute:
        session: 建立会话
        url_signin: 登陆页面链接
        url_login: 登陆接口
        url_captcha: 验证码链接
        headers： 请求头部信息
        num: 识别验证码次数
    '''

    def __init__(self):
        self.session = requests.Session()
        self.session.cookies = cookielib.LWPCookieJar(filename='cookies')
        self.url_signin = 'https://www.zhihu.com/#signin'
        self.url_login = 'https://www.zhihu.com/login/phone_num'
        self.url_captcha = 'https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        self.num = 1

    def load_cookies(self):
        try:
            self.session.cookies.load(ignore_discard=True)
            print("Cookie 加载成功")
        except:
            print("Cookie 未能加载")

    def get_captcha(self):
        # raw_input('capture:')
        if not os.path.exists(cur_path + 'captcha'):
            os.mkdir(cur_path + 'captcha')
        captcha_text = ''
        # while True:
        # 下载验证码图片
        captcha = self.session.get(self.url_captcha, headers=self.headers).content
        captcha_path = cur_path + 'captcha/captcha.gif' # 验证码图片路径
        captcha_path_new = cur_path + 'captcha/captcha_new.gif' # 处理后的验证码图片路径
        with open(captcha_path, 'wb') as f:
            f.write(captcha)
        # 新手教学，不能弄太复杂搞自动化识别
        # 所以请打开当前目录自己看图片并输入吧
        return raw_input('capture:')

    def isLogin(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = 'https://www.zhihu.com/settings/profile'
        login_code = self.session.get(url, headers=self.headers, allow_redirects=False).status_code
        if login_code == 200:
            print('您已经登录')
            return True
        else:
            print('您尚未登录')
            return False

    def login(self, username, password):
        '''
        登陆接口

        Args:
            username: 登陆账户
            password: 登陆密码
        Returns:
            返回登录结果list
        '''
        soup = BeautifulSoup(self.session.get(self.url_signin, headers=self.headers).content, 'html.parser')

        # 获取xsrf_token
        xsrf = soup.find('input', attrs={'name': '_xsrf'}).get('value')

        post_data = {
            '_xsrf': xsrf,
            'phone_num': username,
            'password': password,
            'captcha': self.get_captcha()
        }
        login_ret = self.session.post(self.url_login, post_data, headers=self.headers).json()
        # return login_ret
        if login_ret['r'] == 0:
            print('登陆成功! ')
            self.session.cookies.save()
            print('已保存 session')
        else:
            print '登陆失败 '
            print login_ret

if  __name__ == '__main__':
    zhihu = ZhiHuSpider()
    zhihu.load_cookies()
    if zhihu.isLogin():
        pass
    else:
        zhihu.login('account', 'passwd')


