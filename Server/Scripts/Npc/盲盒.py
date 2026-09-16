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
					('金创药（特）', 50, False, 100),
					('金创药（大）', 100, False, 200),
					('金创药（中）', 200, False, 300),
					('魔法药（特）', 50, False, 100),
					('魔法药（大）', 100, False, 200),
					('魔法药（中）', 200, False, 300),
					('太阳水', 100, False, 200),
					('强效太阳水', 80, False, 150),
					('万年雪霜', 50, False, 100),
					('祝福油', 10, False, 100),
					('僵尸骨头', 200, False, 100),
					('牙齿', 50, False, 200),
					('夜明珠', 50, False, 200),
					('震天魔印', 50, False, 200),
					('骑士手镯', 1, False, 30),
					('心灵手镯', 1, False, 30),
					('龙之手镯', 1, False, 30),
					('润神戒指', 1, False, 30),
					('帝王戒指', 1, False, 30),
					('雷神戒指', 1, False, 30),
					('藏罪据证', 1, False, 100),
					('金色栗子', 3, False, 200),
					('潘夜之泪', 50, False, 200),
					('神灵雕像', 50, False, 200),
					('金条', 1, False, 20),
					('武器强化油', 10, False, 200),
					('昏暗封印（冰）', 1, False, 30),
					('昏暗封印（雷）', 1, False, 30),
					('昏暗封印（风）', 1, False, 30),
					('昏暗封印（火）', 1, False, 30),
					('怨恨项链（暗黑）', 1, False, 30),
					('怨恨项链（神圣）', 1, False, 30),
					('力量戒指', 1, False, 30),
					('紫碧螺', 1, False, 30),
					('泰坦戒指', 1, False, 30),
					('躲避手链', 1, False, 60),
					('夏普儿手镯', 1, False, 60),
					('恶魔铃铛', 1, False, 30),
					('灵魂项链', 1, False, 30),
					('绿色项链', 1, False, 30),
					('潘夜无名刀', 1, False, 5),
					('潘夜血饮', 1, False, 5),
					('潘夜炼狱', 1, False, 5),
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
			Sender.TakeItem("盲盒",1)
			# 最终奖励
			converted_reward = []
			for item in rewards888:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("盲盒", "运营团队", "你打开了盲盒, 请领取你的奖励", my_reward)
			BroadChat('恭喜玩家 {} 开启装备盲盒，获得 {}'.format(Sender.Name, my_reward[0][0]))
			return

	elif (Menu == 2):
		if (Sender.Prestige < 100):
			say ="""你的声望不足100点无法打开盲盒。
			
			[关闭:0]"""
		else:
			SubPrestige(Sender,100)
			Sender.TakeItem("盲盒",1)
			# 最终奖励
			converted_reward = []
			for item in rewards888:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("盲盒", "运营团队", "你打开了盲盒, 请领取你的奖励", my_reward)
			BroadChat('恭喜玩家 {} 开启装备盲盒，获得 {}'.format(Sender.Name, my_reward[0][0]))
			return
	elif (Menu == 3):
		if (Sender.Gold < 200000):
			say ="""你的金币不足无法打开盲盒。
			
			[关闭:0]"""
		else:
			SubGold(Sender,200000)
			Sender.TakeItem("盲盒",1)
			# 最终奖励
			converted_reward = []
			for item in rewards888:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("盲盒", "运营团队", "你打开了盲盒, 请领取你的奖励", my_reward)
			BroadChat('恭喜玩家 {} 开启装备盲盒，获得 {}'.format(Sender.Name, my_reward[0][0]))
			return
#主菜单
	else:
		say = """[20万金币开启盲盒:3]"""
		
#[盲盒钥匙开启盲盒:1]
#[声望100点开启盲盒:2]

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(330,"OnClick",OnClick)