#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import pxssh

def connect(hostParams, verbose):
    hostName, hostAddress, hostPort, userName, passWord = hostParams
    ssh = pxssh.pxssh()
    try:                                                              
        ssh.login(hostAddress, userName, passWord, port=hostPort)
        #ssh.sendline ('whoami')
        #whoAmI = ssh.prompt()
        #whoAmI = ssh.before
        #print "--- Logged in as %s\n" % whoAmI
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
    
    return ssh

def runCommand(ssh, command, verbose):
    ssh.sendline(command)
    ssh.prompt()
    print ssh.before
    
def close(ssh, verbose):
    print "--- Logging out"
    ssh.logout()  