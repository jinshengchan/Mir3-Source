# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
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
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[关闭:0]"""	                             
#跳转菜单1仓库				
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Storage   #类型为NPCDialogType里的仓库类
		say = """嗯...这个放这里，那个先放在那里...不好！~忘记了！
        
		[前一步:99]"""		
#主菜单
	else:	
		say = """快来吧，我叫啊勒。是受叛军首领之命，来帮助人类勇士保管
		物品的。如果有需要保管的物品，请先放在我这里。
	
		[存取:1]物品
		
		[结束:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
	
NpcEvent.add_listener(181,"OnClick",OnClick)
