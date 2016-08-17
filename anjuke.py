# -*- coding: utf-8 -*-
import json
import math
import random
import socket
import threading
import time

from bs4 import BeautifulSoup
from lib import crawler
from lib import fileExtension


class anjukeThread(threading.Thread):
    def __init__(self,url,sleepSec,ipnum):
        super(anjukeThread, self).__init__()
        self.url = url
        self.sleepSec = sleepSec
        self.ipnum = ipnum

    #执行程序
    def run(self):
        #anjuke().getDetail(self.url,self.sleepSec,self.ipnum)
        anjuke().getDetail(self.url,self.sleepSec)



#安居客爬虫
class anjuke:
    def __init__(self):
        self.toCrawl = 'assets/anjuke/toCrawl'
        self.temp = 'assets/anjuke/temp'
        self.analysis = 'assets/anjuke/analysis'
        self.proxy = 'assets/proxy.log'
        self.result = ''

    #获取城市列表
    def getCity(self,url):
        self.result = False
        try:
            self.result = crawler.crawler(url).fecthUrl()
        except Exception as e:
            print e
            pass
        if self.result:
            soup = BeautifulSoup(self.result, 'html.parser')
            location = soup.find('div',{'class':'cities_boxer'})
            f = open(self.toCrawl,'w')
            for link in location.findAll('a'):
                f.write(link.get('href')+'\n')
            return True
        else:
            return False

    #获取城市具体细节
    #def getDetail(self,line,sleepSec,ipnum):
    def getDetail(self,line,sleepSec):
        hasNext = True                                                      #是否有下一页
        i=1
        #ip = crawler.crawlerTool().ipLoop(self.proxy, ipnum)
        while hasNext:
            target =  line.replace('\n','')+'/sale/p%s/#filtersort' % (i)    #某站重复请求
            print '\n Current request url is ',target
            try:
                #self.result = crawler.crawler(target,isProxy =True,proxyUsed = ip).fecthUrl()
                self.result = crawler.crawler(target).fecthUrl()
                print self.result
            except socket.error, e:
                print e
                time.sleep(random.randrange(1, sleepSec*60))
                pass
            if self.result:
                i+=1
                if(i % 5 ==0):                                      #每请求5次换IP,沉睡时间翻倍
                    ipnum+=1
                    time.sleep(random.randrange(1, sleepSec*3))
                else:
                    hasNext = self.analysisDoc(self.result)
                    print 'successed! sleep +1'
                    time.sleep(random.randrange(1,sleepSec))        #同一ip请求随机沉睡
            else:                                                   #请求失败换代理ip
                ipnum+=1
                if ipnum % 10 == 0:                                 #请求失败10次沉睡1-3秒
                    print 'failed! sleep +1'
                    time.sleep(random.randrange(1,sleepSec))
                pass


    #本文分析
    def analysisDoc(self,result):
        hasNext = True
        f = open(self.temp, 'a') #以添加的形式打开临时文件
        soup = BeautifulSoup(result, 'html.parser')
        try:
            pageContent = soup.find('div', {'class': 'multi-page'})  # 检索页面是否有下一页
        except:
            pass
        if pageContent:
            hasNext = pageContent.find('a', {'class', 'aNxt'})
            if hasNext:
                hasNext = True
            else:
                hasNext = False
        else:
            hasNext = False
        house = soup.findAll('div', {'class': 'house-details'})
        for item in house:
            items = item.text.strip().split('\n')
            address = ''
            company = ''
            addressTemp = item.find('span', {'class': 'comm-address'})
            companyTemp = item.find('a', {'data-company': True})
            if addressTemp:
                address = ''.join(addressTemp.text.split('\n')).replace(' ', '')
            if companyTemp:
                company = companyTemp['data-company']
            res = address, items[0], items[3], company  #抓取到的数据写入临时文件
            print res
            f.write(json.dumps(list(res)) + '\n')
        #f.close()
        return hasNext

    def clearTemp(self):
        f = open(self.temp,'w')
        text = ''
        f.write(text)



def main():
    if anjuke().getCity(url):
        thPool = []
        lines = open('assets/anjuke/toCrawl', 'r').readlines()
        listLines =list(set(lines))
        groupNum =math.ceil(len(listLines)/20)
        listItem = fileExtension.fileData().divList(listLines,3)
        for listLine in listItem:
            threadNum = 1
            ipnum = 0
            for line in listLine:  # 装载多线程池
                print 'This is url: ', line
                ipnum += 1
                thPool.append(anjukeThread(line, 3, ipnum))
            for th in thPool:      # 启动多线程
                try:
                    threadNum += 1
                    th.start()
                    if threadNum % 100 == 0:
                        time.sleep(random.randrange(1, 5))
                except Exception as e:
                    print e, 'when thread running'
            for th in thPool:       # 监听结束线程
                try:
                    th.join()
                except Exception as e:
                    print e, 'when thread end'

if __name__ == '__main__':
    main()
