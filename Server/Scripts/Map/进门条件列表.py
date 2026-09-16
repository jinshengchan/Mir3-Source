# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

#仅针对目标地图为任务地图（默认不刷怪的地图）的情况

#地图限制列表：地图编号，进入变量，进入后变量，需要物品，刷怪坐标X,Y,范围，怪物（怪物序号，数量），地图限制时间，地图限制人数，需要物品数量，是否拿走物品，是否打开对话框
Limited_Map = {
			   63:{'value1':{100,},'value2':'','item':'角笛','X':14,'Y':14,'Range':10,'Monster':{100020:1,100021:3,100022:3,100023:2,100024:2,},'TimeLimit':0,'PlayerLimit':1,'ItemCount':1,'TakeItem':0,},
			   64:{'value1':{107,},'value2':'','item':'半块不死牌','X':14,'Y':14,'Range':10,'Monster':{100025:1,100026:3,100027:3,100028:4,},'TimeLimit':0,'PlayerLimit':1,'ItemCount':1,'TakeItem':0,},
			   468:{'value1':{105,106,107,108,109,},'value2':'','item':'','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},
			   70:{'value1':{129,130,},'value2':129,'item':'','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':1,'ItemCount':0,'TakeItem':0,},
			   470:{'value1':{132,133,},'value2':132,'item':'','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':1,'ItemCount':0,'TakeItem':0,},
			   107:{'value1':{144,145,},'value2':145,'item':'毁灭护身符','X':19,'Y':18,'Range':6,'Monster':{100031:1,100030:5},'TimeLimit':0,'PlayerLimit':1,'ItemCount':1,'TakeItem':1,},
			   471:{'value1':{166,167,168,169},'value2':'','item':'沃玛金牌','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':1,'ItemCount':1,'TakeItem':0,},
			   27:{'value1':{''},'value2':'','item':'','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},
			   67:{'value1':{102},'value2':'','item':'','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},
			   469:{'value1':{91,92,93},'value2':'','item':'','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},
#			   362:{'value1':{'100'},'value2':'','item':'筹码包','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},#诺玛遗址1层
#			   375:{'value1':{'100'},'value2':'','item':'筹码包','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},#西沙西沙漠地洞
#			   516:{'value1':{'100'},'value2':'','item':'筹码包','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},#火影地牢1层
#			   480:{'value1':{'100'},'value2':'','item':'筹码包','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},#雪原神宫1层
#			   491:{'value1':{'100'},'value2':'','item':'筹码包','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},#龙血入口
#			   481:{'value1':{'100'},'value2':'','item':'筹码包','X':'','Y':'','Range':'','Monster':'','TimeLimit':0,'PlayerLimit':0,'ItemCount':0,'TakeItem':0,},#雪原入口

}