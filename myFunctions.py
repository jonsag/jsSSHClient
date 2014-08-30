#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, ConfigParser, os, getpass, subprocess

# starting up some variables

config = ConfigParser.ConfigParser()
config.read("%s/config.ini" % os.path.dirname(__file__)) # read config file

hosts = ConfigParser.ConfigParser()
hosts.read("%s/myHosts.ini" % os.path.dirname(__file__)) # read config file

clientType = (config.get('ssh','clientType'))

def onError(errorCode, extra):
    print "\nError:"
    if errorCode == 1:
        print extra
        usage(errorCode)
    elif errorCode == 2:
        print "No options passed"
        usage(errorCode)
    else:
        print "\nError: Unknown"

def usage(exitCode):
    print "\nUsage:"
    print "----------------------------------------"
    print "%s -l [-p <path>] [-r] [-s <suffix>]" % sys.argv[0]
    print "          Find files, set language code if none, and create symbolic 'l'ink to them without language code"
    print "          Options: Set -s <suffix> to set 's'uffix to search for"
    print "                   Set -r to search 'r'ecursively"
    print "                   Set -p <path> to set other 'p'ath than current"
    sys.exit(exitCode)

def newHost(verbose):
    print "--- Add host"
    existingHosts = hosts.sections()
    hostExist = False
    while True:
        hostAddress = raw_input("Address: ") # input host name or IP
        if pingHost(hostAddress): # check if we can ping host
            hostIsUp = True
        else:
            print "Could not ping %s" % hostAddress
            hostIsUp = False
            
        userName = raw_input("User name: ") # input user to log in with
        
        for host in existingHosts: # check if that combination already exist in host file
            if "%s_%s" % (hostAddress, userName) == host:
                print "%s with user %s already in list. Try again" % (hostAddress, userName)
                hostAccepted = False
                break
            else:
                hostAccepted = True
                
        if hostAccepted and hostIsUp:
            print "--- Everything OK"
            break
    
    hostPort = raw_input("Port (22): ")
    if not hostPort:
        hostPort = 22
    
    while True:
        passWord = getpass.getpass("Password: ")
        passWord2 = getpass.getpass("Password again: ")
        if passWord == passWord2:
            break
        else:
            print "*** Passwords don't match. Try again"

    hostEntry = "%s_%s" % (hostAddress, userName)
    
    hostParams = (hostAddress, hostPort, userName, passWord)
    print hostParams
    
    print "--- Adding %s to your hosts" % hostEntry   
    hostsFile = open("%s/myHosts.ini" % os.path.dirname(__file__),'w') # write to hosts file
    hosts.add_section(hostEntry)
    hosts.set(hostEntry,'hostAddress', hostAddress)
    hosts.set(hostEntry,'hostPort', hostPort)
    hosts.set(hostEntry,'userName', userName)
    hosts.set(hostEntry,'passWord', passWord)
    hosts.write(hostsFile)
    hostsFile.close()
    
def pingHost(host):
    pingResponse = subprocess.Popen(["ping", "-c1", "-w100", host], stdout=subprocess.PIPE).stdout.read()
    if not pingResponse:
        print "*** %s is down" % host
        result = False
    else:
        print "--- %s is up" % host
        result = True
    return result