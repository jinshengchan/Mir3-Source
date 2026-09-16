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
	
	if (Menu == 1):
		#获取全部战士职业
		allPlayers= [x for x in SEnvir.CharacterInfoList.Binding if x.Class == MirClass.Warrior]
		sortByLevel = sorted(allPlayers, cmp=None, key=lambda x: x.Rebirth*1000+x.Level, reverse=True)
		qianshi_cike = sortByLevel[:10]   #只显示前10排名
		say = '{0: <10} {1}  {2}  {3}\n'.format('排名', '角色', '转生','等级') 
		say += '\n'.join("第{}名       {}  （{}）（{}）".format(qianshi_cike.index(e) + 1, e.CharacterName, e.Rebirth, e.Level) for e in qianshi_cike)
	elif (Menu == 2):
		#获取全部法师职业
		allPlayers= [x for x in SEnvir.CharacterInfoList.Binding if x.Class == MirClass.Wizard]
		sortByLevel = sorted(allPlayers, cmp=None, key=lambda x: x.Rebirth*1000+x.Level, reverse=True)
		qianshi_cike = sortByLevel[:10]   #只显示前10排名
		say = '{0: <10} {1}  {2}  {3}\n'.format('排名', '角色', '转生','等级') 
		say += '\n'.join("第{}名       {}  （{}）（{}）".format(qianshi_cike.index(e) + 1, e.CharacterName, e.Rebirth, e.Level) for e in qianshi_cike)
	elif (Menu == 3):
		#获取全部道士职业
		allPlayers= [x for x in SEnvir.CharacterInfoList.Binding if x.Class == MirClass.Taoist]
		sortByLevel = sorted(allPlayers, cmp=None, key=lambda x: x.Rebirth*1000+x.Level, reverse=True)
		qianshi_cike = sortByLevel[:10]   #只显示前10排名
		say = '{0: <10} {1}  {2}  {3}\n'.format('排名', '角色', '转生','等级') 
		say += '\n'.join("第{}名       {}  （{}）（{}）".format(qianshi_cike.index(e) + 1, e.CharacterName, e.Rebirth, e.Level) for e in qianshi_cike)
	elif (Menu == 4):
		#获取全部刺客职业
		allPlayers= [x for x in SEnvir.CharacterInfoList.Binding if x.Class == MirClass.Assassin]
		sortByLevel = sorted(allPlayers, cmp=None, key=lambda x: x.Rebirth*1000+x.Level, reverse=True)
		qianshi_cike = sortByLevel[:10]   #只显示前10排名
		say = '{0: <10} {1}  {2}  {3}\n'.format('排名', '角色', '转生','等级') 
		say += '\n'.join("第{}名       {}  （{}）（{}）".format(qianshi_cike.index(e) + 1, e.CharacterName, e.Rebirth, e.Level) for e in qianshi_cike)
	elif (Menu == 5):
		#获取账号信息列表
		allAccounts = SEnvir.AccountInfoList.Binding
		#判断玩家的金币
		sortByGold = sorted(allAccounts, cmp=None, key=lambda x: x.Gold, reverse=True)
		#判断玩家是否相同账号
		sortByGold = [x for x in sortByGold if x.LastCharacter]
		qianshi_cike = sortByGold[:10]   #只显示前10排名
		say = '{0: <10} {1}  {2}\n'.format('排名', '角色', '金币') 
		say += '\n'.join("{}               {}  （{}）".format(qianshi_cike.index(e) + 1, e.LastCharacter.CharacterName, e.Gold) for e in qianshi_cike)
	elif (Menu == 6):
		#获取账号信息列表
		allAccounts = SEnvir.AccountInfoList.Binding
		#判断玩家的元宝
		sortByGameGold = sorted(allAccounts, cmp=None, key=lambda x: x.GameGold, reverse=True)
		#判断玩家是否相同账号
		sortByGameGold = [x for x in sortByGameGold if x.LastCharacter]
		qianshi_cike = sortByGameGold[:10]   #只显示前10排名
		say = '{0: <10} {1}  {2}\n'.format('排名', '角色', '元宝') 
		say += '\n'.join("{}               {}  （{}）".format(qianshi_cike.index(e) + 1, e.LastCharacter.CharacterName, e.GameGold) for e in qianshi_cike)
#主菜单
	else:
		say = """＜本排行榜只显示等级前10名上榜者＞

		[战士排行:1]

		[法师排行:2]

		[道士排行:3]
        
		[刺客排行:4]
		[金币排行:]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(334,"OnClick",OnClick)