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
import PlayerEvent
import collections
import Server.Envir.SEnvir as SEnvir
clr.AddReference("System.Core")
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
	say = ''

	#获取行会信息列表
	allGuild = SEnvir.GuildInfoList.Binding.Where(lambda x: len(x.Members)!=0).ToList()
	#行会排序
	sortByGuild = sorted(allGuild, cmp=None, key=lambda x: len(x.Members), reverse=True)
	#构造一个行会的字典
	guilds = collections.OrderedDict() 
	for i in range(len(allGuild)):
		#新手行会不显示在列表里
		if allGuild[i].GuildName == '新手行会':
			continue
		if i < 20:                  #只显示排名前20的行会
			guilds[str(i)] = allGuild[i]

	# 菜单
	if Menu >= 1 and Menu <= len(guilds):
		guild = guilds[str(Menu)]
		say = """<font color=\"0xff00ff00\">行会名字:</font>   <font color=\"0xffffff00\">{}</font> \n<font color=\"0xff00ff00\">行会等级:</font>   <font color=\"0xffffff00\">{}</font>\n<font color=\"0xff00ff00\">行会人数:</font>   <font color=\"0xffffff00\">{}/{}</font>\n<font color=\"0xff00ff00\">行会首领:</font>   <font color=\"0xffffff00\">{}</font>
		
		
		[申请入会:{}]
		""".format(guild.GuildName, guild.GuildLevel, len(guild.Members), guild.MemberLimit, SEnvir.GetGuildLeader(guild.GuildName), 100+guild.Index)
	
	elif Menu > 100 and Menu < len(guilds):
		if Sender.Character.Account.GuildMember:
			say = """你已有行会，请勿重复申请。

[关闭:0]"""
		else:
			Sender.Character.Account.AllowGuild
			guild = allGuild[Menu-101]
			Sender.ApplyJoinGuild(guild.Index)
			return

	else:
		say = """<font color=\"0xff00ff00\">行会排名按人数从高到低，点击行会名字可查看具体信息</font>
		
		"""
		for key, value in guilds.iteritems():
			say += '{}.    [{}:{}]\n'.format(key, value.GuildName, key)
			
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(220,"OnClick",OnClick)