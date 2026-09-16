# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
import collections
clr.AddReference("Library")
from Library import *
import NpcEvent
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
	Dict={}
	
	if(Menu == 1):
		Sender.TeleportByMapIndex(103,31,373)
		return
	elif (Menu == 2):
		say = """昨天身体状态还可以，就带着鹤嘴锄进了矿山。差不多采完了近处质量较好的矿石后又进入了矿坑深处。像往常一样用鹤嘴锄采矿的时候，却不知从哪儿传来了奇怪的声音！\
			最开始的时候没太在意，可是过了一会却有一股什么腐烂了的恶臭扑鼻而来！ 
			看来的确有点什么不对劲儿，于是停下了手里的活儿进入矿山更深处一看！
			
			[腐烂的恶臭……啊……:3]"""		
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==137):
			PlayerSetV(Sender,BV_NQ_MAIN,138)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """天哪！原来里面是有好多尸体在走来走去的！
				那些家伙一看到我就发出了奇怪的声音向我扑了过来！有用独腿跳着来的，还有干脆爬着来的，还有闪着奇怪的火光的！ 
				我扔下手中的鹤嘴锄拼了命才能逃了出来！
				但是这种话谁都不会相信的，所以直到今天才第一次跟您说！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==137):
			say = """您就是治好珍珍的病的那个年轻人？
				在这么危急的情况下有像您这样的人来到我们村子，真是万幸啊！
				
				[有什么事儿吗？:2]"""
		else:
			say = """到矿石采矿可以挣钱，你也想挣大钱？那就准备好鹤嘴锄去
				矿山吧。如果你不知道怎么去矿山，我可以把你移动过去。
				
				[移动至矿山:1]
				[结束:0]"""
			
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(282,"OnClick",OnClick)