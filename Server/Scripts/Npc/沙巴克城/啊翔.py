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
		say = """请你离开。
		
		我不想和红名交易。
		
		[结束:0]"""
#武器精炼		
	elif (Menu == 1):
		if (Sender.Equipment[int(EquipmentSlot.Weapon)]):
			if((Sender.Equipment[int(EquipmentSlot.Weapon)].Flags & UserItemFlags.Refinable) == UserItemFlags.Refinable):
				say = """好消息,我看你的武器已经准备好了。
					精炼：破坏
					精炼：全系列魔法（自然，灵魂或两者都取决于武器）
					精炼：火元素，冰元素，电元素，风元素
					精炼：神圣元素，黑暗元素
					精炼：幻影元素
					
					[结束:0]"""
				Dict['DialogType']= NPCDialogType.Refine
			else:
				say= """你的武器等级没有升级。

				[前一步:99]"""
		else:
			say = """炼制武器需要手里拿着武器！！

			[结束:0]"""
#取回武器			
	elif(Menu == 2):
		Dict['DialogType']= NPCDialogType.RefineRetrieve
		say="""你在我这儿存放东西了？
		如果是很久以前的东西，你还是回去吧
		我记不住那么遥远以前的事情...
		
		[关闭:0]"""
#精炼说明		
	elif(Menu == 3):
		say = """你在精炼过程中寻求帮助？
		你的武器首先要达到精炼要求。
		你可以使用最多5个黑色铁矿石，纯度越高，成功率越高。
		
		你最多可以使用3个配饰，级别和质量越高成功率越高。
		持续时间越长，精炼时间越长，成功率越高。
		
		[前一步:99]"""
#武器元素
	elif(Menu == 4):
		say = """你想用什么元素来精炼武器？

		改为 [火:41] 元素
		改为 [冰:42] 元素
		改为 [雷:43] 元素
		改为 [风:44] 元素
		改为 [神圣:45] 元素
		改为 [暗黑:46] 元素
		改为 [幻影:47] 元素

		[结束:0]"""
#改为火元素
	elif(Menu == 41):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.FireAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Fire)
				say = """恭喜你，
				你的武器现在更改为火元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#改为冰元素
	elif(Menu == 42):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.IceAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Ice)
				say = """恭喜你，
				你的武器现在更改为冰元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#改为雷元素
	elif(Menu == 43):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.LightningAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Lightning)
				say = """恭喜你，
				你的武器现在更改为雷元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#改为风元素
	elif(Menu == 44):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.WindAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Wind)
				say = """恭喜你，
				你的武器现在更改为风元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#改为神圣元素
	elif(Menu == 45):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.HolyAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Holy)
				say = """恭喜你，
				你的武器现在更改为神圣元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#改为暗黑元素
	elif(Menu == 46):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.DarkAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Dark)
				say = """恭喜你，
				你的武器现在更改为暗黑元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#改为幻影元素
	elif(Menu == 47):
		if (HaseWeapon(Sender)):
			stat = GetWeaponElement(Sender)
			if( stat == Stat.PhantomAttack ):
				say="""无法更改武器的元素。。。。。。
				你的武器已经拥有这个元素。

				[结束:0]"""
			elif(stat ==Stat.None):
				say = """你持有的武器不包含任何元素属性。
				我帮不了。

				[结束:0]"""
			elif(Sender.Gold< 100000):
				say= """你没有足够的金币。
				当你拥有足够的金币时再来。

				[结束:0]"""
			else:
				SubGold(Sender,100000)
				Sender.ChangeElement(Element.Phantom)
				say = """恭喜你，
				你的武器现在更改为幻影元素。

				[结束:0]"""
		else:
			say = """你没有装备武器。
			请装备好武器再来。

			[结束:0]"""	
#精炼石说明		
	elif(Menu == 5):
		Dict['DialogType']= NPCDialogType.RefinementStone
		say = """如果你想做一块精致的石头，您将需要以下内容：
		1X水晶矿
		2X金矿
		4X金刚石
		4X银矿
		4X铁矿
		金币…无论你喜欢多少，越高越好！
		
		[前一步:99]
		[结束:0]"""
#重置武器		
	elif(Menu == 6):
		say = """你好，所以你想重置你的武器级别？
		此过程需要24小时，成功率为100％。有机会保持一些改进的统计数据。重置武器的成本是100万金币和1x 制炼石。
		
		[重置武器:61]
		
		[前一步:99]
		[结束:0]"""
	elif(Menu == 61):
#判断重置时需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[结束:0]"""
#判断重置时手上是否有武器			
		elif (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
			say ="""你没有装备武器。
			请装备好武器再来。

			[结束:0]"""
#判断是否达到重置武器等级要求			
		elif(Sender.Equipment[int(EquipmentSlot.Weapon)].Level<2):	
			say ="""不能重置你的武器。
			还没有达到重置武器等级要求。

			[结束:0]"""	
#判断是否有重置要求的道具			
		elif(Sender.GetItemCount("制炼石") < 1):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[结束:0]"""
#判断是否已经重置过，重置冷却时间			
		elif(Sender.Equipment[int(EquipmentSlot.Weapon)].ResetCoolDown > DateTime.Now):
			say="""你的武器最近被重置了。
			重置冷却完成后再来。

			[结束:0]"""
		else:
#上面条件都达成，扣除重置费用和道具，执行重置		
			SubGold(Sender,1000000)
			Sender.TakeItem("制炼石",1)
			Sender.NPCResetWeapon()
			say="""你的武器重置成功。
			请点击[取回:2]
			
			[结束:0]"""
#精炼过程			
	elif(Menu == 7):
#判断武器是否满级	
		if(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < 17):
			say= """你的武器还没有达到最高等级。
			当你的武器完全升级后请再回来。

			[结束:0]"""
		else:	
			Dict['DialogType']= NPCDialogType.MasterRefine	
			say = """你将需要以下内容：
		
			初级碎片x10
			中级碎片x10
			高级碎片x1~x1000
			精炼石x1

			该过程将添加或删除你选择的5属性类型。
			你不能打破你的武器。

			[前一步:99]
			[结束:0]"""
#特殊精炼		
	elif(Menu == 8):
		say = """特殊精炼要求：
		武器强化油x1
		战神油x1
		[高级碎片:81] x30+结晶x 30
		[高级碎片:82] X60+结晶X 50
		[高级碎片:83] x100+结晶x 50

		[前一步:99]
		[结束:0]"""
#30个高级碎片特殊精炼		
	elif(Menu == 81):
		say = """提供30个碎片可以：
		[体力:811] + 75（限制：+1250）
		[法力:812] +40（限制：+850）
		[准确:813] +3（限制：+30）
		[敏捷:814] +3（限制：+30）
		[防御:815] 0-5（限制：+50）
		[魔御:816] 0-5（限制：+50）

		[继续:8]
		[结束:0]"""
	elif(Menu == 811):
		say = """你确定要为武器添加体力吗？

		[是的，精炼:8111]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8111):
		say = Refine(Sender,'体力')
	elif(Menu == 812):
		say = """你确定要为武器添加法力吗？

		[是的，精炼:8121]
		[继续:8]
		[结束:0]"""	
	elif(Menu == 8121):
		say = Refine(Sender,'法力')		
	elif(Menu == 813):
		say = """你确定要为武器添加准确吗？

		[是的，精炼:8131]
		[继续:8]
		[结束:0]"""	
	elif(Menu == 8131):
		say = Refine(Sender,'准确')		
	elif(Menu == 814):
		say = """你确定要为武器添加敏捷吗？

		[是的，精炼:8141]
		[继续:8]
		[结束:0]"""	
	elif(Menu == 8141):
		say = Refine(Sender,'敏捷')		
	elif(Menu == 815):
		say = """你确定要为武器添加防御吗？

		[是的，精炼:8151]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8151):
		say = Refine(Sender,'防御')		
	elif(Menu == 816):
		say = """你确定要为武器添加魔御吗？

		[是的，精炼:8161]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8161):
		say = Refine(Sender,'魔御')	
#60个高级碎片特殊精炼		
	elif(Menu == 82):
		say = """提供60碎片可以：
		[暴击几率:821] +1（限制：+25）
		[暴击伤害(怪物):822] +5（限制：+200）
		[攻击速度:823] +3（限制：+15）
		[吸血恢复:824] +3（限制：+21）

		[继续:8]
		[结束:0]"""
	elif(Menu == 821):
		say = """你确定要为武器添加暴击几率吗？

		[是的，精炼:8211]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8211):
		say = Refine(Sender,'暴击几率')			
	elif(Menu == 822):
		say = """你确定要为武器添加暴击伤害(怪物)吗？

		[是的，精炼:8221]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8221):
		say = Refine(Sender,'暴击伤害(怪物)')			
	elif(Menu == 823):
		say = """你确定要为武器添加攻击速度吗？

		[是的，精炼:8231]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8231):
		say = Refine(Sender,'攻击速度')			
	elif(Menu == 824):
		say = """你确定要为武器添加吸血恢复吗？

		[是的，精炼:8241]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8241):
		say = Refine(Sender,'吸血恢复')
#100个高级碎片特殊精炼		
	elif(Menu ==83):
		say = """对于100个碎片，我可以提供：
		[麻痹几率:831]+1%（pvp和pve-2秒）（限制值:+13）
		[减速几率:832]+1%（pve）-10秒（限制:+15）
		[沉默几率:833]+1%（pvp和pve-5秒）（限制:+10）
		[格挡几率:834]+1%（近战）（限制值:+10）
		[闪避几率:835]+1%（魔法）（上限+10）

		[继续:8]
		[结束:0]"""
	elif(Menu == 831):
		say = """你确定要为武器添加麻痹几率吗？

		[是的，精炼:8311]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8311):
		say = Refine(Sender,'麻痹几率')
	elif(Menu == 832):
		say = """你确定要为武器添加减速几率吗？

		[是的，精炼:8321]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8321):
		say = Refine(Sender,'减速几率')	
	elif(Menu == 833):
		say = """你确定要为武器添加沉默吗？

		[是的，精炼:8331]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8331):
		say = Refine(Sender,'沉默几率')	
	elif(Menu == 834):
		say = """你确定要为武器添加格挡几率吗？

		[是的，精炼:8341]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8341):
		say = Refine(Sender,'格挡几率')
	elif(Menu == 835):
		say = """你确定要为武器添加闪避几率吗？

		[是的，精炼:8351]
		[继续:8]
		[结束:0]"""
	elif(Menu == 8351):
		say = Refine(Sender,'闪避几率')
#主菜单		
	else:		
		say = """虽然是沙巴克城，行会的人也是这样降价，
		我的自尊心不许。
		
		[制炼武器:1]
		[领取制炼好的武器:2]
		[打听制炼武器:3]
		
		[结束:0]
		
		"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict		

#判断是否有武器	
def HaseWeapon(Sender):
	if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
		return False
	else:
		return True

#判断武器是否有属性		
def GetWeaponElement(Sender):
	weap = Sender.Equipment[int(EquipmentSlot.Weapon)]
	element = Stat.None
	if(weap):
		element = weap.Stats.GetWeaponElement()
		if (element == Stat.None):
			element = weap.Info.Stats.GetWeaponElement();
	return element
#############################################################
###
###特殊精炼工艺要求判断
###
#############################################################	
def Refine(Sender,RefineName):
	list = RefineList[RefineName]
#判断手上是否有武器	
	if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
		return """你没有装备武器。
		请装备好武器再来。

		[结束:0]"""
#判断手上的武器是否已经MAX		
	elif(Sender.Equipment[int(EquipmentSlot.Weapon)].Level < list['Level']):
		return """你的武器还没有达到最高等级。
		当你的武器完全升级后请再回来。

		[结束:0]"""
#判断手上武器是否已经加到指定MaxStat最大值		
	elif(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[list['Stat']] >= list['MaxStat']):
		return """你的属性已经加到最大值，
		你不能再把这个属性添加到你的武器上。
		
		[结束:0]"""
#判断包裹内是否有足够的特殊精炼材料		
	elif(list['Item']):
		for (k,v) in list['Item'].items():
			if (Sender.GetItemCount(k)<v):
				return """你的材料不足。
		请准备好足够的材料在来。

		[结束:0]"""
#如果材料达到要求，那么扣除材料	
	if (list['Item']):
		for (k,v) in list['Item'].items():
			Sender.TakeItem(k,v)
#按列表里的Stat所对应增加的属性给予Refine所增加的值	
	Sender.NPCSpecialRefine(list['Stat'],list['Refine'])
	return """你的属性已经成功添加。
	
		[继续:8]
		[结束:0]"""
#############################################################
###
###特殊精炼工艺条件
###Level武器等级要求  Item需要的材料  MaxStat能增加的最大值   Refine每次增加的值  Stat所对应增加的属性
#############################################################		
RefineList={'体力':{'Level':17,'Item':{'结晶':30,'高级碎片':30,'武器强化油':1,'战神油':1},'MaxStat':1250,'Refine':75,'Stat':Stat.Health},
			'法力':{'Level':17,'Item':{'结晶':30,'高级碎片':30,'武器强化油':1,'战神油':1},'MaxStat':850,'Refine':40,'Stat':Stat.Mana},
			'准确':{'Level':17,'Item':{'结晶':30,'高级碎片':30,'武器强化油':1,'战神油':1},'MaxStat':30,'Refine':3,'Stat':Stat.Accuracy},
			'敏捷':{'Level':17,'Item':{'结晶':30,'高级碎片':30,'武器强化油':1,'战神油':1},'MaxStat':30,'Refine':3,'Stat':Stat.Agility},
			'防御':{'Level':17,'Item':{'结晶':30,'高级碎片':30,'武器强化油':1,'战神油':1},'MaxStat':50,'Refine':5,'Stat':Stat.MaxAC},
			'魔御':{'Level':17,'Item':{'结晶':30,'高级碎片':30,'武器强化油':1,'战神油':1},'MaxStat':50,'Refine':5,'Stat':Stat.MaxMR},
			'暴击几率':{'Level':17,'Item':{'结晶':50,'高级碎片':60,'武器强化油':1,'战神油':1},'MaxStat':25,'Refine':1,'Stat':Stat.CriticalChance},
			'暴击伤害(怪物)':{'Level':17,'Item':{'结晶':50,'高级碎片':60,'武器强化油':1,'战神油':1},'MaxStat':200,'Refine':5,'Stat':Stat.CriticalDamage},
			'攻击速度':{'Level':17,'Item':{'结晶':50,'高级碎片':60,'武器强化油':1,'战神油':1},'MaxStat':15,'Refine':3,'Stat':Stat.AttackSpeed},
			'吸血恢复':{'Level':17,'Item':{'结晶':50,'高级碎片':60,'武器强化油':1,'战神油':1},'MaxStat':21,'Refine':3,'Stat':Stat.LifeSteal},
			'麻痹几率':{'Level':17,'Item':{'结晶':50,'高级碎片':100,'武器强化油':1,'战神油':1},'MaxStat':13,'Refine':1,'Stat':Stat.ParalysisChance},
			'减速几率':{'Level':17,'Item':{'结晶':50,'高级碎片':100,'武器强化油':1,'战神油':1},'MaxStat':15,'Refine':1,'Stat':Stat.SlowChance},
			'沉默几率':{'Level':17,'Item':{'结晶':50,'高级碎片':100,'武器强化油':1,'战神油':1},'MaxStat':10,'Refine':1,'Stat':Stat.SilenceChance},
			'格挡几率':{'Level':17,'Item':{'结晶':50,'高级碎片':100,'武器强化油':1,'战神油':1},'MaxStat':10,'Refine':1,'Stat':Stat.BlockChance},
			'闪避几率':{'Level':17,'Item':{'结晶':50,'高级碎片':100,'武器强化油':1,'战神油':1},'MaxStat':10,'Refine':1,'Stat':Stat.EvasionChance},}
			
			
#NpcEvent.add_listener(95,"OnClick",OnClick)			
			