# -*- coding: utf-8 -*-
#载入模块SYS
import sys
from datetime import datetime, timedelta
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
import NpcEvent
from Defines import *
import Server
import NpcEvent
from Utils.TimeUtil import *
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
	say = ""

#红名判断
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """请你离开，红名无法传送。
		
		[离开:0]"""	
#飞	
	elif(Menu == 1):
		if (Sender.GameGold > 49):   #判断需要的物品数量			
			if(Sender.GetItemCount("号角") > 299):                #判断需要的物品数量				
				if(PlayerGetV(Sender,GV_AWMBOSSFB_COUNT)<3):   #定义个人全局变量
					PlayerSetV(Sender,GV_AWMBOSSFB_COUNT,PlayerGetV(Sender,GV_AWMBOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
					if (Sender.GroupMembers):   
					    Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
					map = Server.Envir.SEnvir.CreateMap(1587)                     #开启副本地图  （地图ID）
					map.CreateMon(50,50,100,'火焰沃玛',150)           
					map.CreateMon(50,50,100,'沃玛战士',150)          
					map.CreateMon(50,50,100,'暗黑战士',50)           
					map.CreateMon(50,50,50,'沃玛教主',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
					map.MapTime = datetime.now()+ timedelta(minutes=30);  #副本地图关卡时间设置
					Sender.Teleport(map,17,20)	#飞地图ID X坐标 Y坐标   
					SubGameGold(Sender,50)    #扣除物品
					Sender.TakeItem("号角",300)                  #扣除物品
					return Dict   #不执行提示框
				else:
					say = "本副本每日只能进入三次，今日已经达到上限无法进入"
			else:
				say = "材料不足，无法进入副本。。。。。"
		else:
			say = """元宝不足，无法进入副本。。。。。

			[离开:0]"""
			
		Dict['Say']=say
		return Dict
   
	elif(Menu == 2):
		if (Sender.GameGold > 99):   #判断需要的物品数量			
			if(Sender.GetItemCount("结晶") > 19):                #判断需要的物品数量				
				if(PlayerGetV(Sender,GV_BWMBOSSFB_COUNT)<3):   #定义个人全局变量
					PlayerSetV(Sender,GV_BWMBOSSFB_COUNT,PlayerGetV(Sender,GV_BWMBOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
					if (Sender.GroupMembers):   
					    Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
					map = Server.Envir.SEnvir.CreateMap(1588)                     #开启副本地图  （地图ID）
					map.CreateMon(50,50,100,'火焰沃玛',150)           
					map.CreateMon(50,50,100,'沃玛战士',150)          
					map.CreateMon(50,50,100,'暗黑战士',50)           
					map.CreateMon(50,50,50,'沃玛教主',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
					map.MapTime = datetime.now()+ timedelta(minutes=40);  #副本地图关卡时间设置
					Sender.Teleport(map,17,20)	#飞地图ID X坐标 Y坐标   
					SubGameGold(Sender,100)    #扣除物品
					Sender.TakeItem("结晶",20)                  #扣除物品
					return Dict   #不执行提示框
				else:
					say = "本副本每日只能进入三次，今日已经达到上限无法进入"
			else:
				say = "材料不足，无法进入副本。。。。。"
		else:
			say = """元宝不足，无法进入副本。。。。。

			[离开:0]"""
			
		Dict['Say']=say
		return Dict
   
	elif(Menu == 3):
		if (Sender.GameGold > 199):   #判断需要的物品数量			
			if(Sender.GetItemCount("魔魂") > 0):                #判断需要的物品数量				
				if(PlayerGetV(Sender,GV_CWMBOSSFB_COUNT)<3):   #定义个人全局变量
					PlayerSetV(Sender,GV_CWMBOSSFB_COUNT,PlayerGetV(Sender,GV_CWMBOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
					if (Sender.GroupMembers):   
					    Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
					map = Server.Envir.SEnvir.CreateMap(1589)                     #开启副本地图  （地图ID）
					map.CreateMon(50,50,100,'火焰沃玛',150)           
					map.CreateMon(50,50,100,'沃玛战士',150)          
					map.CreateMon(50,50,100,'暗黑战士',50)           
					map.CreateMon(50,50,50,'沃玛教主',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
					map.MapTime = datetime.now()+ timedelta(minutes=60);  #副本地图关卡时间设置
					Sender.Teleport(map,17,20)	#飞地图ID X坐标 Y坐标   
					SubGameGold(Sender,200)    #扣除物品
					Sender.TakeItem("魔魂",1)                  #扣除物品
					return Dict   #不执行提示框
				else:
					say = "本副本每日只能进入三次，今日已经达到上限无法进入"
			else:
				say = "材料不足，无法进入副本。。。。。"
		else:
			say = """元宝不足，无法进入副本。。。。。

			[离开:0]"""
			
		Dict['Say']=say
		return Dict

	elif(Menu == 4):
		if (Sender.GameGold > 49):   #判断需要的物品数量			
			if(Sender.GetItemCount("铜矿") > 299):                #判断需要的物品数量				
				if(PlayerGetV(Sender,GV_AWMBOSSFB_COUNT)<3):   #定义个人全局变量
					PlayerSetV(Sender,GV_AWMBOSSFB_COUNT,PlayerGetV(Sender,GV_AWMBOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
					if (Sender.GroupMembers):   
					    Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
					map = Server.Envir.SEnvir.CreateMap(1587)                     #开启副本地图  （地图ID）
					map.CreateMon(50,50,100,'火焰沃玛',150)           
					map.CreateMon(50,50,100,'沃玛战士',150)          
					map.CreateMon(50,50,100,'暗黑战士',50)           
					map.CreateMon(50,50,50,'沃玛教主',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
					map.MapTime = datetime.now()+ timedelta(minutes=30);  #副本地图关卡时间设置
					Sender.Teleport(map,17,20)	#飞地图ID X坐标 Y坐标   
					SubGameGold(Sender,50)    #扣除物品
					Sender.TakeItem("铜矿",300)                  #扣除物品
					return Dict   #不执行提示框
				else:
					say = "本副本每日只能进入三次，今日已经达到上限无法进入"
			else:
				say = "材料不足，无法进入副本。。。。。"
		else:
			say = """元宝不足，无法进入副本。。。。。

			[离开:0]"""
			
		Dict['Say']=say
		return Dict






#主菜单
	else:
		if Sender.Level < 30 : # 等级判断
			say  = """你实力不够，不要白白失去性命。
			请修炼到30级后，再来找我。
			
			[离开:0]"""
		else:
			say = """注意：进入次数每日总计3次，可以选择不同难度进入
					
<font color=\"0xff00ff00\">普通地图：进入条件：300个“号角”,50元宝 </font>
<font color=\"0xff00ff00\">普通地图：进入条件：300个“铜矿”,50元宝 </font>
<font color=\"0xff00ff00\">普通地图：难度设置与BOSS房间难度一样</font>

			[材料进入普通BOSS地图:1]  [矿石进入普通BOSS地图:4]

<font color=0xffcc0099>噩梦地图：进入条件：20个“结晶”，100元宝 </font>
<font color=0xffcc0099>噩梦地图：怪物HP攻击经验增加100%，爆率增加50%</font>

			[进入噩梦BOSS地图:2]

<font color=0xffFF0033>地狱地图：进入条件：1个“魔魂”，200元宝 </font>
<font color=0xffFF0033>地狱地图：怪物HP加200%攻击经验增加400%，爆率增加100%</font>

			[进入地狱BOSS地图:3]			


			
			[我只是路过:0]"""

		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(382,"OnClick",OnClick)	