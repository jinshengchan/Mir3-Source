# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
from Defines import *
from Utils import ServerUtils
import Server.Models.NPCObject
import collections
import NpcEvent
import Server
import random
import Server.Envir.SEnvir as SEnvir
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

ITEM_NAME = ["中秋月饼（花）","中秋月饼（好）","中秋月饼（月）","中秋月饼（圆）","中秋月饼（夜）",]

# 刷新
def Refresh(dont_care):
	# 地图生成新的活动NPC
	npc = SEnvir.GetNpcObject(343)
	npc_info = SEnvir.GetNpcInfo(343)
	new_npc = Server.Models.NPCObject()
	new_npc.NPCInfo = npc_info
	new_npc.Spawn(1, 447, 381, 0)

	ServerUtils.SendMsgToAll("活动使者出现在比奇城, 坐标: 447, 381")

# 移除
def Remove(dont_care):
	# 移除活动NPC
	npc = SEnvir.GetNpcObject(343)
	npc_info = SEnvir.GetNpcInfo(343)
	if npc:
		npc.Die()
		npc.Despawn()

# 活动使者
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	say = ""

	if Menu == 1:
		if(Sender.GetItemCount("中秋月饼（月）") < 1) or (Sender.GetItemCount("中秋月饼（圆）") < 1):
			say ="""你没有对应的月饼，无法兑换。

			[离开:0]"""
		else:
			Sender.TakeItem("中秋月饼（月）",1)
			Sender.TakeItem("中秋月饼（圆）",1)
			Sender.GiveItem("祝福油",1)
			say="""恭喜你，兑换成功。
			
			[继续兑换:1]
			[离开:0]"""
	elif Menu == 2:
		if(Sender.GetItemCount("中秋月饼（月）") < 1) or (Sender.GetItemCount("中秋月饼（圆）") < 1) or (Sender.GetItemCount("中秋月饼（夜）") < 1):
			say ="""你没有对应的月饼，无法兑换。

			[离开:0]"""
		else:
			Sender.TakeItem("中秋月饼（月）",1)
			Sender.TakeItem("中秋月饼（圆）",1)
			Sender.TakeItem("中秋月饼（夜）",1)
			Sender.GiveItem("盲盒",1)
			say="""恭喜你，兑换成功。
			
			[继续兑换:2]
			[离开:0]"""
	elif Menu == 3:
		if(Sender.GetItemCount("中秋月饼（好）") < 1) or (Sender.GetItemCount("中秋月饼（月）") < 1) or (Sender.GetItemCount("中秋月饼（圆）") < 1) or (Sender.GetItemCount("中秋月饼（夜）") < 1):
			say ="""你没有对应的月饼，无法兑换。

			[离开:0]"""
		else:
			Sender.TakeItem("中秋月饼（好）",1)
			Sender.TakeItem("中秋月饼（月）",1)
			Sender.TakeItem("中秋月饼（圆）",1)
			Sender.TakeItem("中秋月饼（夜）",1)
			Sender.GiveItem("钢玉石",1)
			say="""恭喜你，兑换成功。
			
			[继续兑换:3]
			[离开:0]"""
	elif Menu == 4:
		if(Sender.GetItemCount("中秋月饼（花）") < 1) or (Sender.GetItemCount("中秋月饼（好）") < 1) or (Sender.GetItemCount("中秋月饼（月）") < 1) or (Sender.GetItemCount("中秋月饼（圆）") < 1) or (Sender.GetItemCount("中秋月饼（夜）") < 1):
			say ="""你没有对应的月饼，无法兑换。

			[离开:0]"""
		else:
			Sender.TakeItem("中秋月饼（花）",1)
			Sender.TakeItem("中秋月饼（好）",1)
			Sender.TakeItem("中秋月饼（月）",1)
			Sender.TakeItem("中秋月饼（圆）",1)
			Sender.TakeItem("中秋月饼（夜）",1)
			Sender.GiveItem("白色口哨",1)
			say="""恭喜你，兑换成功。
			
			[继续兑换:4]
			[离开:0]"""
	elif Menu == 5:
		say = ""
		count = 0
		itemslist = []
		# 统计背包里所有装备信息
		for i in range(Globals.InventorySize):  #遍历包裹格子
			item = Sender.Inventory[i]  #道具定义格子里的道具
			if item:         #道具不为空
				if item.Info.ItemName in ITEM_NAME:    #道具类型
					count = count + 1 
					itemslist.append(item)
					if count >= 3:   #计数大于3跳出
						break
		SenderChat(Sender,str(count))
#判断包裹里的道具数量
		if count < 3 :
			say= """你没有对应的月饼，无法兑换。
			
			[离开:0]"""
		
		else:
			for item in itemslist:
				#在循环里扣掉道具数量
				Sender.TakeItem(item.Info, 1)
			Sender.GiveItem("双倍经验卷",1)
			say="""恭喜你，兑换成功。
			
			[继续兑换:5]
			[离开:0]"""
# 主菜单
	else:
		say = """中秋佳节活动
		活动时间：9号20点开始 - 12号22点结束
		
		<font color=\"0xff00ff00\">〖月 + 圆〗</font>                           [兑换:1]<font color=\"0xff00ff00\">祝福油</font>
		<font color=\"0xff00ff00\">〖月 + 圆 + 夜〗</font>                      [兑换:2]<font color=\"0xff00ff00\">盲盒</font>
		<font color=\"0xff00ff00\">〖好 + 月 + 圆 + 夜〗</font>                 [兑换:3]<font color=\"0xff00ff00\">钢玉石</font>
		<font color=\"0xff00ff00\">〖花 + 好 + 月 + 圆 + 夜〗</font>            [兑换:4]<font color=\"0xff00ff00\">白色口哨</font>
		<font color=\"0xff00ff00\">〖花好月圆夜〗任意三个</font>                [兑换:5]<font color=\"0xff00ff00\">双倍经验卷</font>"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(343,"OnClick",OnClick)
