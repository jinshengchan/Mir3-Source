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
#跳转菜单1寄售			
	if (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.MarketSearch   #类型为NPCDialogType里的寄售类
		say = """查看所有寄售的物品。
        
		[结束:0]"""	
#主菜单
	else:	
		say = """你好，我是专门的寄售商人你，想看看一般店铺里买不到的物
		品吗？
		如果您想寄售物品，我也可以帮忙。您需要先进行寄售登记，
		手续费为5000金币。物品卖出去后，另收2%的手续费。
		这不是蛮划算吗？不妨来试试吧。请选择要买卖的物品。
		没人最多可以寄售20件物品。

		注意事项 任务用道具过一定时间后会自动消失，所以尽量
		不要购买托管再我这里的任务道具。
	
		[查看所有寄售的物品。:1]
		[查看衣服。:2]
		[查看武器。:3]
		[查看项链。:4]
		[查看头盔（帽子）。:5]
		[查看戒指。:6]
		[查看手镯（手套）。:7]
		[查看鞋类。:8]
		[查看药品。:9]
		[查看图书。:10]
		[查看其他物品。:11]
		
		你以前寄售过物品吗？
		[查看您寄售物品的销售情况。:12]
		"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的普通类			
types =[ItemType.Nothing]

#NpcEvent.add_listener(51,"OnClick",OnClick)
#NpcEvent.add_listener(62,"OnClick",OnClick)
#NpcEvent.add_listener(122,"OnClick",OnClick)
#NpcEvent.add_listener(132,"OnClick",OnClick)
#NpcEvent.add_listener(203,"OnClick",OnClick)
#NpcEvent.add_listener(204,"OnClick",OnClick)
#NpcEvent.add_listener(205,"OnClick",OnClick)
#NpcEvent.add_listener(206,"OnClick",OnClick)
#NpcEvent.add_listener(207,"OnClick",OnClick)
#NpcEvent.add_listener(208,"OnClick",OnClick)
