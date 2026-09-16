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
		if(PlayerGetV(Sender,BV_NQ_MAIN)==75):
			PlayerSetV(Sender,BV_NQ_MAIN,76)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """好像是个从乡下来的人帮助了王大人扩大了比奇商会的势力。
				由于原本拥有绝对优势的崔大夫的传奇商会受到了重大的打击，商权逐渐萎缩，没多久比奇地区的商权就将出现空白的。
				在比奇省中新加入比奇商会的商家除了书店和药剂师之外，还有精肉店、武器商、铁匠铺。
				传奇商会 主要核心成员是 布商 、 首饰店 、 杂货商 。
				我与其它的商家不同，因为我接受官府的统治保持中立，所以现在是两方势力对等的局面。
				[关闭:0]"""	
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==75):
			say = """欢迎。要不要试试你的手气？不过中不中奖我可不负责。
				
				[了解:1] 比奇城商界
				
				[关闭:0]"""
		else:
			say = """要我帮忙吗？
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(252,"OnClick",OnClick)
