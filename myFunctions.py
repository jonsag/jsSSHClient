#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import re, sys, ConfigParser, os, detectlanguage, codecs, codecs, pysrt

from itertools import islice
from sys import exit
from string import digits
from collections import namedtuple
from subprocess import call
from BeautifulSoup import BeautifulSoup, UnicodeDammit
from pycaption import detect_format, SRTReader, SRTWriter, SAMIReader, SAMIWriter, CaptionConverter
from shutil import copyfile

# libraries for subliminal
#from __future__ import unicode_literals  # python 2 only
from babelfish import Language
from datetime import timedelta
import subliminal

# starting up some variables
#num = 0
searchPath = ""
searchPathRecursive = ""
suffix = ""
langSums = []
subDownloads = []

config = ConfigParser.ConfigParser()
config.read("%s/config.ini" % os.path.dirname(__file__)) # read config file

##### mainly for subGetLangs #####
prefLangs = (config.get('languages','prefLangs')).split(',') # prefered languages

detectRows = int(config.get('variables','detectRows')) # number of rows sent to detectlanguage.com in each trys
detectTrys = int(config.get('variables','detectTrys')) # number of trys to detect language at detectlanguage.com

detectlanguage.configuration.api_key = config.get('detectlanguage_com','api-key') # api-key to detectlanguage.com from config file

languages = detectlanguage.languages() # get available languages from detectlanguage.com

languages.append({u'code': u'xx', u'name': u'UNKNOWN'})

prefEncoding = config.get('coding','prefEncoding') # your preferrd file encoding

def onError(errorCode, extra):
    print "\nError:"
    if errorCode == 1:
        print extra
        usage(errorCode)
    elif errorCode == 2:
        print "No options given"
        usage(errorCode)
    elif errorCode == 3:
        print "No program part chosen"
        usage(errorCode)
    elif errorCode == 4:
        print "%s is not a valid path\n" % extra
        sys.exit(4)
    elif errorCode == 5:
        print "Wrong set of options given"
        usage(errorCode)
    elif errorCode == 6:
        print "%s is not a valid argument" % extra
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
    print "     OR\n"
    print "%s -d" % sys.argv[0]
    print "          Get available languages from 'd'etectlanguage.com, and your account status at the same place"
    print "     OR\n"
    print "%s -g [-p <path>] [-r] [-s <suffix>]" % sys.argv[0]
    print "          Search video files, check if there are any srt subtitle files with language code in the name"
    print "          If not try to find and 'g'et subtitles in any of your preferred languages"
    print "          Options: Set -r to search 'r'ecursively"
    print "                   Set -p <path> to set other 'p'ath than current"
    print "     OR\n"
    print "%s -c [all|pref|<code>] [-p <path>] [-r]" % sys.argv[0]
    print "          'C'heck language codes set in filenames manually"
    print "          Arguments: all checks all files with languagecode set"
    print "                     pref checks all files with any of your preferred languages"
    print "                     <code>, give a valid language code"
    print "          Options: Set -s <suffix> to set 's'uffix to search for"
    print "                   Set -r to search 'r'ecursively"
    print "                   Set -p <path> to set other 'p'ath than current"
    print "     OR\n"
    print "%s -f [-k] [-p <path>] [-r] [-s <suffix>]" % sys.argv[0]
    print "          Find subtitles, check 'f'ormat, and convert to UTF8, and convert to srt"
    print "          Options: Set -k to 'k'eep temporary file"
    print "                   Set -s <suffix> to set 's'uffix to search for"
    print "                   Set -r to search 'r'ecursively"
    print "                   Set -p <path> to set other 'p'ath than current"
    print "%s -h" % sys.argv[0]
    print "          Prints this"
    print "\n"
    sys.exit(exitCode)

