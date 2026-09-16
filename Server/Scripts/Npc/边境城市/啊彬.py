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
import System
s1 = clr.Reference[System.Object]()
from Defines import *
import Server
import unicodedata
from Utils import ServerUtils
from Npc import *
import Server.Envir.SEnvir as SEnvir
import Library as Library
import random
from Utils.PlayerUtils import *
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
from Library import *
import unicodedata
import random
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
# 武器初始化设置
###############
# 稀世首饰 加成功率
ELITE_SUCCESS_RATE = 30
# 高级首饰 加成功率
SUPERIOR_SUCCESS_RATE = 20
# 普通首饰 加成功率
COMMOM_SUCCESS_RATE = 15
#####################################################
# 首饰制炼设置
############
#首饰种类限制
ALLOWED_ITEM_TYPES = [ItemType.Necklace, ItemType.Bracelet, ItemType.Ring,]

#首饰合成同种首饰数量（普通3个  高级2个  稀世2个）
REFINE_RARITY_AMOUNT = {'Common':3,'Superior':2,'Elite':2,}

# 首饰合成成功率设置
# 按照装备品质定义成功率和制炼上限
# 0：100意思是属性从+0升级到+1的成功率是100%
# 可以删除也往后添加 不在这个字典里的不能升级
REFINE_SUCCESS_RATES = {
'Common':{0:30, 1:42, 2:54, 3:66, 4:78, 5:80},
'Superior':{0:40, 1:48, 2:56, 3:64, 4:70, 5:70},
'Elite':{0:40, 1:48, 2:56, 3:64, 4:70, 5:70},}
# 用于存储制炼首饰编号的个人临时变量
#TK_SHOUSHIHECHENG = 99999

#####淬炼属性
StatList=[
Stat.CriticalChance,
Stat.CriticalDamage,
Stat.ACIgnoreRate,
Stat.MRIgnoreRate,
Stat.FinalDamageReduceRate,
]

StatString=[
"暴击几率",
"暴击伤害",
"无视物防",
"无视魔防",
"最终伤害减少",
]
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	bg = {}
	font={}
	item={}
	needitems={}
	say=''
	
#红名判断
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """请你离开。
		
		我不想和红名交易。
		
		[结束:0]"""

#重置武器
	elif(Menu == 1):
		say = """初始化武器：把你的武器重新初始化变成1级的新武器
		初始化武器只初始化武器的主属性，如（破坏 魔法 元素）
		幸运 强度 速度 等一些特殊属性不会被初始化
		
		                   [初始化武器:11]
		
		        <font color=\"0xff00ff00\">（需要100万金币，魔晶石和5个饰品）</font>
		
		 <font color=\"0xffff0000\">（初始化武器最好使用5个稀世首饰，武器不容易破碎）</font>
		
		 <font color=\"0xffffffff\">注意：包裹内只能保留洗武器所需材料，无关物品请勿留在包裹内，丢失后果自负！！！</font>
		
		         [取回武器:12]               [关闭:0]"""
	elif(Menu == 11):
		say = ""
		count = 0
		itemslist = []
		# 统计背包里所有装备信息
		for i in range(Globals.InventorySize):  #遍历包裹格子
			item = Sender.Inventory[i]  #道具定义格子里的道具
			if item:         #道具不为空
				if item.Info.ItemType in ALLOWED_ITEM_TYPES:    #道具类型
					count = count + 1 
					itemslist.append(item)
					if count >= 5:   #计数大于5跳出
						break
						
#判断包裹里的首饰数量
		if count < 5 :
			say= """请整理背包首饰，合成需要5个首饰
			
			[结束:0]"""
#判断重置时需要的金币
		elif (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。
			
			[结束:0]"""
#判断重置时手上是否有武器
		elif (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			say ="""你没有装备武器。
			请装备好武器再来。
			
			[结束:0]"""
#判断是否达到重置武器等级要求
		elif(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 2):
			say ="""你的武器等级没有2级以上。
			不能重置你的武器。
			
			[结束:0]"""
		elif(Sender.Equipment[int(EquipmentSlot.Weapon)].IsRefine):
			say = """你的武器处于精炼状态。
			不能重置你的武器。
			
			[结束:0]"""
#判断是否有重置要求的道具
		elif(Sender.GetItemCount("魔晶石") < 1):
			say ="""你的材料不足。
			请准备好足够的材料在来。
			
			[结束:0]"""
		else:
			#成功几率定义
			chance = random.randint(1,100)
			#定义道具增加的几率
			GainsRate = 0
			for item in itemslist:
				if item.Info.Rarity == Rarity.Common:
					GainsRate += COMMOM_SUCCESS_RATE   #普通首饰增加成功几率
				elif item.Info.Rarity == Rarity.Superior:
					GainsRate += SUPERIOR_SUCCESS_RATE  #高级首饰增加成功几率
				elif item.Info.Rarity == Rarity.Elite:
					GainsRate += ELITE_SUCCESS_RATE  #稀世首饰增加成功几率
				#在循环里扣掉首饰
				Sender.TakeItem(item.Info, 1)
			#循环外扣除金币材料
			SubGold(Sender,1000000)
			Sender.TakeItem("魔晶石",1)
			#判断成功几率
			if chance <= GainsRate:
				#成功重置武器
				Sender.NPCResetWeapon()
				say="""你的武器重置成功。
				请点击[取回:12]
				
				[结束:0]"""
			else:
				#失败武器破碎
				deleteEquip(Sender,'武器')
				say="""你的武器重置失败，武器破碎了。
				
				[结束:0]"""
#取回武器
	elif(Menu == 12):
		if(Sender.Character.Refines.Count > 0):
			for i in range(Globals.InventorySize):  #遍历包裹格子
				item = Sender.Inventory[i]  #道具定义格子里的道具
				if item is None:         #道具不为空
					Sender.PYNPCRefineRetrieve()
					break
		else:
			say ="""这是你目前正在改进的武器清单，
			如果你没有看到它，那么你一定已经收到了它。
			
			[关闭:0]"""
#首饰合成
	elif (Menu == 2):
		say = """[输入进行制炼的饰品名:21]
		"""
	elif (Menu == 21):
		GetItemNameInput([Sender])
		say = """[输入进行制炼的饰品名:21]
		"""
	elif (Menu == 22):
		userInput = None
		if len(args) >3:
			userInput = args[3]
		if userInput:
			say = """真的进行制炼 <font color=\"0xff00ff00\">{}</font> 吗？饰品制炼是溶解3个饰品制炼出一个高级饰品的过程。因工艺上比较复杂，所以成功率较低。制炼之前，请注意这一点。不要再失败后怨天尤人，不管怎样都不能拿回原来的物品。
			
			对了，如果是高级物品2个也可以进行制炼。
			
			[制炼破坏力:221]
			[制炼魔法:222]
			[制炼元素（火）:223]
			[制炼元素（冰）:224]
			[制炼元素（雷）:225]
			[制炼元素（风）:226]
			[制炼元素（神圣）:227]
			[制炼元素（暗黑）:228]
			[制炼元素（幻影）:229]
			[了解饰品制炼方法:230]
			""".format(userInput)
# 221-229是制炼
	elif Menu in range(221,230):
#获取输入的道具的ID
		itemindex = PlayerGetTempV(Sender,TK_SHOUSHIHECHENG)
#判断需要的金币
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法制炼。

			[离开:0]"""
#判断是否有要求的刚玉石
		elif(Sender.GetItemCount("钢玉石") < 1):
			say ="""你没有钢玉石，无法制炼。

			[离开:0]"""
		else:
			say = ""
			itemslist = []
			target_item_info = [x for x in SEnvir.ItemInfoList.Binding if x.Index == itemindex]
			if len(target_item_info) > 0 and target_item_info[0]:
				# 输入的饰品名有效 
				# 检查是否可以制炼
				if target_item_info[0].ItemType in ALLOWED_ITEM_TYPES:
					# 确定需要几个饰品
					amount = REFINE_RARITY_AMOUNT[str(target_item_info[0].Rarity)]
					# 开始翻包裹
					for i in range(Globals.InventorySize):  #遍历包裹格子
						item = Sender.Inventory[i]  #道具定义格子里的道具
						if item and item.Info.Index == itemindex: #道具不为空 道具的ID等输入的ID
							itemslist.append(item)
							if len(itemslist) >= amount:
								# 只看前n个饰品就行
								break
					if len(itemslist) < amount:
						Sender.Connection.ReceiveChat("饰品数量不足，无法制炼",MessageType.System)
					else:
						# 可以开始制炼
						say = ZhiLianShouShi(Sender, Menu, itemslist)
				else:
					say = "不是饰品道具，无法制炼"
			else:
				say = "不存在该道具，无法制炼"
				
	elif (Menu == 230):
		say = """我来告诉你饰品制炼的方法吧。
		先告诉你所需要的材料。首先，准备需要进行制炼的3个同样的饰品。还有，一个钢玉石和一定的制炼费用。
		
		下面讲的是进行制炼时需要注意的几点。进行饰品制炼时，最主要的是饰品具有的附加属性。把附加属性视为成败的关键也不为过。还有，必须准备好个制炼属性相同的饰品。这点也很重要。
		
		还有，如果一般物品所需数量为3个，但是，利用高级物品制炼2个即可。
		
		这是我20年来所积累的经验。在饰品制炼时，物品的附加属性越多成功的几率就越高。如果是高级物品或稀有物品，即使没有附加属性成功率也比较高。相信你也听过物有所值这句话。我觉得这句话说的非常好！（。。。。呵呵）
		
		但是，最终成功与否还是看你运气了。还有。。。即使制炼失败也不要责怪我，因为我已经尽力了。。
		
		[重新进行制炼:2]
		"""
#钢玉石合成
	elif (Menu == 3):
		say = """制作钢玉石需要<font color=\"0xff00ff00\">纯度10以上的10个钢玉石矿</font>和<font color=\"0xff00ff00\">10万金币</font>。
		想不想制作？
		
		[收集完所需材料:31]
		[还没有收集好所需材料，等一会再来:0]"""
	elif (Menu == 31):
		if Sender.Gold < 100000:
			say = """你的金币不足，无法制作
			
			[关闭:0]"""
		else:
			say = ""
			itemslist = []
			for i in range(Globals.InventorySize):  #遍历包裹格子
				item = Sender.Inventory[i]  #道具定义格子里的道具
				if item and str(item.Info.ItemName) == '钢玉石矿' and item.CurrentDurability >= 9500:         #道具不为空
					itemslist.append(item)
			if len(itemslist) >= 10:
				for i in range(10):
					Sender.TakeItem(itemslist[i],1)
				SubGold(Sender, 100000)
				Sender.GiveItem('钢玉石', 1, False)   #false 代表 有几率获得极品
			else:
				say = """需要 <font color=\"0xff00ff00\"> 10块钢玉矿石 </font> 才可以帮您冶炼钢玉石。
				你的矿石不足或者纯度不是10以上的，无法制作
				
				[关闭:0]"""
	elif (Menu == 4):
		say = """[淬炼合成:41]
		
		[首饰分解淬炼石:42]
		
		[淬炼首饰重置:43]"""
	elif Menu == 41:
		Dict['bg'] = bg
		Dict['needitems'] = needitems
		item['pos_x'] = 100								#需求物品框位置,相对于bg左上角来说
		item['pos_y'] = 85
		item['file']=3
		item['idx']=910
		needitems[0] = item
		item = {}
		item['pos_x'] = 250								#需求物品框位置,相对于bg左上角来说
		item['pos_y'] = 85
		item['file']=3
		item['idx']=910
		needitems[1] = item
		say = """<font  size=9F  color=0xff00ff00  x=30  y=2 >首饰单属性加3或以上的，两个相同属性首饰即可合成</font>
		<font  size=9F  color=0xff00ff00  x=60  y=22 >要求材料:淬炼石1个，钢玉石1个，10W金币</font>
		<font  size=9F  color=0xff00ff00  x=70  y=42 >放首饰到格子内,不能放入小退下即可</font>
		<font  size=9F  color=0xff00ff00  x=72  y=65 >主首饰:</font>
		<font  size=9F  color=0xff00ff00  x=224  y=65 >副首饰:</font>
		
		
		
		
		
		                         [淬炼合成:411]"""
	elif Menu == 411:
		Links = args[3]
		if Links is None or Links.Count == 0 or Links[0].Slot < 0 or Links[0].Slot > Globals.InventorySize:
			Sender.Connection.ReceiveChat("没有放置物品，无法淬炼。", MessageType.System)
			return
		if Links is None or Links.Count == 1 or Links[1].Slot < 0 or Links[1].Slot > Globals.InventorySize:
			Sender.Connection.ReceiveChat("没有放置物品，无法淬炼。", MessageType.System)
			return
		item = Sender.Inventory[Links[0].Slot]
		item1 = Sender.Inventory[Links[1].Slot]
		#SEnvir.Log("{}  {}".format(Links[0].Slot,Links[1].Slot))
		if item is None or item1 is None:
			Sender.Connection.ReceiveChat("主副首饰格子内没有首饰，无法淬炼。", MessageType.System)
			return
		#判断主首饰格子的首饰是否淬炼过
		cuilianflag = False
		amountflag = True
		count = 0
		
		target_stats = set()
		source_stats = set()
		attrflag = False
		
		exclude_stat_type = None
		exclude_stat_amount = 0
		for stat in item.AddedStats:
			#SEnvir.Log("主首饰：{}， 数值：{}， 来源：{}".format(stat.Stat, stat.Amount, stat.StatSource))
			#attrflag = False
			if stat.StatSource == StatSource.Other:
				# 记录一下 有一个属性，来源是淬炼，在后续判断里面要剔除
				cuilianflag = True
				exclude_stat_type = stat.Stat
				exclude_stat_amount = stat.Amount
			#if stat.StatSource in [StatSource.Added, StatSource.Combine]:
			source_stats.add(stat.Stat)
		for stat in item1.AddedStats:
			#SEnvir.Log("副首饰：{}， 数值：{}， 来源：{}".format(stat.Stat, stat.Amount, stat.StatSource))
			#if stat.StatSource  in [StatSource.Added, StatSource.Combine]:
			target_stats.add(stat.Stat)
		
		stat_ok = False
		for stat_type in source_stats:
			if stat_type in target_stats:
				# 这里需要获取属性总和
				source_stat_total_amount = item.GetTotalAddedStat(stat_type)
				#SEnvir.Log("主首饰属性：{}， 总和：{}".format(stat_type, source_stat_total_amount))
				target_stat_total_amount = item1.GetTotalAddedStat(stat_type)
				#SEnvir.Log("副首饰属性：{}， 总和：{}".format(stat_type, target_stat_total_amount))
				# 主首饰有一个属性的数值大于等于3，并且副首饰的此属性也大于等于3，并且数值相等
				if source_stat_total_amount >= 3 and source_stat_total_amount == target_stat_total_amount:
					stat_ok = True
					# break掉，不用往下看了
					break
		
		# 这里用字典就可以了
		if not set(source_stats).isdisjoint(target_stats):
			amountflag = False
		# for stat1 in item1.AddedStats:
		# if(stat.StatSource == stat1.StatSource and stat.Stat == stat1.Stat and stat.Amount == stat1.Amount):
		# attrflag =True
		# if not attrflag:
		# break
		# if count >= 3:
			# amountflag = False
		# if attrflag:
			#for stat in item1.AddedStats:
				#attrflag = False
			# for stat1 in item.AddedStats:
			# if(stat.StatSource == stat1.StatSource and stat.Stat == stat1.Stat and stat.Amount == stat1.Amount):
			# attrflag =True
			# if not attrflag:
			# break
		if item.Info.ItemType != ItemType.Necklace and item.Info.ItemType != ItemType.Bracelet and item.Info.ItemType != ItemType.Ring:
			Sender.Connection.ReceiveChat("主首饰格子内不是首饰，无法淬炼。", MessageType.System)
		elif item1.Info.ItemType != ItemType.Necklace and item1.Info.ItemType != ItemType.Bracelet and item1.Info.ItemType != ItemType.Ring:
			Sender.Connection.ReceiveChat("副首饰格子内不是首饰，无法淬炼。", MessageType.System)
		elif item.Info.Index != item1.Info.Index:
			Sender.Connection.ReceiveChat("主副首饰格子内首饰不相同，无法淬炼。", MessageType.System)
		#判断两个格子的首饰属性是否一致
		#elif not item.Info.Stats.Compare(item1.Info.Stats):
		#	Sender.Connection.ReceiveChat("主副首饰格子内首饰属性不相同，无法淬炼。", MessageType.System)
		elif cuilianflag:
			Sender.Connection.ReceiveChat("主首饰格子内首饰淬炼过，无法淬炼。", MessageType.System)
		elif not stat_ok:
			Sender.Connection.ReceiveChat("主副首饰格子内首饰极品属性不同，无法淬炼。", MessageType.System)
		else:
			if (Sender.Gold < 100000):
				Sender.Connection.ReceiveChat("你金币不足，无法淬炼。", MessageType.System)
			elif Sender.GetItemCount("钢玉石") < 1:
				Sender.Connection.ReceiveChat("你缺少钢玉石，无法淬炼。", MessageType.System)
			elif Sender.GetItemCount("淬炼石") < 1:
				Sender.Connection.ReceiveChat("你缺少淬炼石，无法淬炼。", MessageType.System)
			else:
				select = random.randint(0,len(StatList)-1)
				select1 = random.randint(0,100)
				if select1 < 20:
					SubGold(Sender,100000)
					Sender.TakeItem("钢玉石",1) #扣掉钢玉石
					Sender.TakeItem("淬炼石",1) #扣掉淬炼石
					Sender.TakeItem(item1,1)    #扣掉副首饰
					say = """淬炼失败。
					
					[离开:0]"""
				else:
					SubGold(Sender,100000)
					Sender.TakeItem("钢玉石",1) #扣掉钢玉石
					Sender.TakeItem("淬炼石",1) #扣掉淬炼石
					Sender.TakeItem(item1,1)    #扣掉副首饰
					item.AddStat(StatList[select], 1, StatSource.Other)  #增加1点随机属性
					Sender.ItemCompleteRefresh(item.Index) #刷新道具属性显示
					say = """淬炼成功。
					
					[离开:0]"""
	elif Menu == 42:
		Dict['bg'] = bg
		Dict['needitems'] = needitems
		item['pos_x'] = 180								#需求物品框位置,相对于bg左上角来说
		item['pos_y'] = 45
		item['file']=3
		item['idx']=910
		needitems[0] = item
		say = """<font  size=9F  color=0xff00ff00  x=35  y=5 >只能放入高级以上首饰，分解随机获得0-2个淬炼石</font>
		<font  size=9F  color=0xff00ff00  x=70  y=25 >放首饰到格子内,不能放入小退下即可</font>
		
		
		
		
		
		               [分解首饰:421]（要求:50000金币）
		"""
	elif Menu == 421:
		Links = args[3]
		if Links is None or Links.Count == 0 or Links[0].Slot < 0 or Links[0].Slot > Globals.InventorySize:
			Sender.Connection.ReceiveChat("没有放置道具。", MessageType.System)
			return
		item = Sender.Inventory[Links[0].Slot]
		if item.Info.ItemType != ItemType.Necklace and item.Info.ItemType != ItemType.Bracelet and item.Info.ItemType != ItemType.Ring:
			Sender.Connection.ReceiveChat("不是首饰类，无法分解。", MessageType.System)
		elif item.Info.Rarity == Rarity.Common:
			Sender.Connection.ReceiveChat("普通首饰不能分解。", MessageType.System)
		elif (Sender.Gold < 50000):
			Sender.Connection.ReceiveChat("你的金币不足，不能分解。", MessageType.System)
		else:
			select = random.randint(1,100)
			if select < 25:
				SubGold(Sender,50000)
				Sender.TakeItem(item,1) #扣掉首饰
				Sender.GiveItem("淬炼石",2)
				Sender.Connection.ReceiveChat("分解成功，获得淬炼石2个。", MessageType.System)
			elif select < 65:
				SubGold(Sender,50000)
				Sender.TakeItem(item,1) #扣掉首饰
				Sender.GiveItem("淬炼石",1)
				Sender.Connection.ReceiveChat("分解成功，获得淬炼石1个。", MessageType.System)
			else:
				SubGold(Sender,50000)
				Sender.TakeItem(item,1) #扣掉首饰
				Sender.Connection.ReceiveChat("分解失败，没有获得淬炼石。", MessageType.System)
	elif Menu == 43:
		Dict['bg'] = bg
		Dict['needitems'] = needitems
		item['pos_x'] = 180								#需求物品框位置,相对于bg左上角来说
		item['pos_y'] = 45
		item['file']=3
		item['idx']=910
		needitems[0] = item
		say = """<font  size=9F  color=0xff00ff00  x=62  y=5 >只能放入淬炼过的首饰，重置恢复原属性</font>
		<font  size=9F  color=0xff00ff00  x=70  y=25 >放首饰到格子内,不能放入小退下即可</font>
		
		
		
		
		
		            [重置淬炼首饰:431]（要求:200000金币）
		"""
	elif Menu == 431:
		Links = args[3]
		if Links is None or Links.Count == 0 or Links[0].Slot < 0 or Links[0].Slot > Globals.InventorySize:
			Sender.Connection.ReceiveChat("没有放置物品，无法淬炼。", MessageType.System)
			return
		item = Sender.Inventory[Links[0].Slot]
		#判断主首饰格子的首饰是否淬炼过
		cuilianflag = False
		for stat in item.AddedStats:
			attrflag = False
			if stat.StatSource == StatSource.Other:
				cuilianflag = True
		if item.Info.ItemType != ItemType.Necklace and item.Info.ItemType != ItemType.Bracelet and item.Info.ItemType != ItemType.Ring:
			Sender.Connection.ReceiveChat("首饰格子内不是首饰，无法重置。", MessageType.System)
		elif not cuilianflag:
			Sender.Connection.ReceiveChat("首饰格子内首饰没有淬炼过，无法重置。", MessageType.System)
		else:
			if (Sender.Gold < 200000):
				Sender.Connection.ReceiveChat("你金币不足，无法熔炼。", MessageType.System)
			else:
				SubGold(Sender,200000)
				for i in range(item.AddedStats.Count -1, 0, -1):
					stat = item.AddedStats[i]
					if stat.StatSource == StatSource.Other:
						item.RemoveStat(stat.Stat, StatSource.Other)  #删除随机属性
						Sender.ItemCompleteRefresh(item.Index) #刷新道具属性显示
				say = """重置成功。
				
				[离开:0]"""
#主菜单
	else:
		say = """你好! 想做什么?
		
		[制炼武器:1]
		[制炼饰品:2]
		[制作钢玉石:3]
		[首饰淬炼:4]
		[关闭:0]
		"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def GetItemNameInput(params):
	Sender = params[0]
	# 用户输入 注意按照需要进行验证 比如不能是负数 不能含有字母等等
	userInput = params[1] if len(params) > 1 else None

	if not userInput or len(userInput) < 1:
		Sender.PyInputBox("输入进行制炼的饰品名", "Npc.边境城市.啊彬.GetItemNameInput", "Npc.边境城市.啊彬.GetCloseInterface")
	else:
		try:
			info = SEnvir.GetItemInfo(userInput)
			if info.ItemType in ALLOWED_ITEM_TYPES:
				# 用户输入 暂存到个人临时变量
				PlayerSetTempV(Sender,TK_SHOUSHIHECHENG,info.Index)
				NPCObject = ServerUtils.GetNPCObject(121)
				if NPCObject:
					NPCObject.NPCCall(Sender, 22, None, userInput)
			else:
				Sender.Connection.ReceiveChat("不是饰品道具，无法制炼",MessageType.System)
		except:
			Sender.Connection.ReceiveChat("不存在该道具，无法制炼",MessageType.System)
			
def GetCloseInterface(params):
	Sender = params[0]
	return

# 制炼首饰
def ZhiLianShouShi(player, menu, items):
	# 打乱一下首饰列表
	#random.shuffle(items)
	# 拿出目标首饰 剩下的就是材料
	target_item = items.pop(0)
	# 想要加的属性
	target_stats = {}
	reference_stat = None

	if menu == 221:
		# 破坏
		target_stats[Stat.MaxDC] = 1
		reference_stat = Stat.MaxDC
		# 道具本身有没有破坏属性？没有的话要加0的最小破坏 否则会显示出错
		if target_item.Info.Stats[Stat.MaxDC] <= 0:
			target_stats[Stat.MinDC] = 0
	elif menu == 222:
		# 魔法
		# 要加灵魂还是自然？
		if target_item.Info.Stats[Stat.MinMC] > 0 or target_item.Info.Stats[Stat.MaxMC] > 0:
			# 有自然属性 加自然
			target_stats[Stat.MaxMC] = 1
			reference_stat = Stat.MaxMC
		if target_item.Info.Stats[Stat.MinSC] > 0 or target_item.Info.Stats[Stat.MaxSC] > 0:
			# 有灵魂属性 加灵魂
			target_stats[Stat.MaxSC] = 1
			reference_stat = Stat.MaxSC
		# 白板
		if target_item.Info.Stats[Stat.MinMC] == 0 and target_item.Info.Stats[Stat.MaxMC] == 0 and target_item.Info.Stats[Stat.MinSC] == 0 and target_item.Info.Stats[Stat.MaxSC] == 0:
			target_stats[Stat.MinMC] = 0
			target_stats[Stat.MaxMC] = 1
			target_stats[Stat.MinSC] = 0
			target_stats[Stat.MaxSC] = 1
			reference_stat = Stat.MaxMC

	elif menu == 223:
		# 火
		target_stats[Stat.FireAttack] = 1
		reference_stat = Stat.FireAttack
	elif menu == 224:
		# 冰
		target_stats[Stat.IceAttack] = 1
		reference_stat = Stat.IceAttack
	elif menu == 225:
		# 雷
		target_stats[Stat.LightningAttack] = 1
		reference_stat = Stat.LightningAttack
	elif menu == 226:
		# 风
		target_stats[Stat.WindAttack] = 1
		reference_stat = Stat.WindAttack
	elif menu == 227:
		# 神圣
		target_stats[Stat.HolyAttack] = 1
		reference_stat = Stat.HolyAttack
	elif menu == 228:
		# 暗黑
		target_stats[Stat.DarkAttack] = 1
		reference_stat = Stat.DarkAttack
	elif menu == 229:
		# 幻影
		target_stats[Stat.PhantomAttack] = 1
		reference_stat = Stat.PhantomAttack
	else:
		return "选项无效"

	if not reference_stat:
		return "无法获取参考属性"

	# 判断材料是否符合要求
	# 对于选定的属性 所有材料都应该有这个属性
	# 而且数值都一样
	for stat_to_check in target_stats.keys():
		expected_amount = StatAmountHelper(target_item, stat_to_check)
		for item_to_check in items:
			if StatAmountHelper(item_to_check, stat_to_check) != expected_amount:
				return "饰品属性不一致，无法制炼，请整理下包裹"

	# 计算成功率
	# 获取目标道具的属性值
	current_amount = StatAmountHelper(target_item, reference_stat)
	target_item_rates = REFINE_SUCCESS_RATES[str(target_item.Info.Rarity)]
	if current_amount not in target_item_rates:
		return "道具 {} 已经+{}，无法继续制炼了".format(target_item.Info.ItemName, current_amount)

	success_rate = target_item_rates[current_amount]
	is_success = random.randint(0, 99) < success_rate
	
	# 扣除材料
	SubGold(player,100000)   #扣除金币10万
	player.TakeItem("钢玉石",1) #扣除钢玉石1个
	for item_to_take in items:
		player.TakeItem(item_to_take, 1)

	if is_success:
		# 开始制炼
		for stat_to_add, amount_to_add in target_stats.iteritems():
			# 属性来源新版首饰合成
			target_item.AddStat(stat_to_add, amount_to_add, StatSource.Combine, "新版首饰合成");
		# 刷新
		player.ItemCompleteRefresh(target_item.Index)
		return "成功了，祝贺你！"
	else:
		# 失败了 扣除首饰
		player.TakeItem(target_item, 1)
		return """我已经尽力了，请不要气馁，下次再试试运气。
		
		[了解饰品制炼方法:230]
		[重新进行制炼:2]
		"""


# 获取装备某项属性的值，忽略镶嵌的属性
def StatAmountHelper(item, stat):
	gem_sources = [StatSource.Gem1, StatSource.Gem2, StatSource.Gem3]
	amount = 0
	for full_stat in item.AddedStats:
		if full_stat.StatSource not in gem_sources and full_stat.Stat == stat:
			amount += full_stat.Amount
	return amount

NpcEvent.add_listener(121,"OnClick",OnClick)