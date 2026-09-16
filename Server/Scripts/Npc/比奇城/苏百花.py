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
		say = """你说那个人姓洪名气霖？啊…… 他还活着啊！
			自从流离失散之后，虽然觉得很难活下去……  但一直认为只要还活着的话总会有一天能见上一面的，所以一直在这儿苦苦等候……终于没有白等啊~！
			拜托侠客您一件事！请您把这个玉指环拿给他，告诉他苏白花还活着！并告诉他如果他依然还爱我的话，就让他来这里接我吧！
			
			[为什么不直接去找他呢？:2]
			[好的:3]"""
	elif (Menu == 2):
		say = """只能这样啊！万一他已经有了别的妻子，我就会妨碍他们的！
			所以请你替我去打听一下他的心意啊！ 
			
			[好的，我去帮你打听:3]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 47):
			PlayerSetV(Sender,BV_NQ_MAIN,48)
			Sender.TakeItem('气霖证书',1)
			Sender.GiveItem('玉指环',1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """那么请你一定要把我给你的这个玉指环带给他看，并探查一下他的心意，多多拜托您了！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==47):
			if (Sender.GetItemCount('气霖证书') < 1):
				say = """要我帮忙吗？
					
					[结束:0]"""
			else:
				say = """来找我有什么事儿吗？ 哦？ 这证书的字体？！
					
					[是您见过的字体吗？:1]"""		
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==48):
			say = """真是太感谢了！
				
				[结束:0]"""
		else:
			say = """要我帮忙吗？
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(262,"OnClick",OnClick)
