# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Library import *

import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)
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


	#先判断城池的名字
	guild = SEnvir.GetGuildFromCastleName("沙巴克")
	#然后做行会判断
	if not guild:
		say = """　<font color=\"0xff00ff00\">沙巴克城主人</font>
		
		<font color=\"0xffff0000\">′ ′</font>  的旗帜
		"""
	else:
		owner = SEnvir.GetGuildLeader(guild.GuildName)
		say = """　<font color=\"0xff00ff00\">沙巴克城主人</font>
		
		<font color=\"0xffff0000\">〖{}〗</font>  的行会旗帜
		""".format(guild.GuildName)
		
		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(87,"OnClick",OnClick)
NpcEvent.add_listener(89,"OnClick",OnClick)
NpcEvent.add_listener(90,"OnClick",OnClick)
NpcEvent.add_listener(91,"OnClick",OnClick)
NpcEvent.add_listener(92,"OnClick",OnClick)