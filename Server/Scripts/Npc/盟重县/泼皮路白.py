# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import random
from 主线任务奖励 import *
clr.AddReference('System')
from System import DateTime
import System
s1 = clr.Reference[System.Object]()
from Defines import *
import Server
import unicodedata
from Utils import ServerUtils
from Npc import *
from Utils.PlayerUtils import *
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from datetime import datetime   #增加时间判断
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
ALLOWED_ITEM_TYPES = [ItemType.Torch]

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	if (Menu == 1):
		say = """（好像是我要找的村子人，没有任何感兴趣的哟。好像在我身找到什么的样子？有什么东西落了吗？）
		
		[结束:0]"""
	elif (Menu == 2):
		say = """如果是那样。。。
		
		[我受大悲圣僧的委托到村庄来参加祭祀，村庄在哪儿？:3]"""
	elif (Menu == 3):
		say = """大悲圣僧。。。？
		不知道他是谁。 一会儿，请上香。。。
		啊，这么看来年轻人是武士吗？
		千万要救救我们吧！
		
		[虽然会使用些剑。。。到底是什么事情？:4]"""
	elif (Menu == 4):
		say = """我们都是生活在<font color=\"0xff00ff00\">百娥村</font>的人。到不久前为止，我们村子还是一
		个安静适合生活的好地方。但是自从<font color=\"0xff00ff00\">原因不明的传染病</font>开始流
		行，个把月间不论老幼都吐血而死。
		村子议员认为生病的原因是水脏。为了确认这个事实，村子里
		还没有生病的几个人到村子里流淌着的<font color=\"0xff00ff00\">水源所在的洞窟</font>去了。
		但是只有一个人从那个地方回来了。他满身是疮地回来了，断
		气之前说<font color=\"0xff00ff00\">蜈蚣</font>们占据了水源，污染了水。
		
		[没有向官吏请求帮助吗？:5]"""
	elif (Menu == 5):
		say = """求了！请求了！！
		但是官吏们堵上了流向村子的水流，村子反而被隔离了。我们
		村子的人们得不到任何帮助，正在死去。
		我们无法在看人们就这样死去！如果得不到官吏的帮助，即使
		凭借我们的力量也要除掉蜈蚣们！！因此体格健壮的人们拿着
		镰刀和镐到蜈蚣所在的洞窟去了。
		但是仅凭借我们自己的力量无论如何也到达不了水源。千万帮
		助我们<font color=\"0xff00ff00\">处理那些怪物</font>，这样衷肯地拜托你。。。
		
		[知道了，我去那个洞窟看看。:6]
		[非常对不起,也许是非常危险的事情。:51]"""
	elif (Menu == 51):
		say = """不行。。。
		等了很久，又等了很久。。。
		如果说这是我们的命运，只有寻求其它的<font color=\"0xff00ff00\">救援之手</font>。。。
		那么请小心走好！
		
		[结束:0]"""
	elif (Menu == 6):
		PlayerSetV(Sender,GV_Taoist_MassHeal,2)
		say = """谢谢！非常感谢！
		蜈蚣们栖息在深而且阴森森的叫做绝命的洞窟中。蜈蚣围剿队
		最后被目击的地方在<font color=\"0xff00ff00\">绝命谷最深地区西南方的某个地方</font>。
		那个地方正是这个村子水源的所在地，但是现在成了蜈蚣们藏
		身处的<font color=\"0xff00ff00\">洞窟入口</font>。有可能进到那里边以后就中断了消息。
		
		[在蜈蚣洞窟中要做什么呢？:7]"""
	elif (Menu == 7):
		say = """蜈蚣洞窟非常深，由弯弯曲曲的洞窟连接而成。进到入口后，
		走很长时间，在中间出现一个宽敞的房间；然后沿着弯弯曲曲
		的通路走很长时间后就到达了我们这个地方的水源地<font color=\"0xff00ff00\">地下莲池</font>
		<font color=\"0xff00ff00\">的宽敞空间</font>。
		首先到那个地方为止，即使有什么事情都要一边小心身体一边
		前进。因为不知道在中间会遇到什么突变。
		在水源地有一个污染水源叫做<font color=\"0xff00ff00\">沃毒蜈蚣</font>的家伙，<font color=\"0xff00ff00\">只要把这个家</font>
		<font color=\"0xff00ff00\">伙处理了就解决了所有的问题</font>。
		
		[处理了这个家伙就可以了噢。那么我走了:0]"""
	elif (Menu == 8):
		PlayerSetV(Sender,GV_Taoist_MassHeal,4)
		Sender.TeleportByMapIndex(50,322,109)
		return

#主菜单
	else:
		if (PlayerGetV(Sender,GV_Taoist_MassHeal)==1):
			hour = datetime.now().hour ###当前小时datetime.now().hour 范围是0-23
			if (hour >= 0 and hour < 5) or (hour >= 12 and hour < 17): ###晚上0-5点 或 中午12-17点之间
				if (Sender.GetItemCount("威魂深怨护身符") > 0):
					say = """陌生的年青人, 什么事情？
					年轻的绅士为什么拿着<font color=\"0xff00ff00\">奇怪的护身符</font>走来走去？
					
					[有个问题想请教一下。是生活在这个地方的人吗？:2]"""
				else:
					say = """陌生的年青人，什么事情？
					晚上的天气很冷，还不快赶路？
					
					[奇异的人。。。:1]"""
			else:
				say = """现在是大白天。。
				很刺眼，什么都看不见。。。
				
				[奇异的人。。。:0]"""
		elif (PlayerGetV(Sender,GV_Taoist_MassHeal)==2):
			say = """我们在这儿等着勇士回来。千万将污染水源的<font color=\"0xff00ff00\">沃毒蜈蚣</font>处置了。
			蜈蚣洞窟在<font color=\"0xff00ff00\">绝命谷最深地区西南的某个地方</font>。。。
			
			[好的，走了。:0]"""
		elif (PlayerGetV(Sender,GV_Taoist_MassHeal)==3):
			say = """解决所有问题了。
			
			[速度离开:8]"""
		elif (PlayerGetV(Sender,GV_Taoist_MassHeal)==4):
			if (GetInventoryCount(Sender) >= 1): #格子大于等于1格
				PlayerSetV(Sender,GV_Taoist_MassHeal,5)
				Sender.GiveItem("群体治愈术（秘籍）",1)
				say = """我们村庄的人们永远都不会忘记<font color=\"0xff00ff00\">你的善行</font>。。。
				现在去找每年在这个地方贴护身符并上香的奇怪老头。
				祝你走运。。。一路小心。。。
				
				[结束:0]"""
			else:
				say = """背囊里没有位置了，整理出位置后，请再来！
				
				[结束:0]"""
		else:
			say = """（....................）
			
			[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(323,"OnClick",OnClick)