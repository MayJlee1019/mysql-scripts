#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   auto_install.py
@Time    :   2019/08/28 22:14:32
@Author  :   Wangjun 
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os 
import sys 
import argparse
import time

mysql80='mysql-8.0.17-linux-glibc2.12-x86_64.tar.gz'
mysql57='mysql-5.7.27-linux-glibc2.12-x86_64.tar.gz'
soft_dir='/opt/software'
install_file=''
my_cnf=''
sock_file='/tmp/'

def base_install():
    global version
    global port
    if os.getlogin() !='root':
        print("please use root to excute this script")        
        sys.exit(1)
    else:
        os.system('mkdir -p '+soft_dir)
        os.system('mkdir -p /data/mysql'+version+'/mysql'+port+'/{data,logs,tmp}')
        os.system('groupadd mysql')
        os.system('useradd -r -g mysql -s /bin/false mysql')
        os.system('yum  install   libaio  libaio-devel  -y')


def downloadMySQL():
    res=0
    global install_file
    global my_cnf
    global sock_file
    global version
    url=''
    if version=='5.7.27':
        install_file=mysql57
        sock_file=sock_file+'mysql.sock'
        url='https://dev.mysql.com/get/Downloads/MySQL-5.7/'+mysql57    
    elif version=='8.0.17':
        install_file=mysql80
        sock_file=sock_file+'mysql.sock'
        url='https://dev.mysql.com/get/Downloads/MySQL-8.0/'+mysql80	
    else:
        print('version number error!')
        sys.exit(1)
    cmd='cd '+soft_dir+' && wget '+url

    
    if res != 0:
        print('download error!')
        sys.exit(1)

def InstallMySQL():
    #tar zxvf /opt/software/mysql-8.0.17-linux-glibc2.12-x86_64.tar.gz && ln -s /opt/mysql/mysql-5.7.19-linux-glibc2.12-x86_64 /usr/local/mysql8.0.17 
    cmd1='tar xzvf '+soft_dir+'/'+install_file+' && ln -s '+soft_dir+'/'+install_file[0:-7]+'  /usr/local/mysql'+version 
    cmd2='echo  export PATH=/usr/local/mysql'+version+'/bin:$PATH >> /etc/profile && source /etc/profile'
    print(cmd1)
    os.system(cmd1)
    print(cmd2)    
    os.system(cmd2)

    #拷贝my.cnf
    if version=='5.7.27':
        #cp -f my_cnf /etc/ && echo ibp >> /etc/my.cnf && echo port >> /etc/my.cnf
        cmd1 ='cp -f my57.cnf /etc/ && chown -R  mysql.mysql /data'
        cmd2 ='echo innodb_buffer_pool_size ='+ibp+' >> /etc/my57.cnf && echo port ='+port+'>> /etc/my57.cnf && echo datadir=/data/mysql'+version+'/mysql'+port+'/data >> /etc/my57.cnf'  
        #初始化mysql
        cmd3='mysqld --defaults-file=/etc/my57.cnf --initialize-insecure --user=mysql  &&  sleep 60'
        #启动mysql
        cmd4='mysqld --defaults-file=/etc/my57.cnf &'
        print(cmd1)
        os.system(cmd1)
        print(cmd2)
        os.system(cmd2)
        print(cmd3)
        os.system(cmd3)
        print(cmd4)
        os.system(cmd4)
    if version =='8.0.17':
        cmd1 ='cp -f my80.cnf /etc/ && chown -R  mysql.mysql /data'
        cmd2 ='echo innodb_buffer_pool_size ='+ibp+' >> /etc/my80.cnf && echo port ='+port+'>> /etc/my80.cnf && echo datadir=/data/mysql'+version+'/mysql'+port+'/data >> /etc/my80.cnf'    
        cmd3='mysqld --defaults-file=/etc/my80.cnf --initialize-insecure --user=mysql  &&  sleep 60'
        cmd4='mysqld --defaults-file=/etc/my80.cnf &'
        print(cmd1)
        os.system(cmd1)
        print(cmd2)
        os.system(cmd2)
        print(cmd3)
        os.system(cmd3)
        print(cmd4)
        os.system(cmd4)
    else:
        print('incorrect version in list !!')
        sys.exit(1)        


    #修改MySQL root 密码
    time.sleep(60)
    sql="alter user root@'localhost' identified by 'root'"
    cmd3='mysql -uroot -p -S '+sock_file+' -e "'+sql+'"'    
    print(cmd3)
    os.system(cmd3)


if __name__=='__main__':
    #传入参数
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--version", help="Install  mysql version ex: --version=5.7.27", type=str,default = None)
    parser.add_argument("--port", help="Install mysql port  ex: --port=3306", type=str,default =3306)    
    parser.add_argument("--ibp", help="Install mysql innodb_buffer_pool_size  ex: --ibp=4G", type=str,default = None)
    args = parser.parse_args()
    version=args.version
    port=args.port
    ibp = args.ibp

    base_install()
    downloadMySQL()
    InstallMySQL()
