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
#红名判断
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单1
	elif (Menu == 1):
		if (Sender.GetItemCount('烧酒') < 1):
			say = """嗨！你这家伙!求别人办事情至少要应该有点诚意吧？
				真是个不明世礼的家伙啊！
				唔, 嗓子有点干… 想去酒店喝杯酒啊……咦？这个月的薪水已经全都喝酒花干净了啊！
				
				[结束:0]"""	
		else:
			say = """哼, 哼哼... 好香啊！...
				这位公子, 能不能给我喝口酒啊！
				
				[把酒瓶递给卫士。:2]
				[不把酒瓶递给卫士。:3]"""
	elif (Menu == 2):
		if (Sender.GetItemCount('烧酒') < 1):
			say = """难道已经喝光了吗？
				真扫兴！
				
				[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,66)
			Sender.TakeItem('烧酒',1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """哦~
				还是烧酒的味道棒啊！ 咕噜咕噜~ 呃~!
				正好口渴，真是非常感谢啊！
				
				[不知道你是否知道比奇省的历史……:4]"""
	elif (Menu == 3):
		say = """难道已经喝光了吗？
			真扫兴！
			
			[结束:0]"""
	elif (Menu == 4):
		say = """比奇省的历史？嗯…唔…
			说起比奇的由来这要追溯到几百年之前啦！
			比奇产生之前，西方有几个国家，由于被叫做内日和半兽人的怪物种族袭击一直都处于危险之中。
			处于威机之中的这几个国家停止了相互之间的战争，协力与怪物们抗争，最后终于赶走了怪物们，但是也全部受到了重创，怪物们的威胁仍然没有完全解除。
			于是这几个国家协力出兵去讨伐怪物们的根据地，那个地方就是比奇地区！
			这些够了吧！
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==65):
			say = """要我帮忙吗？
				
				[询问比奇省的历史:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==66):
			say = """说起比奇的由来这要追溯到几百年之前啦！
				比奇产生之前，西方有几个国家，由于被叫做内日和半兽人的怪物种族袭击一直都处于危险之中。
				处于威机之中的这几个国家停止了相互之间的战争，协力与怪物们抗争，最后终于赶走了怪物们，但是也全部受到了重创，怪物们的威胁仍然没有完全解除。
				于是这几个国家协力出兵去讨伐怪物们的根据地，那个地方就是比奇地区！
				这些够了吧！
				
				[结束:0]"""
		else:
			say = """要我帮忙吗？
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(256,"OnClick",OnClick)
