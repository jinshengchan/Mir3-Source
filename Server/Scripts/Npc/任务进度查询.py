# -*- coding: utf-8 -*-
#载入模块SYS引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import random
from 变量.默认变量 import *
from Utils.PlayerUtils import *
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
	say = "" 
	
#万事通每日任务次数限制
	DailyTask_Limit = 3
	
#红名-传送流放岛	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
		
		[关闭:0]"""
	elif (Menu == 1):
		kmq = PlayerGetV(Sender,BV_NQ_KILLMON)
		knq = PlayerGetV(Sender,BV_NQ_KILLNUM)
		igq = PlayerGetV(Sender,BV_NQ_ITEMGOT)
		MainTaskList = GetMainTaskList(Sender,PlayerGetV(Sender,BV_NQ_MAIN))
		a = MainTaskList[1]
		b = int(MainTaskList[2])
		c = MainTaskList[3]
		if Sender.Character.Account.TempAdmin:  # 判断是否为管理员
			say = """您正在进行的江湖任务进度如下：
		
<font color=\"0xff00ff00\">任务名称</font>： {} 

<font color=\"0xff00ff00\">等级要求</font>： {} 级

<font color=\"0xff00ff00\">任务进度</font>： {} 

[跳过本阶段江湖任务:10]

[前一步:99]""".format(a,b,c)
		else:
			say = """您正在进行的江湖任务进度如下：
		
<font color=\"0xff00ff00\">任务名称</font>： {} 

<font color=\"0xff00ff00\">等级要求</font>： {} 级

<font color=\"0xff00ff00\">任务进度</font>： {} 

[跳过本阶段江湖任务:10 ]

[前一步:99]""".format(a,b,c)
	elif (Menu == 2):
		if(Sender.Level < 22):
			say = """您的等级还不足以接受万事通任务。
			
			[结束:0]"""
		else:
			say = TaskList(Sender,DailyTask_Limit)
	elif (Menu == 10):
		if PlayerGetV(Sender,BV_NQ_MAIN) < 39:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 新手任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 50:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 乞丐任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 56:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 苍蝇拍任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 63:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 石母任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 84:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 王大人任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 87:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 轻型盔甲任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 110:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 半兽人任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 115:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 千年毒蛇任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 127:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 被盗灵魂任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 148:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 堕落道士任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:11]

[我再想一想:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 174:
			say = """您确定要跳过 <font color=\"0xff00ff00\"> 沃玛金牌任务 </font> 吗？

一旦跳过，将无法得到本阶段经验、金币、声望、道具奖励！
并且也可能会因此缺失后续任务需要的道具！

[确定跳过:]

[我再想一想:0]"""
		else:
			say = """抱歉，无法帮您跳过后续任务，请努力完成吧！

[结束:0]"""
	elif (Menu == 11):
		if PlayerGetV(Sender,BV_NQ_MAIN) < 39:
			PlayerSetV(Sender,BV_NQ_MAIN,39)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 新手任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 50:
			PlayerSetV(Sender,BV_NQ_MAIN,50)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 乞丐任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 56:
			PlayerSetV(Sender,BV_NQ_MAIN,56)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 苍蝇拍任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 63:
			PlayerSetV(Sender,BV_NQ_MAIN,63)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 石母任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 84:
			PlayerSetV(Sender,BV_NQ_MAIN,84)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 王大人任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 87:
			PlayerSetV(Sender,BV_NQ_MAIN,87)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 轻型盔甲任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 110:
			PlayerSetV(Sender,BV_NQ_MAIN,110)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 半兽人任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 115:
			PlayerSetV(Sender,BV_NQ_MAIN,115)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 千年毒蛇任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 127:
			PlayerSetV(Sender,BV_NQ_MAIN,127)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 被盗灵魂任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 148:
			PlayerSetV(Sender,BV_NQ_MAIN,148)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 堕落道士任务 </font> 。

[结束:0]"""

		elif PlayerGetV(Sender,BV_NQ_MAIN) < 174:
			PlayerSetV(Sender,BV_NQ_MAIN,174)
			PlayerSetV(Sender,BV_NQ_KILLMON,0)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """您已跳过 <font color=\"0xff00ff00\"> 沃玛金牌任务 </font> 。

[结束:0]"""

		else:
			say = """抱歉，无法帮您跳过后续任务，请努力完成吧！

[结束:0]"""

	#主菜单
	else:
		say = """您好，可以通过我来查询您的当前任务进度。
		

[查询江湖任务进度:1]    [查询每日随机任务进度:2]


[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
def TaskList(Sender,DailyTask_Limit):
	if PlayerGetV(Sender,BV_NUM_DAILYTASK) < DailyTask_Limit:
		if(PlayerGetV(Sender,BV_QT_TODAY)==0):
			return"""您今天已完成 {} 次万事通任务。
快去找万事通领取吧！
注意领取后要再24点之前完成哦......


			[结束:0]""".format(PlayerGetV(Sender,BV_NUM_DAILYTASK))
		else:
			a = ''
			b = ''
			c = ''
			d = ''
			h = ''
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
					DailyMonList.append(mon)
					c = '、'.join(DailyMonList)
				d = DailyTaskList.get('杀怪数量')
			e = ((Sender.Level - 20) * 20000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * ((Sender.Level - 20) * 5000))
			f = ((Sender.Level - 20) * 3000) + (PlayerGetV(Sender,BV_NUM_DAILYTASK) * (Sender.Level - 20) * 500)
			g = (Sender.Level - 20) // 2
			randomitemlist = DailyTaskList.get('随机奖励')
			for y in randomitemlist:
				h = y
			i = randomitemlist.get(h)
			e1 = e * Local_ExpRewards_Rate
			f1 = f * Local_GoldRewards_Rate
			g1 = g * Local_PresRewards_Rate
			return"""您已经领取过万事通任务，快去完成吧！
			
当前任务为今日<font color=\"0xff00ff00\"> 第{}次 </font>万事通任务，内容如下：

<font color=\"0xff00ff00\">任务物品：</font>{} 
<font color=\"0xff00ff00\">收集数量：</font>{}

<font color=\"0xff00ff00\">任务怪物：</font>{} 

<font color=\"0xff00ff00\">目标数量：</font>{}                  <font color=\"0xff00ff00\">已击杀：</font>{}    

<font color=\"0xff00ff00\">经验奖励：</font>{}
<font color=\"0xff00ff00\">金币奖励：</font>{}
<font color=\"0xff00ff00\">声望奖励：</font>{}

<font color=\"0xff00ff00\">随机奖励物品：</font>{}  {} 个

			[结束:0]""".format(num_dt,a,b,c,d,kn,e1,f1,g1,h,i)
	else:
		return"""恭喜，您今天的任务已经完成。
		
		
			[结束:0]"""


NpcEvent.add_listener(247,"OnClick",OnClick)
