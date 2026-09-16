# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import random
from Defines import *
import MapEvent
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
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
		say = """嘿嘿嘿。。
			不害怕，找到地牢空间来了。
			你也有可能成为这个样子，不害怕吗？
			
			[当然恐惧。:11]"""
	elif (Menu == 11):
		say = """很奇怪。。。
			感受到了<font color=\"0xff00ff00\">命运之手的召唤</font>，我已经不是我了。
			哦。。好象凭借谁的法力来到这里，在发生更大的事情之前快些离开这里。
			或者死了，或者成为连死都不行的样子。
			
			[死一点也不害怕，害怕的是没有实现自己的意愿。:12]"""
	elif (Menu == 12):
		say = """。。。
			现在知道了。平静的心脏在怦怦地跳动。。。
			感觉到惊心动魄的兴奋。啊，我希望的东西就在这里。
			我感觉到了<font color=\"0xff00ff00\">战斗的宿命</font>
			好的，我将按照指示做。
			但是，有一个<font color=\"0xff00ff00\">条件</font>。
			
			[什么条件？:13]"""
	elif (Menu == 13):
		say = """我是战士。
			认为名义是最高的价值。。。同时我知道的只有这个。
			哦，条件很简单。<font color=\"0xff00ff00\">和我搏斗，战胜我，使我屈服。</font>
			如何？打吗？
			
			[好的，现在当场开始吧。:14]
			[准备好了，再来！:15]"""
	elif (Menu == 14):
		say = """好的。接受<font color=\"0xff00ff00\">你的挑战</font>。
			那么现在一起去对决场吧。。。
			
			[移动:16]"""
	elif (Menu == 15):
		say = """软弱的人。。。随你的便。
			我要在这个地方等到何时？
			
			[首先逃出这个地方，重新回到清明子那儿。。。:17]"""
	elif (Menu == 16):
		map = Server.Envir.SEnvir.CreateMap(526)                         #开启副本地图（地图ID）
		
		DelayTeleport(Sender,map,1,23,24) #延迟1秒传送进副本
		
		PlayerSetV(Sender,GV_Taoist_SummonSkeleton,2)
		return
	elif (Menu == 17):
		Sender.TeleportByMapIndex(7,407,122)
		return
	elif (Menu == 18):
		if (GetInventoryCount(Sender) >= 1): #格子大于等于1格
			PlayerSetV(Sender,GV_Taoist_SummonSkeleton,4)
			Sender.GiveItem("幻影玉珠",1)
			say = """（虽然很辛苦，但是能拥有这么好的伙伴真是很开心啊。。。）
			
			[回去:19]"""
		else:
			say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 19):
		Sender.TeleportByMapIndex(9,12,11)
		return
	else:
		if (PlayerGetV(Sender,GV_Taoist_SummonSkeleton)==3):
			say = """金属相碰飞溅的火花，呼呼的喘气声，还有战场上面的血腥味
				儿。。。但是即使在极限的状况下，我也无法放弃的名义。。。
				这是给从和我的战斗中取得胜利的你的<font color=\"0xff00ff00\">礼物</font>。谢谢使我想起忘
				却的东西。<font color=\"0xff00ff00\">现在跟随着你重新回到战场</font>。
				如果需要的帮助，请随时联系。
				
				[首先要离开这个地方。。。:18]"""
		else:
			say = """听见喊声了哦。
				叫我的声音。。。
				你是谁?
				
				[为了寻找守护灵而来。:1]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick1(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	say = """哈哈哈。。像你这种家伙还是看不到我原来的样子。
		在哪儿了。。我要休息的地方。。。
		
		[不知道为什么，好象不是人。:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick2(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	say = """啊！别问！什么都别问！
		
		[很奇怪。。。:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick3(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	if (Menu == 31):
		select = random.randint(0,1)
		if select > 0:
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			map.CreateMon(23,25,5,100236,2)
			say = """愚笨的人，你讲的话使人后悔。
				
				[什么意义？这种。。。:0]"""
		else:
			say = """愚笨的人，要知道今天运气很好。
				
				[结束:0]"""
	else:
		say = """哈哈哈。。像你这种家伙还是看不到我原来的样子。
			长久战斗的日子。但是我们得到的东西什么都没有。。。
			嗯？我正在说什么话？
			
			[哈哈哈，象你长得一样竟说傻话儿...:31]
			[好象很长时间一个人了...不幸的灵魂。:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick4(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	say = """不要随便进行随机传送。
		没有做好，将成为我现在的样子哟。哈哈哈
		
		[什么话儿？:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick5(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	if (Menu == 51):
		select = random.randint(0,1)
		if select > 0:
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			map.CreateMon(25,23,5,100236,2)
			say = """果真如此吗？哈哈哈。。。
				
				[这种。。。阴险的家伙。:0]"""
		else:
			say = """要知道今天运气很好。
				
				[结束:0]"""
	else:
		say = """你现在还有带有活人的痕迹，但是马上就会变成我们的样子哟。
			
			[别说假话。根本不可能的事儿。。。:51]
			[不幸的灵魂啊。。。别花心思！:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick6(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	say = """我是自豪的远征队的队员！
		这些半兽人，都给我猛扑上。
		
		[说以前是远征队的:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick7(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	if (Menu == 71):
		if map.MonsterCount > 0:
			map.ClearAllMonsters()
		map.CreateMon(10,24,5,100236,2)
		say = """唐突的家伙，一点也不考虑别人的处境。。。
			
			[出现了这种。。。失误:0]"""
	else:
		say = """想回故乡。。。
		
		[哈哈哈，忘记了家乡在哪儿？:71]
		[快点回家乡吧。。。:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(334,"OnClick",OnClick)
NpcEvent.add_listener(335,"OnClick",OnClick1)
NpcEvent.add_listener(336,"OnClick",OnClick2)
NpcEvent.add_listener(337,"OnClick",OnClick3)
NpcEvent.add_listener(338,"OnClick",OnClick4)
NpcEvent.add_listener(339,"OnClick",OnClick5)
NpcEvent.add_listener(340,"OnClick",OnClick6)
NpcEvent.add_listener(341,"OnClick",OnClick7)