#!/usr/bin/python
# -*- coding:utf-8 -*-

import platform
import os,sys
import commands
import socket
import time



class Host(object):
    def __init__(self):
        """初始化"""
        self.warning_report = ""

    @classmethod
    def getNowTime(cls):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))



    def writeCSV(self,HBAInforList):
        '''
        csv example
        hostName hostIP timeStamp status HBAName HBAStatus HBAWWN Description
        status:
        200 Ok
        404 not online
        503 error
        hbaInfo = {
                "status":"","hbaname":"","hbastatus":"",\
                "hbawwn":"","description":""
                }
        '''
        fileName = self.getHostName() + ".csv"
        hostName = self.getHostName()
        timeStamp = self.getNowTime()
        hostIP = self.getHostIP()
        with open(fileName,'w') as f:
            for hba in HBAInforList:
                line = ("%s|%s|%s|%s|%s|%s|%s|%s\n" % (hostName,timeStamp,hostIP,\
                        hba['status'],hba['hbaname'],hba['hbastatus'],\
                        hba['hbawwn'],hba['description'] ))
                f.write(line)
        return True




    @classmethod
    def getSysInfor(cls):
        '''
        print(platform.machine())
        print(platform.node())
        print(platform.platform(True))
        print(platform.system())
        print(platform.uname())
        print(platform.architecture())
        print(platform.platform() + ' ' + platform.architecture()[0])
        print (os_bits())
        '''
        return platform.system()

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

    def runningCMD(self,cmd):
        pass

    @classmethod
    def getHostName(cls):
        return socket.gethostname()

    @classmethod
    def getHostIP(cls):
        return socket.gethostbyname(cls.getHostName())

    def trans2HEX(self,wwn=(32,0,0,0,201,237,211,27)):
        wwnStr = ""
        for num in wwn:
            str = "%x" % num
            wwnStr = wwnStr + str + ":"
        return wwnStr[0:-1]


class UnixLikeHost(Host):
    def __init__(self):
        """初始化"""
        self.warning_report = ""

    def runningCMD(self,cmd):
        return commands.getstatusoutput(cmd)

    def isHBAOnLine(self,HBAName):
        checkcmd = "cat /sys/class/fc_host/%s/port_state" % HBAName
        result = self.runningCMD(checkcmd)
        return result[1] if result[0] == 0 else result[0]

    def getHBAName(self):
        '''
        csv example
        hostName hostIP timeStamp status HBAName HBAStatus HBAWWN Description
        status:
        200 Ok
        503 error
        '''
        HBAInfoList = []
        HBAInfo = { "status":"","hbaname":"","hbastatus":"",\
                "hbawwn":"","description":"" }
        getHBANameCMD = "ls /sys/class/fc_host"
        result = self.runningCMD(getHBANameCMD)
        if result[0] != 0:
            HBAInfo['status'] = "503"
            HBAInfo['descripttion'] = "get hbaname error %s" % result[0]
            print "Have Collected Nothing!"
            sys.exit(100)
        else:
            HBANameList = result[1].split("\n")
            for hba in HBANameList:
                HBAInfo['status'] = "200"
                HBAInfo['hbaname'] = hba
                HBAInfo['hbastatus'] = self.isHBAOnLine(hba)
                HBAInfo['hbawwn'] = self.getHBAWWN(hba)
                HBAInfo['description'] = "None"
                HBAInfoList.append(HBAInfo)
                print "Have Collected %s HBAInformation!" % hba
                HBAInfo = { "status":"","hbaname":"","hbastatus":"",\
                        "hbawwn":"","description":"" }
            self.writeCSV(HBAInfoList)

    def getHBAWWN(self,HBAName):
        getWWNCMD = "cat /sys/class/fc_host/%s/port_name" % HBAName
        result = self.runningCMD(getWWNCMD)
        return result[1] if result[0] == 0 else result[0]



class WinHost(Host):
    def __init__(self):
        """初始化"""
        self.warning_report = ""

    def getHBAName(self):
        import wmi
        from win32com.client import GetObject

        HBAInfo = {
                "status":"","hbaname":"","hbastatus":"",\
                "hbawwn":"","description":""
                }
        HBAInfoList = []

        try:
            mywmi = GetObject("winmgmts:/root/wmi")
            colItems = mywmi.InstancesOf("MSFC_FCAdapterHBAAttributes")
            for item in colItems:
                HBAInfo['status']      = "200"
                HBAInfo['hbaname']     = item.SerialNumber
                HBAInfo['hbastatus']   = item.HBAStatus
                HBAInfo['hbawwn']      = self.trans2HEX(item.NodeWWN)
                HBAInfo['description'] = "None"
                HBAInfoList.append(HBAInfo)
                HBAInfo = {
                        "status":"","hbaname":"","hbastatus":"",\
                        "hbawwn":"","description":""
                        }
                print "Have Collected %s HBAInformation!" % HBAInfo['hbaname']
        except:
            HBAInfo['status'] = "503"
            HBAInfo['description'] = "Get Win WMI failed!"
            HBAInfoList.append(HBAInfo)
        self.writeCSV(HBAInfoList)


if __name__ == '__main__':
    print Host.getNowTime()
    print Host.getHostIP()
    print Host.getSysInfor()
    if Host.getSysInfor() == "Windows":
         localhost = WinHost()
    else:
        localhost = UnixLikeHost()
    print localhost.trans2HEX()
    localhost.getHBAName()
