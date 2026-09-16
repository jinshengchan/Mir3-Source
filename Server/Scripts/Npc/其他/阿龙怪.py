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
from Utils import ServerUtils
import MapEvent
from Utils.TimeUtil import *
import datetime
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
		say = """（哎呀，尸骨项链掉了..）
		
		[捡起项链。:11]"""
	elif (Menu == 11):
		Sender.TakeItem("尸骨项链",1)
		Sender.Connection.ReceiveChat("尸骨项链物品消失了。", MessageType.System)
		say = """不要用你肮脏的手摸我父亲的项链！
		
		<font color=\"0xffffff00\">你知道这个项链的意义吗？</font>
		<font color=\"0xffffff00\">倘若你真的是这个项链主人的儿子，</font>
		[那你现在就是跟你父亲的敌人混在一起！:12]"""
	elif (Menu == 12):
		say = """你又在说什么血口喷人的话？！想要祈求活命的话就应该跪
		下来求饶，你非但不如此，还反而说出亵渎我的教主大人的
		话？！
		哈！卑鄙之极啊！本来看在你武功不错的份上，准备让你死
		的像以个武士，看你现在的行径，算我高估了你这家伙！
		
		<font color=\"0xffffff00\">那么，为什么这个你父亲死亡当天消失了的项链会传到你的</font>
		<font color=\"0xffffff00\">手上？！把遗物全部收集起来了的你父亲的亲友，也没能找</font>
		<font color=\"0xffffff00\">到这个项链！所谓被比奇人杀害了的你父亲的项链，你肯定</font>
		<font color=\"0xffffff00\">是从诺玛统领那里拿到的，是不是？！你问过诺玛统领，他</font>
		[是怎么拿到这个项链的吗？:13]"""
	elif (Menu == 13):
		say = """呼呼呼呼... 你的相声讲得真不错。
		如果你的手上功夫也能像你的嘴皮子那么厉害的话，你保住
		这条命应该没什么问题吧。可惜的是，你的伸手好像不过如
		此！
		
		<font color=\"0xffffff00\">如果你不相信我的话，就去问叫拉贝卡的人，</font>
		[叫他告诉你真相吧！:14]"""
	elif (Menu == 14):
		say = """... 我会听你“最后的“劝告的。
		但是，当我去找拉贝卡的时候，你早已不在这个世界了。闭
		上你那罗嗦的嘴，吃我一刀吧！
		
		[阿龙怪进行攻击的一瞬间，击退护身符发出光芒。:15]"""
	elif (Menu == 15):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10013):
			PlayerSetV(Sender,BV_NQ_NMKILL,10014)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			Sender.TakeItem("击退护身符",1)
			Sender.Connection.ReceiveChat("击退护身符物品消失了。", MessageType.System)
			map = SEnvir.GetMap(567)
			cell = map.Cells[65,239]
			if cell.Objects != None:
				for object in reversed(cell.Objects):
					if object != None and object.Race == ObjectType.NPC:
						object.Die()
						object.Despawn()
			say = """（... 呼，差点出了大事故呢。占星术士给的护身符果然有
			效。可是，难道说阿龙怪的话是真的吗？如果他果真是勇士
			扎马尔的亲生儿子的话，究竟在扎马尔死后发生了什么事情
			呢？好像事情变得很复杂。。
			算了，先回去把迄今为止发生的事情告诉大法老夏柯吧。）"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	else:
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10013) and Sender.GetItemCount("击退护身符") > 0 and Sender.GetItemCount("尸骨项链") > 0:
			say = """呼呼，你的狗屎运还真的不得了呢。。 但是，那也是到此
			为止了！今天就跟你来个了断！
			
			[避开阿龙怪的一击。:1]"""
		else:
			say = """。。。。。。
			
			[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(373,"OnClick",OnClick)

