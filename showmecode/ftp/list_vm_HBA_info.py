#!/usr/bin/env python
# William Lam
# www.virtuallyghetto.com

"""
vSphere Python SDK program for listing all ESXi datastores and their
associated devices
python list_vm_HBA_info.py  -s 99.1.36.58 -u storage_user -p Paz!2016
"""
import argparse
import atexit
import json
import ssl
import time
import socket

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

"""
This module implements simple helper functions for python samples
"""
import argparse
import getpass

__author__ = "LaopangZhang."

def getNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def getHostName():
    return socket.gethostname()


def writeCSV(HBAInforList):
        '''
                HBAInforList = { "hostname":"","now":"","ip":"","status":"","hbaname":"","hbastatus":"",\
                "hbawwn":"","description":"" }
        '''
        fileName = "c:\%s.txt" % getHostName()
        with open(fileName,'w') as f:
            for hba in HBAInforList:
                line = ("%s|%s|%s|%s|%s|%s|%s|%s\n" % (hba['hostname'],hba['now'],hba['ip'],\
                        hba['status'],hba['hbaname'],hba['hbastatus'],\
                        hba['hbawwn'],hba['description'] ))
                f.write(line)
        return True

def build_arg_parser():
    """
    Builds a standard argument parser with arguments for talking to vCenter

    -s service_host_name_or_ip
    -o optional_port_number
    -u required_user
    -p optional_password

    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter')

    # because -h is reserved for 'help' we use -s for service
    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSphere service to connect to')

    # because we want -p for password, we use -o for port
    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name to use when connecting to host')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use when connecting to host')
    return parser


def prompt_for_password(args):
    """
    if no password is specified on the command line, prompt for it
    """
    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host %s and user %s: ' %
                   (args.host, args.user))
    return args


def get_args():
    """
    Supports the command-line arguments needed to form a connection to vSphere.
    """
    parser = build_arg_parser()

    args = parser.parse_args()

    return prompt_for_password(args)



def get_args():
    """
   Supports the command-line arguments listed below.
   """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=True, action='store',
                        help='Password to use when connecting to host')
    parser.add_argument('-j', '--json', default=False, action='store_true',
                        help='Output to JSON')
    parser.add_argument('-S', '--disable_ssl_verification',
                        required=False,
                        action='store_true',
                        help='Disable ssl host certificate verification')
    args = parser.parse_args()
    return args


def main():
    """
   Simple command-line program for listing all ESXi datastores and their
   associated devices
   """

    args = get_args()
    prompt_for_password(args)
    sslContext = None
    if not args.disable_ssl_verification:
        sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslContext.verify_mode = ssl.CERT_NONE

    try:
        service_instance = connect.SmartConnect(host=args.host,
                                                user=args.user,
                                                pwd=args.password,
                                                port=int(args.port),
                                                sslContext=sslContext)
        if not service_instance:
            print("Could not connect to the specified host using specified "
                  "username and password")
            return -1
        atexit.register(connect.Disconnect, service_instance)
        content = service_instance.RetrieveContent()
        # Search for all ESXi hosts
        objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.HostSystem],
                                                          True)
        esxi_hosts = objview.view
        objview.Destroy()
        datastores = {}
        HBAInforList = []
        HBAInfo = { "hostname":"","now":"","ip":"","status":"","hbaname":"","hbastatus":"",\
                "hbawwn":"","description":"" }
        for esxi_host in esxi_hosts:
            if not args.json:
                print("{}\t{}\t\n".format("ESXi Host:    ", esxi_host.name))
            storage_system = esxi_host.configManager.storageSystem
            for item in storage_system.storageDeviceInfo.hostBusAdapter:
                if hasattr(item,"nodeWorldWideName"):
                    HBAInfo['hostname'] = esxi_host.summary.host
                    HBAInfo['now'] = getNowTime()
                    HBAInfo['ip'] = esxi_host.summary.managementServerIp
                    HBAInfo['status'] = "200"
                    HBAInfo['hbaname'] = item.device
                    HBAInfo['hbastatus'] = item.status
                    HBAInfo['hbawwn'] = item.nodeWorldWideName
                    HBAInfo['description'] = "None"
                    HBAInforList.append(HBAInfo)
                    HBAInfo = {}
                    print "Have Collected %s HBAInformation!" % item.device
    except vmodl.MethodFault as error:
        print("Caught HBA fault : " + error.msg)
        return -1
    if writeCSV(HBAInforList): return 0
    return -1

# Start program
if __name__ == "__main__":
    main()

