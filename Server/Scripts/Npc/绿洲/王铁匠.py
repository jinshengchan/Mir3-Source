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
from Npc.商店列表 import *
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
		
		[结束:0]"""	
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """明明有能力使用攻击力强的武器，却非要使用攻击力弱的武
		器，证明你没有竭尽全力，我们村子不欢迎那种人。那么，
		你想买什么？
		
		[前一步:99]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """在我们这里，武器常修不常换是一种美德。我们村子里的武
		器都是我修的，你也让我修吧。
		
		[前一步:99]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """我把你卖的武器修理好，弄干净，然后给其他人用。你带来
		了什么东西，拿出来给我看看。
		
		[前一步:99]"""
	elif (Menu == 4):
		item = Sender.Equipment[int(EquipmentSlot.Weapon)] #道具=身上装备的道具
		#判断手上是否有武器	
		if (not item):
			say = """你没有装备武器，无法特修。
			
			[结束:0]"""
		elif (not item.Info.CanRepair):
			say = """当前武器不能修理。
			
			[返回:4]"""
		else:
			cost = item.RepairCost(True)
			coststr = str(cost)
			say = """修理费用是"""+ coststr +"""。
			
			这个特修是只有带着物品的情况下才可以特修。请确认一下
			是否带着。
			
			[现在修理:41]
			[前一步:99]"""
#特修武器
	elif (Menu == 41):
		if (Sender.Equipment[int(EquipmentSlot.Weapon)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Weapon)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					SubGold(Sender,cost) #扣除修理的费用
					item.CurrentDurability = item.MaxDurability #执行特修
					Sender.ReflushDurability(GridType.Equipment, int(EquipmentSlot.Weapon), 0) #刷新持久显示
					Sender.RefreshStats()
					say = """修理的很好。
					修理费用是"""+ coststr +"""。
					
					[结束:0]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备武器。
			
			[返回:4]"""
	elif (Menu == 6):
		if((Sender.GetItemCount("书信") > 0) and (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==1)):
			Sender.TakeItem("书信",1)
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,2)
			say = """嗯，是黄河大侠派来的。让你来辛苦了。那么快点回去吧！
			
			[这是什么话？:61]"""
		else:
			say = """没有书信？嗯，那就有些困难。虽然辛苦，请重新拿书信来！
			
			[结束:0]"""
	elif (Menu == 61):
		say = """这是你接受的全部测试。黄河大侠 每年将 几名战士 送到我这里 ，我看到书信后，将你们重新送回去即可。
		
		[还是无法接受哦。:62]"""
	elif (Menu == 62):
		say = """哦，好像发了好大的火。但是请别误解，黄河大侠不会拿你开玩笑的。原来学习武功的方法有数十数百种。让你做这种事情都是有缘由的，不要随意轻举妄动。
		
		[知道了。:63]"""
	elif (Menu == 63):
		say = """那件事就那样了，我想委托你一个<font color=\"0xff00ff00\">个人的委托</font>好吗？
		
		[什么委托？:64]"""
	elif (Menu == 64):
		say = """最近年轻时候受的伤又发作了，即疼痛又很痒，都无法睡觉。
		听说生活在沙漠中的诺玛族拥有一种有着神奇力量称为<font color=\"0xff00ff00\">诺玛石</font>
		的石头，将这个石头捣碎，然后用水冲服可以治疗痼疾。你能帮我找到这个东西吗？
		
		[不用担心！:65]"""
	elif (Menu == 65):
		say = """非常谢谢！‘诺玛石’被装饰于诺玛族长老<font color=\"0xff00ff00\">诺玛法老的手杖</font>上。
		
		[下一步:66]"""
	elif (Menu == 66):
		say = """非常急迫地想掌握新武功吧，别担心！即使那样，我怎么报复？向黄河大侠挑起事端吗？请放心地去吧！我绝对不是一个小气的家伙。
		
		[我将给你找来。:67]"""
	elif (Menu == 67):
		PlayerSetV(Sender,GV_Warrior_ShoulderDash,3)
		PlayerSetV(Sender,BV_NQ_SKILL,10001)
		PlayerSetV(Sender,BV_NQ_SKILLMON,1)
		say = """真的吗？哦，绝对不是故意如此的。‘诺玛石’被装饰于诺玛
		法老的手杖上，而且请找到该<font color=\"0xff00ff00\">诺玛石 5个</font>。
		
		[结束:0]"""
	elif (Menu == 7):
		if (Sender.GetItemCount("诺玛石") > 4):
			say = """非常谢谢！你是一名不忽视别人困难，热心肠的人。希望你以后依然可以不断地帮助有困难的人。
			这个是对你善意的小小答谢。请将书信转交给<font color=\"0xff00ff00\">黄河大侠</font>。
			
			[好的，我将转交。:71]"""
		else:
			say = """我将在此等候你回来。
			
			[结束:0]"""
	elif (Menu == 71):
		if (Sender.GetItemCount("诺玛石") > 4):
			if (Sender.Gender == MirGender.Male):
				if (GetInventoryCount(Sender) >= 2): #包裹格子大于2
					Sender.GiveItem("诺玛重盔甲（男）",1)
					Sender.GiveItem("书信",1)
					Sender.TakeItem("诺玛石",5)
					PlayerSetV(Sender,GV_Warrior_ShoulderDash,4)
					say = """就到这里，请上路吧！要走的路还很远哟。
					
					[结束:0]"""
				else:
					say = """你的背囊装满了。。请整理些位置再来！
					
					[结束:0]"""
			elif (Sender.Gender == MirGender.Female):
				if (GetInventoryCount(Sender) >= 2): #包裹格子大于2
					Sender.GiveItem("诺玛重盔甲（女）",1)
					Sender.GiveItem("书信",1)
					Sender.TakeItem("诺玛石",5)
					PlayerSetV(Sender,GV_Warrior_ShoulderDash,4)
					say = """就到这里，请上路吧！要走的路还很远哟。
					
					[结束:0]"""
				else:
					say = """你的背囊装满了。。请整理些位置再来！
					
					[结束:0]"""
		else:
			say = """我将在此等候你回来。
			
			[结束:0]"""

#主菜单
	else:
		if (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==1):
			say = """黄河大侠让来的？快点拿来书信。
			
			[给你书信。:6]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==2):
			say = """嗯，是黄河大侠派来的。让你来辛苦了。那么快点回去吧！
			
			[这是什么话？:61]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==3):
			if (Sender.GetItemCount("诺玛石") > 4):
				say = """哦，找到‘诺玛石’了。谢谢！今天晚上开始可以好好地睡觉了。
				
				[下一步:7]"""
			else:
				say = """我将在此等候你回来。
				
				[结束:0]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==4):
			if (Sender.GetItemCount("书信") < 1):
				if (Sender.GiveItem("书信",1)):
					say = """书信丢了？让人寒心！重新再给你一本，这次注意拿好。
					
					[结束:0]"""
				else:
					say = """你的背囊装满了。。请整理些位置再来！
					
					[结束:0]"""
			else:
				say = """边境是很远的路。请快赶去！
				
				[结束:0]"""
		else:
			say = """欢迎光临，异乡人。你需要什么？
			
			[购买:1]武器
			[出售:3]武器
			[修理:2]武器
			[特殊修理:4]武器
			
			[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#类型为 Enums里的武器类
types =[ItemType.Weapon]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goods = collections.OrderedDict(wuqidiangoodslist)

NpcEvent.add_listener(315,"OnClick",OnClick)

