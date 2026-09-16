# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
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
#武器工艺	
	if(Menu == 1):
		Dict['DialogType']= NPCDialogType.WeaponCraft	
		say = """。。。

		每个宝石都会为武器添加一个属性。
		更高质量的宝石将会获得更多的属性。
		虽然我是学徒，无法给你打造更高属性的武器
		我花费的材料和精力是一样的，所以，费用如下：

		<font color=\"0xff00ff00\">普通武器：3000万一次</font>  

		<font color=\"0xff00ff00\">高级武器：6000万一次</font> 

		<font color=\"0xff00ff00\">稀世武器：8000万一次</font> 

		
		[返回:99]

		[离开:0]"""
#升级小饰品		
	elif(Menu == 2):
		say = """升级需要材料x100和50000金币

		[黄色的球到黄色的饰品:20] -- 
		[蓝色的球到蓝色的饰品:30] -- 
		[红色的球到红色的饰品:40] -- 
		[紫色的球到紫色的饰品:50] -- 
		[绿色的球到绿色的饰品:60] -- 
		[灰色的球到灰色的饰品:70] -- 

		[返回:99]
		[离开:0]"""
#黄色		
	elif(Menu == 20):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("黄色的球") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("黄色的饰品",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("黄色的球",100)			
				say="""你的物品制作成功。
			
				[继续:20]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""	
	elif(Menu == 21):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("黄色的饰品") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("黄色立方体",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("黄色的饰品",100)
				say="""你的物品制作成功。
			
				[继续:21]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#蓝色		
	elif(Menu == 30):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("蓝色的球") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("蓝色的饰品",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("蓝色的球",100)
				say="""你的物品制作成功。
				
				[继续:30]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 31):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("蓝色的饰品") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("蓝色立方体",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("蓝色的饰品",100)
				say="""你的物品制作成功。
				
				[继续:31]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#红色		
	elif(Menu == 40):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("红色的球") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("红色的饰品",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("红色的球",100)
				say="""你的物品制作成功。
				
				[继续:40]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 41):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("红色的饰品") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("红色立方体",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("红色的饰品",100)
				say="""你的物品制作成功。
				
				[继续:41]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#紫色		
	elif(Menu == 50):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("紫色的球") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("紫色的饰品",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("紫色的球",100)
				say="""你的物品制作成功。
				
				[继续:50]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 51):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("紫色的饰品") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("紫色立方体",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("紫色的饰品",100)
				say="""你的物品制作成功。
				
				[继续:51]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#绿色		
	elif(Menu == 60):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("绿色的球") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("绿色的饰品",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("绿色的球",100)
				say="""你的物品制作成功。
				
				[继续:60]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 61):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("绿色的饰品") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("绿色立方体",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("绿色的饰品",100)
				say="""你的物品制作成功。
				
				[继续:61]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#灰色		
	elif(Menu == 70):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("灰色的球") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("灰色的饰品",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("灰色的球",100)
				say="""你的物品制作成功。
				
				[继续:70]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 71):
#判断需要的金币	
		if (Sender.Gold < 50000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("灰色的饰品") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("灰色立方体",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("灰色的饰品",100)
				say="""你的物品制作成功。
				
				[继续:71]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""	
#批量升级小饰品		
	elif(Menu == 3):
		say = """升级需要材料x10000和5000000金币

		[黄色的球到黄色的饰品:200] -- [黄色的饰品到黄色立方体:210]
		[蓝色的球到蓝色的饰品:300] -- [蓝色的饰品到蓝色立方体:310]
		[红色的球到红色的饰品:400] -- [红色的饰品到红色立方体:410]
		[紫色的球到紫色的饰品:500] -- [紫色的饰品到紫色立方体:510]
		[绿色的球到绿色的饰品:600] -- [绿色的饰品到绿色立方体:610]
		[灰色的球到灰色的饰品:700] -- [灰色的饰品到灰色立方体:710]

		[返回:99]
		[离开:0]"""
#黄色		
	elif(Menu == 200):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("黄色的球") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("黄色的饰品",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("黄色的球",10000)			
				say="""你的物品制作成功。
			
				[继续:200]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""	
	elif(Menu == 210):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("黄色的饰品") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("黄色立方体",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("黄色的饰品",10000)
				say="""你的物品制作成功。
			
				[继续:210]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#蓝色		
	elif(Menu == 300):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("蓝色的球") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("蓝色的饰品",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("蓝色的球",10000)
				say="""你的物品制作成功。
				
				[继续:300]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 310):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("蓝色的饰品") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("蓝色立方体",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("蓝色的饰品",10000)
				say="""你的物品制作成功。
				
				[继续:310]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#红色		
	elif(Menu == 400):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("红色的球") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("红色的饰品",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("红色的球",10000)
				say="""你的物品制作成功。
				
				[继续:400]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 410):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("红色的饰品") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("红色立方体",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("红色的饰品",10000)
				say="""你的物品制作成功。
				
				[继续:410]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#紫色		
	elif(Menu == 500):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("紫色的球") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("紫色的饰品",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("紫色的球",10000)
				say="""你的物品制作成功。
				
				[继续:500]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 510):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("紫色的饰品") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("紫色立方体",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("紫色的饰品",10000)
				say="""你的物品制作成功。
				
				[继续:510]			
				[离开:0]"""	
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#绿色		
	elif(Menu == 600):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("绿色的球") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("绿色的饰品",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("绿色的球",10000)
				say="""你的物品制作成功。
				
				[继续:600]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 610):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("绿色的饰品") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("绿色立方体",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("绿色的饰品",10000)
				say="""你的物品制作成功。
				
				[继续:610]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
#灰色		
	elif(Menu == 700):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("灰色的球") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("灰色的饰品",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("灰色的球",10000)
				say="""你的物品制作成功。
				
				[继续:700]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""				
	elif(Menu == 710):
#判断需要的金币	
		if (Sender.Gold < 5000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("灰色的饰品") < 10000):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("灰色立方体",100)):
				SubGold(Sender,5000000)
				Sender.TakeItem("灰色的饰品",10000)
				say="""你的物品制作成功。
				
				[继续:710]			
				[离开:0]"""
			else:
				say = """你的背包没有空间，无法合成。
				
				[离开:0]"""					
#主菜单		
	else:		
		say = """我刚学习这个武器工艺技能，手法不熟练
			可以找一些球球，我给您练练


		[学徒手艺:1]   武器不会破碎。

		[球球合成小饰品:2]

		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(380,"OnClick",OnClick)	