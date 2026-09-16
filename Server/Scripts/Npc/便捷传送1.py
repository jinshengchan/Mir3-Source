# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import NpcEvent
from Defines import *
import PlayerEvent
import Server
import Utils.Colors as Colors
import Server.Envir.SEnvir as SEnvir
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
from Npc.商店列表 import *
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

#城镇传送
	if(Menu == 1):
		if (Sender.Gold < 0):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,0)
			Sender.TeleportByMapIndex(7,400,125)
			return
	elif(Menu == 2):
		if (Sender.Gold < 0):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,0)
			Sender.TeleportByMapIndex(6,266,190)
			return
	elif(Menu == 3):
		if (Sender.Gold < 0):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,0)
			Sender.TeleportByMapIndex(5,434,268)
			return
	elif(Menu == 4):
		if (Sender.Gold < 0):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,0)
			Sender.TeleportByMapIndex(1,450,390)
			return
	elif(Menu == 5):
		if (Sender.Gold < 0):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,0)
			Sender.TeleportByMapIndex(24,343,224)
			return
	elif(Menu == 6):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(25,220,159)
			return
	elif(Menu == 7):
		if (Sender.Gold < 1000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,1000)
			Sender.TeleportByMapIndex(57,192,577)
			return
	elif(Menu == 8):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(55,288,238)
			return
	elif(Menu == 9):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(33,181,135)
			return
	elif(Menu == 10):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(27,433,81)
			return
	elif(Menu == 11):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(37,200,288)
			return
#比奇买马
	elif(Menu == 12):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(1,378,307)
			return
#银杏加点
	elif(Menu == 13):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(6,248,239)
			return
	elif(Menu == 14):
		if (Sender.Gold < 10000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,10000)
			Sender.TeleportByMapIndex(50,345,327)
			return
#危险地图传送
	elif(Menu == 15):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(77,74,72)
			return
	elif(Menu == 16):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(170,203,201)
			return
	elif(Menu == 17):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(149,159,167)
			return
	elif(Menu == 18):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(270,51,283)
			return
	elif(Menu == 19):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(299,127,172)
			return
	elif(Menu == 20):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[离开:0]"""
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(25,222,157)
			return
	elif(Menu == 21):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(340,173,223)
			return
	elif(Menu == 22):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
			
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(356,119,109)
			return
	elif(Menu == 23):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(362,38,147)
			return
	elif(Menu == 24):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(375,283,278)
			return
	elif(Menu == 25):
		if (Sender.Gold < 50000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(26,170,135)
			return
	elif(Menu == 26):
		NPCObject = ServerUtils.GetNPCObject(247)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.任务进度查询.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif(Menu == 27):
		if (Sender.Gold < 20000):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,20000)
			Sender.TeleportByMapIndex(285,135,180)
			return



	elif(Menu == 63):
		say = """我这里可以用元宝兑换金币，
		
		<font color=\"0xffff0000\">你是否需要兑换？</font>
		
		[1元宝兑换50000金币:631]
			
		[5元宝兑换250000金币:632]
			
		[15元宝兑换750000金币:633]
			
		[20元宝兑换1000000金币:634]
			
		[25元宝兑换1250000金币:635]
			
		[30元宝兑换1500000金币:636]
			
		[50元宝兑换2500000金币:637]
			
		[100元宝兑换5000000金币:638]"""
	elif(Menu == 631):
		if (Sender.GameGold < 1):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,1)
			GiveGold(Sender,50000)
			say = """兑换成功。
			
			[继续兑换:63]
			[离开:0]"""
	elif(Menu == 632):
		if (Sender.GameGold < 5):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,5)
			GiveGold(Sender,250000)
			say = """兑换成功。
			
			[继续兑换:632]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 633):
		if (Sender.GameGold < 15):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,15)
			GiveGold(Sender,750000)
			say = """兑换成功。
			
			[继续兑换:633]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 634):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			GiveGold(Sender,1000000)
			say = """兑换成功。
			
			[继续兑换:634]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 635):
		if (Sender.GameGold < 25):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,25)
			GiveGold(Sender,1250000)
			say = """兑换成功。
			
			[继续兑换:635]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 636):
		if (Sender.GameGold < 30):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,30)
			GiveGold(Sender,1500000)
			say = """兑换成功。
			
			[继续兑换:636]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 637):
		if (Sender.GameGold < 50):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,50)
			GiveGold(Sender,2500000)
			say = """兑换成功。
			
			[继续兑换:637]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 638):
		if (Sender.GameGold < 100):
			say = """你没有足够的元宝，无法兑换。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,100)
			GiveGold(Sender,5000000)
			say = """兑换成功。
			
			[继续兑换:638]
			
			[主菜单:63]
			
			[离开:0]"""
	elif(Menu == 64):
		NPCObject = ServerUtils.GetNPCObject(221)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.背号功能.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif(Menu == 65):
		NPCObject = ServerUtils.GetNPCObject(214)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.一键出售.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif(Menu == 66):
		NPCObject = ServerUtils.GetNPCObject(217)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.游戏声明.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif(Menu == 67):
		NPCObject = ServerUtils.GetNPCObject(218)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.主线任务全攻略.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
#危险地图传送
	elif(Menu == 515):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(77,74,72)
			return
	elif(Menu == 516):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(170,203,201)
			return
	elif(Menu == 517):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(149,159,167)
			return
	elif(Menu == 518):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(270,51,283)
			return
	elif(Menu == 519):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(299,127,172)
			return
	elif(Menu == 520):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(285,135,180)
			return
	elif(Menu == 521):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(340,173,223)
			return
	elif(Menu == 522):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(356,119,109)
			return
	elif(Menu == 523):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(362,38,147)
			return
	elif(Menu == 524):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(375,283,278)
			return
	elif(Menu == 525):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(26,170,135)
			return
	elif(Menu == 526):
		Sender.TeleportByMapIndex(50,349,326)
		return
	elif(Menu == 5231):
		if (Sender.GameGold < 25):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,25)
			Sender.TeleportByMapIndex(363,192,204)
			return
	elif(Menu == 5232):
		if (Sender.GameGold < 30):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,30)
			Sender.TeleportByMapIndex(368,195,181)
			return
	elif(Menu == 5221):
		if (Sender.GameGold < 25):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,25)
			Sender.TeleportByMapIndex(359,186,20)
			return
	elif(Menu == 5222):
		if (Sender.GameGold < 30):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,30)
			Sender.TeleportByMapIndex(360,180,28)
			return
	elif(Menu == 5211):
		if (Sender.GameGold < 25):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,25)
			Sender.TeleportByMapIndex(347,159,150)
			return
	elif(Menu == 5212):
		if (Sender.GameGold < 30):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,30)
			Sender.TeleportByMapIndex(354,180,182)
			return
	elif(Menu == 5181):
		if (Sender.GameGold < 15):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,15)
			Sender.TeleportByMapIndex(274,153,252)
			return
	elif(Menu == 5251):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(138,20,22)
			return
	elif(Menu == 5201):
		if (Sender.GameGold < 12):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,12)
			Sender.TeleportByMapIndex(288,35,64)
			return
	elif(Menu == 5202):
		if (Sender.GameGold < 14):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,14)
			Sender.TeleportByMapIndex(287,207,333)
			return
	elif(Menu == 5203):
		if (Sender.GameGold < 16):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,16)
			Sender.TeleportByMapIndex(294,34,28)
			return
	elif(Menu == 5204):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(297,380,382)
			return
	elif(Menu == 5191):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(302,61,282)
			return
	elif(Menu == 5151):
		if (Sender.GameGold < 15):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,15)
			Sender.TeleportByMapIndex(82,199,195)
			return
	elif(Menu == 5171):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(156,150,67)
			return
	elif(Menu == 5161):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(175,36,18)
			return
	elif(Menu == 527):
		if (Sender.GameGold < 2):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,2)
			Sender.TeleportByMapIndex(103,30,373)
			return
	elif(Menu == 528):
		if (Sender.GameGold < 2):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,2)
			Sender.TeleportByMapIndex(85,25,180)
			return
	elif(Menu == 529):
		if (Sender.GameGold < 2):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,2)
			Sender.TeleportByMapIndex(58,151,362)
			return
	elif(Menu == 530):
		if (Sender.GameGold < 2):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,2)
			Sender.TeleportByMapIndex(1,64,178)
			return
	elif(Menu == 531):
		if (Sender.GameGold < 2):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,2)
			Sender.TeleportByMapIndex(1,64,178)
			return
	elif(Menu == 532):
		if (Sender.GameGold < 20):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,20)
			Sender.TeleportByMapIndex(375,278,269)
			return
	elif(Menu == 533):
		if (Sender.GameGold < 30):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,30)
			Sender.TeleportByMapIndex(376,79,183)
			return
	elif(Menu == 534):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(486,141,51)
			return
	elif(Menu == 535):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(477,215,112)
			return
	elif(Menu == 536):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(886,30,257)
			return
	elif(Menu == 537):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(887,34,35)
			return
	elif(Menu == 538):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(888,46,35)
			return
	elif(Menu == 539):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(889,27,175)
			return
	elif(Menu == 540):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(476,200,376)
			return
	elif(Menu == 541):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(478,263,251)
			return
	elif(Menu == 542):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(480,152,274)
			return
	elif(Menu == 543):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(482,202,349)
			return
	elif(Menu == 544):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(500,266,244)
			return
	elif(Menu == 545):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(501,162,265)
			return
	elif(Menu == 546):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(503,213,254)
			return
	elif(Menu == 547):
		if (Sender.GameGold < 10):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,10)
			Sender.TeleportByMapIndex(504,185,369)
			return

	elif(Menu == 800):
		if (Sender.GameGold < 100):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""
		else:
			SubGameGold(Sender,100)
			Sender.TeleportByMapIndex(246,43,62)
			return
	elif(Menu == 50):
		say = """<font color=\"0xffff0000\">危险传送：费用10元宝起</font>

		<font color=\"0xff00ff00\">移动至矿洞　　:</font>[毒蛇矿洞:527] [比奇矿洞:528]
		<font color=\"0xff00ff00\">移动至半兽洞穴:</font>[半兽洞穴入口:529] [天然洞穴:531]

<font color=\"0xff00ff00\">移动至沃玛神殿:</font>[1层:515] [2层:5151]          
		<font color=\"0xff00ff00\">移动至石阁庙　:</font>[1层:516] [6层:5161]
		<font color=\"0xff00ff00\">移动至万年峡谷:</font>[1层:517] [4层:5171]
		<font color=\"0xff00ff00\">移动至赤月峡谷:</font>[1层:518] [4层:5181]
		<font color=\"0xff00ff00\">移动至潘夜石窟:</font>[1层:519] [4层:5191]
		<font color=\"0xff00ff00\">移动至潘夜神殿:</font>[1层:520] [小3:5201] [大3:5202] [6层:5203] [8层:5204]
		<font color=\"0xff00ff00\">移动至祖玛神殿:</font>[1层:525] [6层:5251]
		<font color=\"0xff00ff00\">移动至真天黑度:</font>[真1:521] [东2:5211] [北5:5212]  [黑1:522] [黑3:5221] [黑4:5222]
		<font color=\"0xff00ff00\">移动至诺玛遗址:</font>[1层:523] [2层:5231] [4层:5232]
		<font color=\"0xff00ff00\">移动至  西沙　:</font>[西沙漠地洞:532] [沙漠地洞1层:533]"""

#主菜单
	else:
		say = """           欢迎来到  <font color=\"0xff00ff00\">逍遥传奇3</font>  玛法大陆
		
		[随身任务进度查询:26]      [元宝换金币:63]      [一键出售:65]

		[江湖事迹任务流程:66]      [主线任务全攻略参考:67]
	
		<font color=\"0xff00ff00\">城镇传送：部分免费</font>

		[道馆:1]   [比奇:4]    [银杏:2]     [边境:3]    [毒蛇:5]  [失乐园:7]  

		[潘夜岛:8]  [诺玛:9]    [绿洲:10]     [沙漠土城:11]    [盟重土城:14]
                     
		<font color=\"0xff00ccff\">危险地图传送：费用20000金币</font>

		[沃玛神殿:15]    [石阁寺庙:16]     [万年峡谷:17]     [赤月峡谷:18]

		[潘夜石窟:19]    [祖玛神殿:25]     [潘夜神殿:27]     [沙巴克:20]

		<font color=\"0xffff0000\">危险地图传送：费用50000金币</font>

		[黑度宫:22]      [真天宫:21]      [诺玛遗址:23]      [西沙漠:24]	
		       
		<font color=\"0xffff0000\">元宝地图传送</font>

		[元宝传送:50]

[自动回收开关:600]  [手动回收:602]  [回收列表:603]  <font color=\"{}\">自动回收状态：{}</font>
		
    # 如果没有处理结果(如成功传送)，则返回None
    if say is None:
        return None
    
    Dict['Say'] = say
    return Dict

def ExecuteEquipmentRecycleForSender(Sender):
    """只针对当前Sender执行装备回收功能"""
    import datetime
    import time
    import os
    
    current_time = datetime.datetime.now()
    player_name = Sender.Character.CharacterName
    
    # 记录到专门的回收日志文件
    log_message = "[{}] 开始检查玩家 {} 的回收状态".format(current_time.strftime("%Y-%m-%d %H:%M:%S"), player_name)
    print(log_message)
    
    # 写入回收日志文件
    try:
        with open("equipment_recycler.log", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    except Exception as e:
        print("写入回收日志失败: {}".format(e))
    
    last_recycle_timestamp = PlayerGetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME)
    print("玩家 {} 的上次回收时间戳: {}".format(player_name, last_recycle_timestamp))
    
    # 手动回收没有间隔限制，每次点击都执行
    print("玩家 {} 执行手动回收".format(player_name))
    
    recycled_count = 0
    gold_given = 0
    
    print("开始检查玩家 {} 的装备:".format(player_name))
    print("回收列表中共有 {} 种装备".format(len(RECYCLE_EQUIPMENT)))
    for equipment in RECYCLE_EQUIPMENT:
        try:
            equipment_count = int(Sender.GetItemCount(equipment))
            print("  - {}: {}个".format(equipment, equipment_count))
            if equipment_count > 0:
                print("发现玩家 {} 有 {} 个 {}".format(player_name, equipment_count, equipment))
                # 检查装备是否在回收字典中
                if equipment in RECYCLE_REWARDS:
                    Sender.TakeItem(equipment, equipment_count)
                    reward = RECYCLE_REWARDS.get(equipment, {"gold": 1000})
                    gold_reward = reward["gold"] * equipment_count
                    # 给予金币
                    Sender.GiveItem("金币", gold_reward)
                    recycled_count += equipment_count
                    gold_given += gold_reward
                    # 发送每种装备的回收消息
                    try:
                        Sender.Connection.ReceiveChat("成功回收{}件装备，获得金币{}".format(equipment_count, gold_reward), MessageType.System)
                    except:
                        print("发送回收消息失败，但回收操作已完成")
                    print("已回收 {} 个 {}，给予 {} 金币".format(equipment_count, equipment, gold_reward))
                else:
                    skip_message = "[{}] 装备 {} 不在回收列表中，跳过".format(current_time.strftime("%Y-%m-%d %H:%M:%S"), equipment)
                    print(skip_message)
                    try:
                        with open("equipment_recycler.log", "a", encoding="utf-8") as f:
                            f.write(skip_message + "\n")
                    except:
                        pass
        except Exception as e:
            error_message = "[{}] 回收装备 {} 时发生错误: {}".format(current_time.strftime("%Y-%m-%d %H:%M:%S"), equipment, e)
            print(error_message)
            try:
                with open("equipment_recycler.log", "a", encoding="utf-8") as f:
                    f.write(error_message + "\n")
            except:
                pass
            continue  # 继续处理下一个武器
    
    if recycled_count > 0:
        # 更新回收时间
        current_timestamp = time.time()
        PlayerSetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME, current_timestamp)
        # 发送总计消息
        Sender.Connection.ReceiveChat("成功回收{}件装备，获得金币{}".format(recycled_count, gold_given), MessageType.System)
        
            # 记录回收完成日志
    success_message = "[{}] 玩家 {} 回收完成，总计回收 {} 件装备，给予 {} 金币".format(
        current_time.strftime("%Y-%m-%d %H:%M:%S"), player_name, recycled_count, gold_given)
    print(success_message)
    try:
        with open("weapon_recycler.log", "a", encoding="utf-8") as f:
            f.write(success_message + "\n")
    except:
        pass
    
    # 检查玩家包裹中是否有不在回收列表中的装备
    print("检查玩家包裹中是否有不在回收列表中的装备...")
    try:
        # 这里可以添加检查玩家包裹中所有装备的逻辑
        # 由于没有直接的API获取所有装备，我们只能通过已知的装备名称来检查
        print("无法直接检查所有装备，请手动确认装备名称")
    except Exception as e:
        print("检查包裹装备时发生错误: {}".format(e))
    
    if recycled_count > 0:
        # 更新回收时间
        current_timestamp = time.time()
        PlayerSetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME, current_timestamp)
        # 发送总计消息
        Sender.Connection.ReceiveChat("成功回收{}件装备，获得金币{}".format(recycled_count, gold_given), MessageType.System)
        
        # 记录回收完成日志
        success_message = "[{}] 玩家 {} 回收完成，总计回收 {} 件装备，给予 {} 金币".format(
            current_time.strftime("%Y-%m-%d %H:%M:%S"), player_name, recycled_count, gold_given)
        print(success_message)
        try:
            with open("equipment_recycler.log", "a", encoding="utf-8") as f:
                f.write(success_message + "\n")
        except:
            pass
    else:
        no_weapon_message = "[{}] 玩家 {} 没有可回收的武器".format(current_time.strftime("%Y-%m-%d %H:%M:%S"), player_name)
        print(no_weapon_message)
        try:
            with open("weapon_recycler.log", "a", encoding="utf-8") as f:
                f.write(no_weapon_message + "\n")
        except:
            pass

def TestRecycleForSender(Sender):
    """手动测试回收功能 - 只针对当前Sender"""
    print("TestRecycleForSender: 清空当前玩家的回收时间记录")
    try:
        PlayerSetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME, 0)
        print("TestRecycleForSender: 已清空玩家 {} 的回收时间记录".format(Sender.Character.CharacterName))
    except Exception as e:
        print("TestRecycleForSender: 清空回收时间记录失败: {}".format(e))
    
    print("TestRecycleForSender: 调用ExecuteEquipmentRecycleForSender")
    ExecuteEquipmentRecycleForSender(Sender)
    print("TestRecycleForSender: 执行完成")

def ImmediateRecycleForSender(Sender):
    """立即回收测试 - 忽略时间间隔，只针对当前Sender"""
    print("ImmediateRecycleForSender: 开始立即回收测试")
    
    # 临时禁用时间间隔检查
    try:
        original_time = PlayerGetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME)
        PlayerSetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME, 0)
        
        ExecuteEquipmentRecycleForSender(Sender)
        print("ImmediateRecycleForSender: 立即回收测试完成")
        
        # 恢复原来的时间记录
        PlayerSetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME, original_time)
    except Exception as e:
        print("ImmediateRecycleForSender: 立即回收测试失败: {}".format(e))

def TestMessageForSender(Sender):
    """测试消息发送功能 - 只针对当前Sender"""
    print("TestMessageForSender: 开始测试消息发送")
    try:
        Sender.Connection.ReceiveChat("测试消息发送功能", MessageType.System)
        print("测试消息发送成功给玩家: {}".format(Sender.Character.CharacterName))
    except Exception as e:
        print("测试消息发送失败给玩家: {} - {}".format(Sender.Character.CharacterName, e))

def GiveTestWeaponsForSender(Sender):
    """给当前Sender测试武器"""
    print("GiveTestWeaponsForSender: 开始给玩家测试武器")
    try:
        # 给玩家一些测试武器
        Sender.GiveItem("匕首", 1)
        Sender.GiveItem("井中月", 1)
        Sender.GiveItem("银蛇", 1)
        print("测试武器发放成功给玩家: {}".format(Sender.Character.CharacterName))
        Sender.Connection.ReceiveChat("已发放测试武器：匕首、井中月、银蛇各1个", MessageType.System)
        
        # 测试TakeItem功能
        print("测试TakeItem功能...")
        if Sender.GetItemCount("匕首") > 0:
            print("玩家有匕首，尝试回收1个")
            Sender.TakeItem("匕首", 1)
            print("TakeItem执行完成")
            Sender.Connection.ReceiveChat("测试：已回收1个匕首", MessageType.System)
        else:
            print("玩家没有匕首")
            Sender.Connection.ReceiveChat("测试：玩家没有匕首", MessageType.System)
            
    except Exception as e:
        print("测试武器发放失败给玩家: {} - {}".format(Sender.Character.CharacterName, e))
        Sender.Connection.ReceiveChat("测试武器发放失败: {}".format(str(e)), MessageType.System)

def TestPlayerVarsForSender(Sender):
    """测试玩家个人变量 - 只针对当前Sender"""
    print("TestPlayerVarsForSender: 开始测试玩家个人变量")
    try:
        player_name = Sender.Character.CharacterName
        # 设置不同的测试值
        test_value = hash(player_name) % 1000  # 根据玩家名生成不同的测试值
        PlayerSetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME, test_value)
        print("玩家 {} 设置变量值: {}".format(player_name, test_value))
        
        # 读取变量值
        read_value = PlayerGetV(Sender, GV_PLAYER_LAST_RECYCLE_TIME)
        print("玩家 {} 读取变量值: {}".format(player_name, read_value))
        
        if read_value == test_value:
            print("玩家 {} 个人变量测试成功".format(player_name))
            Sender.Connection.ReceiveChat("个人变量测试成功", MessageType.System)
        else:
            print("玩家 {} 个人变量测试失败，设置值: {}, 读取值: {}".format(player_name, test_value, read_value))
            Sender.Connection.ReceiveChat("个人变量测试失败", MessageType.System)
            
    except Exception as e:
        print("TestPlayerVarsForSender失败: {}".format(e))

# 类型为 Enums里的普通类
types = [ItemType.Nothing]
# 商品列表 '商品名称' 商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(yaodiangoodslist)

NpcEvent.add_listener(211,"OnClick",OnClick)	
#NpcEvent.add_listener(264,"OnClick",OnClick)
#NpcEvent.add_listener(140,"OnClick",OnClick)
