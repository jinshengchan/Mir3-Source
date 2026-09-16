# -*- coding: utf-8 -*-
# 载入模块SYS
import datetime
import os
import sys
# 引用模块的地址
from Globals import *
import clr
import Server
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent


# 回收数据存储位置
# 可以修改 但是需要手动创建好文件夹
FILE_PATH = u"D:\Server\回收记录"


def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	userInput = ""
	if len(args) > 3 and len(args[3]) > 0:
		userInput = args[3]
	res = ""
	Dict = {}

	if Menu == 1:
		res = """要回收什么？

		[100元红包:2]"""
	elif Menu == 2:
		if int(Sender.GetItemCount("100元红包")) > 0:
			Sender.NPCConfirmationBox("100元红包 回收价100元 确定吗", 3)
			PlayerSetTempV(Sender, TV_PLAYER_RECYCLE_ITEM, "100元红包")
			res = "第一步"
		else:
			res = """你背包里并没有这个物品
			
			[关闭:0]"""

	elif Menu == 3:
		res = """第二步: 请选择
			
			提醒：玩家务必截图留存并发给管理

			[微信:4]
			[支付宝:5]"""

	elif Menu == 4:
		Sender.NPCTextInputBox("请输入微信账号:", 6)
		res = "第三步"
		PlayerSetTempV(Sender, TV_PAYMENT_METHOD, "微信")

	elif Menu == 5:
		Sender.NPCTextInputBox("请输入支付宝账号:", 6)
		res = "第三步"
		PlayerSetTempV(Sender, TV_PAYMENT_METHOD, "支付宝")

	elif Menu == 6:
		PlayerSetTempV(Sender, TV_PAYMENT_ACCOUNT, userInput)
		res = "你输入的支付账号是: " + userInput

		Sender.NPCTextInputBox("请输入电话号码:", 7)

	elif Menu == 7:
		PlayerSetTempV(Sender, TV_PLAYER_PHONE, userInput)
		res = """你输入的电话号码是: {}
			[下一步:8]""".format(userInput)

	elif Menu == 8:
		payment_method = PlayerGetTempV(Sender, TV_PAYMENT_METHOD)
		payment_account = PlayerGetTempV(Sender, TV_PAYMENT_ACCOUNT)
		phone_number = PlayerGetTempV(Sender, TV_PLAYER_PHONE)
		recycle_item = PlayerGetTempV(Sender, TV_PLAYER_RECYCLE_ITEM)

		if not payment_method or not payment_account:
			res = "支付账号记录失败"

		if not phone_number:
			res = "手机号记录失败"

		if not recycle_item:
			res = "回收物品记录失败"

		if payment_method and payment_account and phone_number and recycle_item:

			res = """你的{}账号是: {}, 你的手机号是{}, 将要回收的物品是 {}, 回收价格 {}, 
			点击确定后, 会扣除此物品，同时记录以上信息，将有客服联系你进行下一步
			
			[确定:9]

			[关闭:0]""".format(payment_method, payment_account, phone_number, recycle_item, 100 )

	elif Menu == 9:
		payment_method = PlayerGetTempV(Sender, TV_PAYMENT_METHOD)
		payment_account = PlayerGetTempV(Sender, TV_PAYMENT_ACCOUNT)
		phone_number = PlayerGetTempV(Sender, TV_PLAYER_PHONE)
		recycle_item = PlayerGetTempV(Sender, TV_PLAYER_RECYCLE_ITEM)

		item_count = int(Sender.GetItemCount(recycle_item))
		if item_count < 1:
			return {"Say": "你没有".format(recycle_item)}

		file_name = Sender.Character.CharacterName + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"

		with open(os.path.join(FILE_PATH, file_name), "a") as the_file:
			the_file.write("游戏账号: {}\n".format(Sender.Character.Account.EMailAddress).encode('utf8'))
			the_file.write("玩家角色: {}\n".format(Sender.Character.CharacterName).encode('utf8'))
			the_file.write("支付方式: {}\n".format(payment_method).encode('utf8'))
			the_file.write("支付账号: {}\n".format(payment_account).encode('utf8'))
			the_file.write("手机号码: {}\n".format(phone_number).encode('utf8'))
			the_file.write("回收道具: {}\n".format(recycle_item).encode('utf8'))

		Sender.TakeItem(recycle_item, 1)
		res = """记录完毕，请等待客服处理
		
		[关闭:0]"""
	elif Menu == 20:
		res = """我这里提供兑换红包业务，你可以将零散的红包在我这里兑换成100元红包
		
		[1元红包兑换:21]     [2元红包兑换:22]      [5元红包兑换:23]
		
		[10元红包兑:24]     [50元红包兑换:26]
		
		[3元红包兑换1元红包:27]    [15元红包兑换5元红包:28]
		
		[关闭:0]"""
	elif Menu == 21:
		if(Sender.GetItemCount("1元红包") < 100):
			res ="""你的红包不足100个。

			[关闭:0]"""
		else:
			Sender.TakeItem("1元红包",100)
			Sender.GiveItem("100元红包",1)
			res="""兑换成功。

			[继续兑换:20]
			
			[关闭:0]"""
	elif Menu == 22:
		if(Sender.GetItemCount("2元红包") < 50):
			res ="""你的红包不足50个。

			[关闭:0]"""
		else:
			Sender.TakeItem("2元红包",50)
			Sender.GiveItem("100元红包",1)
			res="""兑换成功。

			[继续兑换:20]
			
			[关闭:0]"""
	elif Menu == 23:
		if(Sender.GetItemCount("5元红包") < 20):
			res ="""你的红包不足20个。

			[关闭:0]"""
		else:
			Sender.TakeItem("5元红包",20)
			Sender.GiveItem("100元红包",1)
			res="""兑换成功。

			[继续兑换:20]
			
			[关闭:0]"""
	elif Menu == 24:
		if(Sender.GetItemCount("10元红包") < 10):
			res ="""你的红包不足10个。

			[关闭:0]"""
		else:
			Sender.TakeItem("10元红包",10)
			Sender.GiveItem("100元红包",1)
			res="""兑换成功。

			[继续兑换:20]
			
			[关闭:0]"""
	elif Menu == 26:
		if(Sender.GetItemCount("50元红包") < 2):
			res ="""你的红包不足2个。

			[关闭:0]"""
		else:
			Sender.TakeItem("50元红包",2)
			Sender.GiveItem("100元红包",1)
			res="""兑换成功。

			[继续兑换:20]
			
			[关闭:0]"""
	elif Menu == 27:
		if(Sender.GetItemCount("3元红包") < 1):
			res ="""你的红包不足。

			[关闭:0]"""
		else:
			Sender.TakeItem("3元红包",1)
			Sender.GiveItem("1元红包",3)
			res="""兑换成功。

			[继续兑换:27]
			
			[关闭:0]"""
	elif Menu == 28:
		if(Sender.GetItemCount("15元红包") < 1):
			res ="""你的红包不足。

			[关闭:0]"""
		else:
			Sender.TakeItem("15元红包",1)
			Sender.GiveItem("5元红包",3)
			res="""兑换成功。

			[继续兑换:28]
			
			[关闭:0]"""
# 主菜单
	else:
		res = """目前我这里提供回收红包登记，
		你需要回收红包？
		
		[回收红包:1]          [兑换100元红包:20]
		
		[关闭:0]"""
	
	Dict['Say'] = res  # 定义聊天框对话内容
	return Dict

#NpcEvent.add_listener(305, "OnClick", OnClick)
