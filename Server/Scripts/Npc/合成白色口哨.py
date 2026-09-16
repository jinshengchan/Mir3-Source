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

#判断是否有要求的道具
	if (Menu == 1):
		if (Sender.GetItemCount("白色口哨碎片") < 5):
			say ="""你的碎片不足5个，无法合成。
			
			[关闭:0]"""
		else:
#上面条件都达成，扣除道具，给予道具
			Sender.TakeItem("白色口哨碎片",5)
			Sender.GiveItem("白色口哨",1)
			say="""合成成功。
			
			[继续合成:1]
			
			[关闭:0]"""
#判断是否有要求的道具
	elif (Menu == 2):
		if (Sender.GetItemCount("幸运斗笠碎片") < 48):
			say ="""你的碎片不足48个，无法合成。
			
			[关闭:0]"""
		else:
#上面条件都达成，扣除道具，给予道具
			Sender.TakeItem("幸运斗笠碎片",48)
			Sender.GiveItem("幸运斗笠",1)
			say="""合成成功。
			
			[继续合成:2]
			
			[关闭:0]"""
#判断是否有要求的道具
	elif (Menu == 3):
		if (Sender.GetItemCount("白色虎齿项链碎片") < 88):
			say ="""你的碎片不足88个，无法合成。
			
			[关闭:0]"""
		else:
#上面条件都达成，扣除道具，给予道具
			Sender.TakeItem("白色虎齿项链碎片",88)
			Sender.GiveItem("白色虎齿项链",1)
			say="""合成成功。
			
			[继续合成:3]
			
			[关闭:0]"""
#主菜单
	else:
		say = """[合成:1]（白色口哨  数量要求5个）
		[合成:2]（幸运斗笠  数量要求48个）
		[合成:3]（白色虎齿项链  数量要求88个）

		[关闭:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	

NpcEvent.add_listener(300,"OnClick",OnClick)
