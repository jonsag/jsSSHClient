#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# edit .conf to suit your needs

import getopt

from myFunctions import *

connect = False
listHosts = False
addHost = False
verbose = False

##### handle arguments #####
try:
    myopts, args = getopt.getopt(sys.argv[1:],'cahv' , ['connect', 'addhost', 'help', 'verbose'])
except getopt.GetoptError as e:
    onError(1, str(e))

if len(sys.argv) == 1: # no options passed
    onError(2, 2)

for option, argument in myopts:
    if option in ('-c', '--connect'):
        connect = True
        if not argument:
            listHosts = True
        else:
            host = argument
    elif option in ('-a', '--addhost'):
        addHost = True
        if not argument:
            host = argument
    elif option in ('-v', '--verbose'):
        verbose = True
    elif option in ('-h', '--help'):
        usage(0)
        
hostName = "amd64-4400"
hostAddress = "amd64-4400"
hostPort = 22
userName = "root"
passWord = "amd64-4400myth0185"
        
hostParams = (hostName, hostAddress, hostPort, userName, passWord)

if connect:
    print "--- Using %s module for the ssh connection\n" % clientType
    if clientType == "pxssh":
        import px
        ssh = px.connect(hostParams, verbose)
        while True:
            command = raw_input("Command: ")
            if command == "close":
                px.close(ssh, verbose)
                break
            else:
                px.runCommand(ssh, command, verbose)
    elif clientType == "paramiko":
        import prmko
        ssh = prmko.connect(hostParams, verbose)
        while True:
            command = raw_input("Command: ")
            if command == "close":
                prmko.close(ssh, verbose)
                break
            else:
                prmko.runCommand(ssh, command, verbose)
                
elif addHost:
    newHost(verbose)
    