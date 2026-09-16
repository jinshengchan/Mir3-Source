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
		say = """请你离开，红名无法传送。
		
		[离开:0]"""	
#飞	
	elif(Menu == 1):
		Sender.TeleportByMapIndex(1,371,335)
		return
	elif(Menu == 2):
		if (Sender.GetItemCount("魔晶石") < 1):
			say = """无法传送到目的地，
			没有启动法阵的魔晶石。

			[离开:0]"""		

		elif (Sender.GameGold < 50):
			say = """你没有足够的元宝，无法传送。
			[离开:0]"""
		else:
			map = Server.Envir.SEnvir.CreateMap(1504)                         #开启副本地图（地图ID）
			Sender.Teleport(map,11,33)	#飞地图ID X坐标 Y坐标
			map.CreateMon(40,30,100,'副本-猿猴',25)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(40,30,50,'副本-魔神怪',25)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(44,28,20,'难民弓箭手',10)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(40,30,20,'经验小兔兔',5)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(52,33,2,'花妖1',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			SubGameGold(Sender,50)
			Sender.TakeItem("魔晶石",1)
			return

#主菜单
	else:
		if Sender.Level < 40 : # 等级判断
			say  = """你实力不够，不要白白失去性命。
			请修炼到40级后，再来找我。
			
			[离开:0]"""
		else:
			say = """你将去一个凶险的地方，做好准备了吗?
			
			[我准备好了:2]    
			
<font color=\"0xff00ff00\">进入下一层地图需要至少40级</font>
<font color=\"0xff00ff00\">打开传送法阵1颗魔晶石，还有50元宝手续费</font>

			
			[我怕死我不去:0]"""

		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(381,"OnClick",OnClick)	