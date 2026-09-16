# -*- coding: utf-8 -*-
import  sys
#修改PythonPath 的值为你安装的python2.7 的路径 不支持python3.0以上版本
PythonPath = r'C:\Python27'
PythonLibPath = PythonPath + r'\Lib'
PythonDllsPath = PythonLibPath + r'\DLLs'
PythonPackPath = PythonLibPath + r'\site-packages'
PythonEggPath = PythonPackPath + r'\requests-2.8.1-py2.7.egg'
sys.path.append(PythonPath)
sys.path.append(PythonDllsPath)
sys.path.append(PythonLibPath)
sys.path.append(PythonPackPath)
sys.path.append(PythonEggPath)
import random
import clr
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import System
import Server
import collections
import NpcEvent
import xlrd
from Defines import *
from 变量.任务杀怪 import *
import Server.Envir.SEnvir as SEnvir


def GlobalGetV(Key):
	ret = SEnvir.GetValues(Key)
	if(ret is None):
		ret = 0
	return ret

def GlobalSetV(Key, Value):
	SEnvir.SetValues(Key,Value)
	
	

def MonsterSetTempV(Monster,Key,Value): #怪物临时变量
	Monster.TempVariables[Key] = Value
	
def MonsterGetTempV(Monster, Key): #怪物设置变量
	return Monster.TempVariables[Key]

def MonsterGetTempVDefault(Monster, Key, Default): #怪物初始化变量
	try:
		return Monster.TempVariables[Key]
	except:
		Monster.TempVariables[Key] = Default
		return Default
	
def PlayerSetV(Sender,Key,Value): #玩家设置变量
	Sender.SetValues(Key,Value)
	
def PlayerGetV(Sender,Key):  #玩家变量
	ret=Sender.GetValues(Key)
	if(ret is None):
		ret =0
	return ret;
	
def PlayerSetObV(Sender,Key,Value):
	Sender.SetObValues(Key,Value)

	
def PlayerGetObV(Sender,Key):
	ret = Sender.GetObValues(Key)
	return ret
	
def MapGetTempV(Map,Key):  #地图临时变量
	ob = clr.Reference[System.Object]()
	Map.TempValue.TryGetValue(Key,ob)
	ret = 0
	if(not(ob.Value is None)):
		ret = ob.Value
	return ret

def MapSetTempV(Map,Key,value):  #地图设置临时变量
	Map.TempValue[Key]=value
	
def PlayerGetTempV(Sender,Key):  #玩家临时变量
	ob = clr.Reference[System.Object]()
	Sender.TempValue.TryGetValue(Key,ob)
	ret = 0
	if(not(ob.Value is None)):
		ret = ob.Value
	return ret

def PlayerSetTempV(Sender,Key,value): #玩家设置临时变量
	Sender.TempValue[Key]=value
	

def GiveGold(Sender,Count):   #给予金币
	Sender.Gold += Count
	Sender.GoldChanged()
	
def SubGold(Sender,Count):    #扣除金币
	if (Sender.Gold < Count):
		return
	Sender.Gold -= Count
	Sender.GoldChanged()
	
def GiveGameGold(Sender,Count):   #给予元宝
	Sender.GameGold += Count
	Sender.GameGoldChanged()
	
def SubGameGold(Sender,Count):    #扣除元宝
	if (Sender.GameGold < Count):
		return
	Sender.GameGold -= Count
	Sender.GameGoldChanged()
	
def GiveExperience(Sender,Count):   #给予经验
	Sender.GainExperience(Count,False,sys.maxint,False,True)
	
def SubExperience(Sender,Count):    #扣除经验
	if (Sender.Experience < Count):
		exp = Sender.Experience
		Sender.Experience -= exp
		Sender.ExperienceChanged(exp)
	else:
		Sender.Experience -= Count
		Sender.ExperienceChanged(Count)
		

def GiveHuntGold(Sender,Count):   #给予赏金
	Sender.Character.Account.HuntGold += Count
	Sender.HuntGoldChanged()
	
def SubHuntGold(Sender,Count):    #扣除赏金
	if (Sender.Character.Account.HuntGold < Count):
		return
	Sender.Character.Account.HuntGold -= Count
	Sender.HuntGoldChanged()
	

def GivePrestige(Sender,Count):   #给予声望
	Sender.Prestige += Count
	Sender.PrestigeChanged()
	
def SubPrestige(Sender,Count):    #扣除声望
	if (Sender.Prestige < Count):
		return
	Sender.Prestige -= Count
	Sender.PrestigeChanged()
	

def GiveContribute(Sender,Count):   #给予荣誉值
	Sender.Contribute += Count
	Sender.ContributeChanged()
	
def SubContribute(Sender,Count):    #扣除荣誉值
	if (Sender.Contribute < Count):
		return
	Sender.Contribute -= Count
	Sender.ContributeChanged()
	
def CanMoveInMap(Level,PlayCount):           #排行榜等级判断  达到多少人数
	count = 0
	for info in Server.Envir.SEnvir.Rankings:
		if(info.Deleted):
			continue
		if(info.Level>=Level):
			count+=1
	#Server.Envir.SEnvir.Log("%d"%count)
	if(count < PlayCount):
		return False
	return True

#获取主线任务进度
def GetMainTaskList(Sender,TaskNumber):
	file = '.\Database\TaskLists\任务列表.xls'
	wb = xlrd.open_workbook(filename=file)              #打开表格
	sheet1 = wb.sheet_by_name('江湖任务')             #定位到万事通任务表
	TaskList = sheet1.row_values(TaskNumber+1)            #获取任务内容
	return TaskList

#获取神舰任务进度
def GetSJTaskList(Sender,TaskNumber):
	file = '.\Database\TaskLists\任务列表.xls'
	wb = xlrd.open_workbook(filename=file)              #打开表格
	sheet1 = wb.sheet_by_name('神舰任务')             #定位到万事通任务表
	TaskList = sheet1.row_values(TaskNumber+1)            #获取任务内容
	return TaskList

#获取每日任务
def GetDailyTaskList(Sender,TaskNumber):
	TaskList = DailyTaskList_all[TaskNumber]            #获取任务内容
	return TaskList


#获取当前级别可接受的每日任务列表
def GetDailyTaskNumber(Sender):
	TaskNumberList = []
	for t in range(1,len(DailyTaskList_all)+1):
		x = DailyTaskList_all[t].get('等级要求')
		if Sender.Level - 12 <= x <= Sender.Level + 5:         #查找符合等级限制的任务（等级-12至等级+5）
			TaskNumberList.append(t)
	if TaskNumberList == []:
		for t in range(1,len(DailyTaskList_all)):
			x = DailyTaskList_all[t].get('等级要求')
			if x > 38:         #如果列表为空，就领取38以上的任务
				TaskNumberList.append(t)
#	Sender.Connection.ReceiveChat(" {} ".format(TaskNumberList), MessageType.System)
#	Sender.Connection.ReceiveChat("以上为调试信息，请无视。", MessageType.System)
	TaskNumber = random.choice(TaskNumberList)
	PlayerSetV(Sender,BV_QT_TODAY,TaskNumber)
	return TaskNumber
#物品占用背包格子数	
def ItemUseIvetoryCount(ItemName, Amount):
	item = SEnvir.GetItemInfo(ItemName)
	count = 0
	if item:
		while Amount>0:
			Amount = Amount - item.StackSize;
			count = count + 1
	
	return count;
	
#背包格子判断
def GetInventoryCount(Sender):
	count = 0
	for i in range(Globals.InventorySize):  #遍历包裹格子
		item = Sender.Inventory[i]  #道具定义格子里的道具
		if not item:
			count +=1
	return count
		
def SenderChat(Sender,message):  #玩家发言
	Sender.Connection.ReceiveChat(message,MessageType.System)
	
def BroadChat(message,type = MessageType.System):   #玩家广播发言
	for player in Server.Envir.SEnvir.Players:
		if(player is None):
			continue
		player.Connection.ReceiveChat(message, type)
					
def DelayTeleport(Sender,map,sec,x,y):  #延迟传送
	Server.Envir.SEnvir.DelayCall("变量.默认变量.Teleport",sec,(Sender,map,x,y))
	
# 更改NPC外观
# 除了NPC序号为必填 其他参数为选填
# SEnvir.UpdateNPCLook(
# NPC的序号, 
# 是否永久改变-默认否，
# NPC名字-默认不改，
# NPC名字颜色-默认不改
# NPC素材文件-默认是NPC
# 外观值-默认不改
# 附加层颜色-默认不设置
# 是否更新NPC头上的任务图标-默认不改
# NPC头上的图标-默认不改
# 绑定的玩家-留空或者写None的话全服玩家都会看到更新，写的话只有指定玩家可以看到
def UpdateNPCLook(Sender, NPCIndex, Status):  #NPC任务图标赋值
	SEnvir.UpdateNPCLook(NPCIndex, permanent = False, name = None, 
                nameColor = None,
                libraryFile = LibraryFile.None, bodyShape = 0, overlay = None,
                updateIcon = True, icon = Status, player = Sender)

PKCount = 199                 #PK值设定

