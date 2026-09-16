# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import random
import Utils
import NpcEvent

clr.AddReference("Library")
clr.AddReference("System")
from Library import *
import Server.Envir.SEnvir as SEnvir

clr.AddReference("IronPython.SQLite.dll")
import sqlite3
from datetime import datetime


# 数据库位置
# 例如 r"C:\sqlite\db\pythonsqlite.db"
CDKEY_DB_LOCATION = r"F:\桌面\145服务端\Database\cdkey.db"



def OnClick(args):
	Self = args[0]
	player = args[1]
	Menu = args[2]
	Dict={}
	say = ""

	if Menu == 1:
		say = """请输入兑换码

		[输入兑换码:2]

		"""

	elif Menu == 2:
		InputCDKey([player])

	else:
		say = """

		CDKEY兑换系统

		[兑换:2] 兑换CDKEY
		
		[关闭:0]

		"""

	Dict["Say"]=say                         #定义聊天框对话内容
	return Dict

def InputCDKey(params):
	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
		player.PyInputBox("请输入卡号", "Npc.卡密充值.InputCDKey", "Npc.卡密充值.InputCDKey")
	else:
		player.Connection.ReceiveChat("用户输入了{}".format(userInput),MessageType.System)
		use_code(player, userInput, player.Character.Account.EMailAddress)
		

########################################################
# 数据库操作
########################################################
def open_connection():
	# sqlite连接
	con = sqlite3.connect(CDKEY_DB_LOCATION)
	return con


def save_and_close(con):
	con.commit()
	con.close()


def fetch_unused_code(code):
	con = open_connection()
	cur = con.cursor()
	res = cur.execute(u"""SELECT * FROM "UnusedCodes" where "Code" = ? and "RemainingUse" >= 0""", (code,)).fetchone()
	save_and_close(con)
	return res

def fetch_used_codes(code, account=None):
	res = None
	con = open_connection()
	cur = con.cursor()
	if account:
		res = cur.execute(u"""SELECT * FROM "UsedCodes" where "Code" = ? and "使用账号" = ?""", (code,account)).fetchall()
	res = cur.execute(u"""SELECT * FROM "UsedCodes" where "Code" = ?""", (code,)).fetchall()
	save_and_close(con)
	return res


def verify_code(code):
	res = fetch_unused_code(code)
	return res is not None


def check_remaining_use(code):
	res = fetch_unused_code(code)
	if res:
		return res[5] > 0
	return False


def check_account_limit(code, account):
	# 先拿到单账号最大使用次数
	unused = fetch_unused_code(code)
	if unused:
		max_limit = unused[6]
		# 最大次数为0 是不限制
		if max_limit == 0:
			return True
		# 再检查账号已使用的次数
		used = fetch_used_codes(code, account)
		if used and len(used) < max_limit:
			return True
		if not used and max_limit > 0:
			return True

	return False


def check_can_use_code(code, account):
	if not verify_code(code):
		
		return "无效的兑换码"

	if not check_remaining_use(code):
		return "此兑换码已没有剩余兑换次数"

	if not check_account_limit(code, account):
		return "此账户已超过最大兑换次数"

	return "OK"


def use_code(player, code, account):
	msg = check_can_use_code(code, account)
	if msg != "OK":
		player.Connection.ReceiveChat("兑换失败: {}".format(msg),MessageType.System)
		return False
	else:
		write_use_record(code, account)
		record = fetch_unused_code(code)
		send_items(player, record[2], record[3], record[4])
		return True


def write_use_record(code, account):
	con = open_connection()
	cur = con.cursor()
	# 剩余兑换次数-1
	cur.execute(u"""UPDATE "UnusedCodes" SET "RemainingUse"="RemainingUse"-1 WHERE "Code" = ?""", (code,))
	# 写入使用记录
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	cur.execute(u"""INSERT INTO "UsedCodes"("Code","Account","Time") VALUES(?,?,?)""", (code, account,dt_string))
	save_and_close(con)


def send_items(player, item_name, amount, bound):
	is_bound = True
	if bound == 0:
		is_bound = False
	item = (item_name, amount, is_bound)
	reward = []
	reward.append(item)
	player.PYMailSend("充值码兑换", "运营团队", "你成功兑换了以下物品", reward)


NpcEvent.add_listener(329,"OnClick",OnClick)
