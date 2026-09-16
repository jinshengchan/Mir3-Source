# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import clr
clr.AddReference("System.Core")
clr.AddReference("Library")
clr.AddReference('System')
import System
clr.ImportExtensions(System.Linq)
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
from Library import *
import unicodedata
s1 = clr.Reference[System.Object]()
import Server
import PlayerEvent
import MapEvent
from Utils.TimeUtil import *
import datetime
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
	
	if (Menu == 3):
		# 计算下一个攻城日期
		war_date = GetNextWarDate()
		
		say = """为了申请攻城战需要祖玛头像。
		你有那个东西吗？
		攻城战将在 <font color=\"0xff00ff00\">{}</font> 开始。
		
		[前一步:99]""".format(war_date.strftime("%Y年%m月%d日 晚上8点"))

	elif Menu == 1:
		say = "下面是已经提交的攻城战:\n\n"
		count = 1
		for conquest in SEnvir.UserConquestList.Binding:
			war_time = conquest.WarDate + conquest.Castle.StartTime
			war_time_str = war_time.strftime("%Y年%m月%d日 %H:%M")
			say += '{}. {} 提交 {} 的攻城战\n 开始时间: {}\n'.format(count, conquest.Guild.GuildName, 
				conquest.Castle.Name, war_time_str)
			count += 1

	elif Menu == 2:
		# 检查是否已经有攻城申请
		if SEnvir.UserConquestList.Count > 0:
			say = """已经有攻城申请了，无法重复申请。
			
			[返回:0]"""
		else:
			# 检查玩家是否有祖玛头像
			if Sender.GetItemCount('祖玛头像') < 1:
				say = """你没有祖玛头像，无法申请攻城战。
				
				[返回:0]"""
			else:
				# 计算下一个攻城日期（固定为每周六晚上8点）
				war_date = GetNextWarDate()
				
				# 扣除祖玛头像
				Sender.TakeItem('祖玛头像', 1)
				
				# 申请攻城战
				Sender.GuildConquest(1)
				
				say = """攻城申请成功！
				
攻城战将在 {} 开始。
				
				[返回:0]""".format(war_date.strftime("%Y年%m月%d日 晚上8点"))
	elif Menu == 10:
		say ="""[看攻城战的日期:1]
		[沙巴克资金管理:11]
		[沙巴克城门管理:12]
		
		[结束:0]"""
	elif Menu == 11:
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#再判断占领沙巴克的行会名
		if guild:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			if(owner and Sender.Character.CharacterName == owner.CharacterName):
				if SEnvir.ConquestWars.Count > 0:  #正在攻城
					say = """正在进行攻城站，无法使用资金管理。
						
						[离开:0]"""
				else:
					# 获取沙巴克资金状况
					shabake = None
					for taxInfo in SEnvir.CastleFundInfoList.Binding:
						if taxInfo.Castle.Name == '沙巴克':
							shabake = taxInfo
							break
					say ="""沙巴克城 剩余资金：{} 金币
						
						[查看城堡财务:110]
						[提取沙巴克资金:111]
						[存入沙巴克资金:112]
						
						[结束:0]""".format(shabake.TotalFund)
			else:
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				return Dict
	elif Menu == 110:
		say = "下面是城堡的财务情况, 城堡占领行会可以提取或存入\n\n"
		for taxInfo in SEnvir.CastleFundInfoList.Binding:
			if taxInfo.Castle.Name == '沙巴克':
				say += "{}:\n税收 {} 金币\n存款 {} 金币\n合计 {} 金币\n".format(taxInfo.Castle.Name, taxInfo.TotalTax, taxInfo.TotalDeposit, taxInfo.TotalFund)

	elif Menu == 111:
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#再判断占领沙巴克的行会名
		if guild:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			if(owner and Sender.Character.CharacterName == owner.CharacterName):
				Sender.PyInputBox("请输入提取金额", "Npc.沙巴克城.沙巴克管理员.Withdraw", "Npc.沙巴克城.沙巴克管理员.Withdraw")
			else:
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				return Dict
	elif Menu == 112:
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#再判断占领沙巴克的行会名
		if guild:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			if(owner and Sender.Character.CharacterName == owner.CharacterName):
				Sender.PyInputBox("请输入存入金额", "Npc.沙巴克城.沙巴克管理员.Deposit", "Npc.沙巴克城.沙巴克管理员.Deposit")
			else:
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				return Dict
	elif Menu == 12:
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#再判断占领沙巴克的行会名
		if guild:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			if(owner and Sender.Character.CharacterName == owner.CharacterName):
				say ="""沙巴克城状态
				
				[正中城门:121]
				[左侧城门:122]
				[右侧城门:123]
				
				[结束:0]"""
			else:
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本警报：{} 使用封包挂打开沙巴克管理脚本".format(Sender.Character.CharacterName))
				return Dict
	elif Menu == 121:
		say = """（破损）
			
			[支付300万金币维修正中城门:1213]
			[结束:0]"""
		#判断正中城门是否去血
		map = Sender.CurrentMap
		cell = map.Cells[234,191]
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
					if (object.CurrentHP >= object.Stats[Stat.Health]):
						say = """（正常）
							
							[开门:1211]
							[关门:1212]
							[结束:0]"""
						break
	elif Menu == 1211:
		map = Sender.CurrentMap
		cell = map.Cells[234,191]
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
					object.Open()
				
					break
		cell = map.Cells[234,190]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[233,191]
		if cell.Objects != None:
			for object in reversed(cell.Objects): 
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[235,190]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
	elif Menu == 1212:
		map = Sender.CurrentMap
		cell = map.Cells[234,191]
		for object in cell.Objects:
			if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530 and object.Direction == MirDirection.UpLeft:
				object.Direction = object.CurrentDir
				objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
				objcetTurn.ObjectID = object.ObjectID
				objcetTurn.Direction = object.Direction
				objcetTurn.Location =  object.CurrentLocation
				object.Broadcast(objcetTurn)
				map.CreateNpc(234,190,344)
				map.CreateNpc(233,191,344)
				map.CreateNpc(235,190,344)
				break
	elif Menu == 1213:
		if (Sender.Gold < 3000000):
			say = """你没有足够的金币，无法维修城门。
			
			[结束:0]"""
		else:
			map = Sender.CurrentMap
			cell = map.Cells[234,191]
			flag = True
			if cell.Objects != None:
				for object in cell.Objects:
					if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
						object.CurrentHP = object.Stats[Stat.Health]
						SubGold(Sender,3000000)
						flag = False
			if flag:
				map.CreateMon(234,191,0,'沙巴克城门1',1)
				for object in cell.Objects:
					if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
						object.Direction = object.CurrentDir
						objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
						objcetTurn.ObjectID = object.ObjectID
						objcetTurn.Direction = object.Direction
						objcetTurn.Location =  object.CurrentLocation
						object.Broadcast(objcetTurn)
						SubGold(Sender,3000000)
						map.CreateNpc(234,190,344)
						map.CreateNpc(233,191,344)
						map.CreateNpc(235,190,344)
						break

	elif Menu == 122:
		say = """（破损）
			
			[支付300万金币维修左侧城门:1223]
			[结束:0]"""
		#判断左侧城门是否去血
		map = Sender.CurrentMap
		cell = map.Cells[169,191]
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 532:
					if (object.CurrentHP >= object.Stats[Stat.Health]):
						say = """（正常）
							
							[开门:1221]
							[关门:1222]
							[结束:0]"""
						break
	elif Menu == 1221:
		map = Sender.CurrentMap
		cell = map.Cells[169,191]
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 532:
					object.Open()
				
					break
		cell = map.Cells[168,190]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[170,191]
		if cell.Objects != None:
			for object in reversed(cell.Objects): 
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[169,190]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
	elif Menu == 1222:
		map = Sender.CurrentMap
		cell = map.Cells[169,191]
		for object in cell.Objects:
			if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 532 and object.Direction == MirDirection.UpLeft:
				object.Direction = object.CurrentDir
				objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
				objcetTurn.ObjectID = object.ObjectID
				objcetTurn.Direction = object.Direction
				objcetTurn.Location =  object.CurrentLocation
				object.Broadcast(objcetTurn)
				map.CreateNpc(168,190,344)
				map.CreateNpc(170,191,344)
				map.CreateNpc(169,190,344)
				break
	elif Menu == 1223:
		if (Sender.Gold < 3000000):
			say = """你没有足够的金币，无法维修城门。
			
			[结束:0]"""
		else:
			map = Sender.CurrentMap
			cell = map.Cells[169,191]
			flag = True
			if cell.Objects != None:
				for object in cell.Objects:
					if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 532:
						object.CurrentHP = object.Stats[Stat.Health]
						SubGold(Sender,3000000)
						flag = False
			if flag:
				map.CreateMon(169,191,0,'沙巴克城门3',1)
				for object in cell.Objects:
					if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 532:
						object.Direction = object.CurrentDir
						objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
						objcetTurn.ObjectID = object.ObjectID
						objcetTurn.Direction = object.Direction
						objcetTurn.Location =  object.CurrentLocation
						object.Broadcast(objcetTurn)
						SubGold(Sender,3000000)
						map.CreateNpc(168,190,344)
						map.CreateNpc(170,191,344)
						map.CreateNpc(169,190,344)
						break

	elif Menu == 123:
		say = """（破损）
			
			[支付300万金币维修右侧城门:1233]
			[结束:0]"""
		#判断左侧城门是否去血
		map = Sender.CurrentMap
		cell = map.Cells[234,127]
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 533:
					if (object.CurrentHP >= object.Stats[Stat.Health]):
						say = """（正常）
							
							[开门:1231]
							[关门:1232]
							[结束:0]"""
						break
	elif Menu == 1231:
		map = Sender.CurrentMap
		cell = map.Cells[234,127]
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 533:
					object.Open()
				
					break
		cell = map.Cells[232,127]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[233,127]
		if cell.Objects != None:
			for object in reversed(cell.Objects): 
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[234,128]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
	elif Menu == 1232:
		map = Sender.CurrentMap
		cell = map.Cells[234,127]
		for object in cell.Objects:
			if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 533 and object.Direction == MirDirection.UpLeft:
				object.Direction = object.CurrentDir
				objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
				objcetTurn.ObjectID = object.ObjectID
				objcetTurn.Direction = object.Direction
				objcetTurn.Location =  object.CurrentLocation
				object.Broadcast(objcetTurn)
				map.CreateNpc(232,127,344)
				map.CreateNpc(233,127,344)
				map.CreateNpc(234,128,344)
				break
	elif Menu == 1233:
		if (Sender.Gold < 3000000):
			say = """你没有足够的金币，无法维修城门。
			
			[结束:0]"""
		else:
			map = Sender.CurrentMap
			cell = map.Cells[234,127]
			flag = True
			if cell.Objects != None:
				for object in cell.Objects:
					if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 533:
						object.CurrentHP = object.Stats[Stat.Health]
						SubGold(Sender,3000000)
						flag = False
			if flag:
				map.CreateMon(234,127,0,'沙巴克城门4',1)
				for object in cell.Objects:
					if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 533:
						object.Direction = object.CurrentDir
						objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
						objcetTurn.ObjectID = object.ObjectID
						objcetTurn.Direction = object.Direction
						objcetTurn.Location =  object.CurrentLocation
						object.Broadcast(objcetTurn)
						SubGold(Sender,3000000)
						map.CreateNpc(232,127,344)
						map.CreateNpc(233,127,344)
						map.CreateNpc(234,128,344)
						break
	elif Menu == 5:
		today = datetime.datetime.now().weekday() + 1  #判断周几
		map = SEnvir.GetMap(550)  # 要传送的地图
		randomLocation = map.GetRandomLocation()      #取随机数坐标值
		#如果是周六 并且是  晚上22点
		if today == 6 and current_time_is_between("22:00:00", "23:59:00"):
			# if (Sender.Gold < 200000):
				# say = """你没有足够的金币，无法传送。
					
					# [离开:0]"""
			# else:
				# SubGold(Sender,200000)
			Sender.TeleportByMapIndex(550,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
			return
		else:
			say = """活动还没开启，请留意活动公告。
			
			[离开:0]"""
	elif Menu == 6:
		today = datetime.datetime.now().weekday() + 1  #判断周几
		map = SEnvir.GetMap(550)  # 要传送的地图
		randomLocation = map.GetRandomLocation()      #取随机数坐标值
		#如果是周六 并且是  晚上22点
		if today == 6 and current_time_is_between("22:00:00", "23:59:00"):
			Sender.TeleportByMapIndex(550,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
			return
		else:
			say = """活动还没开启，请留意活动公告。
			
			[离开:0]"""
#主菜单
	else:
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#如果 角色行会为空 或 行会不是沙巴克成员
		if (not Sender.Character.Account.GuildMember) or (Sender.Character.Account.GuildMember.Guild != guild):
			say = """你好，我是沙巴克的管理员，有什么需要我帮忙的？目前还未开启沙巴克攻城战。
			
			[看攻城战的日期:1]
			
			[申请攻城战:2]
			
			[了解有关攻城战的事:3]
			
			[进入沙巴克地下城:5]
			
			[结束:0]"""
		else:
			#再判断占领沙巴克的行会名
			if guild:
				owner = SEnvir.GetGuildLeader(guild.GuildName)
				if(owner and Sender.Character.CharacterName == owner.CharacterName):
					say = """尊敬的沙巴克城主
					你好，我是沙巴克的管理员，有什么需要我帮忙的？
					
					[沙巴克管理:10]
					
					[看攻城战的日期:1]
					
					[了解有关攻城战的事:3]
					
					[进入沙巴克地下城:6]
					
					[结束:0]"""
				else:
					say = """尊敬的沙巴克成员
					你好，我是沙巴克的管理员，有什么需要我帮忙的？
					
					[看攻城战的日期:1]
					
					[了解有关攻城战的事:3]
					
					[进入沙巴克地下城:6]
					
					[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


def Deposit(params):
	if not params:
		return

	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
	else:
		player.MakeGoldDeposit('沙巴克', int(userInput))


def Withdraw(params):
	if not params:
		return

	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
	else:
		player.WithdrawCastleFund('沙巴克', int(userInput))

def GetNextWarDate():
	"""获取下一个攻城战日期（固定为每周六晚上8点）"""
	now = datetime.datetime.now()
	days_until_saturday = (5 - now.weekday()) % 7  # 5是周六
	if days_until_saturday == 0 and now.hour >= 20:  # 如果今天是周六且已经过了8点
		days_until_saturday = 7  # 推到下周六
	
	next_saturday = now + datetime.timedelta(days=days_until_saturday)
	return next_saturday.replace(hour=20, minute=0, second=0, microsecond=0)

NpcEvent.add_listener(88,"OnClick",OnClick)