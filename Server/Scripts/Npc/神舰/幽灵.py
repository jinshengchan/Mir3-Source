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
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

#飞沙漠土城
	if(Menu == 1):
		Sender.TeleportByMapIndex(37,216,190)
		return
#主菜单
	else:
		say = """这地方是前往异界的通道，是很危险的地方哦。。
			不仅异界的生物力大无穷，也因异界的特性，在这里不能使用回城卷、随机传送卷等卷书。
			一旦进入这个地方，想回去，不是你死，就是霸王教主亡，所以你好好考虑要不要进去...
			
			[想一想还是放弃的好:1]（回沙漠土城）
			
			[关闭:0]"""	
		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(200,"OnClick",OnClick)	
