# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
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
import collections
import PlayerEvent
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
from Utils import ServerUtils
import MapEvent

######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

# 数据库需要新建一个自定义buff, 作为天下第一buff
# 注意设定自定义buff的属性以及持续时间
# 此变量设为这个自定义buff的序号
PLAYER_PK_BUFF_INDEX = 110

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		if(PlayerGetV(Sender,GV_PLAYER_ZHOUJINGJICHANG)==0):                #定义个人全局变量 
			say = """活动奖励丰厚，要领取奖励前建议你清理包裹剩余6格以上空间在领取，否则奖品遗失概不负责。
			
			[确定领奖:11]
			[我整理下包裹先:0]"""
		else:
			say = """当前奖励已被领取。
			
			[关闭:0]"""
	elif (Menu == 11):
		if (Sender.CurrentMap.Players.Count == 1):     #判断地图是否只剩玩家一人
			if Sender.Character.Account.TempAdmin:  # 判断是否是管理员 是管理员就打印出指令
				return
			ServerUtils.SendMsgToAll("恭喜玩家 {} 击败所有强悍对手，成为死亡竞技场的勇者！".format(Sender.Name))
			ServerUtils.SendMsgToAll("恭喜玩家 {} 击败所有强悍对手，成为死亡竞技场的勇者！".format(Sender.Name))
			ServerUtils.SendMsgToAll("恭喜玩家 {} 击败所有强悍对手，成为死亡竞技场的勇者！".format(Sender.Name))
			ServerUtils.SendMsgToAll("恭喜玩家 {} 击败所有强悍对手，成为死亡竞技场的勇者！".format(Sender.Name))
			ServerUtils.SendMsgToAll("恭喜玩家 {} 击败所有强悍对手，成为死亡竞技场的勇者！".format(Sender.Name), MessageType.RollNotice)
			if(PlayerGetV(Sender,GV_PLAYER_ZHOUJINGJICHANG)==0):                #定义个人全局变量
				PlayerSetV(Sender,GV_PLAYER_ZHOUJINGJICHANG,1)                  #赋值领取过
				Sender.CustomBuffAdd(PLAYER_PK_BUFF_INDEX)    #给玩家赋值天下第一的称号BUFF
				GivePrestige(Sender,100)          #给声望100点
				Sender.Connection.ReceiveChat("得到100点声望",MessageType.System)
				GiveGold(Sender,1000000)           #给金币100万
				Sender.Connection.ReceiveChat("得到1000000金币",MessageType.System)
				Sender.GiveItem("万年雪霜",100)    #给100个万年雪霜
				Sender.GiveItem("天下无双·黄金",1)      #给天下无双武器一把
				Sender.GiveItem("攻击神水（特）",1)          #给药水
				Sender.GiveItem("自然神水（特）",1)
				Sender.GiveItem("灵魂神水（特）",1)
				Sender.TeleportByMapIndex(1,461,364)          #飞地图ID X坐标 Y坐标
			return
		else:
			say = """地图里还有剩余玩家，你无法领取奖励。
			
			[关闭:0]"""
	elif (Menu == 2):
		Sender.TeleportByMapIndex(1,461,364)          #飞地图ID X坐标 Y坐标
		return
		
#主菜单
	else:	
		say = """只有战到最后的勇士，才能胜利。
		你确定已经击败了所有对手了吗？
		
		[领取天下第一:1]
		
		[离开比赛:2]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(353,"OnClick",OnClick)