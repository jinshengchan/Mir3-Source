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
		say = """请你离开。
		
		我不想和红名交易。
		
		[离开:0]"""	
#跳转菜单1	
	elif (Menu == 1):
		say = """好极了。。。。。。
		地图开启了。
		
		[离开:0]"""	
		if(PlayerGetV(Sender,GV_XINSHOUFB_ONOFF)==0):                #定义个人全局变量
			PlayerSetV(Sender,GV_XINSHOUFB_ONOFF,1)                  #赋值个人全局变量为1，代表进入过
			map = Server.Envir.SEnvir.CreateMap(614)                         #开启副本地图（地图ID）
			map.CreateMon(241,200,10,'沃玛峡谷-半兽战士',18)
			map.CreateMon(241,200,10,'沃玛峡谷-半兽剑士',18)
			map.CreateMon(241,200,10,'沃玛峡谷-咒术鬼',1)
			Sender.Teleport(map,225,338)	#飞地图ID X坐标 Y坐标
		else:
			#PlayerSetV(Sender,GV_XINSHOUFB_ONOFF,0)           #测试复位全局变量
			say = """你今天已经不能再进入了。。。。。。
			
		
			[离开:0]"""
		
		
	elif (Menu == 3):
		if (Sender.Gold < 2000000):
			say  = """我不是免费干活的，还是意思意思比较好
			你连200万金币都没有，还是不要去凑热闹。
			
			[离开:0]"""             
		else:       
			map = Server.Envir.SEnvir.CreateMap(1502)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=20);  #副本地图关卡时间设置
			Sender.Teleport(map,168,46)	#飞地图ID X坐标 Y坐标
			map.CreateMon(47,38,5,'肥羊',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(105,65,200,'废材树',200)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(104,60,200,'迎客松',20)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			SubGold(Sender,2000000)
			return
	elif (Menu == 4):
		if current_time_is_between("12:01:00", "20:00:00"):
			map = Server.Envir.SEnvir.CreateMap(1505)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=30);  #副本地图关卡时间设置
			Sender.Teleport(map,31,107)	#飞地图ID X坐标 Y坐标
			map.CreateMon(104,27,1,'超级沃玛教主',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
		else:
			say = """没有在开放时间内。
			
		
			[离开:0]"""
		Dict['Say']=say
		return Dict
			 
			
#主菜单
	else:
		say = """既然你有机缘来到这里，我就送你去一个神秘的地方

		<font color=0xff00FF33>山顶地图说明</font>

<font color=\"0xff00ff00\">山顶地图时间20分钟</font>
<font color=\"0xff00ff00\">出产金色、银色等各色栗子</font>	
<font color=\"0xff00ff00\">各种经验券、经验珠</font>
	
	
		[请送我去吧:3] 


		
		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
def DelayCall(args):
	Sender=args[0]
	Sender.Connection.ReceiveChat("123",MessageType.System)
	Server.Envir.SEnvir.Log('delay开始了')
	
	

NpcEvent.add_listener(338,"OnClick",OnClick)