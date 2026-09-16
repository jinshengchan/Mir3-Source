# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Additional  #类型为Library.Additional里的额外属性
		say = """如果使用亡灵之水或诅咒之水，就可以获得重新修炼的机会。

		[前一步:99]

		[取消:0]"""			
#主菜单
	else:	
		say = """练到40级后，每升一级，就给一次强化机会。你要强化哪种
		能力？
		强化的能力，除非喝特殊药水，不会轻易消失。每升一级只
		给一次强化机会，要慎重啊。

		[强化能力:1]

		[取消:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]

NpcEvent.add_listener(139,"OnClick",OnClick)