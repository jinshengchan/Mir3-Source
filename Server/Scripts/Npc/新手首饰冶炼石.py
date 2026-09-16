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
		str = """你想现在制炼项链吗？

		[项链锻造暴击几率:11]


		"""
	elif (Menu == 11):	
		#判断是否有项链	
		if (not (Sender.Equipment[int(EquipmentSlot.Necklace)])):
			Sender.Connection.ReceiveChat("你没有装备项链",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.Necklace)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  	
		#判断项链是否暴击几率5%以上
		if(Sender.Equipment[int(EquipmentSlot.Necklace)].Stats[Stat.CriticalChance] > 4):
			Sender.Connection.ReceiveChat("你的项链暴击几率已经锻造到最大值，无法再锻造了",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False
		#给项链增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.Necklace)].Stats[Stat.CriticalChance] < 5):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Necklace, Stat.CriticalChance, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)		
			elif select < 100:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Necklace, Stat.CriticalChance, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的项链没发生任何改变',MessageType.Hint)
		return
		
	elif (Menu == 2):
		str = """你想现在制炼左手手镯吗？

		[增加破坏:21]
	
		[增加全系列魔法:22]

		"""
	elif (Menu == 21):	
		#判断是否有手镯	
		if (not (Sender.Equipment[int(EquipmentSlot.BraceletL)])):
			Sender.Connection.ReceiveChat("你没有装备左手镯",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.BraceletL)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  
		#判断手镯是否最大攻击+5以上  
		if(Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxDC] > 5):
			Sender.Connection.ReceiveChat("你的左手镯攻击属性已经锻造满级了！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False			
		#给手镯增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxDC] < 6 and Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxAC] < 6):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletL, Stat.MaxDC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)		
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletL, Stat.MaxDC, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)			
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的左手镯没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 22):
		#判断是否有手镯	
		if (not (Sender.Equipment[int(EquipmentSlot.BraceletL)])):
			Sender.Connection.ReceiveChat("你没有装备左手镯",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.BraceletL)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  	
		#判断手镯是否最大全系列魔法+5以上
		if(Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxMC] > 5 and Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxSC] > 5):
			Sender.Connection.ReceiveChat("你的左手镯全系列魔法属性已经锻造满级！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False
		#给手镯增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxMC] < 6 and Sender.Equipment[int(EquipmentSlot.BraceletL)].Stats[Stat.MaxSC] < 6):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletL, Stat.MaxMC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletL, Stat.MaxSC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)			
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletL, Stat.MaxMC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletL, Stat.MaxSC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)						
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的左手镯没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 3):
		str = """你想现在制炼右手手镯吗？

		[增加破坏属性:31]
	
		[增加全系列魔法:32]

		"""
	elif (Menu == 31):	
		#判断是否有手镯	
		if (not (Sender.Equipment[int(EquipmentSlot.BraceletR)])):
			Sender.Connection.ReceiveChat("你没有装备右手镯",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.BraceletR)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  
		#判断手镯是否最大攻击+5以上  
		if(Sender.Equipment[int(EquipmentSlot.BraceletR)].Stats[Stat.MaxDC] > 5):
			Sender.Connection.ReceiveChat("你的右手镯攻击属性已经锻造满级了！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False			
		#给手镯增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.BraceletR)].Stats[Stat.MaxDC] < 6 ):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletR, Stat.MaxDC, 2, StatSource.Enhancement)   #按几率给武器增加攻击属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)		
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletR, Stat.MaxDC, 1, StatSource.Enhancement)   #按几率给武器增加攻击属性刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)			
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的右手镯没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 32):
		#判断是否有手镯	
		if (not (Sender.Equipment[int(EquipmentSlot.BraceletR)])):
			Sender.Connection.ReceiveChat("你没有装备右手镯",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.BraceletR)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  	
		#判断手镯是否最大全系列魔法+5以上 
		if(Sender.Equipment[int(EquipmentSlot.BraceletR)].Stats[Stat.MaxMC] > 5 and Sender.Equipment[int(EquipmentSlot.BraceletR)].Stats[Stat.MaxSC] > 5):
			Sender.Connection.ReceiveChat("你的右手镯全系列魔法属性已经锻造满级！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False
		#给手镯增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.BraceletR)].Stats[Stat.MaxMC] < 6 and Sender.Equipment[int(EquipmentSlot.BraceletR)].Stats[Stat.MaxSC] < 6):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletR, Stat.MaxMC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletR, Stat.MaxSC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)			
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletR, Stat.MaxMC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.BraceletR, Stat.MaxSC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)						
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的右手镯没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 4):
		str = """你想现在制炼左手戒指吗？

		[增加破坏属性:41]
	
		[增加全系列魔法:42]

		"""
	elif (Menu == 41):	
		#判断是否有戒指	
		if (not (Sender.Equipment[int(EquipmentSlot.RingL)])):
			Sender.Connection.ReceiveChat("你没有装备戒指",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.RingL)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  
		#判断戒指是否最大攻击+7以上
		if(Sender.Equipment[int(EquipmentSlot.RingL)].Stats[Stat.MaxDC] > 7):
			Sender.Connection.ReceiveChat("你的左手戒指攻击属性已增加到最大值！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.RingL)].Stats[Stat.MaxDC] < 8):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingL, Stat.MaxDC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingL, Stat.MaxDC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大破坏并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的左手戒指没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 42):
		#判断是否有戒指	
		if (not (Sender.Equipment[int(EquipmentSlot.RingL)])):
			Sender.Connection.ReceiveChat("你没有装备戒指",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.RingL)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  	
		#判断戒指是否最大全系列魔法+7以上
		if(Sender.Equipment[int(EquipmentSlot.RingL)].Stats[Stat.MaxMC] > 7 and Sender.Equipment[int(EquipmentSlot.RingL)].Stats[Stat.MaxSC] > 7):
			Sender.Connection.ReceiveChat("你的左手戒指增加的全系列魔法已经是最大值！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False
		#给戒指增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.RingL)].Stats[Stat.MaxMC] < 8 and Sender.Equipment[int(EquipmentSlot.RingL)].Stats[Stat.MaxSC] < 8):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingL, Stat.MaxMC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingL, Stat.MaxSC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)		
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingL, Stat.MaxMC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingL, Stat.MaxSC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)						
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的左手戒指没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 5):
		str = """你想现在制炼右手戒指吗？

		[增加破坏:51]
	
		[增加全系列魔法:52]

		"""
	elif (Menu == 51):	
		#判断是否有戒指	
		if (not (Sender.Equipment[int(EquipmentSlot.RingR)])):
			Sender.Connection.ReceiveChat("你没有装备戒指",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.RingR)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  
		#判断戒指是否最大攻击+7以上
		if(Sender.Equipment[int(EquipmentSlot.RingR)].Stats[Stat.MaxDC] > 7):
			Sender.Connection.ReceiveChat("你的右手戒指攻击属性已锻造到最大值！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.RingR)].Stats[Stat.MaxDC] < 8):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingR, Stat.MaxDC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingR, Stat.MaxDC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大破坏并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)		
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的右手戒指没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 52):
		#判断是否有戒指	
		if (not (Sender.Equipment[int(EquipmentSlot.RingR)])):
			Sender.Connection.ReceiveChat("你没有装备戒指",MessageType.System)
			return False
		if(Sender.Equipment[int(EquipmentSlot.RingR)].Level < 3):
			Sender.Connection.ReceiveChat("你的装备等级需要大于等于3级",MessageType.System)
			return False  
		#判断戒指是否最大全系列魔法+7以上
		if(Sender.Equipment[int(EquipmentSlot.RingR)].Stats[Stat.MaxMC] > 7 and Sender.Equipment[int(EquipmentSlot.RingR)].Stats[Stat.MaxSC] > 7):
			Sender.Connection.ReceiveChat("你的右手戒指的全系列魔法已经增加到最大值！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False
		#给戒指增加最大全系列魔法
		if(Sender.Equipment[int(EquipmentSlot.RingR)].Stats[Stat.MaxMC] < 8 and Sender.Equipment[int(EquipmentSlot.RingR)].Stats[Stat.MaxSC] < 8):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingR, Stat.MaxMC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingR, Stat.MaxSC, 2, StatSource.Enhancement)  #按几率给首饰加2点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 120:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingR, Stat.MaxMC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大自然并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.RingR, Stat.MaxSC, 1, StatSource.Enhancement)  #按几率给首饰加1点最大灵魂并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)					
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的右手戒指没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 61):
		str = """你想现在制炼衣服吗？

		[增加生命属性:61]

		"""
	elif (Menu == 6):	
		#判断是否有衣服	
		if (not (Sender.Equipment[int(EquipmentSlot.Armour)])):
			Sender.Connection.ReceiveChat("你没有装备衣服",MessageType.System)
			return False
		#判断戒指是否最大防御魔御+19以上
		if(Sender.Equipment[int(EquipmentSlot.Armour)].Stats[Stat.MaxMR] > 19  and Sender.Equipment[int(EquipmentSlot.Armour)].Stats[Stat.MaxAC] > 19):
			Sender.Connection.ReceiveChat("你的衣服防御魔御已经达到修炼最大值！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("装备特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的装备特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.Armour)].Stats[Stat.MaxMR] < 20 and Sender.Equipment[int(EquipmentSlot.Armour)].Stats[Stat.MaxAC] < 20):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Armour, Stat.MaxMR, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Armour, Stat.MaxAC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)	
			elif select < 150:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Armour, Stat.MaxMR, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Armour, Stat.MaxAC, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值		
			else:
				Sender.TakeItem("装备特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的衣服没发生任何改变',MessageType.Hint)
		return


	elif (Menu == 9):	
		#判断是否有头盔	
		if (not (Sender.Equipment[int(EquipmentSlot.Helmet)])):
			Sender.Connection.ReceiveChat("你没有装备头盔",MessageType.System)
			return False
		#判断头盔防御魔御15%以上
		if(Sender.Equipment[int(EquipmentSlot.Helmet)].Stats[Stat.HealthPercent] > 14 and Sender.Equipment[int(EquipmentSlot.Helmet)].Stats[Stat.ManaPercent] > 14):
			Sender.Connection.ReceiveChat("你的头盔防御魔御已经达到修炼的最大值！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("装备特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的装备特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.Helmet)].Stats[Stat.HealthPercent] < 15 and Sender.Equipment[int(EquipmentSlot.Helmet)].Stats[Stat.ManaPercent] < 15):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Helmet, Stat.HealthPercent, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Helmet, Stat.ManaPercent, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)		
			elif select < 150:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Helmet, Stat.HealthPercent, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Helmet, Stat.ManaPercent, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)		
			else:
				Sender.TakeItem("装备特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的头盔没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 7):	
		#判断是否有鞋子	
		if (not (Sender.Equipment[int(EquipmentSlot.Shoes)])):
			Sender.Connection.ReceiveChat("你没有装备鞋子",MessageType.System)
			return False
		#判断戒指是否最大闪避 9%
		if(Sender.Equipment[int(EquipmentSlot.Shoes)].Stats[Stat.EvasionChance] > 9):
			Sender.Connection.ReceiveChat("你的鞋子已经鉴定满10%闪避，不可再鉴定！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("装备特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的装备特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.Shoes)].Stats[Stat.EvasionChance] < 10):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Shoes, Stat.EvasionChance, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)	
			elif select < 100:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Shoes, EvasionChance, 1, StatSource.Enhancement)  #按几率给首饰加1点最大破坏并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)		
			else:
				Sender.TakeItem("装备特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的鞋子没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 8):	
		#判断是否有盾牌	
		if (not (Sender.Equipment[int(EquipmentSlot.Shield)])):
			Sender.Connection.ReceiveChat("你没有装备盾牌",MessageType.System)
			return False
		#判断盾牌是否最大19%格挡
		if(Sender.Equipment[int(EquipmentSlot.Shield)].Stats[Stat.BlockChance] > 19):
			Sender.Connection.ReceiveChat("你的盾牌已经鉴定满20%格挡，不可再鉴定！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("装备特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的装备特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.Shield)].Stats[Stat.BlockChance] < 20):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Shield, Stat.BlockChance, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)		
			elif select < 100:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Shield, Stat.BlockChance, 1, StatSource.Enhancement)  #按几率给首饰加1点最大破坏并刷新属性值
				Sender.TakeItem("装备特殊属性修炼石",1)		
			else:
				Sender.TakeItem("装备特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的盾牌没发生任何改变',MessageType.Hint)
		return

	elif (Menu == 10):	
		#判断是否有火把	
		if (not (Sender.Equipment[int(EquipmentSlot.Torch)])):
			Sender.Connection.ReceiveChat("你没有装备火把",MessageType.System)
			return False
		#判断戒指是否最大攻击+4以上
		if(Sender.Equipment[int(EquipmentSlot.Torch)].Stats[Stat.ProtectionRing] > 49):
			Sender.Connection.ReceiveChat("你的火把已经鉴定出护身效果，不可再鉴定！",MessageType.System)
			return False
		#判断是否有要求的道具			
		if(Sender.GetItemCount("首饰特殊属性修炼石") < 1):
			Sender.Connection.ReceiveChat("你的首饰特殊属性修炼石呢？",MessageType.System)
			return False			
		#给戒指增加最大攻击
		if(Sender.Equipment[int(EquipmentSlot.Torch)].Stats[Stat.ProtectionRing] < 50):
			select = random.randint(0,1000)
			if select < 10:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxDC, 5, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxMC, 5, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxSC, 5, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 20:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxDC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxMC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxSC, 2, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 30:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxDC, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxMC, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.MaxSC, 1, StatSource.Enhancement)   #按几率给武器特殊属性并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 80:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.HealthPercent, 2, StatSource.Enhancement)  #按几率给首饰加1点最大破坏并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			elif select < 250:
				Sender.ItemStatsChangeRefresh(EquipmentSlot.Torch, Stat.HealthPercent, 1, StatSource.Enhancement)  #按几率给首饰加1点最大破坏并刷新属性值
				Sender.TakeItem("首饰特殊属性修炼石",1)	
			else:
				Sender.TakeItem("首饰特殊属性修炼石",1)	
				Sender.Connection.ReceiveChat('你的火把没发生任何改变',MessageType.Hint)
		return

								
	else:
		str = """使用首饰特殊属性修炼石给物品增加随机属性
		当达到该类装备最大值将不再增加属性。
			 
		<font color=\"0xff00ff00\">头盔--HPMP  衣服--防御魔御  鞋子--闪避   盾牌--格挡 </font>
		
		[头盔:9]  可增加15%HPMP       [衣服:6]可增加20点魔防御		
		          		              
		[手镯左:2]可增加6点攻击属性  [手镯右:3]可增加6点攻击属性
		
		[戒指左:4]可增加10点攻击属性 [戒指右:5]可增加10点攻击属性
		
		[鞋子:7]  可增加10%闪避几率  [盾牌:8] 可增加20%格挡几率    
		
		[项链:1]  最高加5%暴击几率属性         

		[关闭:0]
	
	"""
	
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(190,"OnClick",OnClick)