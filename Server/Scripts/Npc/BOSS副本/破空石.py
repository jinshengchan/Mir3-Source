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
		say = """<font color=\"0xff00ff00\">副本出各种BUFF道具</font>
		
		
		[离开:0]"""
		if Sender.Level > 49 :   #判断等级	
			if(Sender.GetItemCount("破空石") > 0):                #判断需要的物品数量
				if(PlayerGetV(Sender,GV_APKSBOSSFB_COUNT)<1):   #定义个人全局变量
					if(Sender.GroupMembers):                    #队伍判断
						if(Sender == Sender.GroupMembers[0]):   #队长判断
							bOpen = True
							if len(Sender.GroupMembers) < 1:    #判断队伍人数
								bOpen = False
								say = """队员数不足3人,无法进入.
								
								[离开:0]"""
							else:
								for player in Sender.GroupMembers:                 #遍历所有队员
									if(PlayerGetV(player,GV_APKSBOSSFB_COUNT) == 1):  #队员变量判断  数值判断是否进入次数
										bOpen = False
										say = """队伍中有队员已经去过副本了
										无法进入
										
										[离开:0]"""
										break
									if player.Level < 50 :                      #队员等级判断
										bOpen = False
										say = """队伍中有队员等级不够50级，实力不够啊
										无法进入
										
										[离开:0]"""
										break

									if(player.GetItemCount("破空石") < 1):  #队员材料判断
										bOpen = False
										say = """队伍中有队员没有“破空石”，无法进入虚空~
										无法进入
										
										[离开:0]"""
										break
							if bOpen:    #如果可以开启
								map = Server.Envir.SEnvir.CreateMap(1623)               #开启副本地图  （地图ID）
								map.MapTime = datetime.now()+timedelta(minutes=60)    #副本地图关卡时间设置（分钟）
								map.CreateMon(70,88,100,'破碎虚空小怪2',2)
								map.CreateMon(70,88,100,'破碎虚空小怪3',2)
								map.CreateMon(70,88,30,'破碎虚空小怪',10)
								map.CreateMon(70,88,30,'破碎虚空小怪1',10)
								map.CreateMon(86,75,30,'破碎虚空小怪',10)
								map.CreateMon(86,75,30,'破碎虚空小怪1',10)
								map.CreateMon(77,83,2,'沉鱼',1)           
								map.CreateMon(29,127,2,'落雁',1)          
								map.CreateMon(30,126,20,'破碎虚空小怪',10)
								map.CreateMon(30,126,20,'破碎虚空小怪1',10)
								map.CreateMon(31,33,2,'闭月',1)           
								map.CreateMon(31,33,20,'破碎虚空小怪',10)
								map.CreateMon(31,33,20,'破碎虚空小怪1',10)
								map.CreateMon(123,30,2,'羞花',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
								map.CreateMon(123,30,20,'破碎虚空小怪',10)
								map.CreateMon(123,30,20,'破碎虚空小怪1',10)
								PlayerSetV(Sender,GV_APKSBOSSFB_COUNT,1)
								PlayerSetV(Sender,GV_KILLMON_PKSCOUNT,0)
								for player in Sender.GroupMembers:                     #遍历所有队员
									PlayerSetV(player,GV_APKSBOSSFB_COUNT,1)             #赋值变量为1，代表进入
									player.TakeItem("破空石",1)                    #扣除材料
									player.Teleport(map,110,118)                        #把全组人传送进副本
						else:
							say = """不是队长
							
							[离开:0]"""
					else:
						say = """没有队伍
						
						[离开:0]"""
				else:
					say = """你今天已经不能再进入了。。。。。。
					
					[离开:0]"""
			else:
				say = """队长身上至少1颗“破空石”，无法进入
				
				[离开:0]"""
		else:
			say = """实力不够，无法进入副本，至少50级。。。。。

			[离开:0]"""

			
		Dict['Say']=say
		return Dict
   
	elif(Menu == 2):
		if Sender.Character.Rebirth < 1 : # 等级判断			
			if(Sender.GetItemCount("破空石") > 4):                #判断需要的物品数量				
				if(PlayerGetV(Sender,GV_BPKSBOSSFB_COUNT)<1):   #定义个人全局变量
					PlayerSetV(Sender,GV_BPKSBOSSFB_COUNT,PlayerGetV(Sender,GV_BPKSBOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
					if (Sender.GroupMembers):   
					    Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
					Sender.TeleportByMapIndex(1624,110,118)                     #开启副本地图  （地图ID）
					Sender.TakeItem("破空石",5)                  #扣除物品
					return Dict   #不执行提示框
				else:
					say = "本副本每日只能进入1次，今日已经达到上限无法进入"
			else:
				say = "材料不足，无法进入副本。。。。。"
		else:
			say = """实力不够，无法进入副本，至少1转。。。。。

			[离开:0]"""
			
		Dict['Say']=say
		return Dict
   
	elif(Menu == 3):
		if Sender.Character.Rebirth < 3 : # 等级判断			
			if(Sender.GetItemCount("破空石") > 9):                #判断需要的物品数量				
				if(PlayerGetV(Sender,GV_CPKSBOSSFB_COUNT)<1):   #定义个人全局变量
					PlayerSetV(Sender,GV_CPKSBOSSFB_COUNT,PlayerGetV(Sender,GV_CPKSBOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
					if (Sender.GroupMembers):   
					    Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
					Sender.TeleportByMapIndex(1625,110,118)                     #开启副本地图  （地图ID）
					Sender.TakeItem("破空石",10)                  #扣除物品
					return Dict   #不执行提示框
				else:
					say = "本副本每日只能进入1次，今日已经达到上限无法进入"
			else:
				say = "材料不足，无法进入副本。。。。。"
		else:
			say = """实力不够，无法进入副本，至少3转。。。。。

			[离开:0]"""
			
		Dict['Say']=say
		return Dict

#主菜单
	else:
		#if(Sender.GetItemCount("传送石") < 3): # 条件判断
			#say  = """包裹内需要至少3颗“传送石”。
			#如果没有足够多的“传送石”，进入副本也是白搭。

			#[离开:0]"""
		if Sender.Level < 50 :   #判断等级	
			say  = """等级不够。
			没修炼到50级，去了也是队伍的累赘

			[离开:0]"""

		else:
			say = """注意：进入次数每日总计1次，可以根据情况选择不同难度进入
					

<font color=\"0xff00ff00\">普通难度：50级及以上等级，1个“破空石” </font>
<font color=\"0xff00ff00\">普通地图：难度适中，爆率一般</font>

			[进入沉鱼落雁秘境:1]

<font color=0xffcc0099>噩梦难度：一级转生；5个“破空石” </font>
<font color=0xffcc0099>噩梦地图：难度哇塞，爆率比较哇塞</font>

			[进入闭月羞花秘境:2]

<font color=0xffFF0033>地狱难度：三级转生，10个“破空石” </font>
<font color=0xffFF0033>地狱地图：难度大，爆率高</font>

			[进入红粉骷髅秘境:3]			


			
			[我只是路过:0]"""

		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(394,"OnClick",OnClick)	