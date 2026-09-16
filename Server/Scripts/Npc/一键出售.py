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
	#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
		
		[关闭:0]"""

#跳转菜单1卖				
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		say = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""
#主菜单	
	else:
		say = """<font color=\"0xffff0000\">欢迎来到传奇3!感谢您的支持和厚爱!
</font>
		
		[一键出售:1]
		
		[关闭:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
		
#类型为 Enums里的武器 衣服 头盔 鞋子 盾牌 项链 戒指 手镯类			
types =[ItemType.Weapon,ItemType.Armour,ItemType.Helmet,ItemType.Shoes,ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]	

NpcEvent.add_listener(214,"OnClick",OnClick)
