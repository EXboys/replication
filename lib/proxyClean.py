# -*- coding: utf-8 -*-
import random
import threading
import time
from pyquery import PyQuery as pq
from crawler import crawler


#多线程代理爬虫验证
class clean(threading.Thread):
    def __init__(self,url,proxyUsed,sleepTime):
        super(clean, self).__init__()
        self.url = url
        self.proxyUsed = proxyUsed
        self.sleepTime = sleepTime

    def run(self):
        try:
            result = crawler(self.url,isCookie=False,isProxy=True,proxyUsed=self.proxyUsed).fecthUrl()
            if result:
                doc = pq(result)
                print doc('title').text()
                if u'无法访问' or u'错误' not in doc('title').text():
                    self.save(self.proxyUsed)
                else:
                    print 'failed open url'
                time.sleep(self.sleepTime)
            else:
                pass
        except Exception:
            return None

    def save(self,text):
        f = open('./log/proxy.log', 'a')  # 文件末尾添加内容
        f.write(text)
        print 'Success ip ',text


def now():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def main():
    thPool = []
    target = [
        'http://www.baidu.com',
        'http://www.weibo.com',
        'http://www.qq.com',
        'http://hangzhou.anjuke.com/',
        'http://ent.qq.com/movie/',
        'http://www.taobao.com',
        'http://www.vip.com/',
        'https://www.hao123.com/',
        'http://www.gome.com.cn/',
        'http://tieba.baidu.com/',
    ]
    print 'starting at:', now()
    proxyFile = './log/proxyToTest.log'
    #proxyFile = '../assets/proxy.log'
    lines = open(proxyFile, 'r').readlines()
    print lines
    i=1
    for line in list(set(lines)):                   #装载多线程池
        print 'This is ip ',line
        proxyUsed = ''.join(line.split('//'))
        thPool.append(clean(random.choice(target),proxyUsed,1))
    for th in thPool:                               #启动多线程
        try:
            i+=1
            th.start()
            if i% 100 ==0:
                print 'Fuck! I need have a rest!'
                time.sleep(random.randrange(1,5))
        except Exception as e:
            print e,'when thread running'
    for th in thPool:                               #监听结束线程
        try:
            th.join()
        except Exception as e:
            print e,'when thread end'
    print 'all Done at:', now()

if __name__ == '__main__':
    main()