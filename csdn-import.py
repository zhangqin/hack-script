#!/usr/bin/env python

import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="xxxxxxx", db="bulu", charset="utf8")
cursor = conn.cursor()

sql = "insert into sl_user(nickname, password, email, website) values(%s, %s, %s, 'csdn')"
success_count = fail_count = 1

fp = open("www.csdn.net.sql", "r")
while True:
	line = fp.readline()
	if len(line) == 0:
		break
	data = line.strip().split("#")
	params = (data[0], data[1], data[2])
	n = cursor.execute(sql, params)
	if n==1:
		print "success "+str(success_count)
		success_count += 1
	else:
		print "fail "+str(fail_count)
		fail_count += 1

print "total success:"+str(success_count)
print "total fail:"+str(fail_count)
fp.close()
cursor.close()
conn.close()

