# -*- coding: utf-8 -*-
#载入模块SYS
import sys
from datetime import datetime, timedelta
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import Server
import collections
import MapEvent
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Utils.TimeUtil import *
import Utils.ServerUtils as ServerUtils
from 主线任务奖励 import *
from 变量.默认变量 import *
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

#跳转菜单1
	if (Menu == 1):
		say = """看来你对当年的那段往事已经有所了解。
			不错，我就是被神舰害死的西部国王，这些年来我一直在寻找能够帮我消灭邪恶的神舰的勇士……
			你能来到我面前，已经初步证明了自己的勇气，但是这样还远远不够，你还要通过更严格的考验……苏醒吧，幽灵们！
			
			[喂，你等一下！不由分说就开打，这算是什么意思嘛！:2]"""
	elif (Menu == 2):
		say = """我暂时把你送到异界的一个空间吧。稍微等一下。
			
			[呃，好的:3]"""
	elif (Menu == 3):
		map = SEnvir.GetMap(262)               #开启地图
		if map.PlayerCount < 1:
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			Sender.Teleport(map,16,8)                        #传送进副本
			map.CreateMon(12,15,5,10102,2)
			PlayerSetV(Sender,BV_NQ_SJKILL,5003)
			PlayerSetV(Sender,BV_NQ_SJKILLMON,1)
			PlayerSetV(Sender,BV_NQ_SJKILLNUM,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			return
		else:
			say = """异界空间已人满为患，请稍微等一下。
			
			[重试:2]"""
	elif (Menu == 4):
		if (Sender.GetItemCount('魔灵牌') < 1):
			say = """你把刚刚还带在身上的魔灵牌弄到哪里去了？没有魔灵牌，不要指望我为你做任何事。
				
				[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_SJKILL,5005)
			Sender.TakeItem('魔灵牌',1)
			Sender.GiveItem('航海日志',1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """是的……他为我找来了这本航海日志，但是却没有能够帮助我完成消灭霸王教主的心愿。你将这本日志拿去吧，好好阅读它
				
				……你还拥有一次选择自己命运的机会，希望你好好把握。等到你真的决定要进行这段危险的冒险的时候再回来找我吧！
				
				[好的，我会慎重考虑的。:0]"""
	elif (Menu == 10):
		say = """你对我存在着敌心吗。能暂时听听我的话吗？
			
			[请说吧。:11]
			[跟来者不明的人也没有什么话可说:0]"""
	elif (Menu == 11):
		say = """这里面有异界的存在物。既然你已经来到这里了，我想你应该见到它们了。。。
			虽然它们是没有形体的无的存在，但也不能说是没有的存在物。
			还有它们是永远也不会死的存在。
			即使杀了它们也是在我们眼里只能看见盔甲。。
			
			[所以它们死了之后只有盔甲没有形体啊。。。:12]"""
	elif (Menu == 12):
		say = """只有关了异界的门它们才会重新回到异界啊。。
			你如果真要进这个地方的话，能听我的嘱托吗？
			
			[什么嘱托啊？:13]"""
	elif (Menu == 13):
		say = """这里面有叫霸王教主的异界的王。杀了他的话异界的力会暂时变弱的。
			以后的事情由我来做，你能帮我干掉他吗？
			要注意的是他不会死掉，只是暂时会隐藏自己的形体而已。。
			就是那个时候要关掉异界的门啊。你能帮我关异界的门吗？
			
			[我帮你吧。:14]
			[我不能信任你，那我就走了。。:0]"""
	elif (Menu == 14):
		if (Sender.GetItemCount('连环明珠') < 1):
			say = """你不能进到这里去。要进这儿的话需要我的力量。
				不过你没有 连环明珠 ，不能跟我联动啊。
				求到 连环明珠 后再来吧。
				
				[结束。:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_SJKILL,5012)
			PlayerSetV(Sender,BV_NQ_SJKILLMON,1)
			PlayerSetV(Sender,BV_NQ_SJKILLNUM,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """幸亏你带着连环明珠啊。
				连环明珠给我吧。我会突破困魔咒把你弄进去的。
				不过，已我的力量只能让你在困魔咒里面待24小时的时间而已。
				所以一定要那之前废了霸王教主的力才行。抓住霸王教主的话，弄到 霸王教主雕像 给我吧。
				那是霸王教主的力的一部分所以能用在关异界的门的时候。
				一定要杀了霸王教主，然后取他的雕像拿给我啊。。
				那，现在你就进到那个门里面吧。
				
				[好的，我会尽力的。:0]"""
	elif (Menu == 21):
		say = """从前面 49.43 的位置就可以出去。
		
		[关闭:0]"""
	elif (Menu == 22):
		say = """恭喜你获得每日跑船任务海量奖励。
		你可以获得50万经验，30万金币，30个万年雪霜。
		记得包裹要空出2-3个格子，否则无法领取到对应的奖励。
		
		[确定领取奖励:221]
		
		[我整理下包裹:0]"""
	elif (Menu == 221):
		PlayerSetV(Sender,GV_PLAYER_ZHOUPAOCHUANG,1)                  #赋值个人全局变量为2，表示已经领取奖励
		GiveExperience(Sender,5000000)     #给经验50万
		GiveGold(Sender,30000)           #给金币30万
		Sender.GiveItem("万年雪霜",30)    #给30个万年雪霜
		say = """恭喜你获得每日跑船任务海量奖励。

		[关闭:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,GV_PLAYER_ZHOUPAOCHUANG)==0):                #定义个人全局变量
			say = """我就是你要找的霸王幽灵……年轻人，我知道有一天你会出现在我面前的！
	
			[交谈:21]
			
			[领取每日跑船任务奖励:22]
			
			[关闭:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5002):
			say = """ 我就是你要找的霸王幽灵……年轻人，我知道有一天你会出现在我面前的！
				
				[你就是当年西部王国的国王？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5003):
			say = """我看你还没有准备好啊。再给你一次机会吧。
				
				[我证明给你看我的能力。:3]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5004):
			if Sender.GetItemCount('魔灵牌') < 1:
				say = """你的实力果然是非同一般啊！
					
					[关闭:0]"""
			else:
				say = """你的实力果然是非同一般……啊，你怎么会有这个魔灵牌？
					这是我送给上一个进入神舰的勇士的，为什么会在你这里？
					
					[上一个进入神舰的勇士？难道，你认识梅山侠的朋友？:4]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5007):
			PlayerSetV(Sender,BV_NQ_SJKILL,5008)
			PlayerSetV(Sender,BV_NQ_SJKILLMON,1)
			PlayerSetV(Sender,BV_NQ_SJKILLNUM,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """勇士啊，我知道你一定会再来的。啊，什么，你说以前那个帮助过我的勇士将遭到厄运，被变成霸王守卫！
				这样的话就相当麻烦了，必须杀死他才能让他的灵魂得到解脱！
				你说你下不去手么？为了彻底消灭霸王教主，有些时候我们必须做出牺牲，希望你能够为大局着想！
				
				[也只有这样了……唉:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5008):
			say = """为了彻底消灭霸王教主，有些时候我们必须做出牺牲，希望你能够为大局着想！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5009):
			PlayerSetV(Sender,BV_NQ_SJKILL,5010)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你终于将霸王守卫打败了，也令以前那个帮助过我的勇士能够得到解脱，希望你能够继承他的遗志，完成他未完成的事业阿！
				
				[我一定会努力的:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5010):
			say = """你终于将霸王守卫打败了，也令以前那个帮助过我的勇士能够得到解脱，希望你能够继承他的遗志，完成他未完成的事业阿！
				
				[我一定会努力的:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5011):
			say = """你想到这里来找什么？
				现在你要进去的这个地方是异界和现世共存的空间啊。
				
				我想阻止你进这个地方啊。。。
				
				[那么这个家伙是敌人吗。。:10]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5012):
			say = """一定要杀了霸王教主，然后取他的雕像拿给我啊。。
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5013):
			say = """你好像抓到霸王教主了。对吧。。。
				可是霸王教主雕像你放到哪里去了？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5014):
			if (Sender.GetItemCount('霸王教主雕像') < 1):
				say = """你好像抓到霸王教主了。对吧。。。
					可是霸王教主雕像你放到哪里去了？
					
					[结束:0]"""
			else:
				Sender.TakeItem('霸王教主雕像',1)
				PlayerSetV(Sender,BV_NQ_SJKILLNUM,0)
				MainQuestRewards(Sender,BV_NQ_SJKILL)
				Sender.Connection.ReceiveChat("任务日志更新：幽灵神舰任务完成！", MessageType.System)
				say = """你把霸王教主。。。
					是这样。你把雕像给我。还有请收下这个。。。
					我以前对那个 很大的“力”有着渴望。
					哪个战斗时使用了它，也因那个出来了神舰。
					现在要去关异界的门了。你解了我好久的宿愿啊。。
					谢谢你。。
					
					[结束:0]"""
		else:
			say = """我就是你要找的霸王幽灵……年轻人，我知道有一天你会出现在我面前的！
		
			[交谈:21]
			
			[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(201,"OnClick",OnClick)