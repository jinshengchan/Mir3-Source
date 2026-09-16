# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir

import clr
clr.AddReference("System.Core")
clr.AddReference("Library")
clr.AddReference('System')
import System
clr.ImportExtensions(System.Linq)

# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
from Library import *
import unicodedata
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
	
	if (Menu == 3):
		say = """为了申请攻城战需要祖玛头像。
		你有那个东西吗？
		现在申请的话 <font color=\"0xff00ff00\">2天后晚上8点</font> 开始战争。
		
		[前一步:99]"""

	elif Menu == 1:
		say = "下面是已经提交的攻城战:\n\n"
		count = 1
		for conquest in SEnvir.UserConquestList.Binding:
			say += '{}. {} 提交 {} 的攻城战\n 开始时间: {}\n'.format(count, conquest.Guild.GuildName, 
				conquest.Castle.Name, conquest.WarDate + conquest.Castle.StartTime)
			count += 1

	elif Menu == 2:
		Sender.GuildConquest(1)

	elif Menu == 10:
		say ="""[看攻城战的日期:1]
		[沙巴克资金管理:11]
		[沙巴克城门管理:12]
		[沙巴克守卫管理:13]
		
		[结束:0]"""
	elif Menu == 11:
		# 获取沙巴克资金状况
		shabake = None
		for taxInfo in SEnvir.CastleFundInfoList.Binding:
			if taxInfo.Castle.Name == '沙巴克':
				shabake = taxInfo
				break
		say ="""沙巴克城 剩余资金：{} 金币
		
		[查看城堡财务:110]
		[提取沙巴克资金:111]
		[存入沙巴克资金:112]
		
		[结束:0]""".format(shabake.TotalFund)
	elif Menu == 110:
		say = "下面是城堡的财务情况, 城堡占领行会可以提取或存入\n\n"
		for taxInfo in SEnvir.CastleFundInfoList.Binding:
			if taxInfo.Castle.Name == '沙巴克':
				say += "{}:\n税收 {} 金币\n存款 {} 金币\n合计 {} 金币\n".format(taxInfo.Castle.Name, taxInfo.TotalTax, taxInfo.TotalDeposit, taxInfo.TotalFund)

	elif Menu == 111:
		Sender.PyInputBox("请输入提取金额", "Npc.沙巴克城.沙巴克管理员.Withdraw", "Npc.沙巴克城.沙巴克管理员.Withdraw")
		
	elif Menu == 112:
		Sender.PyInputBox("请输入存入金额", "Npc.沙巴克城.沙巴克管理员.Deposit", "Npc.沙巴克城.沙巴克管理员.Deposit")
		
	elif Menu == 12:
		say ="""沙巴克城状态
		
		[正中城门状态:121]
		[左侧城门状态:122]
		[右侧城门状态:123]
		
		[结束:0]"""
	elif Menu == 13:
		say ="""沙巴克城守卫补充
		
		[正中城门守卫1:131]    [正中城门守卫2:132]
		[正中城门守卫3:133]    [正中城门守卫4:134]
		
		[左侧城门守卫1:135]    [左侧城门守卫2:136]
		
		[右侧城门守卫1:137]    [右侧城门守卫2:138]
		
		[结束:0]"""
#主菜单
	else:
		say = """你不是沙巴克城主行会的城主啊。。。。。。
				
			[看攻城战的日期:1]
			[申请攻城战:2]
			[了解有关攻城战的事:3]
			
			[结束:0]"""

		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#再判断占领沙巴克的行会名
		if guild:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			if(owner and Sender.Character.CharacterName == owner.CharacterName):
				say = """[沙巴克管理:10]
				
				"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


def Deposit(params):
	if not params:
		return

	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
	else:
		player.MakeGoldDeposit('沙巴克', int(userInput))


def Withdraw(params):
	if not params:
		return

	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
	else:
		player.WithdrawCastleFund('沙巴克', int(userInput))
NpcEvent.add_listener(88,"OnClick",OnClick)