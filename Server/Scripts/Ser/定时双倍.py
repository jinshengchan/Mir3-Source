# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import datetime
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils



'''
先在服务端添加自定义buff 如双倍经验 双倍爆率等等
'''

DOUBLE_EXP_BUFF_INDEX = 150
DOUBLE_DROP_BUFF_INDEX = 145


def doubleEXP(begin):
    if begin:
        ServerUtils.SendMsgToAll("新服庆祝活动开始！", MessageType.System)
        ServerUtils.SendMsgToAll("新服庆祝活动开始！", MessageType.System)
        ServerUtils.SendMsgToAll("新服庆祝活动开始！", MessageType.System)
        return {'添加全服BUFF': DOUBLE_EXP_BUFF_INDEX}

    else:
        #结束活动
        ServerUtils.SendMsgToAll("新服庆祝活动结束！", MessageType.System)
        ServerUtils.SendMsgToAll("新服庆祝活动结束！", MessageType.System)
        ServerUtils.SendMsgToAll("新服庆祝活动结束！", MessageType.System)
        return {'移除全服BUFF': DOUBLE_EXP_BUFF_INDEX}


def doubleDrop(begin):
    if begin:
        ServerUtils.SendMsgToAll("周末乐欢天活动开始！", MessageType.System)
        ServerUtils.SendMsgToAll("周末乐欢天活动开始！", MessageType.System)
        ServerUtils.SendMsgToAll("周末乐欢天活动开始！", MessageType.System)
        return {'添加全服BUFF': DOUBLE_DROP_BUFF_INDEX}

    else:
        #结束活动
        ServerUtils.SendMsgToAll("周末乐欢天活动结束！", MessageType.System)
        ServerUtils.SendMsgToAll("周末乐欢天活动结束！", MessageType.System)
        ServerUtils.SendMsgToAll("周末乐欢天活动结束！", MessageType.System)
        return {'移除全服BUFF': DOUBLE_DROP_BUFF_INDEX}
