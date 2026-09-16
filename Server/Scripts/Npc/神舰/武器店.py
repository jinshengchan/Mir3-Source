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
		
		[关闭:0]"""	
#跳转菜单1修理				
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.SpecialRepair   #类型为Library.Enums里的特修类
		say = """稍微等一下我马上给你修。
		
		[返回:99]
		[关闭:0]"""
#主菜单
	else:
		say = """喂，老兄你的武器太旧了。
		我这里有很多工具，可以修怎么样？
		稍微贵一点没问题吧？
		
		[修理:1] 武器
		
		[关闭:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	

#类型为 Enums里的武器 衣服 头盔 鞋子 盾牌 项链 戒指 手镯类			
types =[ItemType.Weapon,ItemType.Armour,ItemType.Helmet,ItemType.Shoes,ItemType.Shield,ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]

NpcEvent.add_listener(193,"OnClick",OnClick)
NpcEvent.add_listener(198,"OnClick",OnClick)
NpcEvent.add_listener(199,"OnClick",OnClick)

