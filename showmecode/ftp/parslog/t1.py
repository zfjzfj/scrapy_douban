#!/usr/bin/python
# -*- coding:utf-8 -*-
import json


adict={"xiaoqiangk":"xiaoqiangv","xiaofeik":"xiaofeiv",\
"xiaofeis":{"xiaofeifk":"xiaofeifv","xiaofeimk":{"xiaoqik":"xiaoqiv","xiaogou":{"xiaolei":"xiaolei"}}},\
"xiaoer":{"xiaoyuk":"xiaoyuv"}}

adict = '''{"BODY":{"$APPIST$":[{"xAppSts":"A","xHbtTim":"1476422238584","xDplSeq":"1","xDbDivNam":"MONDB005","xAppIst":"ZM91DB504QA00A"}],\
        "$THDSTS$":[{"xThdDsc":"数据库连接池守护线程","xThdNam":"CCK","xThdSts":"N","xMdlCod":"ZZ1DBC"},{"xThdDsc":"应用心跳发送",\
        "xThdNam":"HBT","xThdSts":"N","xMdlCod":"ZZ1MGC"},{"xThdDsc":"性能数据发送","xThdNam":"PRF","xThdSts":"N","xMdlCod":"ZZ1MGC"},\
        {"xThdDsc":"错误日志发送","xThdNam":"ERR","xThdSts":"N","xMdlCod":"ZZ1MGC"},\
        {"xThdDsc":"管理指令通讯服务器","xThdNam":"SVR","xThdSts":"N","xMdlCod":"ZZ1MNV"},\
        {"xThdDsc":"异步调度(SZM00-ZM9-CMDSND)","xThdNam":"HDL","xThdSts":"N","xMdlCod":"ZZ1MNV"},\
        {"xThdDsc":"5 - 转历史表","xThdNam":"FTT","xThdSts":"N","xMdlCod":"ZZ1SCD"},\
        {"xThdDsc":"1 - 监控数据抓取线程","xThdNam":"ITT","xThdSts":"T","xMdlCod":"ZZ1SCD"},\
        {"xThdDsc":"3 - 作业条性能数据汇并","xThdNam":"ITT","xThdSts":"N","xMdlCod":"ZZ1SCD"},\
        {"xThdDsc":"4 - 进程性能数据汇并","xThdNam":"ITT","xThdSts":"N","xMdlCod":"ZZ1SCD"}]},\
        "HEAD":{"xDevNbr":"","xRtnLvl":"","xTypCod":"","xPreIsu":"","xIsuCnl":"","xEntUsr":"","xKeyVal":"","xMacCod":"","xTlrNbr":"",\
        "xCmmTyp":"","xRtnCod":"","xEncCod":"","xIsuDat":"0","xHdrLen":"0","xAppRsv":"","xDocSiz":"","xSysCod":"","xCmmRsv":"",\
        "xOrgIsu":"","xUsrPwd":"","xItvTms":"","xDalCod":"","xRqsNbr":"","xIsuTim":"0","xDskSys":"","xWkeCod":"ZM9RHIR1","xMsgFlg":""}}
        '''

adict = json.loads(adict)

def hJson(json1,i=0):
    print ("*" * 180)
    if(isinstance(json1,dict)):
        for item in json1:
            if (isinstance(json1[item],dict)):
                print("****"*i+"%s : %s"%(item,json1[item]))
                hJson(json1[item],i=i+1)
            else:
                print("****"*i+"%s : %s"%(item,json1[item]))
    else:
        print("json1  is not json object!")
    print ("*" * 180)

hJson(adict,10)
