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
from System import *
clr.ImportExtensions(System.Linq)
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import unicodedata
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Defines import *
import Server


# 使用注意
# 本脚本并未检查是否存在交叉背号
# 即允许A和B互相背 允许A背B同时B背C


# 个人变量序号 确保不跟已使用的个人变量序号重复即可
# 暂时只允许1个主号 主号变量定义
MASTER_KEYS = [101]
#设置可带人数变量，131 132 为2人，类推 133 134
SLAVE_KEYS = [131, 132]
#申请列表，按你限制的人数增加变量
APPLICATION_KEYS = [161, 162, 163]

# 背号buff序号 注意是自定义buff
BUFF_INDEX = 109
# 几秒传送1次
TELEPORT_DELAY = 1
# 限制传送的地图index
RESTRICTED_MAPS = [25, 84, 142, 157, 176,
                   246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262,  #神舰
                   277, 297, 298, 302, 303, 354, 355, 360, 361,
                   364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374,      #诺玛
                   382, 383, 384, 385, 386, 387, 486, 487, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502,
                   509, 510, 511, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534,
                   1018, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514,
                   1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1526, 1527, 1528, 1529, 1530]


def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	say = "OK"

	if Menu == 1:
		slaves = "\n"
		for slave_key in SLAVE_KEYS:
			slave_index = (int) (PlayerGetV(Sender, slave_key))
			if slave_index != 0:
				slave_char = SEnvir.GetCharacter(slave_index)
				slave_obj = SEnvir.GetPlayerByCharacter(slave_char.CharacterName)
				online = "在线" if slave_obj else "不在线"
				slaves += "{} [停止背:{}] \n".format(slave_char.CharacterName, slave_key+2000)

		say = """
		我的副号:

		{}


		[添加:11] 添加副号
		[删除:12] 删除副号

		""".format(slaves)

	elif Menu == 11:
		text = "\n"
		approve_menu = 1100
		for index, app_key in enumerate(APPLICATION_KEYS):
			app = (int) (PlayerGetV(Sender, app_key))
			if app != 0:
				name = SEnvir.GetCharacter((int) (PlayerGetV(Sender, app_key))).CharacterName
				text += "{}  [通过:{}] [删除:{}]\n".format(name, approve_menu+index, approve_menu+3+index)
				Sender.Connection.ReceiveChat(str(approve_menu),MessageType.System)

		say = """
		我的申请:


		""" + text

	elif Menu >= 1100 and Menu < 2000:
		if Menu < 1103:
			#通过
			app = APPLICATION_KEYS[(Menu - 1100)]
			salve_char = SEnvir.GetCharacter((int) (PlayerGetV(Sender, app)))
			salve_obj = SEnvir.GetPlayerByCharacter(salve_char.CharacterName)
			if not salve_obj or salve_obj.Character.CharacterName != salve_char.CharacterName:
				say = "副号不在线 无法添加"
			else:
				#添加进列表
				add_slave_sig = AddSlave(Sender)  # 除了表示布尔值外还表示位置
				if add_slave_sig != False:
					add_master_sig = AddMaster(salve_obj) # 除了表示布尔值外还表示位置
					if add_master_sig:
						# 向主号增加副号
						PlayerSetV(Sender, add_slave_sig, (int) (PlayerGetV(Sender, app)))
						# 向副号增加主号
						PlayerSetV(salve_obj, add_master_sig, Sender.Character.Index)
						PlayerSetV(Sender, app, 0)
						salve_obj.Connection.ReceiveChat("你成为{}副号的申请已通过。".format(Sender.Character.CharacterName),MessageType.System)
						say = "完成"
					else:
						say = "副号添加主号发生错误，列表已满（副号最多一个主号）"
				else:
					say = "主号添加副号发生错误，主号列表已满（主号最多两个副号）"

		else:
			#拒绝
			app = APPLICATION_KEYS[(Menu - 1103)]
			PlayerSetV(Sender, app, 0)
			say = "已删除此申请"

	elif Menu >= 2000:
		slave_char_index = (int) (PlayerGetV(Sender, Menu-2000))
		if slave_char_index != 0:
			slave_char = SEnvir.GetCharacter(slave_char_index)
			if slave_char:
				slave_obj = SEnvir.GetPlayerByCharacter(slave_char.CharacterName)
				if slave_obj:
					StopSlaveFollowing(slave_obj)
					say = "停止背{}".format(slave_char.CharacterName)
				else:
					say = "{}不在线".format(slave_char.CharacterName)
			else:
				say = "找不到副号角色信息"
		else:
			say = "找不到副号信息"


	elif Menu == 12:
		say = """
		删除副号

		[输入副号名字:121] 输入副号的名字：

		"""

	elif Menu == 121:
		DeleteSlaveName([Sender])
		say = """删除副号

		请输入对方角色名
		
		[离开:0]"""


	elif Menu == 2:
		text = "\n"
		for master_key in MASTER_KEYS:
			master_char_index = (int) (PlayerGetV(Sender, master_key))
			if master_char_index != 0:
				master_char = SEnvir.GetCharacter(master_char_index)
				text += master_char.CharacterName + "\n"
		say = """
		我的主号:

		{}


		[添加:21] 添加主号
		[删除:22] 删除主号

		""".format(text)

	elif Menu == 21:
		say = """
		添加主号


		[输入主号名字:211] 输入主号的名字：

		"""

	elif Menu == 211:
		InputMaterName([Sender])
		say = """添加主号

		请输入对方角色名
		
		[离开:0]"""


	elif Menu == 22:
		say = """
		删除主号

		[输入主号名字:221] 输入主号的名字：

		"""
	elif Menu == 221:
		DeleteMaterName([Sender])
		say = """删除主号

		请输入对方角色名
		
		[离开:0]"""

	elif Menu == 3:
		master_char_index = (int) (PlayerGetV(Sender, MASTER_KEYS[0]))
		master_char = SEnvir.GetCharacter(master_char_index)
		if master_char:
			mater_obj = SEnvir.GetPlayerByCharacter(master_char.CharacterName)
			if mater_obj:
				StartFollowing([mater_obj, Sender])
				say = "开始跟随"
			else:
				say = "主号不在线"
		else:
			say = "找不到主号"

	elif Menu == 4:
		say = """<font color=\"0xffff0000\">注意：购买背号功能只需要小号购买，带人的主号是不需要购买的。</font>
		
		背号BUFF使用时间为7天，时间到自动消失。
		背号BUFF购买使用需要花费<font color=\"0xff00ff00\">500W金币</font>，是否需要购买？
		
		[购买背号BUFF:5]
		
		[离开:0]
		"""
	elif Menu == 5:
		#判断需要的金币
		if (Sender.Gold < 5000000):
			say = """你没有足够的金币，无法购买背号BUFF。
			
			[离开:0]"""
		else:
#上面条件达成，扣除金币，赋值自定义BUFF
			SubGold(Sender,5000000)
			Sender.CustomBuffAdd(BUFF_INDEX)    #给玩家赋值自定义背号BUFF
			say="""你获得5天背号BUFF。
			
			[离开:0]"""
	elif Menu == 998:
		StopFollowing(Sender)
		return
#主菜单
	else:
		say = """<font color=\"0xff00ff00\">背号练级</font>
		<font color=\"0xffff0000\">注意：添加或删除时，双方必须都在线</font>
		<font color=\"0xffff0000\">注意：互为好友才可以使用</font>
		<font color=\"0xffff0000\">允许好友命令：@允许好友  </font>
		<font color=\"0xffff0000\">添加好友命令：@添加好友 潘金莲</font>

		[主号选项:1] 我是主号

		[副号选项:2] 我是副号

		[开始跟随主号:3] 开始跟随主号

		[我是副号停止跟随:998] 我是副号停止跟随主号


		主号主动停止背副号请点击 "主号选项" 选择停止的对象


		[小号购买背号功能:4] 主号无需购买，需要被带的小号购买
		"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


def InputMaterName(params):
	player = params[0]
	player_name = player.Character.CharacterName
	player.Connection.ReceiveChat(str(player.Character.CharacterName),MessageType.System)
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None
	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
		player.PyInputBox("请输入主号名字", "Npc.背号功能.InputMaterName", "Npc.背号功能.InputMaterName")
	elif player_name == userInput:
		player.Connection.ReceiveChat("不能背自己哦~",MessageType.System)
		player.PyInputBox("请输入主号名字", "Npc.背号功能.InputMaterName", "Npc.背号功能.InputMaterName")
	else:
		player.Connection.ReceiveChat("用户输入了{}".format(userInput),MessageType.System)

		# 检查主号是否在线
		master = SEnvir.GetPlayerByCharacter(userInput)
		if not master or master.Character.CharacterName != userInput:
			player.Connection.ReceiveChat("找不到此角色或不在线",MessageType.System)
			return

		# 检查主号是否已经添加过此副号
		for slave_key in SLAVE_KEYS:
			slave_char_index = (int) (PlayerGetV(master, slave_key))
			if slave_char_index != 0:
				slave_char = SEnvir.GetCharacter(slave_char_index)
				if slave_char and slave_char.Index == player.Character.Index:
					player.Connection.ReceiveChat("你已经是对方的副号了，不能重复添加",MessageType.System)
					return

		# 判断是否申请互为主副号
		for slave_key in SLAVE_KEYS:
			slave_char_index = (int) (PlayerGetV(player, slave_key))
			if slave_char_index != 0:
				slave_name = SEnvir.GetCharacter(slave_char_index).CharacterName
				if userInput == slave_name:
					player.Connection.ReceiveChat("对方是你的副号了，不能添加为主号",MessageType.System)
					return

		# 判断是否重复申请
		for app_key in APPLICATION_KEYS:
			add_char_index = (int) (PlayerGetV(master, app_key))
			if add_char_index != 0:
				name = SEnvir.GetCharacter(add_char_index).CharacterName
				if name == player_name:
					player.Connection.ReceiveChat("你已经申请了，不要重复申请。",MessageType.System)
					return


		# 将申请写入主号
		for app_key in APPLICATION_KEYS:
			app_char_index = (int) (PlayerGetV(master, app_key))
			if app_char_index == 0:
				PlayerSetV(master, app_key, player.Character.Index)
				player.Connection.ReceiveChat("申请成功，请通知对方通过",MessageType.System)
				master.Connection.ReceiveChat("你收到了{}成为你副号的申请".format(player.Character.CharacterName),MessageType.System)
				return

		player.Connection.ReceiveChat("申请发生错误，可能是主号列表满了",MessageType.System)


def DeleteMaterName(params):
	# 我是副号
	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
		player.PyInputBox("请输入主号名字", "Npc.背号功能.DeleteMaterName", "Npc.背号功能.DeleteMaterName")
	else:
		player.Connection.ReceiveChat("用户输入了{}".format(userInput),MessageType.System)

		# 检查主号是否在线
		master = SEnvir.GetPlayerByCharacter(userInput)
		if not master or master.Character.CharacterName != userInput:
			player.Connection.ReceiveChat("找不到此角色或不在线",MessageType.System)
			return

		# 检查主号是否已经添加过自己
		target_slave = 0
		for slave_key in SLAVE_KEYS:
			slave_char_index = (int) (PlayerGetV(master, slave_key))
			if slave_char_index != 0:
				slave_char = SEnvir.GetCharacter(slave_char_index)
				if slave_char and slave_char.Index == player.Character.Index:
					target_slave = slave_key

		# 检查自己是否存在要删除的主号
		target_master = 0
		for master_key in MASTER_KEYS:
			master_char_index = (int) (PlayerGetV(player, master_key))
			if master_char_index != 0:
				if master_char_index == master.Character.Index:
					target_master = master_key


		if target_master == 0 and target_slave == 0:
			player.Connection.ReceiveChat("{}不是你的主号。".format(master.Character.CharacterName),MessageType.System)
			return


		# 从主号中移除自己
		PlayerSetV(master, target_slave, 0)
		master.Connection.ReceiveChat("你的副号{}已经将你移除".format(player.Character.CharacterName),MessageType.System)
		# 移除主号
		PlayerSetV(player, target_master, 0)
		player.Connection.ReceiveChat("删除主号成功",MessageType.System)


def DeleteSlaveName(params):
	# 我是主号
	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
		player.PyInputBox("请输入副号名字a", "Npc.背号功能.DeleteSlaveName", "Npc.背号功能.DeleteSlaveName")
	else:
		# 检查副号是否在线
		slave = SEnvir.GetPlayerByCharacter(userInput)
		if not slave or slave.Character.CharacterName != userInput:  # 输入副号的其他角色名不属于在线
			player.Connection.ReceiveChat("找不到此角色或不在线",MessageType.System)
			return

		# 检查自己是否存在要删除的副号
		target_slave = 0
		for slave_key in SLAVE_KEYS:
			slave_char_index = (int) (PlayerGetV(player, slave_key))
			if slave_char_index != 0:
				slave_char = SEnvir.GetCharacter(slave_char_index)
				if slave_char and slave_char.Index == slave.Character.Index:
					target_slave = slave_key


		# 检查副号是否已经添加过自己
		target_master = 0
		for master_key in MASTER_KEYS:
			master_char_index = (int) (PlayerGetV(slave, master_key))
			if master_char_index != 0:
				if master_char_index == player.Character.Index:
					target_master = master_key


		if target_master == 0 and target_slave == 0:
			player.Connection.ReceiveChat("{}不是你的副号。".format(slave.Character.CharacterName),MessageType.System)
			return

		# 从副号中移除自己
		PlayerSetV(slave, target_master, 0)
		slave.Connection.ReceiveChat("你的主号{}已经将你移除".format(player.Character.CharacterName),MessageType.System)
		# 移除副号
		PlayerSetV(player, target_slave, 0)
		player.Connection.ReceiveChat("删除副号成功",MessageType.System)


# 向副号添加主号
def AddMaster(slave):
	for master_key in MASTER_KEYS:
		master_char_index = (int) (PlayerGetV(slave, master_key))
		if master_char_index == 0:
			# 找到空位 可以添加
			return master_key
	return False


# 向主号添加副号
def AddSlave(master):
	for slave_key in SLAVE_KEYS:
		slave_char_index = (int) (PlayerGetV(master, slave_key))
		if slave_char_index == 0:
			# 找到空位 可以添加
			return slave_key
	return False


def StartFollowing(params):
	master = params[0]
	slave = params[1]

	# 副号掉线或其他情况 退出
	if len(params) != 2 or not slave:
		#移除定时脚本
		SEnvir.RemoveScript("Npc.背号功能.StartFollowing", slave)
		return

	# 检查主号是否在线
	if not master:
		slave.Connection.ReceiveChat("主号不在线",MessageType.System)
		#移除定时脚本
		SEnvir.RemoveScript("Npc.背号功能.StartFollowing", slave)
		return

	# 检查主号是否在限制地图
	if master.CurrentMap.Info.Index in RESTRICTED_MAPS:
		slave.Connection.ReceiveChat("主号在限制地图，无法跟随",MessageType.System)
		#移除定时脚本
		SEnvir.RemoveScript("Npc.背号功能.StartFollowing", slave)
		return

	# 检查是否有背号buff
	if slave.HasCustomBuff(BUFF_INDEX):
		slave.Teleport(master.CurrentMap, master.CurrentMap.GetRandomLocation(master.CurrentLocation, 3))
		Server.Envir.SEnvir.DelayCall("Npc.背号功能.StartFollowing", TELEPORT_DELAY, (master, slave), slave)
	else:
		slave.Connection.ReceiveChat("你没有背号Buff",MessageType.System)
		return

	# 检查副号是否死亡
	if slave.Dead:
		slave.TownRevive()


def StopFollowing(slave):
	SEnvir.RemoveScript("Npc.背号功能.StartFollowing", slave)


def StopSlaveFollowing(slave):
	SEnvir.RemoveScript("Npc.背号功能.StartFollowing", slave)

# 这里绑定NPC序号
NpcEvent.add_listener(221,"OnClick",OnClick)