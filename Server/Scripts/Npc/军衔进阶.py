# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import collections
import NpcEvent
import Server
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
		say="""以下是军衔升级条件
		
		五阶民兵： 黑龙奇石一个（江湖任务中可获得）贡献值50点
		四阶民兵： 五阶民兵一个   贡献值100点
		三阶民兵： 四阶民兵一个   贡献值150点
		二阶民兵： 三阶民兵一个   贡献值200点
		一阶民兵： 二阶民兵一个   贡献值250点
		
		五阶军士： 一阶民兵一个   贡献值400点
		四阶军士： 五阶军士一个   贡献值500点
		三阶军士： 四阶军士一个   贡献值600点
		二阶军士： 三阶军士一个   贡献值700点
		一阶军士： 二阶军士一个   贡献值800点
		
		五阶副将： 一阶军士一个   贡献值1000点
		四阶副将： 五阶副将一个   贡献值1500点
		三阶副将： 四阶副将一个   贡献值2000点
		二阶副将： 三阶副将一个   贡献值2500点
		一阶副将： 二阶副将一个   贡献值3000点
		
		百人将：   一阶副将一个   贡献值5000点
		牙门将：   百人将一个     贡献值6000点
		都尉：     牙门将一个     贡献值8000点
		
		羽林中郎将： 都尉一个     贡献值10000点
		虎贲中郎将： 羽林中郎将一个   贡献值12000点
		偏将军：    虎贲中郎将一个   贡献值15000点
		
		四征将军：  偏将军一个     贡献值18000点
		骠骑将军：  四征将军一个   贡献值24000点
		大将军：    骠骑将军一个   贡献值30000点
		
		[关闭:0]"""
	elif(Menu == 2):
		say="""你想升级什么军衔
		
		[五阶民兵:201]        [四阶民兵:202]        [三阶民兵:203]
		[二阶民兵:204]        [一阶民兵:205]
		
		[五阶军士:211]        [四阶军士:212]        [三阶军士:213]
		[二阶军士:214]        [一阶军士:215]
		
		[五阶副将:221]        [四阶副将:222]        [三阶副将:223]
		[二阶副将:224]        [一阶副将:225]
		
		[百人将:231]          [牙门将:232]          [都尉:233]
		
		[羽林中郎将:241]      [虎贲中郎将:242]      [偏将军:243]
		
		[四征将军:251]        [骠骑将军:252]        [大将军:253]
		
		[关闭:0]"""
	elif(Menu == 201):
		if (Sender.Contribute < 50):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("黑龙奇石") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("五阶民兵[军衔]",1)):
				SubContribute(Sender,50)
				Sender.TakeItem("黑龙奇石",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 202):
		if (Sender.Contribute < 100):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("五阶民兵[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("四阶民兵[军衔]",1)):
				SubContribute(Sender,100)
				Sender.TakeItem("五阶民兵[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 203):
		if (Sender.Contribute < 150):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("四阶民兵[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("三阶民兵[军衔]",1)):
				SubContribute(Sender,150)
				Sender.TakeItem("四阶民兵[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 204):
		if (Sender.Contribute < 200):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("三阶民兵[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("二阶民兵[军衔]",1)):
				SubContribute(Sender,200)
				Sender.TakeItem("三阶民兵[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 205):
		if (Sender.Contribute < 250):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("二阶民兵[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("一阶民兵[军衔]",1)):
				SubContribute(Sender,250)
				Sender.TakeItem("二阶民兵[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 211):
		if (Sender.Contribute < 400):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("一阶民兵[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("五阶军士[军衔]",1)):
				SubContribute(Sender,400)
				Sender.TakeItem("一阶民兵[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 212):
		if (Sender.Contribute < 500):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("五阶军士[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("四阶军士[军衔]",1)):
				SubContribute(Sender,500)
				Sender.TakeItem("五阶军士[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 213):
		if (Sender.Contribute < 600):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("四阶军士[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("三阶军士[军衔]",1)):
				SubContribute(Sender,600)
				Sender.TakeItem("四阶军士[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 214):
		if (Sender.Contribute < 700):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("三阶军士[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("二阶军士[军衔]",1)):
				SubContribute(Sender,700)
				Sender.TakeItem("三阶军士[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 215):
		if (Sender.Contribute < 800):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("二阶军士[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("一阶军士[军衔]",1)):
				SubContribute(Sender,800)
				Sender.TakeItem("二阶军士[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 221):
		if (Sender.Contribute < 1000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("一阶军士[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("五阶副将[军衔]",1)):
				SubContribute(Sender,1000)
				Sender.TakeItem("一阶军士[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 222):
		if (Sender.Contribute < 1500):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("五阶副将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("四阶副将[军衔]",1)):
				SubContribute(Sender,1500)
				Sender.TakeItem("五阶副将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 223):
		if (Sender.Contribute < 2000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("四阶副将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("三阶副将[军衔]",1)):
				SubContribute(Sender,2000)
				Sender.TakeItem("四阶副将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 224):
		if (Sender.Contribute < 2500):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("三阶副将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("二阶副将[军衔]",1)):
				SubContribute(Sender,2500)
				Sender.TakeItem("三阶副将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 225):
		if (Sender.Contribute < 3000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("二阶副将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("一阶副将[军衔]",1)):
				SubContribute(Sender,3000)
				Sender.TakeItem("二阶副将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 231):
		if (Sender.Contribute < 5000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("一阶副将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("百人将[军衔]",1)):
				SubContribute(Sender,5000)
				Sender.TakeItem("一阶副将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 232):
		if (Sender.Contribute < 6000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("百人将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("牙门将[军衔]",1)):
				SubContribute(Sender,6000)
				Sender.TakeItem("百人将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 233):
		if (Sender.Contribute < 8000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("牙门将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("都尉[军衔]",1)):
				SubContribute(Sender,8000)
				Sender.TakeItem("牙门将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 241):
		if (Sender.Contribute < 10000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("都尉[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("羽林中郎将[军衔]",1)):
				SubContribute(Sender,10000)
				Sender.TakeItem("都尉[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 242):
		if (Sender.Contribute < 12000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("羽林中郎将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("虎贲中郎将[军衔]",1)):
				SubContribute(Sender,12000)
				Sender.TakeItem("羽林中郎将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 243):
		if (Sender.Contribute < 15000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("虎贲中郎将[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("偏将军[军衔]",1)):
				SubContribute(Sender,15000)
				Sender.TakeItem("虎贲中郎将[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 251):
		if (Sender.Contribute < 18000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("偏将军[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("四征将军[军衔]",1)):
				SubContribute(Sender,18000)
				Sender.TakeItem("偏将军[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 252):
		if (Sender.Contribute < 24000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("四征将军[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("骠骑将军[军衔]",1)):
				SubContribute(Sender,24000)
				Sender.TakeItem("四征将军[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
	elif(Menu == 253):
		if (Sender.Contribute < 30000):
			say= """你的贡献值不足，无法兑换

			[关闭:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("骠骑将军[军衔]") < 1):
			say ="""你的材料不足，无法兑换

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			if (Sender.GiveItem("大将军[军衔]",1)):
				SubContribute(Sender,30000)
				Sender.TakeItem("骠骑将军[军衔]",1)
				say="""兑换成功。
				
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，无法兑换。
				
				[关闭:0]"""
#主菜单		
	else:		
		say = """欢迎光临，有什么需要吗？

		[查看:1]  进阶条件
		[升级:2]  军阶进级

		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(213,"OnClick",OnClick)