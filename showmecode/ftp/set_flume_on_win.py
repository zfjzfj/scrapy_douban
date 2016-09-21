#!/usr/bin/env python

import re
import os
import sys
import platform
import subprocess
import logging
import shutil
import re
import datetime


def init_logger(loglevel=logging.DEBUG):
    '''Set logging utility'''
    os.putenv('TZ', 'BST-8')
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    log_fmt = '#[%(levelname)-.3s] [%(asctime)s] : ' + platform.node() + ' : %(message)s'
    fmt = logging.Formatter(log_fmt)
    console.setFormatter(fmt)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger('')
    logger.setLevel(loglevel)


def shell(cmd):
    if not cmd:
        return
    code, output = 0, []
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, bufsize=1, shell=True)
        ostype = platform.system()
        if ostype == 'Windows':
            output = [x.rstrip('\r\n') for x in p.stdout.readlines() if x]
        else:
            output = [x.rstrip('\n') for x in p.stdout.readlines() if x]
        code = p.wait()
    except subprocess.CalledProcessError, e:
        logging.error(str(e))
    return (code, output)


def get_base_with_wmi():
    c = wmi.WMI()
    for p in c.Win32_Process():
        ln = [p.Name, p.ExecutablePath]
        ln = [str(x) for x in ln]
        if re.search(r'CWAgen.exe', ln[0]):
            base = '\\'.join(ln[1].split('\\')[0:3])
            return base
    return None


def get_base_with_shell():
    cmd = '''wmic.exe process where Name='CWAgen.exe' get ExecutablePath'''
    code, output = shell(cmd)
    base = '-'
    if len(output) > 2:
        base = '\\'.join(output[1].rstrip().split('\\')[0:3])
        logging.debug(base)
    return base


def check_flume(base):
    if base is None:
        return False
    base_conf = os.path.join(base, 'conf')
    conf = os.path.join(base_conf, 'flume-conf.properties')
    if os.path.exists(conf):
        return True
    else:
        return False


def get_timestamp():
    utc_now = datetime.datetime.utcnow()
    china_now = utc_now + datetime.timedelta(hours=8)
    tm = china_now.strftime('%Y-%m-%d %H:%M:%S')
    return tm


def flume_log_updated(base):
    base = os.path.join(base, 'logs')
    log = os.path.join(base, 'lastSendTime.log')
    if not os.path.exists(log):
        logging.error('missing %s' % log)
        return False
    # check if lastSendTime.log has not been updated for a while
    tm = os.path.getmtime(log)
    ctime = datetime.datetime.fromtimestamp(tm)
    utc_now = datetime.datetime.utcnow()
    now = utc_now + datetime.timedelta(hours=8)
    delta = now - ctime
    logging.debug('delta = %s' % delta)
    if delta.days > 1:
        logging.warn('log has not been updated for %s days' % delta.days)
        return False
    # elif delta.seconds > 300:
    #     logging.warn('log has not been updated for more than 5 minutes')
    #     return False
    return True


def restart_flume_service(base):
    if flume_log_updated(base) is True:
        return
    logging.info('stopping CorewareAgentService')
    cmd = 'net stop CorewareAgentService'
    code, output = shell(cmd)
    logging.debug(code)
    logging.debug(output)
    logging.info('starting CorewareAgentService')
    cmd = 'net start CorewareAgentService'
    code, output = shell(cmd)
    logging.debug(code)
    logging.debug(output)


def run_script():
    script = 'c:\\opsware\\app\\get_proc_info.py'
    if not os.path.exists(script):
        logging.error('missing %s' % script)
        return
    logging.info('running get_proc_info.py')
    # execfile(script)
    code = subprocess.call(script, shell=True)
    # cmd = '%s' % script
    # code, output = shell(cmd)
    # if code == 0 or output:
    #     logging.info('done for get_proc_info.py')


def work():
    try:
        import wmi
        base = get_base_with_wmi()
    except Exception as e:
        logging.error('failed to import wmi : %s' %  e)
        base = get_base_with_shell()
    #
    flume = check_flume(base)
    # node = platform.node()
    # print('%s|%s|%s|%s|%s|%s' % (num,uuid,node, version, base, flume))
    if check_flume(base) is False:
        logging.error('failed to locate [flume-conf.properties]')
        return
    #
    set_flume(base)
    #
    run_script()
    #
    restart_flume_service(base)


def dispatch_script():
    '''Copy get_proc_info.py into C:/opsware/app
    '''
    # create base if necessary
    base = 'C:/opsware/app'
    if os.path.exists(base):
        logging.info('base [%s] exits' % base)
    if not os.path.exists(base):
        logging.info('creating base [%s]' % base)
        try:
            os.makedirs(base, mode=0755)
            logging.info('base [%s] has been created' % base)
        except Exception as e:
            logging.error(e)


def backup_flume_conf(conf):
    utc_now = datetime.datetime.utcnow()
    china_now = utc_now + datetime.timedelta(hours=8)
    tm = china_now.strftime('%Y%m%d.%H%M%S')
    new_conf = '%s.sav.%s' % (conf, tm)
    logging.info('backup flume conf : [%s]' % new_conf)
    shutil.copy(conf, new_conf)

def adptive_conf_toflume(confdir):
    conf1=os.path.join(confdir,"flume-conf.properties")
    conf2=os.path.join(confdir,"collect-conf.properties")
    conf3=os.path.join(confdir,"flume-conf.properties")
    for conf in [conf1,conf2,conf3]:
        if os.path.exists(conf):
            return conf
    return None

def set_flume(base):
    '''Set flume config
    '''
    base_conf = os.path.join(base, 'conf')
    conf = adptive_conf_toflume(base_conf)
    if not conf:
        logging.error("%s conf file of flume is not exists,and exit programe" % (conf))
        exit()
    with open(conf, 'r') as f:
        con = f.read()
    # check if has been set
    logging.info('checking process and netconn setting in [flume-conf.properties]')
    f_process, f_netconn = True, True
    if re.search(r'app.win.process', con):
        f_process = False
    if re.search(r'app.win.netconn', con):
        f_netconn = False
    logging.debug('process, netconn = %s, %s' % (f_process, f_netconn))

    # check if need update
    if (f_process, f_netconn) == (False, False):
        logging.info('no need to update flume-conf')
        return

    # caculate the start number
    num = 0
    for line in con.split('\n'):
        if not line:
            continue
        ln = line.split(' = ')
        if ln[0] == 'dirs' and re.search(r'varLogDir\d+', ln[1]):
            nums = [x.replace('varLogDir', '')
                    for x in ln[1].split(' ') if re.search(r'varLogDir', x)]
            nums.sort()
            num = int(nums[-1]) + 1
            break
    # if failed to get number, use a huge one
    if num == 0:
        logging.warn('failed to get the begin number of varLogDir, use 99 instead')
        num = 99
    #
    base_logs = os.path.join(base, 'logs')
    offset_path = os.path.join(base_logs, 'offset')
    logging.debug('offset_path = %s' % offset_path)
    var_log_dirs = ''
    counter = 0
    # generate the content
    # process
    if f_process is True:
        logging.info('generating conf for procss')
        var_log_dirs = 'varLogDir%s' % num
        counter += 1
        data = '''
dirs.varLogDir%s.path = C:/opsware/app
dirs.varLogDir%s.file-pattern =  ^(process\.csv)$
dirs.varLogDir%s.offsetPath = %s
dirs.varLogDir%s.cpusleep = 500
dirs.varLogDir%s.code = GBK
dirs.varLogDir%s.redFromBegin = false
dirs.varLogDir%s.otherInfo = SOURCE_TYPE,,opsware
dirs.varLogDir%s.isWindows = true
dirs.varLogDir%s.encode = 0
dirs.varLogDir%s.topic = app.win.process
                   ''' % (num, num, num, offset_path, num, num,
                          num, num, num, num, num)
        num = num + 1
    # netconn
    if f_netconn is True:
        logging.info('generating conf for netconn')
        if var_log_dirs:
            var_log_dirs = '%s varLogDir%s' % (var_log_dirs, num)
        else:
            var_log_dirs = 'varLogDir%s' % num
        counter += 1
        if data:
            data = '%s\n' % data
        data = '''%s\n
dirs.varLogDir%s.path = C:/opsware/app
dirs.varLogDir%s.file-pattern =  ^(netconn\.csv)$
dirs.varLogDir%s.offsetPath = %s
dirs.varLogDir%s.cpusleep = 500
dirs.varLogDir%s.code = GBK
dirs.varLogDir%s.redFromBegin = false
dirs.varLogDir%s.otherInfo = SOURCE_TYPE,,opsware
dirs.varLogDir%s.isWindows = true
dirs.varLogDir%s.encode = 0
dirs.varLogDir%s.topic = app.win.netconn
                   ''' % (data, num, num, num, offset_path,
                          num, num, num, num, num, num, num)
    # backup flume-conf.properties first
    backup_flume_conf(conf)

    # update flume-conf.properties
    logging.info('updating flume-conf.properties')
    with open(conf, 'w') as f:
        # update origin content
        for line in con.split('\n'):
            ln = line.split(' = ')
            # check the first line
            if ln[0] == 'dirs' and re.search(r'varLogDir\d+', ln[1]):
                rico = '%s %s' % (line, var_log_dirs)
                f.write('%s\n' % rico)
                continue
            # check the second line
            #   dirs.thread = 3
            if ln[0].strip() == 'dirs.thread' and len(ln) == 2:
                sum = int(ln[1]) + counter
                rico = '%s = %s' % (ln[0], sum)
                f.write('%s\n' % rico)
                continue
            # print other content
            f.write('%s\n' % line)
        # append new content
        f.write('\n%s\n' % data)


if __name__ == '__main__':
    init_logger()
    work()
