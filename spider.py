import urllib2
import threading
from optparse import OptionParser
from bs4 import BeautifulSoup
import sys
import re
import urlparse
import Queue
import hashlib

#set args deal function
def deal_opt():
    usage = "usage: ./%prog [options] "
    parser = OptionParser(usage=usage, version="%prog 1.0")

    parser.add_option('-d',  dest = 'deep',
                      default=1,
                      help="set the deep,eg: -d 3")
    parser.add_option('-u',
                      dest ='url',
                      help = "set the url, eg: -u 'http://www.baidu.com'")
    parser.add_option('--threads',
                      dest ='threads',
                      default = 5,
                      help = "set the threads, eg: --threads = 10")
    
    return parser


class UrlSpider(threading.Thread):
    def __init__(self,  url_queue, urled, data_queue, deep):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.urled = urled
        self.data_queue = data_queue
        self.deep = deep
        
    def run(self):
        while True:
            num, url = self.url_queue.get()
            print num,url,url_queue.qsize()
            if num <= self.deep:
                num = num + 1
                self.url_spider(num, url)
                urlhash = hashlib.md5(url).hexdigest()
                self.urled[urlhash] = True
            else:
                break
            
    def url_spider(self, num, url):
        urlarr = urlparse.urlparse(url)
        try:
            u = urllib2.urlopen(url)
        except:
            print 'error'
            return
        chunk =  u.read()
        self.data_queue.put( chunk )
        soup = BeautifulSoup(chunk)
        a =  soup.findAll('a')
        for i in a:
            if i.has_attr('href'):
                h = i.attrs['href']
                if h[:1] != 'h':
                    h = urlarr.scheme+'://'+urlarr.netloc+h
                try:
                    urlhash = hashlib.md5(h).hexdigest()
                except:
                    continue
                if not self.urled.has_key(urlhash):
                    print (num, h)
                    self.url_queue.put( (num, h) )
                
   
    
class DatamineSpider(threading.Thread):
    def __init__(self, url_queue, data_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.data_queue = data_queue
        
    
    def run(self):
        while True:
            data = self.data_queue.get()  
            print data    

class PoolManage(object):
    def __init__(self):
        self.pool = {}
    def creat(self, key, threads):
        self.pool[key] = threads
    def start(self, key):
        for x in self.pool[key]:
            #x.setDaemon(True)
            x.start()
    def stop(self, key):
        exit()            

if __name__ == '__main__':
    
    opt = deal_opt()
    url_queue = Queue.Queue()
    urled = {}
    data_queue = Queue.Queue()
    if len(sys.argv) <= 1:
        print opt.print_help()
    else:
        (options, args) = opt.parse_args()
        url = (1, options.url)
        deep = int(options.deep)
        url_queue.put(url)
        
        pool = []
        for x in xrange(int(options.threads)):
            pool.append( UrlSpider(url_queue, urled, data_queue, deep) )
            
        poolmanager = PoolManage()
        poolmanager.creat('urlspider', pool)
        poolmanager.start('urlspider')
        
            
        
        
        
        

                 

            

                
        
    