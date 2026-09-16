# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
from Library import *
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
	if(Menu == 1):
		if(Sender.Character.Rebirth>=5):
			if(Sender.Character.Rebirth>5):
				Sender.Character.Rebirth=5;
				Sender.RefreshStats();
			txt="""
			你已经达到最高转生等级
			
		[离开:0]
		"""
		else:
			txt = """对于您接受的每次转生，将发生以下更改：
			<font color=0xff7fff00>你将需要等级75 +当前重估计数。</font>
			<font color=0xff7fff00>转生时，您将被设置为65级并保持当前经验的0.5％</font>
			<font color=0xff7fff00>PvE伤害增加30％</font>
			<font color=0xff7fff00>PvP伤害增加20％</font>
			<font color=0xff7fff00>爆率加成+ 20％</font>
			<font color=0xff7fff00>金币加成+ 20％</font>
			<font color=0xff7fff00>杀怪获得的经验减少0％</font>
			<font color=0xff7fff00>魔御防御加20，攻魔道加20</font>
			<font color=0xff7fff00>PvE中的每一次死亡都会让您失去所有经验。</font> （PvP无惩罚）
			
			[接受:11]
			
			
			"""
	elif(Menu == 11):
##转生的等级判断 和 是否达到转生条件	
		if (Sender.Level >= 75 + Sender.Character.Rebirth):
			Sender.NPCRebirth()
			txt = """恭喜你，成功转生了。
			
			[离开:0]"""
		else:
			txt="""你的转生条件不足无法完成转生...
			
			[离开:0]"""
	else:
		txt="你当前转生等级："+str(Sender.Character.Rebirth)
		txt += """
		
			
		
			[转生:1]
		
			[离开:0]
			
			
			
			提示：最高转到5级
			"""
	Dict['Say']=txt                         #定义聊天框对话内容
	return Dict		
	
NpcEvent.add_listener(30,"OnClick",OnClick)	