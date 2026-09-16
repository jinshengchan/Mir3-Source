# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import random
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from 变量.默认变量 import *
from Utils.PlayerUtils import *
#Server.Envir.SEnvir.Log(__name__+"导入")
import System
s1 = clr.Reference[System.Object]()
import NpcEvent
import os

def OnProcess(args):
	Sender=args[0]
	#Server.Envir.SEnvir.Log("循环调用成功")
	starttime = PlayerGetTempV(Sender,TK_PD_VALUE)  #时间等于泡点个人变量
	if(starttime == 0 or starttime < SEnvir.Now): #如果时间小于系统时间
		PlayerSetTempV(Sender,TK_PD_VALUE,SEnvir.Now.AddMinutes(1)) #个人变量时间设置1分钟
		
		#玩家在线时长小于120分钟，那么每分钟加1
		if (PlayerGetV(Sender,GV_PLAYER_ONLINETIME) < 121):
			PlayerSetV(Sender,GV_PLAYER_ONLINETIME,PlayerGetV(Sender,GV_PLAYER_ONLINETIME) + 1)
		if (PlayerGetV(Sender,GV_PLAYER_ONLINETIME) == 120):
			Sender.Connection.ReceiveChat("你在线时间已超过两个小时，可以去比奇行政长官签到了！", MessageType.System)
	
	starttime1 = PlayerGetTempV(Sender,TK_GJ_VALUE)  #时间等于泡点个人变量
	if(starttime1 == 0 or starttime1 < SEnvir.Now): #如果时间小于系统时间
		PlayerSetTempV(Sender,TK_GJ_VALUE,SEnvir.Now.AddSeconds(3)) #按秒判断循环

		if (Sender.setConfArr[17] ):   #判断是否挂机状态
			if (not Sender.HasCustomBuff(143)):
				Sender.CustomBuffAdd(143)  #增加挂机BUFF状态
		else:
			Sender.CustomBuffRemove(143)  #移除挂机BUFF状态
def OnWeekChange(args):
	Sender=args[0]
	PlayerSetV(Sender, GV_PLAYER_YXSM, 0)
	PlayerSetV(Sender, GV_PLAYER_ZHOUPAOCHUANG, 0)  #周跑船任务复位
	Sender.Connection.ReceiveChat("******玛法大陆迎来了新的一周******",MessageType.System)
	#Server.Envir.SEnvir.Log("隔周调用成功")
	
def OnMonthChange(args):
	Sender=args[0]
	PlayerSetV(Sender, GV_PLAYER_ZZLB, 0)
	PlayerSetV(Sender, GV_PLAYER_NMLB, 0)
	Sender.Connection.ReceiveChat("******玛法大陆迎来了新的一月******",MessageType.System)
	#Server.Envir.SEnvir.Log("隔月调用成功")
	
def sendMsgToAll(msg):
	for con in SEnvir.Connections:
		con.ReceiveChat(msg,MessageType.System)

def OnChat(args):
	Sender = args[0]
	Text = args[1]
	if Text.startswith('@'):
		cmd = Text[1:]
		parts = cmd.split()
		if len(parts) > 0:  # 判断指令长度
			if Sender.Character.Account.TempAdmin:  # 判断是否是管理员 是管理员就打印出指令
				Sender.Connection.ReceiveChat("你执行了指令:{}".format(cmd), MessageType.System)
			if parts[0].upper() == "123":  # 如果指令是123 则执行 upper()字符串英文字符转换成大写格式 是为了能够接受大小写混写指令
				if not Sender.Character.Account.TempAdmin:  # 判断是否是管理员
					return True
				for str in parts:
					Sender.Connection.ReceiveChat(str, MessageType.System)
				return True  # 返回True 服务端将不对这条聊天进行处理
			# if parts[0].upper() == "R":
				# Sender.Connection.ReceiveChat("GM指令重载脚本", MessageType.System)
				# return False  # 返回False 让服务端继续处理 这里只是为了能够在聊天框提示 你成功的输入了这个指令
			if parts[0].upper() == "踢人":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				con = SEnvir.GetConnectionByCharacter(parts[1])
				if con is None or (con.Stage != Server.Envir.GameStage.Observer and con.Stage != Server.Envir.GameStage.Game) or SEnvir.IsBlocking(Sender.Character.Account, con.Account):
					Sender.Connection.ReceiveChat("无法找到角色 {}".format(parts[1]), MessageType.System)
					return True
				else:
					con.TryDisconnect()
					return True
			if parts[0].upper() == "给予":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				con = SEnvir.GetConnectionByCharacter(parts[1])
				if con is None or (con.Stage != Server.Envir.GameStage.Observer and con.Stage != Server.Envir.GameStage.Game) or SEnvir.IsBlocking(Sender.Character.Account, con.Account):
					Sender.Connection.ReceiveChat("无法找到角色 {}".format(parts[0]), MessageType.System)
					return True
				else:
					if parts[2].isdigit():
						if con.Player.GiveItem(int(parts[2]), int(parts[3])):
							Sender.Connection.ReceiveChat("给予角色 {}，发放物品 {} {} 个成功".format(parts[1], parts[2], parts[3]), MessageType.System)
						else:
							Sender.Connection.ReceiveChat("给予角色 {}，发放物品 {} {} 个失败".format(parts[1], parts[2], parts[3]), MessageType.System)
					else:
						if con.Player.GiveItem(parts[2], int(parts[3])):
							Sender.Connection.ReceiveChat("给予角色 {}，发放物品 {} {} 个成功".format(parts[1], parts[2], parts[3]), MessageType.System)
						else:
							Sender.Connection.ReceiveChat("给予角色 {}，发放物品 {} {} 个失败".format(parts[1], parts[2], parts[3]), MessageType.System)
			if parts[0].upper() == "管理":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
				mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(144)
				mynpc.NPCCall(Sender)
				return True
			if parts[0].upper() == "变量":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				if len(parts)<4:
					if parts[1].isdigit():
						PlayerSetV(Sender,int(parts[1]),int(parts[2]))
					else: 
						PlayerSetV(Sender,eval(parts[1]),int(parts[2]))
				else:
					con = SEnvir.GetConnectionByCharacter(parts[1])
					if con is None or (con.Stage != Server.Envir.GameStage.Observer and con.Stage != Server.Envir.GameStage.Game) or SEnvir.IsBlocking(Sender.Character.Account, con.Account):
						Sender.Connection.ReceiveChat("无法找到角色 {}".format(parts[0]), MessageType.System)
						return True
					elif parts[2].isdigit():
						PlayerSetV(con.Player,int(parts[2]),int(parts[3]))
					else: 
						PlayerSetV(con.Player,eval(parts[2]),int(parts[3]))
				return True
			if parts[0].upper() == "全局变量":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				if parts[1].isdigit():
					GlobalSetV(int(parts[1]),int(parts[2]))
				else:
					GlobalSetV(eval(parts[1]),int(parts[2]))
				return True
			if parts[0].upper() == "全局临时变量":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				if parts[1].isdigit():
					GlobalSetTempV(int(parts[1]),int(parts[2]))
				else:
					GlobalSetTempV(eval(parts[1]),int(parts[2]))
				return True
			if parts[0].upper() == "赞助":
				count = PlayerGetTempV(Sender,TK_KMCZ_ERRORCOUNT)
				if count> 2:
					freezeTime = PlayerGetTempV(Sender, TK_KMCZ_FROZENTIME)
					if(SEnvir.Now < freezeTime):
						SenderChat(Sender, "由于你出错次数太多，锁定充值，请一小时以后再试")
						return True
					else: 
						PlayerSetTempV(Sender, TK_KMCZ_ERRORCOUNT, 0)
						count = 0
				userInput = parts[1] if len(parts) > 1 else None
				if not userInput or len(userInput) < 1:
					Sender.Connection.ReceiveChat("输入信息出错",MessageType.System)
				else:
					if not Npc.卡密充值.use_code(Sender, userInput, Sender.Character.Account.EMailAddress):
						count = count + 1
						PlayerSetTempV(Sender, TK_KMCZ_ERRORCOUNT, count)
						if count > 2:
							PlayerSetTempV(Sender,TK_KMCZ_FROZENTIME,SEnvir.Now.AddMinutes(60))
				return True
			if parts[0].upper() == "移动": 
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				Sender.TeleportByMapIndex(int(parts[1]),int(parts[2]),int(parts[3]))
				return True
			if parts[0].upper() == "卡图自救": 
				if not Sender.CurrentMap.Info.AllowRT:
					return True
				starttime = PlayerGetTempV(Sender,TK_KTZJ_VALUE)  #时间等于泡点个人变量
				if(starttime == 0 or starttime < SEnvir.Now): #如果时间小于系统时间
					PlayerSetTempV(Sender,TK_KTZJ_VALUE,SEnvir.Now.AddMinutes(1)) #个人泡点变量时间设置1分钟
					Sender.TeleportByMapIndex(1,451,390)
				return True
			if parts[0].upper() == "整理快捷栏":
				for i in range(Sender.Character.BeltLinks.Count-1,-1,-1):   #判断药品快捷栏的物品数量
					Sender.Character.BeltLinks[i].Delete()   #删除所有快捷设置
				SenderChat(Sender, "你执行了药品快捷栏整理。")
				return True
			if parts[0].upper() == "清怪":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				monsterName = parts[1]
				map = Sender.CurrentMap
				for i in range(map.Objects.Count-1, -1 , -1):
					mob = map.Objects[i]
					if mob is None or mob.Dead or mob.Race != ObjectType.Monster:
						continue
					if mob.MonsterInfo.MonsterName == monsterName:
						mob.EXPOwner = None
						mob.Die()
						mob.Despawn()
				SenderChat(Sender, "你清除了怪物{}".format(monsterName))
				return True
			if parts[0].upper() == "删除":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				con = SEnvir.GetConnectionByCharacter(parts[1])
				if con is None or (con.Stage != Server.Envir.GameStage.Observer and con.Stage != Server.Envir.GameStage.Game) or SEnvir.IsBlocking(Sender.Character.Account, con.Account):
					Sender.Connection.ReceiveChat("无法找到角色 {}".format(parts[0]), MessageType.System)
					return True
				else:
					if con.Player.TakeItem(parts[2], int(parts[3])):
						Sender.Connection.ReceiveChat("删除角色 {} 物品 {} {} 个失败".format(parts[1], parts[2], parts[3]), MessageType.System)
					else:
						Sender.Connection.ReceiveChat("删除角色 {} 物品 {} {} 个成功".format(parts[1], parts[2], parts[3]), MessageType.System)
			if parts[0].upper() == "指定删除":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				items = SEnvir.UserItemList.Binding.Where(lambda x:x.Info.Index == int(parts[1])).ToList()
				for item in items:
					item.Delete()
			if parts[0].upper() == "任务":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				PlayerSetV(Sender,BV_QT_TODAY,int(parts[1]))
			if parts[0].upper() == "行会升级":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				Sender.Character.Account.GuildMember.Guild.GuildLevel = int(parts[1])
				update = Sender.Character.Account.GuildMember.Guild.GetUpdatePacket()
				for member in Sender.Character.Account.GuildMember.Guild.Members:
					if member.Account.Connection is not None and member.Account.Connection.Player is not None:
						member.Account.Connection.Player.Enqueue(update)
			if parts[0].upper() == "增加BUFF":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				con = SEnvir.GetConnectionByCharacter(parts[1])
				if con is None or (con.Stage != Server.Envir.GameStage.Observer and con.Stage != Server.Envir.GameStage.Game) or SEnvir.IsBlocking(Sender.Character.Account, con.Account):
					Sender.Connection.ReceiveChat("无法找到角色 {}".format(parts[0]), MessageType.System)
					return True
				else:
					con.Player.CustomBuffAdd(int(parts[2]))
			if parts[0].upper() == "删除BUFF":
				if not Sender.Character.Account.TempAdmin:  # 判断是否为管理员
					return True
				con = SEnvir.GetConnectionByCharacter(parts[1])
				if con is None or (con.Stage != Server.Envir.GameStage.Observer and con.Stage != Server.Envir.GameStage.Game) or SEnvir.IsBlocking(Sender.Character.Account, con.Account):
					Sender.Connection.ReceiveChat("无法找到角色 {}".format(parts[0]), MessageType.System)
					return True
				else:
					con.Player.CustomBuffRemove(int(parts[2]))
		else:
			return True
	else:
		return False  # 返回False 服务端将处理这条聊天信息
		
def OnStartGame(args):   #开启游戏
	Sender = args[0]

	
	#任务初始化 给NPC增加新任务图标
	if (Sender.Class == Sender.Class.Wizard) and (PlayerGetV(Sender,BV_NQ_MAIN)==0):  #法师 任务还没开始
		UpdateNPCLook(Sender, 244, QuestIcon.NewQuest)
	if (Sender.Class == Sender.Class.Warrior) and (PlayerGetV(Sender,BV_NQ_MAIN)==0):  #战士 任务还没开始
		UpdateNPCLook(Sender, 243, QuestIcon.NewQuest)
	if (Sender.Class == Sender.Class.Taoist) and (PlayerGetV(Sender,BV_NQ_MAIN)==0):  #道士 任务还没开始
		UpdateNPCLook(Sender, 245, QuestIcon.NewQuest)
	
	if Sender.Character.Account.TempAdmin:  # 判断是否为管理员
		return True
	for player in SEnvir.Players:
		if(player is None):
			continue
		player.Connection.ReceiveChat("玩家【{}】加入游戏".format(Sender.Name),MessageType.System)
	
	PlayerSetTempV(Sender,TK_PD_VALUE,Server.Envir.SEnvir.Now.AddMinutes(1)) #玩家临时变量 泡点 每分钟循环判断
	
def OnStopGame(args):   #结束游戏
	Sender = args[0]
	if Sender.Character.Account.TempAdmin:  # 判断是否为管理员
		return True
	# for player in SEnvir.Players:
		# if(player is None):
			# continue
		# player.Connection.ReceiveChat("玩家【{}】离开游戏".format(Sender.Name),MessageType.System)

	
PlayerEvent.add_listener("OnStartGame",OnStartGame)
PlayerEvent.add_listener("OnStopGame",OnStopGame)
PlayerEvent.add_listener("OnChat",OnChat) #注册聊天函数 如果返回True则服务端不在处理这个聊天  返回False 服务端会继续处理这个聊天 运用在写指令的场景
PlayerEvent.add_listener("OnWeekChange",OnWeekChange)
PlayerEvent.add_listener("OnMonthChange",OnMonthChange)
PlayerEvent.add_listener("OnProcess",OnProcess)

