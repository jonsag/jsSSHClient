#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import paramiko

def connect(hostParams, verbose):
    hostName, hostAddress, hostPort, userName, passWord = hostParams
    paramiko.util.log_to_file("filename.log")
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    try:                                                              
        ssh.connect(hostAddress, username=userName, password=passWord, port=hostPort, look_for_keys=True)
        #ssh.sendline ('whoami')
        #whoAmI = ssh.prompt()
        #whoAmI = ssh.before
        #print "--- Logged in as %s\n" % whoAmI
        stdin, stdout, stderr = ssh.exec_command('ls -l')
        type(stdin)
        stdout.readlines()
    except Exception as e:
    #except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
        print "paramiko failed on login: %s" % e
    
    return ssh

def runCommand(ssh, command, verbose):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
    except Exception as e:
        print "Error: %s" % e
    type(stdin)
    stdout.readlines()
    
def close(ssh, verbose):
    print "--- Logging out"
    ssh.close()  
