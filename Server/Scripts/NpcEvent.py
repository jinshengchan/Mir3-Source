# -*- coding: utf-8 -*-
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import Server
_data={}
_all_data={}

def add_listener(npc_index,fun_name,fun):
	if (npc_index not in _data.keys()):  
		_data[npc_index] = {}
	d = _data[npc_index];
	d[fun_name] = fun;

def add_all_listener(fun_name,fun):
	_all_data[fun_name] = fun



def trig_npc(npc,fun_name,args):
	if(npc.NPCInfo.Index in _data.keys()):
		d = _data[npc.NPCInfo.Index];
		if(fun_name in d.keys()):
			fun = d[fun_name]
			return fun(args)
		else:
			return
	elif(fun_name in _all_data.keys()):
		fun = _all_data[fun_name]
		return fun(args)
	else:	
		return
		
		
		
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	
	Dict={}	 
	say = """欢迎你进入游戏..."""+"%d"%Self.NPCInfo.Index
	#Sender.Connection.ReceiveChat("123",MessageType.System)
	#Server.Envir.SEnvir.Log("%d"%Self.NPCInfo.Index+"未找到")
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
add_all_listener("OnClick",OnClick)