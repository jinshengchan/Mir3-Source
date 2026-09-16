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
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[结束:0]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		say = """如果是新鲜的肉，我会出高价的。快拿出来，让我看看。
		我快忍不住了。
		
		[前一步:99]"""			
#主菜单
	else:
		say = """我们特别喜欢吃人类饲养的家畜肉。因为它们的肉比蜥蜴肉
		嫩多了。
		但是人类很小气，不会把肉白白送给我们。所以只能按人类的
		方式进行现金交易。
		
		[卖:3]肉
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的肉类
types =[ItemType.Meat]

NpcEvent.add_listener(180,"OnClick",OnClick)


