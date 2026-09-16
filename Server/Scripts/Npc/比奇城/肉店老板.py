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
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """高价收购优质肉。
		沾上土或者被火烧过的肉廉价收购。
		
		[返回:5]
		[结束:0]"""	
	elif (Menu == 2):
		say = """可以通过屠宰鸡、鹿、羊、狼等动物获取肉。
		首先抓住那些动物，然后按Alt键，在动物尸体上点击鼠标，
		然后看到切肉的动作，你的包裹里就会出现大块大块的肉。
		要记住越是不愿意被抓住而拼命逃跑的动物品质越好，
		使用魔法抓住的动物品质为0。
		
		[前一步:5]"""
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """高价收购优质肉。
		沾上土的或被火烧过的肉廉价收购。
		
		[前一步:99]"""			
#主菜单
	else:
		say = """你是来卖肉的？
		
		[卖:3]肉
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的肉类			
types =[ItemType.Meat]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数

NpcEvent.add_listener(68,"OnClick",OnClick)


