# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from Library import *
import NpcEvent
import MapEvent
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

#跳转菜单1
	if (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你快点挑啊？
		挑好了我才能去继续练级。
		
		[关闭:0]"""	
#跳转菜单3卖
	# elif (Menu == 2):
		# Dict['Types'] =types		        #定义类别
		# Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		# say = """闲置不用的物品我出高价回收。
		
		# [返回:99]
		# [关闭:0]"""
	# elif (Menu == 3):
		# say = """请买我的药吧。
		
		# [虽然是为了生意，不过还是需要你的:4]
		# （为了生意）[不买:0]"""
	# elif (Menu == 4):
		# say = """不要骂我先到这里来独占药仓库啊。我到这里也挺不容易的。。。
		# 哼。。我看你也很辛苦的。就帮帮你吧。
		
		# [不用你帮:5]
		# [你想帮我什么:1]"""
	# elif (Menu == 5):
		# say = """真可惜。
		# 说帮你，你也不要。你的自尊心好强啊。
		# 不要那样，收下这个吧。
		# 还有我告诉你进入1层的秘密通道吧。
		# 怎么样，跟着我走吗？
		
		# [好的，带我去吧:51]
		# [对不起，我会用我自己的力量去的:0]"""
	# elif (Menu == 6):
		# say = """你很需要我的帮助啊。把这个拿走，要好好用它啊。
		
		# [结束:0]"""
	# elif (Menu == 51):
		# if(PlayerGetV(Sender,GV_PLAYER_ZHOUPAOCHUANG)==0):                #定义个人全局变量
			# PlayerSetV(Sender,GV_PLAYER_ZHOUPAOCHUANG,1)
			# Sender.GiveItem('急救丸（大）',20)
			# Sender.GiveItem('清心丸（大）',20)
			# Sender.TeleportByMapIndex(250,188,154)
			# return
		# else:
			# say = """你很需要我的帮助啊。
			
			# [结束:0]"""
#主菜单
	else:
		say = """哇。
		你真厉害啊，敢进这里。
		我有事情想让你帮个忙，你帮我的话，我也会帮你的。
		
		[帮你:1]
		[不帮你:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的普通类
types =[ItemType.Nothing]
goodslist=[
('金创药（小）',float(1.5)),
('金创药（中）',float(1.5)),
('金创药（大）',float(1.5)),
('魔法药（小）',float(1.5)),
('魔法药（中）',float(1.5)),
('魔法药（大）',float(1.5)),
]
goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(195,"OnClick",OnClick)
