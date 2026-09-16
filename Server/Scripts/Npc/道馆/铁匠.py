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
		say = """各种武器在这里保存得很好。
		你想要什么武器？
		
		[前一步:99]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """请把要修理的武器放上去。
		
		[前一步:99]
		[结束:0]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你想卖掉手里的武器？
		让我看看。
		
		[前一步:99]"""
#物品回购
	elif Menu == 5:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""

#宠物扩展背包升级功能
	elif (Menu == 4):
		say = """矿石提炼。

		[银矿提炼结晶:31] <font color=0xff00ff00>成功率：10%</font>	
		需要材料：<font color=0xff00ff00>银矿</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>金币</font> * <font color=0xff00ff00>10000</font>	

		[金矿提炼结晶:32] <font color=0xff00ff00>成功率：20%</font>	
		需要材料：<font color=0xff00ff00>金矿</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>金币</font> * <font color=0xff00ff00>20000</font>

		[黑铁矿提炼结晶:33] <font color=0xff00ff00>成功率：30%</font>	
		需要材料：<font color=0xff00ff00>黑铁矿</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>金币</font> * <font color=0xff00ff00>30000</font>

		[结晶提炼传送石:34] <font color=0xff00ff00>成功率：50%</font>	
		需要材料：<font color=0xff00ff00>结晶</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>金币</font> * <font color=0xff00ff00>100000</font>

		[魔晶石提炼破空石:35] <font color=0xff00ff00>成功率：50%</font>	
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>5</font>
		需要材料：<font color=0xff00ff00>铜矿</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>20</font>

		[钢玉石提炼破空石:36] <font color=0xff00ff00>成功率：50%</font>	
		需要材料：<font color=0xff00ff00>钢玉石</font> * <font color=0xff00ff00>5</font>
		需要材料：<font color=0xff00ff00>铁矿</font> * <font color=0xff00ff00>20</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>20</font>

		[返回:99]
		[离开:0]"""
	
	elif (Menu == 31):

		#判断需要的金币	
		if (Sender.Gold < 10000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("银矿") < 20):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("银矿",20)
			SubGold(Sender,10000)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 90:
				say ="""哦，非常抱歉！这堆材料品质太差了！
				
				[再次提炼:4]
				"""
			else:
				Sender.GiveItem("结晶",1)
				say = """恭喜你，提炼成功！
								
				[继续提炼:31]
				"""
	elif (Menu == 32):
		#判断需要的金币	
		if (Sender.Gold < 20000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("金矿") < 20):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("金矿",20)
			SubGold(Sender,20000)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 80:
				say ="""哦，非常抱歉！这堆材料品质太差了！
				
				[再次提炼:4]
				"""
			else:
				Sender.GiveItem("结晶",1)
				say = """恭喜你，提炼成功！
								
				[继续提炼:32]
				"""
	elif (Menu == 33):
		#判断需要的金币	
		if (Sender.Gold < 30000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("黑铁") < 20):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("黑铁",20)
			SubGold(Sender,30000)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 70:
				say ="""哦，非常抱歉！这堆材料品质太差了！
				
				[再次提炼:4]
				"""
			else:
				Sender.GiveItem("结晶",1)
				say = """恭喜你，提炼成功！
								
				[继续提炼:33]
				"""
	elif (Menu == 34):
		#判断需要的金币	
		if (Sender.Gold < 100000):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("结晶") < 10):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("结晶",10)
			SubGold(Sender,100000)
			select = random.randint(0,100)
			#设置获得书的几率
			if select < 50:
				say ="""哦，非常抱歉！这堆材料品质太差了！
				
				[再次提炼:4]
				"""
			else:
				Sender.GiveItem("传送石",1)
				say = """恭喜你，提炼成功！
								
				[继续提炼:34]
				"""
	elif (Menu == 35):
		#判断需要的金币	
		if (Sender.GameGold < 20):
			say= """世界上的事情没有免费的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("铜矿") < 20):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 5):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具			
			Sender.TakeItem("铜矿",20)
			Sender.TakeItem("魔晶石",5)
			SubGameGold(Sender,20)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！这堆材料品质太差了！
				
				[继续:4]
				"""
			else:
				Sender.GiveItem("破空石",1)
				say = """恭喜你，提炼成功！
								
				[继续:35]
				"""

	elif (Menu == 36):
		#判断需要的金币	
		if (Sender.GameGold < 20):
			say= """世界上的事情没有免费的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("铁矿") < 20):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("钢玉石") < 5):
			say ="""抱歉，原材料不够，无法提炼。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具			
			Sender.TakeItem("铁矿",20)
			Sender.TakeItem("钢玉石",5)
			SubGameGold(Sender,20)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！这堆材料品质太差了！
				
				[继续:4]
				"""
			else:
				Sender.GiveItem("破空石",1)
				say = """恭喜你，提炼成功！
								
				[继续:36]
				"""
#主菜单
	else:
		say = """这里是道馆寄存武器的地方，你需要什么武器吗？
		
		[购买:1]武器
		[出售:3]武器
		[修理:2]武器

		[变废为宝:4]

		<font color=0xffFF00FF>“破空石”可以破碎虚空，进入神秘空间</font>

		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的武器类			
types =[ItemType.Weapon]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goods = collections.OrderedDict(wuqidiangoodslist)

NpcEvent.add_listener(44,"OnClick",OnClick)