import datetime
import gzip
import http.cookiejar as ck
import os.path
import queue
import random
import re
import sys
import time
import urllib.parse as up
import urllib.request as ur
from threading import Thread

ABSPATH=os.path.abspath(sys.argv[0])
ABSPATH=os.path.dirname(ABSPATH)+"/"

proxy = [
    {'http':'118.190.95.3:9001'},
    {'http':'61.135.217.7:80'},
    {'http':'118.213.182.194:47944'},
    {'http':'110.40.13.5:80'},
    {'http':'183.129.207.82:21231'},
    {'http':'58.57.101.4:43872'},
    {'http':'222.221.11.119:3128'},
    {'http':'116.77.204.2:80'},
    {'http':'115.237.88.143:8118'},
    {'http':'122.237.107.98:80'},
    {'http':'121.31.192.205:8123'}
]
useragent = [

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'

]


#1 get公开课连接
def getClassUrl(page=1,limit=100):
    global proxy
    global useragent
    video_page_url=[]
    url='https://c.open.163.com/dwr/call/plaincall/OpenSearchBean.searchCourse.dwr'
    headers={
        'Accept': '*/*',
        'Accept-Encoding':'deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en-HK;q=0.8,en;q=0.7',
        'Cache-Control':'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': 242,
        'Content-Type': 'text/plain',
        'Host': 'c.open.163.com',
        'Origin': 'https://c.open.163.com',
        'Pragma': 'no-cache',
        'Referer': 'https://c.open.163.com/search/search.htm?query=&enc=',
        'User-Agent': random.choice(useragent)
    }
    data = {
        'callCount':1,
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':'6814487256c841f786816b5b99f99bcb',
        'c0-scriptName':'OpenSearchBean',
        'c0-methodName':'searchCourse',
        'c0-id':0,
        'c0-param0':'string:TED',
        'c0-param1':page,
        'c0-param2':limit,
        'batchId':round(time.time()*1000),
        'Cookie': '_ntes_nnid=9d1f490b291d6e33312d80fc071af4b5,1528569151726; _ntes_nuid=9d1f490b291d6e33312d80fc071af4b5; mail_psc_fingerprint=9636ebd492df7973434d16dd52b0696a; __oc_uuid=d1578080-97a9-11e8-a022-1d92778da47c; __f_=1540093196488; __utmc=187553192; __utmz=187553192.1540110877.3.3.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=130438109; __utma=187553192.609099623.1533361625.1540110877.1540114884.4; Province=020; City=0755; __utma=130438109.1978328531.1533361634.1540114025.1540117265.3; __utmz=130438109.1540117265.3.3.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ted/; __utmb=130438109.2.10.1540117265; NTESOPENSI=6814487256c841f786816b5b99f99bcb'
    }
    proxyHandler = ur.ProxyHandler(random.choice(proxy))
    opener = ur.build_opener()
    data = up.urlencode(data).encode('utf-8')
    req = ur.Request(url,data,headers=headers,method='POST')
    try:
        res = opener.open(req,timeout=3)
        response = res.read().decode('unicode-escape')
        RE_GETURL = re.compile(r'courseUrl="(.{55,58}html)"')
        video_page_url = RE_GETURL.findall(response)
    except:
        pass
    return video_page_url
    

def getAllclassUrl():

    global ABSPATH
    
    allVideoNum = 2334
    limit = 2234
    videoUrl = []
    for i in range(1,allVideoNum//limit+1):
        videoUrl = getClassUrl(i,limit)
        try:
            videoUrl = '\n'.join(videoUrl)+'\n'
            with open (os.path.join(ABSPATH,'video_page_url.txt'),'a+') as f:
                f.write(videoUrl)
        except:
            pass

def getVideoDownUrl(url):
    import random
    global ABSPATH
    global proxy
    global useragent
    url = url
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en-HK;q=0.8,en;q=0.7',
        'Cache-Control':'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Host': 'open.163.com',
        'Cookie': '_ntes_nnid=9d1f490b291d6e33312d80fc071af4b5,1528569151726; _ntes_nuid=9d1f490b291d6e33312d80fc071af4b5; mail_psc_fingerprint=9636ebd492df7973434d16dd52b0696a; __oc_uuid=d1578080-97a9-11e8-a022-1d92778da47c; __f_=1540093196488; __utmz=187553192.1540110877.3.3.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/; Province=020; City=0755; __utma=187553192.609099623.1533361625.1540222671.1540304565.9; __utmc=187553192; __utmb=187553192.1.10.1540304565',
        
    }
   

    proxyHandler = ur.ProxyHandler({'http':'39.105.95.204:80'})
    opener = ur.build_opener()
    req = ur.Request(url,headers=headers)
    req.add_header('User-Agent',random.choice(useragent))
    res = opener.open(req)
 
    response=gzip.decompress(res.read())
    import random
    import os
    bufferfile = 'buffer%s.txt' % random.random()
    with open(bufferfile,'wb')as f:
        f.write(response)


    RE_GETDOWNURL =  re.compile(r"appsrc\s:\s'(.{,70}m3u8)")
    RE_GETTITLE = re.compile(r"title\s:\s'(.*?)',")
    videoDownUrl = []
    try:
        with open(bufferfile,'rb') as f:
            f.seek(-1800,2)
            response = f.read(1800).decode('gbk')
        videoDownUrl = RE_GETDOWNURL.findall(response)
        videotitle = RE_GETTITLE.findall(response)
    except BaseException as e:
        print(e)
    finally:
        os.remove(bufferfile)
    
    if len(videoDownUrl)>0 and len(videotitle)>0:
        rdata =videotitle[0]+','+videoDownUrl[0].replace('mp4','flv').replace('m3u8','flv').replace('-list','')
        with open(os.path.join(ABSPATH,'video_down_url.txt'),'a+',encoding='utf-8') as f:
            f.write((rdata+'\n'))
    else:
        with open(os.path.join(ABSPATH,'video_down_url.txt'),'a+') as f:
            f.write('None'+'\n')







def getAllVideoDownUrl():
    global ABSPATH
    # 多线程
    
    with open(os.path.join(ABSPATH,'video_page_url.txt'),'r') as f:
        videoPageUrl = f.readlines()
    videoPageUrl = list(map(lambda x: x.replace('\n',''),videoPageUrl))
    print(len(videoPageUrl))
    q = queue.Queue()
    for url in videoPageUrl:
        q.put(url)
    threads = []
    num = 20
    for i in range(0,num):
        threads.append(Thread(target=getVideoDownUrl,args=(q.get(),)))
    for i in range(0,num):
        threads[i].start() 
    x = 0 
    while not q.empty():
        for i in range(0,num):
            if not threads[i].isAlive():
                x+=1
                print('\r %s 个已下载'%(x),end='')
                url = q.get()
                if url is not None:
                    threads[i] = Thread(target=getVideoDownUrl,args=(url,))
                    threads[i].start()
    print('done')

def getVideo(title,url):
    global proxy
    global useragent
    url = url
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-HK;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'mov.bn.netease.com',
        'Pragma':'no-cache',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': random.choice(useragent)
    }    

    proxyHandler = ur.ProxyHandler(random.choice(proxy))
    opener = ur.build_opener(property)
    req = ur.Request(url,headers = headers)
    response = opener.open(req)
    if not os.path.exists('video'):
        os.mkdir('video')
        
    with open (os.path.join(ABSPATH,'video','%s.flv'%title),'wb') as f:
        f.write(response.read())


def getAllVideo():
    global ABSPATH
    with open(os.path.join(ABSPATH,'video_down_url.txt'),'r',encoding='utf-8') as f:
        videoDownUrl = f.readlines()
    videoDownUrl = list(map(lambda x: x.replace('\n',''),videoDownUrl))
    q = queue.Queue()
    threads = []
    num = 20
    x = 0
    for url in videoDownUrl:
        if 'None' not in url:
            q.put(url)

    for i in range(0,num):
        title,url = q.get().split(',')
        threads.append(Thread(target=getVideo,args=(title,url)))
    for i in range(0,num):
        threads[i].start() 

    while not q.empty():
        for i in range(0,num):
            if not threads[i].isAlive():
                x+=1
                print('\r %s 个已下载'%(x),end='')
                title,url = q.get().split(',')
                if url is not None:
                    title,url = q.get().split(',')
                    threads[i] = Thread(Thread(target=getVideo,args=(title,url)))
                    threads[i].start()
    print('done')


getAllVideoDownUrl()
