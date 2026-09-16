# -*- coding: utf-8 -*-
#载入模块SYS
import sys
from Globals import *
#引用模块的地址
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
#跳转菜单1管理宠物	
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.CompanionManage  #类型为Library.Enums里的宠物管理类
		say = """请慢慢挑选。。。
		
		[返回:99]
		
		[关闭:0]"""
#跳转菜单2买卖				
	elif (Menu == 2):
    		Dict['Goods'] =goods                #定义可购买商品	
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell   #类型为Library.Enums里的买卖类
		say = """这里出售宠物需要的商品。
		
		[返回:99]
		
		[关闭:0]"""			
#宠物扩展背包升级功能
	elif (Menu == 3):
		say = """宠物装备升级功能。

		[宠物背带:31] <font color=0xff00ff00>成功率：80%</font>	
		需要材料：<font color=0xff00ff00>宠物小背带</font> * <font color=0xff00ff00>2个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>20</font>
		需要材料：<font color=0xff00ff00>宠物道具碎片</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>500</font>	

		[宠物小马甲:32] <font color=0xff00ff00>成功率：60%</font>	
		需要材料：<font color=0xff00ff00>宠物背带</font> * <font color=0xff00ff00>2个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>宠物道具碎片</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>1000</font>

		[宠物头带:33] <font color=0xff00ff00>成功率：80%</font>	
		需要材料：<font color=0xff00ff00>宠物小头带</font> * <font color=0xff00ff00>2个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>20</font>
		需要材料：<font color=0xff00ff00>宠物道具碎片</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>500</font>

		[宠物红帽:34] <font color=0xff00ff00>成功率：60%</font>	
		需要材料：<font color=0xff00ff00>宠物头带</font> * <font color=0xff00ff00>2个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>宠物道具碎片</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>1000</font>

		[宠物背包袖里乾坤:35] <font color=0xff00ff00>成功率：70%</font>	
		需要材料：<font color=0xff00ff00>华丽的皮包</font> * <font color=0xff00ff00>5个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>宠物道具碎片</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>1000</font>

		[返回:99]
		[离开:0]"""
	
	elif (Menu == 31):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		宠物背带：宠物小背带*2；炼制结晶*20；宠物道具碎片*20；几率80%！
        
		
		[请帮忙升级:311]
		[返回:99]
		"""
	elif (Menu == 311):
		#判断需要的元宝	
		if (Sender.GameGold < 500):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("宠物小背带") < 2):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 20):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("宠物道具碎片") < 20):
			say ="""抱歉，无法为你升级，你带够了“宠物道具碎片”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",20)
			Sender.TakeItem("宠物道具碎片",20)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 30:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,500)
				Sender.GiveItem("宠物背带",1)
				Sender.TakeItem("宠物小背带",2)
				say = """恭喜你，升级成功。宠物更加强大了！
								
				[结束:0]
				"""
	elif (Menu == 32):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		宠物小马甲：宠物背带*2；炼制结晶*50；宠物道具碎片*50；元宝1000；几率60%！
        
		
		[请帮忙升级:321]
		[结束:0]
		"""
	elif (Menu == 321):
		#判断需要的金币	
		if (Sender.GameGold < 1000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("宠物背带") < 2):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("宠物道具碎片") < 50):
			say ="""抱歉，无法为你升级，你带够了“宠物道具碎片”吗。

			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("宠物道具碎片",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,1000)
				Sender.GiveItem("宠物小马甲",1)
				Sender.TakeItem("宠物背带",2)
				say = """恭喜你，升级成功。宠物更加强大了！
								
				[结束:0]
				"""
	elif (Menu == 33):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		宠物头带：宠物小头带*1；炼制结晶*20；宠物道具碎片*20；几率80%！
        
		
		[请帮忙升级:331]
		[结束:0]
		"""
	elif (Menu == 331):
		#判断需要的金币	
		if (Sender.GameGold < 500):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("宠物小头带") < 2):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 20):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("宠物道具碎片") < 20):
			say ="""抱歉，无法为你升级，你带够了“宠物道具碎片”吗。

			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",20)
			Sender.TakeItem("宠物道具碎片",20)
			select = random.randint(0,10)
			#设置获得书的几率
			if select < 3:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,500)
				Sender.GiveItem("宠物头带",1)
				Sender.TakeItem("宠物小头带",2)
				say = """恭喜你，升级成功。宠物更加强大了！
								
				[结束:0]
				"""
	elif (Menu == 34):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		宠物小红帽：宠物头带*2；炼制结晶*50；宠物道具碎片*50；几率60%！
        
		
		[请帮忙升级:341]
		[结束:0]
		"""
	elif (Menu == 341):
		#判断需要的金币	
		if (Sender.GameGold < 1000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("宠物头带") < 2):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("宠物道具碎片") < 50):
			say ="""抱歉，无法为你升级，你带够了“宠物道具碎片”吗。

			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("宠物道具碎片",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,1000)
				Sender.GiveItem("宠物小红帽",1)
				Sender.TakeItem("宠物头带",2)
				say = """恭喜你，升级成功。宠物更加强大了！
								
				[结束:0]
				"""
	elif (Menu == 35):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		袖里乾坤：华丽的皮包*5；炼制结晶*50；宠物道具碎片*50；元宝1000；几率70%！
        
		
		[请帮忙升级:351]
		[结束:0]
		"""
	elif (Menu == 351):
		#判断需要的金币	
		if (Sender.GameGold < 1000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("华丽的皮包") < 5):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("宠物道具碎片") < 50):
			say ="""抱歉，无法为你升级，你带够了“宠物道具碎片”吗。

			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具			
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("宠物道具碎片",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 4:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,1000)
				Sender.GiveItem("袖里乾坤",1)
				Sender.TakeItem("华丽的皮包",5)
				say = """恭喜你，升级成功。宠物更加强大了！
								
				[结束:0]
				"""


#主菜单
	else:
		say = """想收养一个可爱的宠物吗？
		它会在你打猎时帮你拾取物品。
		并且我这里也出售各种宠物粮食和道具。

		<font color=0xffFF00FF>注意：购买宠物请注意选择与自己职业相匹配的！！</font>

		<font color=0xffFF00FF>注意：I级宠物不具备捡物设置功能！！</font>

		[购买宠物:1] 宠物清单

		[购买:2] 宠物物品

		[打听宠物装备升级的方法:3]
		
		[关闭:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的宠物类			
types =[ItemType.CompanionFood,ItemType.CompanionBack,ItemType.CompanionBag,ItemType.CompanionHead]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goodslist=[
	('苹果',float(1)),
	('粽子',float(1)),
	('肉包子',float(1)),
	('意识药水（3级）（绑定）',float(1)),
	('意识药水（5级）（绑定）',float(1)),
	('意识药水（7级）（绑定）',float(1)),
	('意识药水（10级）（绑定）',float(1)),
	('意识药水（11级）（绑定）',float(1)),
	('意识药水（13级）（绑定）',float(1)),
	('意识药水（15级）（绑定）',float(1)),]
goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(52,"OnClick",OnClick)
NpcEvent.add_listener(313,"OnClick",OnClick)
NpcEvent.add_listener(369,"OnClick",OnClick)
NpcEvent.add_listener(368,"OnClick",OnClick)




