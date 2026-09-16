# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
import random
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
		say = """请你离开。
		
		我不想和红名交易。
		
		[离开:0]"""
	elif (Menu == 1):
		say = """（战士魔法）
		
		（1-10 等级 修炼魔法）
		 [基本剑术:11]
		
		（11-20 等级 修炼魔法）
		 [攻杀剑术:13],   [刺杀剑术:14]
		
		（21-30 等级 修炼魔法）
		 [半月弯刀:15],   [野蛮冲撞:16]
		
		（31-40 等级 修炼魔法）
		[烈火剑法:17],   [翔空剑法:18],   [莲月剑法:19]
		
		[结束:0]
		
		"""
	elif (Menu == 11):
		say = """如果想学基本剑术，请支付700金币。
		想得到指教吗？
		
		[请写武功秘籍:111]
		[结束:0]
		"""
	elif (Menu == 111):
		#判断需要的金币	
		if (Sender.Gold < 700):
			say= """世界上的事情没有免费的，修炼武功也是同样的，下次不要忘了带修炼费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("基本剑术") < 1):
			say ="""在可以证明你有得到武功秘籍的实力之前，我是不能给你进行指导的。请首先找到基本剑术武功书。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,700)
			Sender.TakeItem("基本剑术",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""哦，非常抱歉！书太旧了，无论如何也无法看清楚，请找到保存状态好些的书！
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("基本剑术（秘籍）",1)
				say = """这里有秘籍，请拿着吧！江湖是很残酷的地方，你千万要专心于一个领域，如果不这样，不要说绝世武功，就是成为一名真正的侠士都很困难，江湖呀......
				
				[结束:0]
				"""
	elif (Menu == 12):
		say = """如果想学运气术，请支付1200金币。
		想得到指教吗？
		
		[请写武功秘籍:121]
		[结束:0]
		"""
	elif (Menu == 121):
		#判断需要的金币	
		if (Sender.Gold < 1200):
			say= """世界上的事情没有免费的，修炼武功也是同样的，下次不要忘了带修炼费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("运气术") < 1):
			say ="""在可以证明你有得到武功秘籍的实力之前，我是不能给你进行指导的。请首先找到运气术武功书。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,1200)
			Sender.TakeItem("运气术",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""哦，非常抱歉！书太旧了，无论如何也无法看清楚，请找到保存状态好些的书！
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("运气术（秘籍）",1)
				say = """这里有秘籍，请拿着吧！江湖是很残酷的地方，你千万要专心于一个领域，如果不这样，不要说绝世武功，就是成为一名真正的侠士都很困难，江湖呀......
				
				[结束:0]
				"""
	elif (Menu == 13):
		say = """如果想学攻杀剑术，请支付1400金币。
		想得到指教吗？
		
		[请写武功秘籍:131]
		[结束:0]
		"""
	elif (Menu == 131):
		#判断需要的金币
		if (Sender.Gold < 1400):
			say= """世界上的事情没有免费的，修炼武功也是同样的，下次不要忘了带修炼费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("攻杀剑术") < 1):
			say ="""在可以证明你有得到武功秘籍的实力之前，我是不能给你进行指导的。请首先找到攻杀剑术武功书。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,1400)
			Sender.TakeItem("攻杀剑术",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""哦，非常抱歉！书太旧了，无论如何也无法看清楚，请找到保存状态好些的书！
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("攻杀剑术（秘籍）",1)
				say = """这里有秘籍，请拿着吧！江湖是很残酷的地方，你千万要专心于一个领域，如果不这样，不要说绝世武功，就是成为一名真正的侠士都很困难，江湖呀......
				
				[结束:0]
				"""
	elif (Menu == 14):
		say = """如果想学刺杀剑术，请支付1900金币。
		想得到指教吗？
		
		[请写武功秘籍:141]
		[结束:0]
		"""
	elif (Menu == 141):
		#判断需要的金币	
		if (Sender.Gold < 1900):
			say= """世界上的事情没有免费的，修炼武功也是同样的，下次不要忘了带修炼费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("刺杀剑术") < 1):
			say ="""在可以证明你有得到武功秘籍的实力之前，我是不能给你进行指导的。请首先找到刺杀剑术武功书。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,1900)
			Sender.TakeItem("刺杀剑术",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""哦，非常抱歉！书太旧了，无论如何也无法看清楚，请找到保存状态好些的书！
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("刺杀剑术（秘籍）",1)
				say = """这里有秘籍，请拿着吧！江湖是很残酷的地方，你千万要专心于一个领域，如果不这样，不要说绝世武功，就是成为一名真正的侠士都很困难，江湖呀......
				
				[结束:0]
				"""
	elif (Menu == 15):
		say = """如果想学半月弯刀，请支付2300金币。
		想得到指教吗？
		
		[请写武功秘籍:151]
		[结束:0]
		"""
	elif (Menu == 151):
		#判断需要的金币	
		if (Sender.Gold < 2300):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("半月弯刀") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,2300)
			Sender.TakeItem("半月弯刀",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""书太陈旧破碎了......，下次请拿像样的书来。
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("半月弯刀（秘籍）",1)
				say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 16):
		say = """如果想学野蛮冲撞，请支付2700金币。
		想得到指教吗？
		
		[请写武功秘籍:161]
		[结束:0]
		"""
	elif (Menu == 161):
		#判断需要的金币	
		if (Sender.Gold < 2700):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("野蛮冲撞") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,2700)
			Sender.TakeItem("野蛮冲撞",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""书太陈旧破碎了......，下次请拿像样的书来。
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("野蛮冲撞（秘籍）",1)
				say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 17):
		say = """如果想学烈火剑法，请支付3200金币。
		想得到指教吗？
		
		[请写武功秘籍:171]
		[结束:0]
		"""
	elif (Menu == 171):
		#判断需要的金币	
		if (Sender.Gold < 3200):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("烈火剑法") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,3200)
			Sender.TakeItem("烈火剑法",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""书太陈旧破碎了......，下次请拿像样的书来。
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("烈火剑法（秘籍）",1)
				say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 18):
		say = """如果想学翔空剑法，请支付3500金币。
		想得到指教吗？
		
		[请写武功秘籍:181]
		[结束:0]
		"""
	elif (Menu == 181):
		#判断需要的金币	
		if (Sender.Gold < 3500):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("翔空剑法") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,3500)
			Sender.TakeItem("翔空剑法",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""书太陈旧破碎了......，下次请拿像样的书来。
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("翔空剑法（秘籍）",1)
				say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 19):
		say = """如果想学莲月剑法，请支付3800金币。
		想得到指教吗？
		
		[请写武功秘籍:191]
		[结束:0]
		"""
	elif (Menu == 191):
		#判断需要的金币	
		if (Sender.Gold < 3800):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("莲月剑法") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,3800)
			Sender.TakeItem("莲月剑法",1)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 20:
				say ="""书太陈旧破碎了......，下次请拿像样的书来。
				
				[结束:0]
				"""
			else:
				Sender.GiveItem("莲月剑法（秘籍）",1)
				say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
			    """
	else:
		if Sender.Class == Sender.Class.Wizard:
			say = """人们都叫我龙血先生，因为我专门帮助那些想成为战士的年青
			人。
			不过，你不是战士。魔法师应该去银杏山谷。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Taoist:
			say = """人们都叫我龙血先生，因为我专门帮助那些想成为战士的年青
			人。
			不过，你不是战士。道士应该去道馆。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Assassin:
			say = """人们都叫我龙血先生，因为我专门帮助那些想成为战士的年青
			人。
			不过，你不是战士。刺客应该去比奇。
			
			[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==6):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """每当我看到那些专心修炼武功的年轻人，我就觉得自己所做的
				事很有意义。
				看来你的实力已经得到了上官小姐的认可，那么，这本武功秘籍就送给你吧。
				
				[结束:0]"""
		else:
			say = """每当我看到那些专心修炼武功的年轻人，我就觉得自己所做的
			事很有意义。呵呵呵，你找我有什么事吗？
			
			[寻求武功指导:1]
			[结束:0]
			"""
			
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
		

NpcEvent.add_listener(112,"OnClick",OnClick)