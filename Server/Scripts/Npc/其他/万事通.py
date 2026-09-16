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
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import random
import sys
import Server.Envir.SEnvir as SEnvir
from datetime import datetime, timedelta
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)
import unicodedata
s1 = clr.Reference[System.Object]()
from Defines import *
import Server
from Npc.商店列表 import *
import collections
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
rewardsJY = [
			('半兽勇士召唤卷', 1, True, 3000),
			('骷髅精灵召唤卷', 1, True, 3000),
			('尸王召唤卷', 1, True, 3000),
			('红甲虫召唤卷', 1, True, 3000),
			('巨型多角虫召唤卷', 1, True, 3000),
			('蚂蚁将军召唤卷', 1, True, 2000),
			('白野猪召唤卷', 1, True, 2000),
			('沃玛卫士召唤卷', 1, True, 2000),
			('邪恶钳虫召唤卷', 1, True, 2000),
			('八角首领召唤卷', 1, True, 2000),
			('骨鬼将召唤卷', 1, True, 1000),
			('大法老召唤卷', 1, True, 1000),
			('疯狂魔神盗召唤卷', 1, True, 1000),
			('护法天召唤卷', 1, True, 1000),
			('神鬼王召唤卷', 1, True, 1000),
			('潘夜鬼将召唤卷', 1, True, 500),
			('震天首将召唤卷', 1, True, 500),
			]

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}	
	say = "" 

	if (Menu == 1):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("万事通江湖任务")
		NPCObject = ServerUtils.GetNPCObject(294)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.万事通江湖任务.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	elif (Menu == 2):
		if(Sender.Level < 33):
			say = """你还不够强大，当你等级达到33级时再来吧。
			
			[结束:0]"""
		elif Sender.HasDaily:
			say = """你当前的每日任务还没做完呢！
			
			[结束:0]"""
		elif Sender.RemainingDailyCount < 1:
			say = """今天已经没有任务给你了，请明天再来
			
			[结束:0]"""
		else:
			Sender.GetDailyQuest()
			say = """任务给你了，打开任务界面查看
			
			[结束:0]"""
	elif (Menu == 3):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("万事通每日随机任务")
		NPCObject = ServerUtils.GetNPCObject(295)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.万事通每日任务.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	elif (Menu == 4):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("管理员")
		if(not Sender.Character.Account.TempAdmin):
			SEnvir.Log("脚本警报：{} 使用封包挂".format(Sender.Character.CharacterName))
			return Dict
		NPCObject = ServerUtils.GetNPCObject(224)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.管理员.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	elif (Menu == 5):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("任务进度查询")
		NPCObject = ServerUtils.GetNPCObject(247)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.任务进度查询.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"



	elif (Menu == 6):
		say = """你当前拥有 {} 点声望。
		
		[结束:0]""".format(Sender.Prestige)
	elif (Menu == 7):
		say = """欢迎来到相聚传奇三，请前往新手指引 NPC 开启玛法大陆之旅
		
		提示：
		      <font color=\"0xff00ff00\">边境村庄  上官小姐 （458:258）</font>
		      <font color=\"0xff00ff00\">银杏山谷  南宫小姐 （265:202）</font>
		      <font color=\"0xff00ff00\">道馆      士官     （404:134）</font>
		
		[结束:0]"""
	elif (Menu == 8):
		say = """每周循环任务，要求等级35级，
		你确定要接任务吗？
		
		[领取每周击杀精英任务:81] [查询精英任务进度:811]
		
		[领取每周击杀BOSS任务:83]"""
#[领取每周击杀BOSS任务:82] [查询BOSS任务进度:821]
	elif (Menu == 81):
		if(Sender.Level < 35):
			say = """你还不够强大，当你等级达到35级时再来吧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)>0):
			say = """你已经获取本周任务了，请下周再来！
			
			[结束:0]"""
		else:
			PlayerSetV(Sender,GV_PLAYER_ZHOUKILLELITE,1)
			say = """请你击杀下列的精英达到20只，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">半兽勇士</font>                  <font color=\"0xffffff00\">巨型多角虫</font>
			<font color=\"0xffffff00\">骷髅精灵</font>                  <font color=\"0xffffff00\">蚂蚁将军</font>
			<font color=\"0xffffff00\">红甲虫</font>                    <font color=\"0xffffff00\">沃玛卫士</font>
			<font color=\"0xffffff00\">邪恶钳虫</font>                  <font color=\"0xffffff00\">白野猪</font>
			<font color=\"0xffffff00\">骨鬼将</font>                    <font color=\"0xffffff00\">八角首领</font>
			<font color=\"0xffffff00\">大法老</font>                    <font color=\"0xffffff00\">神鬼王</font>
			<font color=\"0xffffff00\">护法天</font>                    <font color=\"0xffffff00\">潘夜鬼将</font>
			<font color=\"0xffffff00\">疯狂魔神盗</font>                <font color=\"0xffffff00\">震天首将</font>
			<font color=\"0xffffff00\">霸王守卫</font>                  <font color=\"0xffffff00\">诺玛突击队长</font>
			<font color=\"0xffffff00\">诺玛族长老</font>
			
			[结束:0]"""

	
	elif (Menu == 811):
		if(Sender.Level < 35):
			say = """你还不够强大，当你等级达到35级时再来吧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)==0):
			say = """你还没有获得本周任务，快去接任务吧！
			
			[领取每周击杀精英任务:81]
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)>=1) and (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)<21):
			say = """请你击杀下列的精英达到20只，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">半兽勇士</font>      <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">巨型多角虫</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">骷髅精灵</font>      <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">蚂蚁将军</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">红甲虫</font>        <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">沃玛卫士</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">邪恶钳虫</font>      <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">白野猪</font>        <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">骨鬼将</font>        <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">八角首领</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">大法老</font>        <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">神鬼王</font>        <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">护法天</font>        <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">潘夜鬼将</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">疯狂魔神盗</font>    <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">震天首将</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">霸王守卫</font>      <font color=\"0xffffff00\">（{}）</font>          <font color=\"0xffffff00\">诺玛突击队长</font>  <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">诺玛族长老</font>    <font color=\"0xffffff00\">（{}）</font>
			
			总击杀数    <font color=\"0xffffff00\">（{}）</font>
			
			[结束:0]""".format(PlayerGetV(Sender,GV_KILLELITE_BSYSELITE),
PlayerGetV(Sender,GV_KILLELITE_JXDJCELITE),
PlayerGetV(Sender,GV_KILLELITE_KLJYELITE),
PlayerGetV(Sender,GV_KILLELITE_MYJJELITE),
PlayerGetV(Sender,GV_KILLELITE_HJCELITE),
PlayerGetV(Sender,GV_KILLELITE_WMWSELITE),
PlayerGetV(Sender,GV_KILLELITE_XEQCELITE),
PlayerGetV(Sender,GV_KILLELITE_BYZELITE),
PlayerGetV(Sender,GV_KILLELITE_GGJELITE),
PlayerGetV(Sender,GV_KILLELITE_BJSSELITE),
PlayerGetV(Sender,GV_KILLELITE_DFLELITE),
PlayerGetV(Sender,GV_KILLELITE_SGWELITE),
PlayerGetV(Sender,GV_KILLELITE_HFTELITE),
PlayerGetV(Sender,GV_KILLELITE_PYGJELITE),
PlayerGetV(Sender,GV_KILLELITE_FKMSDELITE),
PlayerGetV(Sender,GV_KILLELITE_ZTSJELITE),
PlayerGetV(Sender,GV_KILLELITE_BWSWELITE),
PlayerGetV(Sender,GV_KILLELITE_NMDZELITE),
PlayerGetV(Sender,GV_KILLELITE_NMZZLELITE),
PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE) -1,)
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)>=21) and (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)<999):
			say = """恭喜你完成本周精英任务。
			
			[领取每周击杀精英任务奖励:812]"""
		else:
			say = """你已经完成本周任务了，请下周再来！
			
			[结束:0]"""
	elif (Menu == 812):
		if (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)>=21) and (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLELITE)<999):
			PlayerSetV(Sender,GV_PLAYER_ZHOUKILLELITE,999)
			GiveExperience(Sender,2000000)
			# 最终奖励
			converted_reward = []
			for item in rewardsJY:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("周击杀精英任务", "运营团队", "你获得随机奖励", my_reward)
			BroadChat('恭喜玩家 {} 完成周击杀精英任务，获得 {}'.format(Sender.Name, my_reward[0][0]))
			#已经有师傅了，显示对应的信息
			if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
				MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
				if SEnvir.GetPlayerByCharacter(str(MasterName)):
					player = SEnvir.GetPlayerByCharacter(str(MasterName))
					PlayerSetV(player,BV_SHI_BONUSCOUNT,PlayerGetV(player,BV_SHI_BONUSCOUNT) + 10)  #师傅获得临时授业值
					player.Connection.ReceiveChat("恭喜你的徒弟完成周击杀精英任务，你获得10点授业值。".format(Sender.Name), MessageType.System)
					PlayerSetV(Sender,BV_TU_BONUSCOUNT,PlayerGetV(Sender,BV_TU_BONUSCOUNT) + 5)    #徒弟获得临时授业值
					Sender.Connection.ReceiveChat("恭喜你完成周击杀精英任务，获得5点授业值。", MessageType.System)
			#老玩家回归，完成周小BOSS额外奖励
			if (Sender.HasCustomBuff(135) and PlayerGetV(Sender,GV_PLAYER_OLDZHOUBOSS) == 0) and Sender.Level >= 45:
				Sender.PYMailSend("老玩家回归", "系统", "邮件发送老玩家回归周BOSS奖励", [('钢玉石',1,True)])
				ServerUtils.SendMsgToAll('恭喜回归玩家【{}】获得周BOSS额外奖励【钢玉石】'.format(Sender.Name),MessageType.System)
				PlayerSetV(Sender,GV_PLAYER_OLDZHOUBOSS,1)
			say = """你已经完成本周击杀精英任务。
			
			[结束:0]"""
	# elif (Menu == 82):
		# if(Sender.Level < 35):
			# say = """你还不够强大，当你等级达到35级时再来吧。
			
			# [结束:0]"""
		# elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS)>0):
			# say = """你已经获取本周任务了，请下周再来！
			
			# [结束:0]"""
		# else:
			# PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS,1)
			# say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			# <font color=\"0xffffff00\">僵尸王</font>
			# <font color=\"0xffffff00\">沃玛教主</font>
			# <font color=\"0xffffff00\">触龙神</font>
			# <font color=\"0xffffff00\">黑猪王</font>
			# <font color=\"0xffffff00\">骷髅教主</font>
			# <font color=\"0xffffff00\">赤月恶魔</font>
			# <font color=\"0xffffff00\">祖玛教主</font>
			# <font color=\"0xffffff00\">潘夜牛魔王</font>
			# <font color=\"0xffffff00\">震天魔神</font>
			# <font color=\"0xffffff00\">霸王教主</font>
			
			# [结束:0]"""
	# elif (Menu == 821):
		# if(Sender.Level < 35):
			# say = """你还不够强大，当你等级达到35级时再来吧。
			
			# [结束:0]"""
		# elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS)==0):
			# say = """你还没有获得本周任务，快去接任务吧！
			
			# [领取每周击杀BOSS任务:82]
			
			# [结束:0]"""
		# elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS)>=1) and (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS)<11):
			# say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			# <font color=\"0xffffff00\">僵尸王</font>      <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">沃玛教主</font>    <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">触龙神</font>      <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">黑猪王</font>      <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">骷髅教主</font>    <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">赤月恶魔</font>    <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">祖玛教主</font>    <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">潘夜牛魔王</font>  <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">震天魔神</font>    <font color=\"0xffffff00\">（{}）</font>
			# <font color=\"0xffffff00\">霸王教主</font>    <font color=\"0xffffff00\">（{}）</font>
			
			# [结束:0]""".format(PlayerGetV(Sender,GV_KILLBOSS_JSWBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_WMJZBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_KLJZBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS),
# PlayerGetV(Sender,GV_KILLBOSS_BWJZBOSS),)
		# elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS)==11):
			# say = """恭喜你完成本周BOSS任务。
			
			# [领取每周击杀BOSS任务奖励:822]"""
		# else:
			# say = """你已经完成本周任务了，请下周再来！
			
			# [结束:0]"""
	# elif (Menu == 822):
		# if (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS)==11):
			# if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				# PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS,99)
				# Sender.GiveItem("勇士勋章",1)
				# say = """你已经完成本周击杀BOSS任务。
				
				# [结束:0]"""
			# else:
				# say ="""你的包裹没有空格。
				
				# [离开:0]"""
	elif (Menu == 83):
		say = """以下三个任务里，只能选择其中一个任务完成。
		<font color=\"0xff00ff00\">注意：点击对应的任务，就将获得当前周任务，无法更换。</font>
		
		[周击杀BOSS任务一:831]     [查询当前进度:8311]
		要求：沃玛教主，僵尸王，骷髅教主
		奖励：100万经验，荣誉勋章
		
		[周击杀BOSS任务二:832]     [查询当前进度:8321]
		要求：黑猪王，赤月恶魔，触龙神，祖玛教主，潘夜牛魔王，震天魔神
		奖励：200万经验，玛法勋章
		
		[周击杀BOSS任务三:833]     [查询当前进度:8331]
		要求：黑猪王，赤月恶魔，触龙神，祖玛教主，潘夜牛魔王，震天魔神，霸王教主，诺玛教主
		奖励：600万经验，勇士勋章
		"""
	elif (Menu == 831):
		if(Sender.Level < 35):
			say = """你还不够强大，当你等级达到35级时再来吧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS1)>0) or (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS2)>0) or (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS3)>0):
			say = """你已经获取本周任务了，请下周再来！
			
			[结束:0]"""
		else:
			PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS1,1)
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">僵尸王</font>
			<font color=\"0xffffff00\">沃玛教主</font>
			<font color=\"0xffffff00\">骷髅教主</font>
			
			[结束:0]"""
	elif (Menu == 8311):
		if (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS1)==0):
			say = """你还没有获得本周任务，快去接任务吧！
			
			[领取周击杀BOSS任务一:831]
			
			[结束:0]"""
		elif PlayerGetV(Sender,GV_KILLBOSS_JSWBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_WMJZBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_KLJZBOSS)!=1:
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">僵尸王</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">沃玛教主</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">骷髅教主</font>    <font color=\"0xffffff00\">（{}）</font>
			
			[结束:0]""".format(PlayerGetV(Sender,GV_KILLBOSS_JSWBOSS),PlayerGetV(Sender,GV_KILLBOSS_WMJZBOSS),PlayerGetV(Sender,GV_KILLBOSS_KLJZBOSS),)
		elif PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS1)==1 and PlayerGetV(Sender,GV_KILLBOSS_JSWBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_WMJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_KLJZBOSS)>0:
			say = """恭喜你完成本周BOSS任务。
			
			[领取每周击杀BOSS任务奖励:8312]"""
		else:
			say = """你已经完成本周任务了，请下周再来！
			
			[结束:0]"""
	elif (Menu == 8312):
		if PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS1)==1 and PlayerGetV(Sender,GV_KILLBOSS_JSWBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_WMJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_KLJZBOSS)>0:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS1,99)
				GiveExperience(Sender,1000000)
				Sender.GiveItem("荣誉勋章",1)
				#已经有师傅了，显示对应的信息
				if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
					MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
					if SEnvir.GetPlayerByCharacter(str(MasterName)):
						player = SEnvir.GetPlayerByCharacter(str(MasterName))
						PlayerSetV(player,BV_SHI_BONUSCOUNT,PlayerGetV(player,BV_SHI_BONUSCOUNT) + 50)  #师傅获得临时授业值
						player.Connection.ReceiveChat("恭喜你的徒弟完成周击杀精英任务，你获得50点授业值。".format(Sender.Name), MessageType.System)
						PlayerSetV(Sender,BV_TU_BONUSCOUNT,PlayerGetV(Sender,BV_TU_BONUSCOUNT) + 25)    #徒弟获得临时授业值
						Sender.Connection.ReceiveChat("恭喜你完成周击杀精英任务，获得25点授业值。", MessageType.System)
				say = """你已经完成本周击杀BOSS任务。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""

	elif (Menu == 832):
		if(Sender.Level < 35):
			say = """你还不够强大，当你等级达到35级时再来吧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS1)>0) or (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS2)>0) or (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS3)>0):
			say = """你已经获取本周任务了，请下周再来！
			
			[结束:0]"""
		else:
			PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS2,1)
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">触龙神</font>
			<font color=\"0xffffff00\">黑猪王</font>
			<font color=\"0xffffff00\">赤月恶魔</font>
			<font color=\"0xffffff00\">祖玛教主</font>
			<font color=\"0xffffff00\">潘夜牛魔王</font>
			<font color=\"0xffffff00\">震天魔神</font>
			
			[结束:0]"""
	elif (Menu == 8321):
		if (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS2)==0):
			say = """你还没有获得本周任务，快去接任务吧！
			
			[领取周击杀BOSS任务二:832]
			
			[结束:0]"""
		elif PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS)!=1:
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">触龙神</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">黑猪王</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">赤月恶魔</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">祖玛教主</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">潘夜牛魔王</font>  <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">震天魔神</font>    <font color=\"0xffffff00\">（{}）</font>
			
			[结束:0]""".format(PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS),PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS),PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS),PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS),PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS),PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS),)
		elif PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS2)==1 and PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS)>0:
			say = """恭喜你完成本周BOSS任务。
			
			[领取每周击杀BOSS任务奖励:8322]"""
		else:
			say = """你已经完成本周任务了，请下周再来！
			
			[结束:0]"""
	elif (Menu == 8322):
		if PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS2)==1 and PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS)>0:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS2,99)
				GiveExperience(Sender,2000000)
				Sender.GiveItem("玛法勋章",1)
				#已经有师傅了，显示对应的信息
				if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
					MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
					if SEnvir.GetPlayerByCharacter(str(MasterName)):
						player = SEnvir.GetPlayerByCharacter(str(MasterName))
						PlayerSetV(player,BV_SHI_BONUSCOUNT,PlayerGetV(player,BV_SHI_BONUSCOUNT) + 50)  #师傅获得临时授业值
						player.Connection.ReceiveChat("恭喜你的徒弟完成周击杀精英任务，你获得50点授业值。".format(Sender.Name), MessageType.System)
						PlayerSetV(Sender,BV_TU_BONUSCOUNT,PlayerGetV(Sender,BV_TU_BONUSCOUNT) + 25)    #徒弟获得临时授业值
						Sender.Connection.ReceiveChat("恭喜你完成周击杀精英任务，获得25点授业值。", MessageType.System)
				say = """你已经完成本周击杀BOSS任务。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""

	elif (Menu == 833):
		if(Sender.Level < 35):
			say = """你还不够强大，当你等级达到35级时再来吧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS1)>0) or (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS2)>0) or (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS3)>0):
			say = """你已经获取本周任务了，请下周再来！
			
			[结束:0]"""
		else:
			PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS3,1)
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">触龙神</font>
			<font color=\"0xffffff00\">黑猪王</font>
			<font color=\"0xffffff00\">赤月恶魔</font>
			<font color=\"0xffffff00\">祖玛教主</font>
			<font color=\"0xffffff00\">潘夜牛魔王</font>
			<font color=\"0xffffff00\">震天魔神</font>
			<font color=\"0xffffff00\">霸王教主</font>
			<font color=\"0xffffff00\">诺玛教主</font>
			
			[结束:0]"""
	elif (Menu == 8331):
		if (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS3)==0):
			say = """你还没有获得本周任务，快去接任务吧！
			
			[领取周击杀BOSS任务三:833]
			
			[结束:0]"""
		elif PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_BWJZBOSS)!=1 or PlayerGetV(Sender,GV_KILLBOSS_NMJZBOSS)!=1:
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">触龙神</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">黑猪王</font>      <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">赤月恶魔</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">祖玛教主</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">潘夜牛魔王</font>  <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">震天魔神</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">霸王教主</font>    <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">诺玛教主</font>    <font color=\"0xffffff00\">（{}）</font>
			
			[结束:0]""".format(PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS),PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS),PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS),PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS),PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS),PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS),PlayerGetV(Sender,GV_KILLBOSS_BWJZBOSS),PlayerGetV(Sender,GV_KILLBOSS_NMJZBOSS),)
		elif PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS3)==1 and PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_BWJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_NMJZBOSS)>0:
			say = """恭喜你完成本周BOSS任务。
			
			[领取每周击杀BOSS任务奖励:8332]"""
		else:
			say = """你已经完成本周任务了，请下周再来！
			
			[结束:0]"""
	elif (Menu == 8332):
		if PlayerGetV(Sender,GV_PLAYER_ZHOUKILLBOSS3)==1 and PlayerGetV(Sender,GV_KILLBOSS_CLSBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CJHYZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_CYEMBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZMJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_PYNMWBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_ZTMSBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_BWJZBOSS)>0 and PlayerGetV(Sender,GV_KILLBOSS_NMJZBOSS)>0:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				PlayerSetV(Sender,GV_PLAYER_ZHOUKILLBOSS3,99)
				GiveExperience(Sender,6000000)
				Sender.GiveItem("勇士勋章",1)
				#已经有师傅了，显示对应的信息
				if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
					MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
					if SEnvir.GetPlayerByCharacter(str(MasterName)):
						player = SEnvir.GetPlayerByCharacter(str(MasterName))
						PlayerSetV(player,BV_SHI_BONUSCOUNT,PlayerGetV(player,BV_SHI_BONUSCOUNT) + 50)  #师傅获得临时授业值
						player.Connection.ReceiveChat("恭喜你的徒弟完成周击杀精英任务，你获得50点授业值。".format(Sender.Name), MessageType.System)
						PlayerSetV(Sender,BV_TU_BONUSCOUNT,PlayerGetV(Sender,BV_TU_BONUSCOUNT) + 25)    #徒弟获得临时授业值
						Sender.Connection.ReceiveChat("恭喜你完成周击杀精英任务，获得25点授业值。", MessageType.System)
				say = """你已经完成本周击杀BOSS任务。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 9):
		if(Sender.Level < 40):
			say = """你还不够强大，当你等级达到40级时再来吧。
			
			[结束:0]"""
		elif(Sender.Level > 48):
			say = """你已经超过48级，无法接取新人进阶任务。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS) > 0 and PlayerGetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS) < 99) and ((PlayerGetV(Sender,GV_KILLBOSS_YHBOSS)== 0) or (PlayerGetV(Sender,GV_KILLBOSS_NMWBOSS)== 0)):
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">蚁后</font>        <font color=\"0xffffff00\">（{}）</font>
			<font color=\"0xffffff00\">驽马王</font>      <font color=\"0xffffff00\">（{}）</font>
			
			[结束:0]""".format(PlayerGetV(Sender,GV_KILLBOSS_YHBOSS),PlayerGetV(Sender,GV_KILLBOSS_NMWBOSS))
		elif (PlayerGetV(Sender,GV_KILLBOSS_YHBOSS)== 1) and (PlayerGetV(Sender,GV_KILLBOSS_NMWBOSS)== 1) and (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS)== 1):
			say = """恭喜你完成本周新人进阶任务。
			
			[领取每周新人进阶任务奖励:91]"""
		elif (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS)== 99):
			say = """你已经完成本周新人进阶任务。
				
				[结束:0]"""
		else:
			PlayerSetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS,1)
			say = """请你击杀下列BOSS，完成以后找我领取奖励。
			
			<font color=\"0xffffff00\">蚁后</font>
			<font color=\"0xffffff00\">驽马王</font>
			
			[结束:0]"""
	elif (Menu == 91):
		if (PlayerGetV(Sender,GV_KILLBOSS_YHBOSS)== 1) and (PlayerGetV(Sender,GV_KILLBOSS_NMWBOSS)== 1) and (PlayerGetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS)== 1):
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				PlayerSetV(Sender,GV_PLAYER_ZHOUKILLXSJJBOSS,99)
				GiveExperience(Sender,1000000)
				Sender.GiveItem("强效太阳水（绑定）",50)
				say = """你已经完成本周新人进阶任务。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""

	else:
		if(Sender.Character.Account.TempAdmin):
			say = """<font color=\"0xff00ff00\">服务器当前时间：{}年{}月{}日{}时{}分</font>
				<font color=\"0xff00ff00\">服务器启动时间：{}年{}月{}日{}时{}分</font>
				
				江湖上的朋友都叫我万拍子。
				不是我吹，你不了解的武功或其它的任务我都可以给你解答。
				你有什么想问的吗？
				
				[江湖任务:1] （可获经验、装备、声望、金币）
				
				[领取每日随机任务:3] （每天有惊喜！33级可接）
				
				[领取每周循环任务:8] （每周有难度！35级可接）
				
				[新人进阶每周任务:9] （40-48级可接）
				
				[任务查询:5]
				
				[管理系统:4]
				
				[结束:0]""".format(SEnvir.Now.Year, SEnvir.Now.Month, SEnvir.Now.Day, SEnvir.Now.Hour, SEnvir.Now.Minute, SEnvir.StartTime.Year, SEnvir.StartTime.Month, SEnvir.StartTime.Day, SEnvir.StartTime.Hour, SEnvir.StartTime.Minute)
		else:
			say = """服务器当前时间：{}年{}月{}日{}时{}分
				服务器启动时间：{}年{}月{}日{}时{}分
				
				江湖上的朋友都叫我万拍子。
				不是我吹，你不了解的武功或其它的任务我都可以给你解答。
				你有什么想问的吗？
				
				[江湖任务:1] （可获经验、装备、声望、金币）
				
				[领取每日随机任务:3] （每天有惊喜！33级可接）
				
				[领取每周循环任务:8] （每周有难度！35级可接）
				
				[新人进阶每周任务:9] （40-48级可接）
				
				[任务查询:5]

				[结束:0]""".format(SEnvir.Now.Year, SEnvir.Now.Month, SEnvir.Now.Day, SEnvir.Now.Hour, SEnvir.Now.Minute, SEnvir.StartTime.Year, SEnvir.StartTime.Month, SEnvir.StartTime.Day, SEnvir.StartTime.Hour, SEnvir.StartTime.Minute)

#[声望查询:6]

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(yaodiangoodslist)

NpcEvent.add_listener(50,"OnClick",OnClick)
NpcEvent.add_listener(75,"OnClick",OnClick)
#NpcEvent.add_listener(79,"OnClick",OnClick)
#NpcEvent.add_listener(123,"OnClick",OnClick)
#NpcEvent.add_listener(130,"OnClick",OnClick)
