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
		say = """哪里只是传闻而已啊？这可是我亲眼所见的！
			
			[您能给我详细地讲一下吗？:2]"""		
	elif (Menu == 2):
		say = """那是大概在一个月之前的事儿了！
			凌晨的时候我要去外面小解，偶然看见什么东西从墙角闪过。
			正好那天没出月亮黑漆漆的我没能看清楚，但好像是个男子的模样。
			我还以为是个贼就没出声儿，原地不动的站在那儿看，只见他解开腰间的一个好像是葫芦瓶模样的东西拿在手里轻轻摇晃，嘴里还念念有词的不知在嘟囔着什么。
			看了一会儿我觉得他行为异常刚想出声赶走他，那个家伙向我的呆的地方~嚯得一下，
			被他眼光盯到的那一瞬间我一下子喘不过气来，出了一身冷汗，
			可是就在我想“这下子可完蛋了”的那一瞬间，那个妖怪就不知道消失到哪儿去了！
			
			[那后来怎么样了呢？:3]"""		
	elif (Menu == 3):
		say = """唉！甭提了！那家伙消失之后我身上就渐渐起了好多绿色的斑点，而且开始发高烧、吐血……
			好不容易回到卧室吃了从爷爷那里传下来的秘药才算捡回了这条性命。
			真的……我还以为死定了呢！就那么看了我一眼我就好像中了剧毒，看来那妖怪真是神通广大啊！
			
			[这好像是道士的招数啊！:4]"""		
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==118):
			PlayerSetV(Sender,BV_NQ_MAIN,119)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """道士？世上哪有对无辜的人用毒术的道士啊？
				这一定是害人的妖怪没错儿！唉……不会有错儿的！
				
				[结束:0]"""		
	elif (Menu == 5):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==123):
			PlayerSetV(Sender,BV_NQ_MAIN,124)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """嗯！没错，这个就是那妖怪带着的葫芦瓶。那人是摄人魂魄的妖怪，可是这个东西怎么又带在您身上呢？
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==118):
			say = """嗯？你说什么？啊，你说王小姐啊？王小二正伤心着呢。还不是因为她女儿……
				
				[您听说过关于那个妖怪摄人魂魄的传闻吗？:1]"""
		elif(118 < PlayerGetV(Sender,BV_NQ_MAIN) < 123):
			say = """现在想来还挺想知道那个妖怪带着的 葫芦瓶 到底是用来做什么的东西……
				不过可不再想和那个妖怪碰面了。
				可不能因为好奇心而丧了性命啊！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==123):
			if(Sender.GetItemCount('灵魂护卫') < 1):
				say = """现在想来还挺想知道那个妖怪带着的 葫芦瓶 到底是用来做什么的东西……
					不过可不再想和那个妖怪碰面了。
					可不能因为好奇心而丧了性命啊！
					
					[结束:0]"""
			else:
				say = """嗯？那个葫芦瓶！能给我看一下那个葫芦瓶吗？
					
					[给他看灵魂护卫。:5]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==124):
			say = """不知道这个葫芦瓶里有没有医治王小姐的办法？
				
				[结束:0]"""
		else:
			say = """今天去哪里呢？这附近没有什么值得骑马逛逛的好地方吗？
			
			[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(261,"OnClick",OnClick)
