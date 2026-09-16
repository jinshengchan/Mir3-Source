# -*- coding: utf-8 -*-
#载入模块SYS
import sys
from datetime import datetime, timedelta
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import collections
import NpcEvent
import MapEvent
import Server
import re
from Utils.PlayerUtils import *
from Utils.TimeUtil import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from 变量.默认变量 import *
from Server.DBModels import *
from MirDB import *
from Player.泡点 import *
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import unicodedata

clr.AddReference('System.Drawing')
import System.Drawing
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
	bg = {}
	font={}
	Dict={}
	say=""

	if(not Sender.Character.Account.TempAdmin):
		SEnvir.Log("脚本警报：{} 使用封包挂".format(Sender.Character.CharacterName))
		return Dict

	if(Menu == 1):
		Sender.TestDrop(100000,1,1)
		say = """爆率测试

		(10万次,1个玩家,1倍爆率)"""
	elif(Menu == 2):
		Sender.LearnSkill("天之怒火")
	elif(Menu == 3):
		Sender.ChangeSkillLevel("天之怒火", 3)
	elif(Menu == 4):
		Sender.ForgetSkill("天之怒火")
	elif(Menu == 5):
		if(Sender.Pets.Count > 1):
			say = "你已经有宠物了"
		else:
			# 怪物名 数目 多久叛变(秒)
			Sender.AddPet("稻草人", 5, 6000)
	elif(Menu == 6):
		for i in range(1000):
			Sender.QuestRemoveByUserQuestIndex(i)
	elif(Menu == 7):
		SEnvir.ScheduledCall("Utils.ServerUtils.SendMsgToAll", SEnvir.Now.AddSeconds(5), "1次延迟py测试")
	elif(Menu == 8):
		StartPaoDian(Sender)
	elif(Menu == 9):
		StopPaoDian(Sender)
	elif(Menu == 10):
		InputBoxTest([Sender])
	elif(Menu == 11):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("满月老人")
		NPCObject = ServerUtils.GetNPCObject(139)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.智善大师.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	elif(Menu == 12):
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#然后做行会判断
		if not guild:
			say = "沙巴克无人占领"
		else:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			say = "沙巴克现在由[{}]行会占领, 城主[{}]".format(guild.GuildName, owner.CharacterName)
	elif(Menu == 13):
		#判断全部玩家信息列表
		allPlayers = SEnvir.CharacterInfoList.Binding
		#获取玩家的等级
		sortByLevel = sorted(allPlayers, cmp=None, key=lambda x: x.Level, reverse=True)
		say = '{0: <32} {1: <32} {2}\n'.format('排名', '角色', '等级') 
		say += '\n'.join("{:<24}{:^24}{:>24}".format(sortByLevel.index(e) + 1, e.CharacterName, 1) for e in sortByLevel)
		

	elif(Menu == 14):
		allAccounts = SEnvir.AccountInfoList.Binding
		sortByGold = sorted(allAccounts, cmp=None, key=lambda x: x.Gold, reverse=True)
		sortByGold = [x for x in sortByGold if x.LastCharacter]
		say = '\n'.join("{}: {}".format(e.LastCharacter.CharacterName, e.Gold) for e in sortByGold)

	elif(Menu == 15):
		allPlayers = [x for x in SEnvir.CharacterInfoList.Binding if x.Class == MirClass.Warrior]
		sortByLevel = sorted(allPlayers, cmp=None, key=lambda x: x.Level, reverse=True)
		say = '\n'.join("{}: {}".format(e.CharacterName, e.Level) for e in sortByLevel)

	elif(Menu == 16):
		Sender.ApplyJoinGuild(2)

	elif(Menu == 17):
		Npc.游方货郎.Refresh(None)

	elif(Menu == 18):
		Sender.Equipment[int(EquipmentSlot.Weapon)].Experience += 5000
		Sender.ItemCompleteRefresh((Sender.Equipment[int(EquipmentSlot.Weapon)]).Index)

	elif(Menu == 19):
		bg['file']=2									#定义聊天框背景(该字段有值则不适用url,且和idx一起存在.否则不生效)
		bg['idx']=150									#图库图片序号
		bg['center']=0									#是否居中显示(0左上角显示,1居中显示)
		bg['title'] = " "					 #自定义标签内容 只支持最普通文字
		Dict['bg'] = bg
		say= """
		<img file=3 idx=1870 count=10 delay=500 x=30 y=30 />
		
		"""
	elif(Menu == 20):
		map = Sender.CurrentMap
		say = "当前地图名称: {}\n当前地图编号: {}\n当前地图玩家数: {}\n当前地图怪物数: {}".format(map.Info.Description, map.Info.FileName, map.PlayerCount, map.MonsterCount)
		say += "\n\n[清理当前地图怪物:21]"
	elif(Menu == 21):
		map = Sender.CurrentMap
		map.ClearAllMonsters()
	elif Menu == 21:
		# SetItemCustomPrefix(物品, 自定义前缀, 自定义颜色)
		# 自定义颜色支持留空（默认黄色）,内置颜色, 或者RGB颜色
		# 重置时 可以写 SetItemCustomPrefix(物品, "")

		# 使用内置颜色
		Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Weapon)], "青青草原", System.Drawing.Color.YellowGreen)
		# 使用RGB颜色 (R, G, B)
		#Sender.SetItemCustomPrefix(Sender.Equipment[int(EquipmentSlot.Weapon)], "纯黑", (255,255,255))
	elif Menu == 22:
		Sender.DailyQuestReset()
	elif(Menu == 23):
		new = PlayerGetV(Sender,BV_NQ_MAIN)
		say = """当前主线任务进度：
			
			进度编号：  {}  。
			
			[回退:25]    [推进:26]    [初始化主线任务:27]
			
			[打开杀怪开关:24]
			
			[结束:0]""".format(new)
	elif(Menu == 24):
		PlayerSetV(Sender,BV_NQ_KILLMON,1)
		PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
		PlayerSetV(Sender,BV_NQ_KILLNUM,0)
		say = """已打开主线任务杀怪开关，
			并初始化获取物品数量和杀怪数量。
			
			[关闭:0]"""
	elif(Menu == 25):
		new = PlayerGetV(Sender,BV_NQ_MAIN)
		new += -1
		PlayerSetV(Sender,BV_NQ_MAIN,new)
		say = """当前主线任务进度：
			
			进度编号：  {}  。
			
			[回退:25]    [推进:26]    [打开杀怪开关:24]
			
			[结束:0]""".format(new)
	elif(Menu == 26):
		new = PlayerGetV(Sender,BV_NQ_MAIN)
		new += 1
		PlayerSetV(Sender,BV_NQ_MAIN,new)
		say = """当前主线任务进度：
			
			进度编号：  {}  。
			
			[回退:25]    [推进:26]    [打开杀怪开关:24]
			
			[结束:0]""".format(new)
	elif(Menu == 27):
		PlayerSetV(Sender,BV_NQ_MAIN,0)
		PlayerSetV(Sender,BV_NQ_KILLMON,0)
		PlayerSetV(Sender,BV_NQ_KILLNUM,0)
		say = """主线任务已初始化。
			
			[关闭:0]"""
	elif(Menu == 28):
		PlayerSetV(Sender,BV_NUM_DAILYTASK,0)
		PlayerSetV(Sender,BV_QT_TODAY,0)
		PlayerSetV(Sender,BV_QT_KILLMON,0)
		PlayerSetV(Sender,BV_QT_KILLNUM,0)
		say = """每日任务已重置。
			
			[关闭:0]"""
	elif(Menu == 30):
		SEnvir.ResetVariableForAllPlayers(GV_BOSSFB_COUNT,0) #比奇每日副本任务复位
		SEnvir.ResetVariableForAllPlayers(GV_ZDBOSSFB_COUNT,0) #每日副本任务复位
		SEnvir.ResetVariableForAllPlayers(GV_XINSHOUFB_ONOFF,0) #每日奇遇副本任务复位
		SEnvir.ResetVariableForAllPlayers(GV_AWMBOSSFB_COUNT,0) #沃玛普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BWMBOSSFB_COUNT,0) #沃玛噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CWMBOSSFB_COUNT,0) #沃玛地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_AZMBOSSFB_COUNT,0) #祖玛普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BZMBOSSFB_COUNT,0) #祖玛噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CZMBOSSFB_COUNT,0) #祖玛地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_AWGBOSSFB_COUNT,0) #蜈蚣普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BWGBOSSFB_COUNT,0) #蜈蚣噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CWGBOSSFB_COUNT,0) #蜈蚣地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_ASGMBOSSFB_COUNT,0) #石阁庙普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BSGMBOSSFB_COUNT,0) #石阁庙噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CSGMBOSSFB_COUNT,0) #石阁庙地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_ASJBOSSFB_COUNT,0) #神舰普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BSJBOSSFB_COUNT,0) #神舰噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CSJBOSSFB_COUNT,0) #神舰地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_ACYBOSSFB_COUNT,0) #赤月普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BCYBOSSFB_COUNT,0) #赤月噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CCYBOSSFB_COUNT,0) #赤月地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_APYBOSSFB_COUNT,0) #潘夜神殿普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BPYBOSSFB_COUNT,0) #潘夜神殿噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CPYBOSSFB_COUNT,0) #潘夜神殿地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_APYSBOSSFB_COUNT,0) #潘夜石窟普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BPYSBOSSFB_COUNT,0) #潘夜石窟噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CPYSBOSSFB_COUNT,0) #潘夜石窟地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_AZTGBOSSFB_COUNT,0) #真天宫普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BZTGBOSSFB_COUNT,0) #真天宫噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CZTGBOSSFB_COUNT,0) #真天宫地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_AHDGBOSSFB_COUNT,0) #黑度宫普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BHDGBOSSFB_COUNT,0) #黑度宫噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CHDGBOSSFB_COUNT,0) #黑度宫地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_ANMBOSSFB_COUNT,0) #诺玛遗址普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BNMBOSSFB_COUNT,0) #诺玛遗址噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CNMBOSSFB_COUNT,0) #诺玛遗址地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_AXSBOSSFB_COUNT,0) #西部沙漠普通副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BXSBOSSFB_COUNT,0) #西部沙漠噩梦副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CXSBOSSFB_COUNT,0) #西部沙漠地狱副本复位
		SEnvir.ResetVariableForAllPlayers(GV_APKSBOSSFB_COUNT,0) #沉鱼落雁副本复位
		SEnvir.ResetVariableForAllPlayers(GV_BPKSBOSSFB_COUNT,0) #闭月羞花副本复位
		SEnvir.ResetVariableForAllPlayers(GV_CPKSBOSSFB_COUNT,0) #红粉骷髅副本复位




		say = """每日任务已重置。
			
			[关闭:0]"""


	elif(Menu == 29):
		PlayerSetV(Sender,BV_QT_KILLMON,1)
		PlayerSetV(Sender,BV_QT_KILLNUM,0)
		say = """已打开每日任务杀怪开关，并初始化杀怪数量。
			
			[关闭:0]"""
	else:
		say = """＜游戏后台管理页面＞

	[爆率测试:1] 爆率测试(面对目标怪物)
	[学习技能:2] 学习技能(限本职业)
	[调整技能:3] 调整技能等级
	[删除技能:4] 删除技能
	[召唤宠物:5] 召唤宠物
	[延迟py测试:7] 延迟py测试
	[开始泡点:8] 开始泡点
	[结束泡点:9] 结束泡点
	[对话框测试:10] 对话框测试
	[调用其他NPC:11] 调用其他NPC
	[沙巴克城主:12] 沙巴克城主
	[等级排行:13] 等级排行
	[金币排行:14] 金币排行
	[战士排行:15] 战士排行
	[申请入会:16] 申请入会(服务端查看行会index)
	[重新刷新货郎:17] 重新刷新货郎
	[武器增加经验:18] 武器增加经验并刷新武器属性
	[富文本动态图:19] 富文本动图测试
	[地图刷怪测试:20] 地图怪物刷新
	[手上武器刻名:21] 手上武器刻名测试
	
	[重置每日任务:22] 重置服务端每日任务
	[移除任务:6] 删除所有个人任务
	
	[调整主线任务进度:23] （江湖任务）
	[打开主线任务杀怪开关:24] （江湖任务）

	[初始化每日副本:30] （每日副本重置）
	
	[初始化每日任务:28] （每日任务）
	[打开每日任务杀怪开关:29] （每日任务）
	

	"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


def InputBoxTest(params):
	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
		# 显示一个输入框
		# PyInputBox(提示信息， 用户点了确定后执行的函数，用户点了取消后执行的函数 可以留空, 覆盖取消执行函数的参数 可以留空)
		# 注意：点确定时执行的py函数 传入的参数是固定的 [player, 用户输入的信息(string格式)]
		# 注意：点取消时执行的py函数 传入的参数也是 [player, 用户输入的信息(string格式)] 除非写了覆盖取消执行函数的参数

		# 例子
		# player.PyInputBox("请输入信息", "Npc.管理员.InputBoxTest", "Player.泡点.StopPaoDian", player)
		# 意思是	用户点确定的时候 执行 Npc.管理员.InputBoxTest 此时传入的参数是  [player, 用户输入的信息(string格式)]
		# 		用户点取消的时候 执行 Player.泡点.StopPaoDian 此时传入的被替换为 player

		player.PyInputBox("请输入信息", "Npc.管理员.InputBoxTest", "Npc.管理员.InputBoxTest")
	else:
		player.Connection.ReceiveChat("用户输入了{}".format(userInput),MessageType.System)


NpcEvent.add_listener(224,"OnClick",OnClick)	