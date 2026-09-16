# -*- coding: utf-8 -*-
#载入模块SYS引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import 额外奖励 as ExtraRewards
from 变量.默认变量 import *
from 变量.任务杀怪 import *
import Utils.ServerUtils as ServerUtils
import random
import Server.Envir.SEnvir as SEnvir
from Utils.PlayerUtils import *
from string import digits
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
	bg = {}
	font={}
	Dict={}
	
#万事通每日任务次数限制
	DailyTask_Limit = 3
#红名
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
	elif (Menu == 1):
		bg['file']=2									#定义聊天框背景(该字段有值则不适用url,且和idx一起存在.否则不生效)
		bg['idx']=151									#图库图片序号
		bg['center']=1									#是否居中显示(0左上角显示,1居中显示)
		bg['title'] = " "					 #自定义标签内容 只支持最普通文字
		bg['close'] = 1
		bg['drag'] = 1
		Dict['bg'] = bg
		say = TaskList(Sender,DailyTask_Limit)
	elif (Menu == 10):
		return
	elif (Menu == 21):
		if PlayerGetV(Sender,BV_NUM_DAILYTASK) < DailyTask_Limit:
			bg['file']=2									#定义聊天框背景(该字段有值则不适用url,且和idx一起存在.否则不生效)
			bg['idx']=150									#图库图片序号
			bg['center']=1									#是否居中显示(0左上角显示,1居中显示)
			bg['title'] = " "					 #自定义标签内容 只支持最普通文字
			Dict['bg'] = bg
			say = CompleteTask(Sender)
		else:
			SEnvir.Log("脚本警报：{} 使用封包挂".format(Sender.Character.CharacterName))
	elif (Menu == 22):
		bg['file']=2									#定义聊天框背景(该字段有值则不适用url,且和idx一起存在.否则不生效)
		bg['idx']=150									#图库图片序号
		bg['center']=1									#是否居中显示(0左上角显示,1居中显示)
		bg['title'] = " "					 #自定义标签内容 只支持最普通文字
		Dict['bg'] = bg
		if(PlayerGetV(Sender,BV_NUM_DAILYTASK) >= DailyTask_Limit):
			say = """
			
			您已经完成今天的任务，无法帮您重置。

<btn file=3 idx=424 x=85 y=123 data=1 mirbtntype=4 />"""
		else:
			Gold_Need = (Sender.Level - 20) * 5000
			if Sender.Gold < Gold_Need:
				say = """
				
				您的金币不足 {} ，无法帮您重置万事通任务。
			

<btn file=3 idx=424 x=85 y=123 data=1 mirbtntype=4 />""".format(Gold_Need)
			else:
				PlayerSetV(Sender,BV_QT_TODAY,0)
				PlayerSetV(Sender,BV_QT_KILLMON,0)
				PlayerSetV(Sender,BV_QT_KILLNUM,0)
				SubGold(Sender,Gold_Need)
				say = """
				
				帮您重置了万事通任务，消耗 {} 金币。

<btn file=3 idx=424 x=85 y=123 data=1 mirbtntype=4 />""".format(Gold_Need)

	#主菜单
	elif(Sender.Level < 22):
		say = """22级以上每天可领取 <font color=\"0xff00ff00\"> {} </font> 次万事通随机每日任务，完成任务可获得丰厚的经验金币以及道具奖励。
<font color=\"0xff00ff00\">每次完成任务都可获得额外奖励。</font> 

你还不够强大，当你等级达到22级时再来吧。

[结束:0]""".format(DailyTask_Limit)
	elif (Sender.Level > 64):
		say = """你的实力已经不需要获取每日任务。
		
		[结束:0]"""
	elif PlayerGetV(Sender,BV_NUM_DAILYTASK) < DailyTask_Limit:
		bg['file']=2									#定义聊天框背景(该字段有值则不适用url,且和idx一起存在.否则不生效)
		bg['idx']=151									#图库图片序号
		bg['center']=1									#是否居中显示(0左上角显示,1居中显示)
		bg['title'] = " "					 #自定义标签内容 只支持最普通文字
		bg['close'] = 1
		bg['drag'] = 1
		Dict['bg'] = bg
		say = TaskList(Sender,DailyTask_Limit)
	else:
		say = """22级以上每天可领取 <font color=\"0xff00ff00\"> {} </font> 次万事通随机每日任务，完成任务可获得丰厚的经验金币以及道具奖励。
<font color=\"0xff00ff00\">每次完成任务都可获得额外奖励。</font> 

[查看万事通任务:1]

[结束:0]""".format(DailyTask_Limit)

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def TaskList(Sender,DailyTask_Limit):
	a = ''
	b = ''
	c = ''
	d = ''
	h = ''
	image = 1
	if PlayerGetV(Sender,BV_NUM_DAILYTASK) < DailyTask_Limit:                         #检测已领取次数
		if(PlayerGetV(Sender,BV_QT_TODAY)==0):
			num_dt = PlayerGetV(Sender,BV_NUM_DAILYTASK) + 1
			TaskNumber = GetDailyTaskNumber(Sender)
			DailyTaskList = GetDailyTaskList(Sender,TaskNumber)
			if '任务道具' in DailyTaskList.keys():
				require_itemlist = DailyTaskList.get('任务道具')
				for x in require_itemlist:
					a = x
					b = require_itemlist.get(a)
			if '任务怪物' in DailyTaskList.keys():
				DailyMonList = []
				for mon in DailyTaskList.get('任务怪物'):
					mon = mon.translate(None,digits) #怪物名去除数字后缀
					DailyMonList.append(mon)
					c = '、'.join(DailyMonList)
				d = DailyTaskList.get('杀怪数量')
				PlayerSetV(Sender,BV_QT_KILLMON,1)
				PlayerSetV(Sender,BV_QT_KILLNUM,0)
			e = ((Sender.Level - 20) * 50000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * ((Sender.Level - 20) * 20000))
			f = ((Sender.Level - 20) * 20000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * (Sender.Level - 20) * 5000)
			g = (Sender.Level - 20) // 2
			randomitemlist = DailyTaskList.get('随机奖励')
			for y in randomitemlist:
				itemname = y
			i = randomitemlist.get(itemname)
			item = SEnvir.GetItemInfo(itemname)
			h = itemname
			if item is None:
				SEnvir.Log("数据库不存在{}道具".format(itemname))
			image = item.Image
			e1 = e * Local_ExpRewards_Rate
			f1 = f * Local_GoldRewards_Rate
			g1 = g * Local_PresRewards_Rate
			Gold_Need = (Sender.Level - 20) * 5000
			return"""<font size=10 color=0xffffff00 x=96 y=23 >{}</font> <font size=10 color=0xffffff00 x=255 y=23 >{}</font>
<font size=9 color=0xffffff00 x=77 y=87 >{}</font> <font size=9 color=0xffffff00 x=280 y=87 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=108 >{}</font> <font size=9 color=0xffffff00 x=270 y=108 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=179 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=200 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=221 >{}</font> 
<btn file=3 idx=1222 x=293 y=328 data=10 mirbtntype=3 />
<img file=9 idx={} item={} x=200 y=270 /> <font size=9 color=0xffffff00 x=283 y=280 >{}</font> 
















[提交任务:21]      [重置任务:22]    （收取 {} 金币）""".format(DailyTask_Limit,num_dt,a,b,c,d,e1,f1,g1,image,h,i,Gold_Need)
		else:
			num_dt = PlayerGetV(Sender,BV_NUM_DAILYTASK) + 1
			TaskNumber = PlayerGetV(Sender,BV_QT_TODAY)
			kn = PlayerGetV(Sender,BV_QT_KILLNUM)
			tn = PlayerGetV(Sender,BV_QT_TODAY)
			DailyTaskList = GetDailyTaskList(Sender,TaskNumber)
			if '任务道具' in DailyTaskList.keys():
				require_itemlist = DailyTaskList.get('任务道具')
				for x in require_itemlist:
					a = x
					b = require_itemlist.get(a)
			if '任务怪物' in DailyTaskList.keys():
				DailyMonList = []
				for mon in DailyTaskList.get('任务怪物'):
					mon = mon.translate(None,digits)  #怪物名去除数字后缀
					DailyMonList.append(mon)
					c = '、'.join(DailyMonList)
				d = DailyTaskList.get('杀怪数量')
			e = ((Sender.Level - 20) * 50000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * ((Sender.Level - 20) * 20000))
			f = ((Sender.Level - 20) * 20000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * (Sender.Level - 20) * 5000)
			g = (Sender.Level - 20) // 2
			randomitemlist = DailyTaskList.get('随机奖励')
			for y in randomitemlist:
				itemname = y
			i = randomitemlist.get(itemname)
			item = SEnvir.GetItemInfo(itemname)
			h = itemname
			if item is None:
				SEnvir.Log("数据库不存在{}道具".format(itemname))
			image = item.Image
			e1 = e * Local_ExpRewards_Rate
			f1 = f * Local_GoldRewards_Rate
			g1 = g * Local_PresRewards_Rate
			Gold_Need = (Sender.Level - 20) * 5000
			return"""<font size=10 color=0xffffff00 x=96 y=23 >{}</font> <font size=10 color=0xffffff00 x=255 y=23 >{}</font>
<font size=9 color=0xffffff00 x=77 y=87 >{}</font> <font size=9 color=0xffffff00 x=280 y=87 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=108 >{}</font> <font size=9 color=0xffffff00 x=260 y=108 >{} / {}</font> 
<font size=9 color=0xffffff00 x=77 y=179 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=200 >{}</font> 
<font size=9 color=0xffffff00 x=77 y=221 >{}</font> 
<btn file=3 idx=1222 x=293 y=328 data=10 mirbtntype=3 />
<img file=9 idx={} item={} x=200 y=270 /> <font size=9 color=0xffffff00 x=283 y=280 >{}</font> 
















[提交任务:21]      [重置任务:22]    （收取 {} 金币）""".format(DailyTask_Limit,num_dt,a,b,c,kn,d,e1,f1,g1,image,h,i,Gold_Need)
	else:
		Sender.Connection.ReceiveChat("今天的任务已全部完成。", MessageType.System)
		return ''

def CompleteTask(Sender):
	a = ''
	b = ''
	c = ''
	d = ''
	h = ''
	TaskNumber = PlayerGetV(Sender,BV_QT_TODAY)
	DailyTaskList = GetDailyTaskList(Sender,TaskNumber)
	if '任务道具' in DailyTaskList.keys():
		require_itemlist = DailyTaskList.get('任务道具')
		for x in require_itemlist:
			a = x
			b = require_itemlist.get(a)
	if '任务怪物' in DailyTaskList.keys():
		DailyMonList = []
		for mon in DailyTaskList.get('任务怪物'):
			DailyMonList.append(mon)
			c = '、'.join(DailyMonList)
		d = DailyTaskList.get('杀怪数量')
	e = ((Sender.Level - 20) * 50000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * ((Sender.Level - 20) * 20000))
	f = ((Sender.Level - 20) * 20000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * (Sender.Level - 20) * 5000)
	g = (Sender.Level - 20) // 2
	randomitemlist = DailyTaskList.get('随机奖励')
	for y in randomitemlist:
		h = y
	i = randomitemlist.get(h)
	j = DailyTaskList.get('随机参数')
	e1 = e * Local_ExpRewards_Rate
	f1 = f * Local_GoldRewards_Rate
	g1 = g * Local_PresRewards_Rate
	e1 = e * Local_ExpRewards_Rate
	f1 = f * Local_GoldRewards_Rate
	g1 = g * Local_PresRewards_Rate
	if c:
		if(PlayerGetV(Sender,BV_QT_KILLNUM) < d):
			return"""
			
			您还没有完成杀怪目标，请完成以后再来吧。

<btn file=3 idx=970 x=85 y=123 data=99 mirbtntype=4 />"""
	if a:
		if(Sender.GetItemCount(a)<b):
			return"""
			
			您没有收集够 {} 个 {}，检查一下再过来交差吧。

<btn file=3 idx=970 x=85 y=123 data=99 mirbtntype=4 />""".format(b,a)
		else:
			Sender.TakeItem(a,b)
	
	GiveExperience(Sender,e1)
	GiveGold(Sender,f1)
	GivePrestige(Sender,g1)
	PlayerSetV(Sender,BV_QT_TODAY,0)
	PlayerSetV(Sender,BV_QT_KILLMON,0)
	PlayerSetV(Sender,BV_QT_KILLNUM,0)
	num_dt = PlayerGetV(Sender,BV_NUM_DAILYTASK) + 1
	PlayerSetV(Sender,BV_NUM_DAILYTASK,num_dt)
	Sender.Connection.ReceiveChat("得到 {} 金币".format(f1), MessageType.System)
	Sender.Connection.ReceiveChat("得到 {} 声望".format(g1), MessageType.System)
	ExtraRewards.OnTaskComplete(Sender,num_dt)
	select = random.randint(0,10000)
	if select < j:
		if Sender.GiveItem(h,i):
			ServerUtils.SendMsgToAll('万事通任务：{} 完成任务，获得 {} 个 {} ！'.format(Sender.Name,i,h),MessageType.System)
			return"""
			
			感谢您及时完成任务。
奖励您经验：{}，金币{}，声望{}。
额外奖励您 {} {} 个。
<btn file=3 idx=424 x=85 y=123 data=1 mirbtntype=4 />""".format(e1,f1,g1,h,i)
		else:
			return"""
			
			您的包裹空间不足。

无法获得随机奖励的 {} 。

<btn file=3 idx=424 x=85 y=123 data=1 mirbtntype=4 />""".format(h)
	else:
		return"""
		
		感谢您及时完成任务。

奖励您经验：{}，金币{}，声望{}。
<btn file=3 idx=424 x=85 y=123 data=1 mirbtntype=4 />""".format(e1,f1,g1)


NpcEvent.add_listener(295,"OnClick",OnClick)