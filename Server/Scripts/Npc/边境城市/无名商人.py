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
#红名
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单1
	elif (Menu == 1):
		say = """沃玛金牌是我从比奇省的王大人那儿购买的古董……啊，看来你就是把沃玛金牌卖给王大人的那个人吧！可是现在你又为什么需要它呢？
			
			[其实是为了把沃玛教主:2]"""
	elif (Menu == 2):
		say = """....
			嗯……原来是这样啊！虽然我能够理解，不过对我来说，这东西是为开辟贸易道路而精心准备的礼物，所以要我让步可不容易，你还是回去吧！
			
			[那你要怎么样才能把这个沃玛金牌还给我呢？:3]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==156):
			PlayerSetV(Sender,BV_NQ_MAIN,157)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """如果你一定要这个沃玛金牌的话，可以拿别的东西来和我交换。
				如果你能给我找来沃玛神殿中比沃玛金牌更有价值的古董的话我就会把这个东西还给你的！
				
				[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==162):
			if(Sender.GetItemCount('地狱神钟') < 1):
				say = """地狱神钟在哪儿啊？要是打算骗我的话，还是算了吧！
					
					[结束:0]"""
			else:
				Sender.TakeItem('地狱神钟',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """哇……这个看来确实是比沃玛金牌更有价值啊！好吧！成交！拿走沃玛金牌吧！ 
					
					[结束:0]"""
		else:
			SEnvir.Log("脚本警报：{} 任务序号变更使用封包挂".format(Sender.Character.CharacterName))
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==156):
			say = """来找我有什么事儿吗？
				
				[我是为要回沃玛金牌而来的！:1]"""
		elif(156 < PlayerGetV(Sender,BV_NQ_MAIN) < 161):
			say = """还没找来交换沃玛金牌的东西吗？离我要出发去沙漠的日子已经没有几天了，你还是尽快吧！ 
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==162):
			say = """带来可以代替沃玛金牌的东西了？
				
				[这个宝物是地狱神钟。:4]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==163):
			say = """您拿给我的神钟将会为开拓比奇省的未来派上大用场的！
				
				[结束:0]"""
		else:
			say = """我打算在沙漠地区寻找新的贸易道路，因此正在准备从那里横断沙漠。
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(287,"OnClick",OnClick)
