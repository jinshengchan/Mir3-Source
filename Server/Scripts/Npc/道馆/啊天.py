# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
from 主线任务奖励 import *
import Server.Envir.SEnvir as SEnvir
import time
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
	say = ''
	
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[关闭:0]"""	                             
#跳转菜单1仓库
	elif(PlayerGetTempV(Sender,TV_PLAYER_STORE_PASSWORD_SUCCESS)==1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Storage   #类型为NPCDialogType里的仓库类
		say = """把东西存放在这里，你可放心。
			
			[前一步:99]"""
		PlayerSetTempV(Sender,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
	elif (Menu == 1):
		if CheckPassWord([Sender]):
			Dict['Types'] =types		        #定义类别
			Dict['DialogType'] = NPCDialogType.Storage   #类型为NPCDialogType里的仓库类
			say = """把东西存放在这里，你可放心。
			
				[前一步:99]"""
	elif (Menu == 2):
		say = """[设置或修改密码:21]
		
		[取消密码:22]
		"""
	elif Menu ==  21:
		InputPassWord([Sender])
	elif Menu == 22:
		DeletePassWord([Sender])
#主菜单
	else:	
		say = """欢迎光临！你可以把东西存放在我这里。
	
		[存取:1]物品
		
		[仓库密码管理:2]
		
		[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def InputPassWord(params):
	player = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None
	PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
	if not userInput or len(userInput) < 1:	
		password = PlayerGetObV(player, GV_PLAYER_STORE_PASSWORD)
		if password is None:#如果没有设置密码
			PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,1)
			player.PyInputBox("请输入新密码（不超过10位）\n\n密码不能为空", "Npc.道馆.啊天.InputNewPassWord1", "Npc.道馆.啊天.CannelPassWord")
		else:
			#player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
			player.PyInputBox("请输入仓库密码", "Npc.道馆.啊天.InputPassWord", "Npc.道馆.啊天.CannelPassWord")
	else:
		password = PlayerGetObV(player, GV_PLAYER_STORE_PASSWORD)
		if password is None: return
		if len(userInput)>10 or password.ToString() != userInput: #验证旧密码
			PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)#设置验证标识为FALSE 防止外挂
			player.Connection.ReceiveChat("您输入的密码有误",MessageType.System)
		else:
			PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,1)#设置验证标识为TRUE 防止外挂
			player.PyInputBox("请输入新密码（不超过10位）\n\n密码不能为空", "Npc.道馆.啊天.InputNewPassWord1", "Npc.道馆.啊天.CannelPassWord")
		#use_code(player, userInput, player.Character.Account.EMailAddress)

def InputNewPassWord1(params):#第一次输入密码
	player = params[0]
	userInput = params[1] if len(params) > 1 else 0
	if PlayerGetTempV(player, TV_PLAYER_STORE_PASSWORD_SUCCESS) == 0:
		#外挂
		pass
	else:
		if len(userInput)>10:
			player.PyInputBox("请输入新密码（不超过10位）\n\n密码不能为空", "Npc.道馆.啊天.InputNewPassWord1", "Npc.道馆.啊天.CannelPassWord")
			return
		PlayerSetTempV(player, TV_PLAYER_STORE_PASSWORD1,userInput)#记录第一次输入的密码
		player.PyInputBox("请再次输入新密码", "Npc.道馆.啊天.InputNewPassWord2", "Npc.道馆.啊天.CannelPassWord")
		
def InputNewPassWord2(params):#第二次输入密码验证
	player = params[0]
	userInput = params[1] if len(params) > 1 else 0		
	if PlayerGetTempV(player, TV_PLAYER_STORE_PASSWORD_SUCCESS) == 0:
		#外挂
		pass
	elif PlayerGetTempV(player, TV_PLAYER_STORE_PASSWORD1) == userInput:#二次验证成功
		PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
		player.Connection.ReceiveChat("密码修改成功",MessageType.System)
		PlayerSetObV(player, GV_PLAYER_STORE_PASSWORD,userInput)
	else:
		player.PyInputBox("两次密码输入不同，请重新输入新密码", "Npc.道馆.啊天.InputNewPassWord1", "Npc.道馆.啊天.CannelPassWord")

def CannelPassWord(params):
	player = params[0]
	userInput = params[1] if len(params) > 1 else 0	
	PlayerSetTempV(player, TV_PLAYER_STORE_PASSWORD1,0)#记录第一次输入的密码
	PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
	
def DeletePassWord(params):
	player = params[0]
	userInput = params[1] if len(params) > 1 else 0
	PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
	if not userInput or len(userInput) < 1:
		password = PlayerGetObV(player, GV_PLAYER_STORE_PASSWORD)
		if password is None:#如果没有设置密码
			player.Connection.ReceiveChat("仓库密码已撤销",MessageType.System)
		else:
			#player.Connection.ReceiveChat("用户还没有输入信息",MessageType.System)
			player.PyInputBox("请输入仓库密码", "Npc.道馆.啊天.DeletePassWord", "Npc.道馆.啊天.CannelPassWord")
	else:
		password = PlayerGetObV(player, GV_PLAYER_STORE_PASSWORD)
		if password is None: return
		if len(userInput)>10 or password.ToString() != userInput: #验证旧密码
			player.Connection.ReceiveChat("您输入的密码有误",MessageType.System)
		else:
			player.Connection.ReceiveChat("仓库密码已撤销",MessageType.System)
			PlayerSetObV(player, GV_PLAYER_STORE_PASSWORD ,None)

def CheckPassWord(params):
	player = params[0]
	userInput = params[1] if len(params) > 1 else 0
	PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
	if not userInput or len(userInput) < 1:
		password = PlayerGetObV(player, GV_PLAYER_STORE_PASSWORD)
		if password is None:#如果没有设置密码
			return True
		else:
			player.PyInputBox("请输入仓库密码", "Npc.道馆.啊天.CheckPassWord", "Npc.道馆.啊天.CannelPassWord")
	else:
		password = PlayerGetObV(player, GV_PLAYER_STORE_PASSWORD)
		if password is None: return False
		if len(userInput)>10 or password.ToString() != userInput: #验证旧密码
			player.Connection.ReceiveChat("您输入的密码有误",MessageType.System)
		else:
			PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,1)
			targetNPCInfo = SEnvir.GetNpcInfo(41);
			NPCMap = SEnvir.GetMap(targetNPCInfo.Region.Map)
			ob = NPCMap.NPCs.Find(lambda x: x.NPCInfo.Index == 41) 
			player.NPCCall(ob.ObjectID,False)
			PlayerSetTempV(player,TV_PLAYER_STORE_PASSWORD_SUCCESS,0)
			pass
		
	return False


#类型为 Enums里的普通类
types =[ItemType.Nothing]
	
NpcEvent.add_listener(41,"OnClick",OnClick)
