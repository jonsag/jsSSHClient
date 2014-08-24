#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# edit .conf to suit your needs

import getopt

from myFunctions import *

##### handle arguments #####
try:
    myopts, args = getopt.getopt(sys.argv[1:],'p:rs:ldgc:fkhv' , ['path=', 'recursive', 'suffix=', 'link', 'detectlang', 'get', 'check=', 'format', 'keep', 'help', 'verbose'])

except getopt.GetoptError as e:
    onError(1, str(e))

