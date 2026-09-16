# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import MapEvent
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from 主线任务奖励 import *
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
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	Dict={}

#跳转菜单1
	if (Menu == 1):
		say = """竟然连这儿都知道~？真是像传闻中说的那样手腕高明啊！
			
			[我是来取回被你偷走了的不死牌的！:2]"""
	elif (Menu == 2):
		say = """哈哈哈！您可真是个奇怪的人啊!难道我会那么轻易的还给你？还是别痴心妄想了，赶快回去吧！
			
			[别说大话，赶快拿出来！:3]"""
	elif (Menu == 3):
		say = """反正在你手里也实现不了这个宝物的真正价值，难道不该到合适的主人手里吗？
			哈哈，这个世界上唯一有资格拥有不死牌这个宝物只有我……研究了一辈子长生不老的署箭！
			
			[好像没有再说什么的必要了！:4]"""
	elif (Menu == 5):
		say = """只是……？这东西算得了什么？我已经超越了死亡。和神仙没什么区别了！
			现在我马上就能够长生不老，永葆青春的生活下去了。到那时我就能超越神仙了！怎么样？难道不认为我的梦想很不错吗？
			
			[你别痴心妄想了！:6]"""
	elif (Menu == 6):
		say = """很遗憾！那只是个我看看你实力到底如何的机会而已！
			看来你真的可以和我一起联手支配世界啊……
			
			[真是彻底疯了！:7]"""
	elif (Menu == 7):
		say = """这样啊！结果又回到了原点！ 
			我可不想再和你作为对手而浪费体力。就先走一步了……
			
			[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==129):
			PlayerSetV(Sender,BV_NQ_MAIN,130)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			map.CreateMon(16,13,5,100030,5)
			say = """我也正好是这么想的！不过我想好像没有冒这个险跟你亲自动手的必要，哈哈……正好有了一个试验我刚研究出来的怪物的机会。你就和它比试一下吧！ 
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==129):
			say = """比我想象的来的还要早啊！
				
				[你就是署箭道士！:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==130):
			if (map.MonsterCount > 0 ):
				say = """你的对手就是它！
					
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,131)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
				Sender.Connection.ReceiveChat(" 10 秒后将自动传出本区域。",MessageType.System)
				say = """果然实力非凡啊！现在我终于相信你能独自打败半兽勇士的事儿了！
					
					[你偷走不死牌就只是为了制造这种怪物？:5]"""
		else:
			say = """你是抓不到我的！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(279,"OnClick",OnClick)
