#!/usr/bin/python
# encoding=utf-8
import os
import signal
import subprocess
import time
import re
import thread

findtime = 60
maxretry = 5
bantime = 60

starttime = time.time()

ips = dict()
banips = dict()

def monitorLog(logFile):
	global starttime
	popen = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	pid = popen.pid
	print('Popen.pid:' + str(pid))
	while True:
		line = popen.stdout.readline().strip()
		ip = attackMatch(line)
		print "match ip:"+ip[0]
		if ip:
			nowtime = time.time() - starttime
			if nowtime > findtime:
			    starttime = nowtime
			    ips.clear()
			else:
			    hander(ip[0])
		print "banStopHander"
		banStopHander(ip[0])

def hander(ip):
    ip_tuple = ips.get(ip)
    if ip_tuple:
		num, isban = ip_tuple
		if num > maxretry and isban == False:
			banstart(ip)
			ips[ip] = (num+1, True)
		else:
			num += 1
			ips[ip] = (num, False)
			print "ip:"+ip+"-->num:"+str(num)
    else:
        ips[ip] = (1, False)

def attackMatch(line):
    #pattern = re.compile(r"(\d+.\d+.\d+.\d+).*(\[.*\]).*(\".*\/icons/poweredby.png.*HTTP).*$")
	pattern = re.compile(r"(\d+.\d+.\d+.\d+.).*$")
	match = pattern.match(line)
	if match:  
	    return match.groups(1)
	return False


def banstart(ip):
    global banips
    cmd = " /root/.init_sys/iptables -A INPUT -s "+ip+" -j REJECT"
    os.system(cmd)
    print "ban diao ip "+ ip
    banips[ip] =  time.time() 

def banStopHander():
    global banips
    while True:
    	for ip,banStartTime in banips:
    		nowbantime = time.time() - banStartTime
    		if nowbantime > bantime:
    	    		popen = subprocess.Popen(" /root/.init_sys/iptables -L --line-number|grep "+ip+"|awk '{print $1}' " , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    	        	n = popen.stdout.readline().strip()
    	        	cmd = " /root/.init_sys/iptables -D INPUT "+ n
    	        	os.system(cmd)
    			del banips[ip]
    	        	print "qu shiao ban diao ip "+ ip
        time.sleep(1)
        
if __name__ == '__main__':
    logFile = "/var/log/httpd/access_log"
    monitorLog(logFile)
    thread.start_new_thread( banStopHander, ( 1, ) )
    
