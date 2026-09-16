# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Library import *
from datetime import datetime, timedelta
import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)
import unicodedata
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Defines import *
import Server
clr.AddReference('System.Drawing')
import System.Drawing
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

MAX_PREFIX_LENGTH = 6  #设置文字的长度

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		#判断手上是否有武器
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			say = """你没有装备武器。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在武器上刻的名字
			
			[输入名字:11]
			
			[返回:99]"""
	elif (Menu == 11):
		SubGold(Sender,100000)   #扣除金币
		InputBoxWeapon([Sender])  #开始刻字
		return
	elif (Menu == 2):
		#判断手上是否有勋章
		if (not (Sender.Equipment[int(EquipmentSlot.Emblem)])):
			say = """你没有装备勋章。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在勋章上刻的名字
			
			[输入名字:21]
			
			[返回:99]"""
	elif (Menu == 21):
		SubGold(Sender,100000)   #扣除金币
		InputBoxEmblem([Sender])  #开始刻字
		return
	elif (Menu == 3):
		#判断手上是否有头盔
		if (not (Sender.Equipment[int(EquipmentSlot.Helmet)])):
			say = """你没有装备头盔。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在头盔上刻的名字
			
			[输入名字:31]
			
			[返回:99]"""
	elif (Menu == 31):
		SubGold(Sender,100000)   #扣除金币
		InputBoxHelmet([Sender])  #开始刻字
		return
	elif (Menu == 4):
		#判断手上是否有项链
		if (not (Sender.Equipment[int(EquipmentSlot.Necklace)])):
			say = """你没有装备项链。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在项链上刻的名字
			
			[输入名字:41]
			
			[返回:99]"""
	elif (Menu == 41):
		SubGold(Sender,100000)   #扣除金币
		InputBoxNecklace([Sender])  #开始刻字
		return
	elif (Menu == 5):
		#判断手上是否有衣服
		if (not (Sender.Equipment[int(EquipmentSlot.Armour)])):
			say = """你没有装备衣服。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在衣服上刻的名字
			
			[输入名字:51]
			
			[返回:99]"""
	elif (Menu == 51):
		SubGold(Sender,100000)   #扣除金币
		InputBoxArmour([Sender])  #开始刻字
		return
	elif (Menu == 6):
		#判断手上是否有鞋子
		if (not (Sender.Equipment[int(EquipmentSlot.Shoes)])):
			say = """你没有装备鞋子。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在鞋子上刻的名字
			
			[输入名字:61]
			
			[返回:99]"""
	elif (Menu == 61):
		SubGold(Sender,100000)   #扣除金币
		InputBoxShoes([Sender])  #开始刻字
		return
	elif (Menu == 7):
		#判断手上是否有盾牌
		if (not (Sender.Equipment[int(EquipmentSlot.Shield)])):
			say = """你没有装备盾牌。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在盾牌上刻的名字
			
			[输入名字:71]
			
			[返回:99]"""
	elif (Menu == 71):
		SubGold(Sender,100000)   #扣除金币
		InputBoxShield([Sender])  #开始刻字
		return
	elif (Menu == 8):
		#判断手上是否有左手镯
		if (not (Sender.Equipment[int(EquipmentSlot.BraceletL)])):
			say = """你没有装备左手镯。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在左手镯上刻的名字
			
			[输入名字:81]
			
			[返回:99]"""
	elif (Menu == 81):
		SubGold(Sender,100000)   #扣除金币
		InputBoxBraceletL([Sender])  #开始刻字
		return
	elif (Menu == 9):
		#判断手上是否有右手镯
		if (not (Sender.Equipment[int(EquipmentSlot.BraceletR)])):
			say = """你没有装备右手镯。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在右手镯上刻的名字
			
			[输入名字:91]
			
			[返回:99]"""
	elif (Menu == 91):
		SubGold(Sender,100000)   #扣除金币
		InputBoxBraceletR([Sender])  #开始刻字
		return
	elif (Menu == 10):
		#判断手上是否有左戒指
		if (not (Sender.Equipment[int(EquipmentSlot.RingL)])):
			say = """你没有装备左戒指。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在左戒指上刻的名字
			
			[输入名字:101]
			
			[返回:99]"""
	elif (Menu == 101):
		SubGold(Sender,100000)   #扣除金币
		InputBoxRingL([Sender])  #开始刻字
		return
	elif (Menu == 12):
		#判断手上是否有右戒指
		if (not (Sender.Equipment[int(EquipmentSlot.RingR)])):
			say = """你没有装备右戒指。

			[离开:0]"""
		#判断需要的金币
		elif (Sender.Gold < 100000):
			say = """你没有足够的金币，无法装备刻名。

			[离开:0]"""
		else:
			say = """请输入你要在右戒指上刻的名字
			
			[输入名字:121]
			
			[返回:99]"""
	elif (Menu == 121):
		SubGold(Sender,100000)   #扣除金币
		InputBoxRingR([Sender])  #开始刻字
		return
#主菜单
	else:
		say = """你好！欢迎使用装备刻名功能：
		此服务需要10W金币，请确定你选择的装备已经戴上，并且要刻的名字不能超6位！
		
		[［武器］:1]
		[［头盔］:3]          [［项链］:4]
		[［衣服］:5]          [［鞋子］:6]
		[［左手镯］:8]        [［右手镯］:9]
		[［左戒指］:10]        [［右戒指］:12]
		
		[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def InputBoxWeapon(params): #武器
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxWeapon", "Npc.装备刻名.InputBoxWeapon")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxWeapon", "Npc.装备刻名.InputBoxWeapon")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Weapon)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("武器刻名成功",MessageType.System)

def InputBoxEmblem(params): #勋章
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxEmblem", "Npc.装备刻名.InputBoxEmblem")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxEmblem", "Npc.装备刻名.InputBoxEmblem")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Emblem)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("勋章刻名成功",MessageType.System)

def InputBoxHelmet(params): #头盔
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxHelmet", "Npc.装备刻名.InputBoxHelmet")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxHelmet", "Npc.装备刻名.InputBoxHelmet")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Helmet)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("头盔刻名成功",MessageType.System)

def InputBoxNecklace(params): #项链
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxNecklace", "Npc.装备刻名.InputBoxNecklace")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxNecklace", "Npc.装备刻名.InputBoxNecklace")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Necklace)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("项链刻名成功",MessageType.System)

def InputBoxArmour(params): #衣服
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxArmour", "Npc.装备刻名.InputBoxArmour")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxArmour", "Npc.装备刻名.InputBoxArmour")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Armour)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("衣服刻名成功",MessageType.System)

def InputBoxShoes(params): #鞋子
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxShoes", "Npc.装备刻名.InputBoxShoes")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxShoes", "Npc.装备刻名.InputBoxShoes")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Shoes)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("鞋子刻名成功",MessageType.System)

def InputBoxShield(params): #盾牌
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxShield", "Npc.装备刻名.InputBoxShield")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxShield", "Npc.装备刻名.InputBoxShield")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Shield)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("盾牌刻名成功",MessageType.System)

def InputBoxBraceletL(params): #左手镯
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxBraceletL", "Npc.装备刻名.InputBoxBraceletL")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxBraceletL", "Npc.装备刻名.InputBoxBraceletL")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.BraceletL)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("左手镯刻名成功",MessageType.System)

def InputBoxBraceletR(params): #右手镯
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxBraceletR", "Npc.装备刻名.InputBoxBraceletR")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxBraceletR", "Npc.装备刻名.InputBoxBraceletR")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.BraceletR)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("右手镯刻名成功",MessageType.System)

def InputBoxRingL(params): #左戒指
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxRingL", "Npc.装备刻名.InputBoxRingL")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxRingL", "Npc.装备刻名.InputBoxRingL")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.RingL)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("左戒指刻名成功",MessageType.System)

def InputBoxRingR(params):
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput:
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxRingR", "Npc.装备刻名.InputBoxRingR")
	elif len(userInput) < 1 or len(userInput) > MAX_PREFIX_LENGTH:   #判断字符长度
		Sender.Connection.ReceiveChat("输入的名字不能超过6位，请重新输入",MessageType.System)
		Sender.PyInputBox("请输入名字", "Npc.装备刻名.InputBoxRingR", "Npc.装备刻名.InputBoxRingR")
	else:
		# SetItemCustomPrefix(物品, 定义前缀, 定义颜色)
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.RingR)], "{}".format(userInput), System.Drawing.Color.Yellow)
		Sender.Connection.ReceiveChat("右戒指刻名成功",MessageType.System)

#NpcEvent.add_listener(234,"OnClick",OnClick)
NpcEvent.add_listener(223,"OnClick",OnClick)