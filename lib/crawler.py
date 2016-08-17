# -*- coding: utf-8 -*-
import urllib2,urllib
import random,os,hashlib,json
import cookielib
import urlparse
import chardet
import time
import StringIO
import gzip
import re
import fileExtension

import socket
socket.setdefaulttimeout(8.0)


userAgent = [
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50\
    (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .\
    NET CLR 2.0.50727;.NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
]
referer = [
    'http://www.baidu.com',
    'http://www.weibo.com',
    'http://www.qq.com',
    'http://hangzhou.anjuke.com/',
    'http://hangzhou.anjuke.com/sale/rd1/?kw=&from=sugg',
    'http://www.anjuke.com/topic/?from=navigation',
    'http://blog.sina.com.cn/duancheng509',
    'http://www.cnblogs.com/xiaowuyi/archive/2012/03/09/2387173.html',
    'http://blog.csdn.net/tianzhu123/article/details/8187470',
    'http://baike.baidu.com/link?url=UupMPrM6xe0NkL5hGxCyOF1-Hqs-bGS8dI50WYvhiKNUw5BlMg_K4zHPz8oiq5GFQj_zfPdOArcz5-nT8GXWG_',
    'http://ent.qq.com/movie/',
]

class crawler:
    def __init__(self,url,isCookie = False,isProxy =False,proxyUsed = ''):
        self.url = url   # 请求目标网站
        self.domain   = urlparse.urlsplit(self.url)[1].split(':')[0]
        self.isCookie = isCookie
        self.isProxy  = isProxy
        if isProxy:
            if proxyUsed:   #判断是够是验证代理IP
                self.proxyUsed = proxyUsed
            else:
                proxyFile = 'log/proxy.log'
                arr = fileExtension.fileData().fileToList(proxyFile)
                self.proxyUsed = ''.join(random.choice(arr).split('//'))
        else:
            self.proxyUsed = 'localhost'
        if isCookie:
            cookieDir = 'cookie\\'+hashlib.md5(self.proxyUsed).hexdigest()
            if not os.path.exists(cookieDir):
                try:
                    os.mkdir(cookieDir)
                except e:
                    pass
            self.filename = 'cookie/'+hashlib.md5(self.proxyUsed).hexdigest()+'/'+ hashlib.md5(self.domain).hexdigest() + '.txt'


    #随机选择referer
    def randReferer(self):
        rand = random.randint(0,10)
        #print rand
        if rand <= 5:
            refer = self.domain
        elif rand>5 and rand < 8:
            refer =  self.url
        else:
            refer = random.choice(referer)
        return refer

    #使用cookie
    def getCookie(self):
        if not os.path.exists(self.filename):
            # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
            cookie = cookielib.MozillaCookieJar(self.filename)
            handler = urllib2.HTTPCookieProcessor(cookie)
            opener = urllib2.build_opener(handler)
            res = opener.open(self.url)
            cookie.save(ignore_discard=True, ignore_expires=True)
            urllib2.install_opener(opener)
        else:
            # 创建MozillaCookieJar实例对象
            cookie = cookielib.MozillaCookieJar()
            cookie.load(self.filename, ignore_discard=True, ignore_expires=True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            urllib2.install_opener(opener)

     # 代理服务器请求
    def getProxy(self):
        ip = 'http://' + self.proxyUsed
        fixed = {'http':ip}
        print ' Current proxy ip is '+ip   #shell输出
        proxy = urllib2.ProxyHandler(fixed)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    #请求连接
    def fecthUrl(self):
        try:
            req = urllib2.Request(self.url)
            req.add_header('User-Agent', random.choice(userAgent));
            req.add_header('Content-Type', 'application/x-www-form-urlencoded');
            req.add_header('Cache-Control', 'no-cache');
            req.add_header('Accept', '*/*');
            req.add_header('Referer', self.randReferer());
            req.add_header('Connection', 'Keep-Alive');
            if self.isCookie:
                self.getCookie()
            if self.isProxy:
                self.getProxy()
            response = urllib2.urlopen(req,timeout=8)
            #压缩网站解析
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                result = f.read()
            else:
                result =  response.read()
            # 将不是utf8的网站转码
            if chardet.detect(result)['encoding'] == 'GB2312':
                result = result.decode('GB2312','ignore')
            return result
        except Exception:
            print u"urlopen error\n"
            return None

#爬虫拓展工具
class crawlerTool:
    #ip 循环触发器
    def ipLoop(self,proxy,index):
        ipAll = fileExtension.fileData().fileToList(proxy)
        cur = index % len(ipAll)
        return ipAll[cur]

    #检查外网IP是否变更，用于VPN
    def checkIP(self,latest,excetpIP = '112.16.76.6'):
        nowIP = self.getIP(html)
        if nowIP==latest or nowIP == excetpIP:
            print 'This ip has requested too much'
            time.sleep(2)
            self.checkIP(latest)
        else:
            return self.getIP(html)

    #从文件中匹配所有的ip
    def getIP(self,obj):
        url = 'http://http://1212.ip138.com/ic.asp'
        html = crawler(url, isCookie=True).fecthUrl()
        regex = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',re.IGNORECASE)
        ip = re.findall(regex, obj)
        print ip
        return ip

    # 从文件中匹配所有的Phone
    def getPhone(self,fobj):
        regex = re.compile(r'1\d{10}', re.IGNORECASE)
        phonenums = re.findall(regex, fobj)
        print phonenums
        return phonenums

    # 从文件中匹配所有的Mails
    def getMail(self,fobj):
        regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
        mails = re.findall(regex, fobj)
        print mails
        return mails