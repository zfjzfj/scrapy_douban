#!/usr/bin/env python
# -*- coding: utf8 -*-


"""
  Author: Laopang Zhang
  Created: 2016/11/21
  Usage: 'Through the SA API to get a list of all the server software.'
"""
import subprocess
import datetime
import logging
import threading
import os
import re
import sys
import Queue
import time
import timeit
import shutil
import zipfile
import platform
import psutil
import commands

import csv
# sys.path.append("/opt/opsware/pylibs27")
# from pytwist import *
# from pytwist.com.opsware.search import Filter


def get_info(csvFile):
    ts = twistserver.TwistServer()
    serverService = ts.server.ServerService
    filter = Filter()
    filter.expression = 'ServerVO.osVersion CONTAINS "Windows" '
    #filter.expression = ''
    serverRefs = serverService.findServerRefs(filter)
    if len(serverRefs) < 1:
        print('Not found managed server')
        sys.exit(1)
    with open(csvFile, 'w') as file:
        spamwriter = csv.writer(file)
    #    row = ['Hostname', 'mid','OS', 'IP', 'Type', 'Software']
    #    spamwriter.writerow(row)
    #    print(row)
        for serverRef in serverRefs:
            serverName = serverRef.name
            mid = serverService.getServerVO(serverRef).mid
            os = serverService.getServerVO(serverRef).platform.name
            ip = serverService.getServerVO(serverRef).managementIP
            installedSoftwares = serverService.getInstalledSoftware(serverRef)
            for installedSoftware in installedSoftwares:
                type = installedSoftware.type
                packageName = installedSoftware.packageName
                matchobj1 = re.match(r'([a-z]*IIS [a-z]*)',packageName,re.I)
                matchobj2 = re.match(r'Microsoft SQL Server',packageName)
                if matchobj1 or matchobj2 :
                    row = [serverName,mid, os, ip, type, packageName]
                    spamwriter.writerow(row)
                    print (', '.join(row))

def copy_file(csvfile, target):
    logging.info('copying %s' % os.path.basename(csvfile))
    shutil.copy(csvfile, target)
    return


def copy_file_to_bsae(csvfile):
    t0 = timeit.default_timer()
    logging.info('copying csv to BSAE')
    ogfs_base = '/opsw/Server/@/szbsae.cmb.com/files/oracle'
    local_base = '/opt/opsware/customer_dev/softwarelist/csv/softwarelist.csv'
    target = '%s/%s' % (ogfs_base, local_base)
    copy_file(csvfile, target)
    tm_con = timeit.default_timer() - t0
    logging.info('copy done, took [%.3f] seconds' % tm_con)
    return


def inject():
    '''Load data into BSAE
    '''
    t0 = timeit.default_timer()
    logging.info('begin injecting data')
    keyword = 'os_inst_package'
    csvname = '%s.csv' % keyword
    KW_DATA_BASE='/tmp'
    csv = os.path.join(KW_DATA_BASE, csvname)
    if not os.path.exists(csv):
        logging.error('missing csv : %s' % csvname)
        return
    #
    copy_file_to_bsae(csv)
    #
    cmd = '/opt/opsware/customer_dev/softwarelist/inject_kanbandatabase.sh'
    cmd = '/opsw/bin/rosh -l oracle -n szbsae.cmb.com "%s"' % cmd
    logging.info('calling db_loader on bsae')
    code, output = shell(cmd)

    tm_con = timeit.default_timer() - t0
    logging.info('code = %s' % code)
    logging.info('inject done, took [%.3f] sceconds' % tm_con)
    return

class Host(object):
    def __init__(self,loglevel=logging.DEBUG):
        self.sys = platform.system()
	'''Set logging utility'''
	os.putenv('TZ', 'BST-8')
	console = logging.StreamHandler()
	console.setLevel(logging.NOTSET)
	log_fmt = '#[%(levelname)-.3s][%(asctime)s] :  %(message)s'
	fmt = logging.Formatter(log_fmt)
	console.setFormatter(fmt)
	logging.getLogger('').addHandler(console)
	logger = logging.getLogger('')
	logger.setLevel(loglevel)
	# add file log
	abspath = os.path.abspath(__file__)
	base = os.path.dirname(abspath)
	script = os.path.basename(abspath)
	# prefix = '.'.join(script.split('.')[:-1])
	prefix = script.replace('.ogfs.py', '')
	log_file_name = '%s.log' % prefix
	log_file = os.path.join(base, log_file_name)
	file_handler = logging.FileHandler(log_file, mode='w')
	file_handler.setLevel(loglevel)
	file_handler.setFormatter(fmt)
	logger.addHandler(file_handler)

    def machine(self):
        """Return type of machine."""
        if os.name == 'nt' and sys.version_info[:2] < (2,7):
            return os.environ.get("PROCESSOR_ARCHITEW6432",
                   os.environ.get('PROCESSOR_ARCHITECTURE', ''))
        else:
            return platform.machine()

    def os_bits(self):
        """Return bitness of operating system, or None if unknown."""
        machine = self.machine()
        machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
        return machine2bits.get(machine, None)

    def writeCSV(self,data):
        with open(csvFile, 'w') as f:
            for line in data:
                str = line
                f.write(str)



class Linux(Host):
    def __init__(self):
        pass

    def getProCMD(self):
        CMDList = [
             {"process":"FLUME","cmd":""},
             {"process":"SA","cmd":""},
             {"process":"ZANYUE","cmd":""},
             {"process":"ORACLE","cmd":""},
             {"process":"MYSQl","cmd":""},
             {"process":"DB2","cmd":""},
             {"process":"JBOSS","cmd":""},
             {"process":"WAS","cmd":""},
             {"process":"TOMCAT","cmd":""}
        ]

        CSVContent = []
        line = {}
        for cmd in CMDList:
            output = commands.getstatusoutput(cmd['cmd'])
            if output[0] == 0:
                PID = output[1]
                if len(PID) > 0 and int(PID) >= 0:
                    line['software'] = psutil.Process(PID).name()
                    CSVContent.append(line)
                    line = {}

        return CSVContent


class AIX(Host):
    def __init__(self):
        pass

    def getProCMD(self):
        CMDList = [
             {"process":"FLUME","cmd":""},
             {"process":"SA","cmd":""},
             {"process":"ORACLE","cmd":""},
             {"process":"DB2","cmd":""},
        ]

        CSVContent = []
        line = {}
        for cmd in CMDList:
            output = commands.getstatusoutput(cmd['cmd'])
            if output[0] == 0: PID = output[1]
            if len(PID) > 0 and int(PID) >= 0:
                line['software'] = psutil.Process(PID).name()
                CSVContent.append(line)
                line = {}

        return CSVContent




if __name__ == "__main__":
    h = Host()
    hostOS = getattr(Host, "getSysteminfo")
    print hostOS,type(hostOS)
    Foo = type(hostOS, (), {})
    print Foo
    # csvFile = '/tmp/os_inst_package.csv'
    # init_logger()
    # get_info(csvFile)
    # inject()

