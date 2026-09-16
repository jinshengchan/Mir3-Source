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
#跳转菜单1	
	elif (Menu == 1):
		say = """有人在雪原本国看到一个巨大的石阵。
			
		[关闭:0]"""	
#跳转菜单2商品	
	elif (Menu == 2):	
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library里的NPCDialogType买卖类
		say = """十赌九输。。。
		
		[返回:99]
		[关闭:0]"""  		
#主菜单
	else:	
		say = """人生不过是一场游戏一场梦，钱乃身外之物。
	
		[购买:2]
		[交谈:1]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数			
goodslist=[
('彩票',float(1)),]
goods = collections.OrderedDict(goodslist)	

NpcEvent.add_listener(209,"OnClick",OnClick)