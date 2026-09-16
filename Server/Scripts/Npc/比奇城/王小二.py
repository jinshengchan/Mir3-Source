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
		say = """唉……这孩子可是我家唯一的独生女儿啊！
			在一次赶着牛群去远方的市场的途中，我妻子生下了这孩子后就离开了这个世上。以后就是只剩下我看着我们的丽灵，辛辛苦苦把她拉扯大，
			可是谁知道竟会发生了这种没有天理的事儿呢……
			
			[到底发生了什么事儿，能给我详细的说一下吗？:2]"""
	elif (Menu == 2):
		say = """我们丽灵的爱好是在附近骑马散步，那天丽灵也是像往常一样进了马厩骑上专门为她准备的浑身雪白的白马出去散步了。
			可是已经过了回来的时间，太阳都落山了丽灵却一直没有回来！
			正当我们无法再等，集合了村里的壮丁高举火把要去寻找的时候，丽灵却突然回来了，可是……
			就像你现在看到的这样，回来的只是个没有知觉的肉身了！
			
			[诊断过丽灵小姐为何变成这样的原因了吗？:3]"""
	elif (Menu == 3):
		say = """四处寻医求治，无论是什么医生大夫还是巫师、巫婆全都找过了，可还是一点儿用都没有。
			结果就只好根据剩下的一种传闻作为线索来请您来帮忙了。
			
			[能告诉我传闻的内容是什么吗？:4]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==116):
			PlayerSetV(Sender,BV_NQ_MAIN,117)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """不久之前开始流传一个关于专门摄取夜间外出的人魂魄的妖怪的传闻。
				虽然不敢确定，但是据说也有和我们的丽灵一样遇害的人。
				所以拜托您一定要调查出这传闻的真相，让我们的丽灵恢复到原来的样子啊！
				我相信这是名声显赫的您一定能解决的事情！
				
				[结束:0]"""
	elif (Menu == 5):
		if(Sender.GetItemCount('灵魂护卫') < 1):
			say = """什么也没有啊，不要骗人啊。。。
				
				[结束:0]"""
		else:
			say = """这是干什么用的东西啊？难道用这个葫芦瓶能治好丽灵的病？ 
				
				[请打开瓶塞看看吧！:6]"""
	elif (Menu == 6):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==124):
			Sender.TakeItem('灵魂护卫',1)
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """哦，好的……可是打开瓶塞干嘛……啊，这……
				丽灵啊！你醒过来了吗？哈哈哈……丽灵啊！
				真是太感谢您了！丽灵已经醒过来了！我的丽灵儿啊！这是我表示我谢意的一点东西，虽然不够丰厚，但希望你不要嫌弃，把这收下吧！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==116):
			say = """哦哦！
				您来了啊！久仰久仰啊！大概您也是已经听说了这件事儿才来的吧？ 
				
				[就是旁边的这位小姐吧？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==117):
			say = """如果我们丽灵没有发生这种事儿的话，我也不会对这种妖怪摄人魂魄的事儿十分在意……
				可是既然发生了这种事儿也觉得的确是有些诡异啦！先去找找在这附近住的人听听他们是怎么说的吧！
				没准儿能得到对调查这件事儿有帮助的情报呢！
				
				[结束:0]"""
		elif(117 < PlayerGetV(Sender,BV_NQ_MAIN) < 120):
			say = """丽灵现在还没能恢复意识呢！您还没能找到让这孩子清醒的办法吗？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==120):
			say = """如果我们丽灵没有发生这种事儿的话，我也不会对这种妖怪摄人魂魄的事儿十分在意……
				可是既然发生了这种事儿也觉得的确是有些诡异啦！先去找找在这附近住的人听听他们是怎么说的吧！
				没准儿能得到对调查这件事儿有帮助的情报呢！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==124):
			say = """丽灵现在还没能恢复意识呢！不知道您是否找到了让这孩子清醒的办法……
				
				[给他看灵魂护卫！:5]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) > 124):
			say = """谢谢你这么尽力帮助我们丽灵啊！
				
				[结束:0]"""
		else:
			say = """我是向比奇商会提供牛的王小二，你对牛感兴趣吗？ 
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(259,"OnClick",OnClick)
