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
from Npc.商店列表 import *
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
	
	guild = SEnvir.GetGuildFromCastleName("沙巴克")
	
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[结束:0]"""	
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你需要什么东西？
		
		[前一步:99]"""	
#跳转菜单2卖				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的物品交给我。
		
		[前一步:99]"""
#主菜单
	else:
		if not guild:
			say = """欢迎光临，这里出售一些简单的药品。
			
			[购买:1]药品
			[出售:2]药品
			
			[结束:0]"""
		else:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			say = """这里是<font color=\"0xff00ff00\">沙巴克城</font><font color=\"0xffffff00\">{}</font>行会的领地。
			欢迎光临，这里出售一些简单的药品。
			
			[购买:1]药品
			[出售:2]药品
			
			[结束:0]""".format(guild.GuildName)

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(jianshanggoodslist)

NpcEvent.add_listener(304,"OnClick",OnClick)