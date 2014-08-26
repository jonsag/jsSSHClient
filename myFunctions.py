#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, ConfigParser, os, getpass

# starting up some variables

config = ConfigParser.ConfigParser()
config.read("%s/config.ini" % os.path.dirname(__file__)) # read config file

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
    hostName = raw_input("Host name: ")
    hostAddress = raw_input("Address:")
    hostPort = raw_input("Port (22): ")
    if not hostPort:
        hostPort = 22
    userName = raw_input("User name: ")
    while True:
        passWord = getpass.getpass("Password: ")
        passWord2 = getpass.getpass("Password again: ")
        if passWord == passWord2:
            break
        else:
            print "*** Passwords don't match. Try again"
    configEntry = "%s-%s" % (hostName, userName)
    hostParams = (hostName, hostAddress, hostPort, userName, passWord)
    print hostParams
    print "--- Adding %s to your hosts" % configEntry