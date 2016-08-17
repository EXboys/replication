import datetime
import os
import random
import time
import urlparse

from lib import fileExtension
from lib import proxyClean
from lib import proxyCollect
from lib.header import computer,mobile,spider,referer

def getValidIP(refresh):
    text = './log/proxy.log'
    now_time = datetime.datetime.now()
    create_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(os.stat(text).st_mtime)),
                                             "%Y-%m-%d %H:%M:%S")
    if (now_time - create_time).seconds >refresh*60:
        proxyCollect.main()
        proxyClean.main()
    valid = fileExtension.fileData().fileToList(text)
    return valid

def randReferer(url):
    rand = random.randint(0,10)
    #print rand
    if rand <= 4:
        refer = random.choice(referer)
    elif rand>4 and rand < 8:
        refer = url
    else:
        refer = urlparse.urlsplit(url)[1].split(':')[0]
    return refer

def run(url,header = 0,proxy=False,refresh = 30):
    logdir = './log'
    if not os.path.exists(logdir):
        try:
            os.mkdir(logdir)
            f = file('./log/proxy.log','w')
            f.close()
            if proxy:
                proxyCollect.main()
                proxyClean.main()
        except Exception as e:
            print e
    proxy = random.choice(getValidIP(refresh)) if proxy else ''
    if header == 0:
        headers = computer
    elif header == 1:
        headers = mobile
    else:
        headers = spider
    userAgent = random.choice(headers)
    referer = randReferer(url)
    header = {
        'user-agent':userAgent,
        'referer':referer,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection':'close',
        'Cache-Control':'no-cache',
        'Accept': '*/*',
    }
    return proxy,header

if __name__ == '__main__':
    print run('http;//www.baidu.com/test')