#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Author : yun


import os
import platform
import sys
import time
mysql8='mysql-8.0.11-linux-glibc2.12-x86_64.tar.gz'
mysql7='mysql-5.7.22-linux-glibc2.12-x86_64.tar.gz'
mysql6='mysql-5.6.40-linux-glibc2.12-x86_64.tar.gz'
mysql5='mysql-5.5.60-linux-glibc2.12-x86_64.tar.gz'
soft_dir='/u01/soft'
install_file=''
ln_dir=''
my_inf=''
sock_file='/tmp/'
def init_install():
    if platform.architecture()[0] !='64bit':
        print('os version error,pls intall 64bit os!')
    if os.getuid()==0:
        pass
    else:
        print("please use root to excute this script")
        sys.exit(1)
    os.system('mkdir -p '+soft_dir)
    os.system('groupadd mysql')
    os.system('useradd -r -g mysql -s /bin/false mysql')


def downloadSoft():
    res=0
    global install_file
    global ln_dir
    global my_inf
    global sock_file
    version=raw_input("please input mysql version(8.0/5.7/)")
    url=''
    if version=='8.0':
        install_file=mysql8
        ln_dir='mysql8.0'
        my_inf='my8.0.cnf'
        sock_file=sock_file+'mysql.sock8'
        url='https://dev.mysql.com/get/Downloads/MySQL-8.0/'+mysql8	
    elif version=='5.7':
        install_file=mysql7
        sock_file=sock_file+'mysql.sock7'
        my_inf='my5.7.cnf'
        ln_dir='mysql5.7'
        url='https://dev.mysql.com/get/Downloads/MySQL-5.7/'+mysql7
    elif version=='5.6':
        sock_file='mysql.sock6'
        ln_dir=sock_file+'mysql5.6'
        my_inf='my5.6.cnf'
        install_file=mysql6
        url='https://dev.mysql.com/get/Downloads/MySQL-5.6/'+mysql6
    elif version=='5.5':
        sock_file='mysql.sock5'
        ln_dir=sock_file+'mysql5.5'
        my_inf='my5.5.cnf'
        install_file=mysql5
        url='https://dev.mysql.com/get/Downloads/MySQL-5.5/'+mysql5
    else:
        print('version number error!')
        sys.exit(1)
    cmd='cd '+soft_dir+' && wget '+url
    #res=os.system(cmd)
    
    if res != 0:
        print('download error!')
        sys.exit(1)

def installMysql():
    cmd='cd /usr/local && tar xzvf '+soft_dir+'/'+install_file+' && ln -s '+' '+install_file[0:-7]+' '+ln_dir
    print(cmd)
    #res=os.system(cmd)
    cmd='cp '+my_inf+' /usr/local/'+ln_dir+'/ && mkdir -p /db/'+ln_dir+'/data && chown -R mysql:mysql /db'
    print(cmd)
    os.system(cmd)
    cmd2='  cd /usr/local/'+ln_dir+' && bin/mysqld --defaults-file='+my_inf+' --initialize --user=mysql  &&  sleep 5 &&  bin/mysql_ssl_rsa_setup --defaults-file='+my_inf+' &&'
    
    cmd2=cmd2+' bin/mysqld --defaults-file='+my_inf+' &'
    print(cmd2)
    os.system(cmd2)
    sql="alter user root@'localhost' identified by 'root'"
    time.sleep(80)
    cmd2='sleep 5 && a=`grep password /db/'+ln_dir+"/data/error.log | awk '{print $NF}'` && echo $a && /usr/local/"+ln_dir+'/bin/mysql -uroot -p$a -S '+sock_file+' -e "'+sql+'" --connect-expired-password'
    print(cmd2)
    os.system(cmd2)
    ##cmd3="grep password /db/data/error.log | awk '{print $NF}'"
    
if __name__=='__main__':
    init_install()
    downloadSoft()
    installMysql()
