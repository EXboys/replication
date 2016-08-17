# -*- coding: utf-8 -*-
import socket
import threading
import time

from pyquery import PyQuery as pq
from crawler import crawler


#西祠多线程代理爬虫
class xiciProxy(threading.Thread):
    def __init__(self, url,pageID,nsec):
        super(xiciProxy, self).__init__()
        self.url = url
        self.page = pageID
        self.nsec = nsec

    def run(self):
        target = self.url+str(self.page)
        print target
        try:
            result = crawler(target,isCookie=False,isProxy=False).fecthUrl()
            if result:
                doc = pq(result)
                tr = doc('table #ip_list tr')
                for k,item in enumerate(tr.items()):
                    if k >= 1:
                        d = pq(item)
                        tds = d('td').text().split(' ')
                        ip = tds[1]
                        port = tds[2]
                        protocol = tds[5]
                        if protocol == 'HTTP':
                            print ip+':'+port
                            f.write('%s:%s\n'%(ip,port))
                time.sleep(0.5)
            else:
                pass
        except socket.error:
                return None

#快代理多线程代理爬虫
class kuaiProxy(threading.Thread):
    def __init__(self, url,pageID,nsec):
        super(kuaiProxy, self).__init__()
        self.url = url
        self.page = pageID
        self.nsec = nsec

    def run(self):
        #target = self.url+str(self.page)
        target = self.url+str(self.page)
        print target
        try:
            result = crawler(target,isCookie=False,isProxy=False).fecthUrl()
            if result:
                doc = pq(result)
                tr = doc('div#index_free_list tbody tr')
                for item in tr.items():
                        d = pq(item)
                        tds = d('td').text().split(' ')
                        ip = tds[0]
                        port = tds[1]
                        #protocol = tds[5]
                        print ip + ':' + port
                        f.write('%s:%s\n' % (ip, port))
                time.sleep(0.5)
            else:
                pass
        except socket.error:
                return None

def now():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def main():
    thPool = []
    global f
    f = open('./log/proxyToTest.log', 'a') #文件末尾添加内容
    print 'starting at:', now()
    for i in range(1,5):
        thPool.append(xiciProxy('http://www.xicidaili.com/nn/',i, 2))
        thPool.append(kuaiProxy('http://www.kuaidaili.com/proxylist/',i, 2))
        #thpool.append(kuaiProxy('http://www.cdtest.com/1.html', i, 2)) 本地开发测试链接
    for th in thPool:
        th.start()
    for th in thPool:
        th.join()
    f.close()
    print 'all Done at:', now()

if __name__ == '__main__':
    main()