#!/usr/bin/env python
# -*- coding: utf8 -*-


import platform
import os


class HBA(object):
    def __init__(self):
        """初始化"""
        self.warning_report = ""

    def getSysteminfo(self):
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
if __name__ == '__main__':
    hba =  HBA()
    print hba.os_bits()
    print hba.getSysteminfo()
