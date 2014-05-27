﻿#用python3写的获取Google亚洲ip速度。结果放在ip.txt中，win下使用。
#--*-- coding:utf-8 --*--

import os.path
import threading
import re

#ip数据
ip_all=['173.194.38.','173.194.72.','173.194.117.','173.194.120.',
    '173.194.123.','173.194.126.','173.194.127.','74.125.23.',
    '74.125.31.','74.125.37.','74.125.135.','74.125.200.',
    '74.125.203.','74.125.204.','74.125.235.','74.125.236.',
    '74.125.237.',]

#线程中文件写入锁
file_lock=threading.Lock()

#线程中输出锁
print_lock=threading.Lock() 

#执行 win下的 ping.exe 命令，获取数据。
def p(ippp,n=10):
    'p函数，ip为ip地址，n为测试包数量，返回ip地址和最小时间。'
    cmd='ping -n '+str(n)+' ' + str(ippp)
    #print(cmd,end='\n')
    a=os.popen(cmd).readlines()
    return( ippp+'\t '+ a[-1].strip().split(',')[2] +'\n')

#线程类
class ping_thread (threading.Thread):
    def __init__(self,thread_id,ip1,n1=10):
        '初始化。'
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.ip5=ip1
        self.n5=n1
    
    def run(self):
        '重新定义运行内容。'
        
        print_lock.acquire()
        print('Starting: %s \n' % self.ip5)
        print_lock.release()
        
        a=p(self.ip5,self.n5)
        
        file_lock.acquire()
        with open('ip.txt','a+') as ff:
            ff.write(a)
        file_lock.release()
        
        print_lock.acquire()
        print('Finish: %s \n' % self.ip5)
        print_lock.release()

#运行线程，每次255个。
def run_ping(n5=10):
    for ee in ip_all:
        c=[]
        for i in range(1,255):
            f=str(ee)+str(i) #生成ip
            g=ping_thread(f,f,n5)
            c.append(g)
            g.start()

        for t in c: 
            t.join()  #等待线程结束
        print('Ping %s ok \n' % ee)

#对数据进行分析
def ipdata_fx():
    findstr='(\d+.\d+.\d+.\d+).+= (\d+)ms'
    restr=re.compile(findstr)
    ipdata=[] 
    ip=[]
    with open('ip.txt') as f:
        for a in f.readlines():
            #print(a)
            fd=restr.findall(a)
            if fd :
                if len(fd[0][1])<3:
                    fd_a='0'+fd[0][1] #最小时间3位数。
                else:
                    fd_a=fd[0][1]
                ipdata.append(fd_a+'\t'+fd[0][0])
    
            
    ipdata.sort() #排序
    print("\n".join(ipdata))

    yy=map(lambda x : x[3:].strip(),ipdata)
    print("|".join(yy))

if __name__ == '__main__' :
    if (os.path.exists('ip.txt') == False):
        run_ping() #获取数据
    ipdata_fx() #分析数据