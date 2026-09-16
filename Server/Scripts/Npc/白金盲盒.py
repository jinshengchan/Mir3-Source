# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
from Defines import *
import PlayerEvent
import Server
import random
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
import System
s1 = clr.Reference[System.Object]()
from Utils.TimeUtil import *
import os
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
rewards888 = [
					('白色口哨碎片', 1, False, 80),
					('魔晶石', 1, False, 2),
					('虹魔项链', 1, False, 6),
					('十方斩（残页）', 1, False, 4),
					('移花接玉（残页）', 1, False, 4),
					('魄冰刺（残页）', 1, False, 4),
					('白色虎齿项链碎片', 1, False, 15),
					('幸运斗笠碎片', 1, False, 15),
					('万年雪霜', 50, False, 80),
					('万年雪霜', 50, False, 90),
					('万年雪霜', 50, False, 100),
					('祝福油', 3, False, 80),
					('祝福油', 3, False, 80),
					('虹魔手镯', 1, False, 6),
					('破坏项链', 1, False, 3),
					('昏暗封印', 1, False, 3),
					('怨恨项链', 1, False, 3),
					('自然神水（特）', 1, False, 150),
					('攻击神水（特）', 1, False, 150),
					('体力强效神水（特）', 1, False, 150),
					('疾风神水（特）', 1, False, 150),
					('灵魂神水（特）', 1, False, 150),
					('骑士手镯', 1, False, 6),
					('心灵手镯', 1, False, 6),
					('龙之手镯', 1, False, 6),
					('润神戒指', 1, False, 6),
					('帝王戒指', 1, False, 6),
					('雷神戒指', 1, False, 6),
					('藏罪据证', 1, False, 100),
					('金色栗子', 3, False, 200),
					('双倍经验卷', 1, False, 100),
					('亡灵之药水', 1, False, 10),
					('金条', 1, False, 20),
					('武器强化油', 10, False, 200),
					('莲丸戒指', 1, False, 2),
					('石榴戒指', 1, False, 2),
					('魔灵戒指', 1, False, 2),
					('魔令项链', 1, False, 6),
					('追魂项链', 1, False, 6),
					('追风项链', 1, False, 6),
					('铁系项链', 1, False, 6),
					('紫碧螺', 1, False, 13),
					('泰坦戒指', 1, False, 13),
					('躲避手链', 1, False, 30),
					('夏普儿手镯', 1, False, 30),
					('恶魔铃铛', 1, False, 13),
					('灵魂项链', 1, False, 13),
					('绿色项链', 1, False, 13),
					('旋风流星刀', 1, False, 1),
					('飞魂魔刃', 1, False, 1),
					('封魔剑', 1, False, 1),
					('凝血离魂（残页）', 1, False, 1),
					('破血狂杀（残页）', 1, False, 1),
					('阴阳法环（残页）', 1, False, 1),
					('妙影无踪（残页）', 1, False, 1),
					('焰天火雨（残页）', 1, False, 2),
					('铁布衫（残页）', 1, False, 2),
					('怒神霹雳（残页）', 1, False, 2),
					('魄冰刺（残页）', 1, False, 2),
					('云寂术（残页）', 1, False, 2),
					('十方斩（残页）', 1, False, 2),
					('移花接玉（残页）', 1, False, 2),
					('斗转星移（残页）', 1, False, 2),
					('乾坤大挪移（残页）', 1, False, 2),
					('师承戒指', 1, False, 1),
					('破荒项链', 1, False, 1),
					('金棱手镯', 1, False, 1),
					('青云戒指', 1, False, 1),
					('世尊手镯', 1, False, 1),
					('定心项链', 1, False, 1),
					('龙马戒指', 1, False, 1),
					('思过手镯', 1, False, 1),
					('魔云项链', 1, False, 1),
					]

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}	

#判断是否有要求的道具
	if (Menu == 1):
		if (Sender.GetItemCount("盲盒钥匙") < 1):
			say ="""你没有盲盒钥匙无法使用。
			
			[关闭:0]"""
		else:
#上面条件都达成，扣除道具，给予道具
			Sender.TakeItem("盲盒钥匙",1)
			Sender.TakeItem("白金盲盒",1)
			# 最终奖励
			converted_reward = []
			for item in rewards888:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("白金盲盒", "运营团队", "你打开了白金盲盒, 请领取你的奖励", my_reward)
			BroadChat('恭喜玩家 {} 开启装备白金盲盒，获得 {}'.format(Sender.Name, my_reward[0][0]))
			return

	elif (Menu == 2):
		if (Sender.Prestige < 100):
			say ="""你的声望不足100点无法打开盲盒。
			
			[关闭:0]"""
		else:
			SubPrestige(Sender,100)
			Sender.TakeItem("白金盲盒",1)
			# 最终奖励
			converted_reward = []
			for item in rewards888:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("白金盲盒", "运营团队", "你打开了白金盲盒, 请领取你的奖励", my_reward)
			BroadChat('恭喜玩家 {} 开启装备白金盲盒，获得 {}'.format(Sender.Name, my_reward[0][0]))
			return
	elif (Menu == 3):
		if (Sender.Gold < 200000):
			say ="""你的金币不足无法打开盲盒。
			
			[关闭:0]"""
		else:
			SubGold(Sender,200000)
			Sender.TakeItem("白金盲盒",1)
			# 最终奖励
			converted_reward = []
			for item in rewards888:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("白金盲盒", "运营团队", "你打开了白金盲盒, 请领取你的奖励", my_reward)
			BroadChat('恭喜玩家 {} 开启装备白金盲盒，获得 {}'.format(Sender.Name, my_reward[0][0]))
			return
#主菜单
	else:
		say = """[20万金币开启白金盲盒:3]"""
		
#[盲盒钥匙开启金质盲盒:1]
#[声望100点开启金质盲盒:2]

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(379,"OnClick",OnClick)