# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
from System import DateTime
import NpcEvent
import random
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
	
	if (Menu == 1):	
		#判断手上是否有战士武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否指定武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [354,206,652,918,1366,5818,17011]):
			Sender.Connection.ReceiveChat("你的武器不是特定武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False                      
		#判断手上的武器是否最大攻速+19以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.AttackSpeed] > 19):
			Sender.Connection.ReceiveChat("你的武器攻击速度也打到最高等级",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石制炼石呢？",MessageType.System)
			return False			
		#给手上的武器增加攻击速度
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.AttackSpeed] < 20):
			select = random.randint(0,1000)
			if select < 50:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.AttackSpeed, 1, StatSource.Enhancement)   #按几率给武器加2点最大破坏并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 100:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.AttackSpeed, 1, StatSource.Enhancement)   #按几率给武器加1点最大破坏并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.AttackSpeed]  < 2:              #前3点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.AttackSpeed, 1, StatSource.Enhancement)   #按几率给武器加1点最大破坏并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return
	elif(Menu == 2):	
		#判断手上是否有战士武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否是特定武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [354,206,652,918,1366,5818,17011]):
			Sender.Connection.ReceiveChat("你的武器不是可修炼武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False                                            
		#判断手上的武器是否最大吸血+10%以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.LifeSteal] > 9):
			Sender.Connection.ReceiveChat("你的武器吸血几率制炼已经满级",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False			
		#给手上的武器增加吸血几率
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.LifeSteal] < 10):
			select = random.randint(0,1000)
			if select < 50:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.LifeSteal, 2, StatSource.Enhancement)   #按几率给武器加2点最大吸血并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 100:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.LifeSteal, 1, StatSource.Enhancement)   #按几率给武器加1点最大破坏并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.LifeSteal]  < 2:              #前2点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.LifeSteal, 1, StatSource.Enhancement)   #按几率给武器加1点最大破坏并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return


	elif (Menu == 4):
		#判断手上是否有法师武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否特定武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [209,355,654,665,918,1119,5819,17011]):
			Sender.Connection.ReceiveChat("你的武器不是特定武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False               
		#判断手上的武器是否最大幻影攻击+20以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.PhantomAttack] > 19):
			Sender.Connection.ReceiveChat("你的武器幻影攻击元素已经达到最大值，无法再增加了",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False
		#给手上的武器增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.PhantomAttack] < 20):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.PhantomAttack, 2, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 150:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.PhantomAttack, 1, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)					
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.PhantomAttack] < 2:  #前5点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.PhantomAttack, 1, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return
	elif (Menu == 7):
		#判断手上是否有法师武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否特定武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [209,355,654,665,918,1119,5819,17011]):
			Sender.Connection.ReceiveChat("你的武器不是特定武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False               
		#判断手上的武器是否最大会心几率+20以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalHit] > 19):
			Sender.Connection.ReceiveChat("你的武器幻影攻击元素已经达到最大值，无法再增加了",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False
		#给手上的武器增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalHit] < 20):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalHit, 2, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 120:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalHit, 1, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)					
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalHit] < 2:  #前3点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalHit, 1, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 6):
		#判断手上是否有武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否有道士武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [208,356,653,890,918,5820,17011]):
			Sender.Connection.ReceiveChat("你的武器不是可修炼武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False 	
		#判断手上的武器是否武器暴击几率最大+20以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalChance] > 19):
			Sender.Connection.ReceiveChat("你的武器已经元素属性已经升级到最高等级",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False
		#给手上的武器增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalChance] < 20):
			select = random.randint(0,1000)
			if select < 50:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 2, StatSource.Enhancement)  #按几率给武器加1点最大暴击几率并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 150:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 1, StatSource.Enhancement)  #按几率给武器加1点最大暴击几率并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)					
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalChance] < 2:  #前2点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 1, StatSource.Enhancement)  #按几率给武器加1点最大暴击几率并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return



	elif (Menu == 3):
		#判断手上是否有战士武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否新手武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [354,206,652,918,1366,5818,17011]):
			Sender.Connection.ReceiveChat("你的武器不是可修炼武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False 	
		#判断手上的武器麻痹属性是否+10以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.ParalysisChance] > 9):
			Sender.Connection.ReceiveChat("你的武器鉴定已经满麻痹率10%，不可再鉴定！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False
		#给手上的武器增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.ParalysisChance] < 10):
			select = random.randint(0,1000)
			if select < 5:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.ParalysisChance, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)
			elif select < 50:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.ParalysisChance, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.ParalysisChance]  < 2:              #前2点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.ParalysisChance, 1, StatSource.Enhancement)   #按几率给武器加1点最大破坏并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return
	elif (Menu == 5):
		#判断手上是否有武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否有道士武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [208,356,653,890,918,5820,17011]):
			Sender.Connection.ReceiveChat("你的武器不是可修炼武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False 	
		#判断手上的武器是否最大+20以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.HolyAttack] > 19):
			Sender.Connection.ReceiveChat("你的武器已经元素属性已经升级到最高等级",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False
		#给手上的武器增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.HolyAttack] < 20):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.HolyAttack, 2, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 150:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.HolyAttack, 1, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)					
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.HolyAttack] < 2:  #前3点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.HolyAttack, 1, StatSource.Enhancement)  #按几率给武器加1点最大自然并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return
	elif (Menu == 8):
		#判断手上是否有武器	
		if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
			return False
		#判断手上的武器是否有战士武器	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [354,206,652,918,1366,5818,17011]):
			Sender.Connection.ReceiveChat("你的武器不是可修炼武器",MessageType.System)
			return False
        #判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			Sender.Connection.ReceiveChat("你的武器没有升级到最高等级",MessageType.System)
			return False 	
		#判断手上的武器是否武器暴击几率最大+20以上
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalChance] > 19):
			Sender.Connection.ReceiveChat("你的武器已经元素属性已经升级到最高等级",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("武器特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的武器特殊属性修炼石呢？",MessageType.System)
			return False
		#给手上的武器增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalChance] < 20):
			select = random.randint(0,1000)
			if select < 50:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 2, StatSource.Enhancement)  #按几率给武器加1点最大暴击几率并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			elif select < 150:
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 1, StatSource.Enhancement)  #按几率给武器加1点最大暴击几率并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)					
			elif select > 10 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.CriticalChance] < 2:  #前2点几乎必成
				Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 1, StatSource.Enhancement)  #按几率给武器加1点最大暴击几率并刷新属性值
				Sender.TakeItem("武器特殊属性修炼石",1)	
			else:
				Sender.TakeItem("武器特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
		return							
	else:
		str = """武器升级到满级后，
如果有武器特殊属性修炼石，
我这里可以给武器附加特殊属性
成功后，属性会增加1-2点，失败武器不会破碎！
提醒<font color=0xffFF0033>工艺完成后再来进行特殊属性提升</font>


三职业通用武器：

<font color=0xffFF00CC>飞龙剑</font>||<font color=0xffFF00CC>影魅之刃</font>

战士可升级武器：

<font color=0xff009966>霹雷</font>||<font color=0xff009966>屠龙</font>||<font color=0xff009966>破山剑</font>||<font color=0xff009966>天狼刀</font>||<font color=0xff009966>桃源虎翼刀</font>

[武器增加攻击速度:1][武器加吸血:2][武器加麻痹:3][武器加暴击:8]

法师可升级武器：

<font color=0xff00FF33>嗜魂法杖</font>||<font color=0xff00FF33>铁轮</font>||<font color=0xff00FF33>天神法杖</font>||<font color=0xff00FF33>拐杖</font>||<font color=0xff00FF33>桃源曜灵杖</font>
	
[法师武器增加幻影元素:4] [法师武器增加会心一击几率:7] 
 
道士可升级武器：

<font color=0xff00FF00>龙纹剑</font>||<font color=0xff00FF00>逍遥扇</font>||<font color=0xff00FF00>泰轮拂尘</font>||<font color=0xff00FF00>阴阳刀</font>||<font color=0xff00FF00>桃源三焰扇</font>
 
[道士武器增加神圣元素:5] [道士武器增加暴击几率:6]

		[关闭:0]"""
	
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(191,"OnClick",OnClick)