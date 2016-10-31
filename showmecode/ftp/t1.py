#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
adict={"xiaoqiangk":"xiaoqiangv","xiaofeik":"xiaofeiv",\
"xiaofeis":{"xiaofeifk":"xiaofeifv","xiaofeimk":{"xiaoqik":"xiaoqiv","xiaogou":{"xiaolei":"xiaolei"}}},\
"xiaoer":{"xiaoyuk":"xiaoyuv"}}
def hJson(json1,i=0):
    if(isinstance(json1,dict)):
        for item in json1:
            if (isinstance(json1[item],dict)):
                print("****"*i+"%s : %s"%(item,json1[item]))
                hJson(json1[item],i=i+1)
            else:
                print("****"*i+"%s : %s"%(item,json1[item]))
    else:
        print("json1  is not josn object!")


hJson(adict,0)
