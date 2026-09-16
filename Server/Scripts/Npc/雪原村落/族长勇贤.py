# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import clr

clr.AddReference("Library")
from Library import *
import collections
import NpcEvent

from Utils.PlayerUtils import *


######################################################
# 本函数为程序调用的固定格式 函数名和参数数量不要修改
# OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict = {}

	if  (Menu == 1):
		say = """我在这寒冷的世界里研究出了一套印记的升级方法。

		[强化破坏印记:31] <font color=0xff00ff00>成功率：60%</font>	
		需要材料：<font color=0xff00ff00>破坏印记（限时）</font> * <font color=0xff00ff00>10个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>100</font>	

		[强化自然印记:32] <font color=0xff00ff00>成功率：60%</font>	
		需要材料：<font color=0xff00ff00>自然印记（限时）</font> * <font color=0xff00ff00>10个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>100</font>	

		[强化灵魂印记:33] <font color=0xff00ff00>成功率：60%</font>	
		需要材料：<font color=0xff00ff00>灵魂印记（限时）</font> * <font color=0xff00ff00>10个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>100</font>	

		[强化神圣印记:34] <font color=0xff00ff00>成功率：50%</font>	
		需要材料：<font color=0xff00ff00>神圣印记（限时）</font> * <font color=0xff00ff00>10个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>200</font>	

		[强化暗黑印记:35] <font color=0xff00ff00>成功率：50%</font>	
		需要材料：<font color=0xff00ff00>暗黑印记（限时）</font> * <font color=0xff00ff00>10个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>200</font>	

		[强化幻影印记:36] <font color=0xff00ff00>成功率：50%</font>	
		需要材料：<font color=0xff00ff00>幻影印记（限时）</font> * <font color=0xff00ff00>10个</font>
		需要材料：<font color=0xff00ff00>炼制结晶</font> * <font color=0xff00ff00>50</font>
		需要材料：<font color=0xff00ff00>魔晶石</font> * <font color=0xff00ff00>50</font>
		需要手续费：<font color=0xff00ff00>元宝</font> * <font color=0xff00ff00>1000</font>	

		[返回:99]
		[离开:0]"""
	
	elif (Menu == 31):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		强化破坏印记：破坏印记（限时）*10；炼制结晶*50；魔晶石*50；元宝100，几率60%！
        
		
		[请帮忙升级:311]
		[返回:99]
		"""
	elif (Menu == 311):
		#判断需要的元宝	
		if (Sender.GameGold < 100):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("破坏印记（限时）") < 10):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 50):
			say ="""抱歉，无法为你升级，你带够了“魔晶石”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("魔晶石",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,100)
				Sender.GiveItem("强化破坏印记",1)
				Sender.TakeItem("破坏印记（限时）",10)
				say = """恭喜你，升级成功。你的能力增强了！
								
				[结束:0]
				"""
	elif (Menu == 32):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		强化自然印记：自然印记（限时）*10；炼制结晶*50；魔晶石*50；元宝100，几率60%！
        
		
		[请帮忙升级:321]
		[结束:0]
		"""
	elif (Menu == 321):
		#判断需要的金币	
		if (Sender.GameGold < 100):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("自然印记（限时）") < 10):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 50):
			say ="""抱歉，无法为你升级，你带够了“魔晶石”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("魔晶石",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,100)
				Sender.GiveItem("强化自然印记",1)
				Sender.TakeItem("自然印记（限时）",10)
				say = """恭喜你，升级成功。你的能力增强了！
								
				[结束:0]
				"""
	elif (Menu == 33):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		强化灵魂印记：灵魂印记（限时）*10；炼制结晶*50；魔晶石*50；元宝100，几率60%！
        
		
		[请帮忙升级:331]
		[结束:0]
		"""
	elif (Menu == 331):
		if (Sender.GameGold < 100):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("灵魂印记（限时）") < 10):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 50):
			say ="""抱歉，无法为你升级，你带够了“魔晶石”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("魔晶石",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 5:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,100)
				Sender.GiveItem("强化灵魂印记",1)
				Sender.TakeItem("灵魂印记（限时）",10)
				say = """恭喜你，升级成功。你的能力增强了！
								
				[结束:0]
				"""
	elif (Menu == 34):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		强化神圣印记：神圣印记（限时）*10；炼制结晶*50；魔晶石*50；元宝200，几率50%！
        
		
		[请帮忙升级:341]
		[结束:0]
		"""
	elif (Menu == 341):
		#判断需要的金币	
		if (Sender.GameGold < 200):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("神圣印记（限时）") < 10):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 50):
			say ="""抱歉，无法为你升级，你带够了“魔晶石”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("魔晶石",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 6:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,200)
				Sender.GiveItem("强化神圣印记",1)
				Sender.TakeItem("神圣印记（限时）",10)
				say = """恭喜你，升级成功。你的能力增强了！
								
				[结束:0]
				"""
	elif (Menu == 35):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		强化暗黑印记：暗黑印记（限时）*10；炼制结晶*50；魔晶石*50；元宝200，几率50%！
        
		
		[请帮忙升级:351]
		[结束:0]
		"""
	elif (Menu == 351):
		#判断需要的金币	
		if (Sender.GameGold < 200):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("暗黑印记（限时）") < 10):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 50):
			say ="""抱歉，无法为你升级，你带够了“魔晶石”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("魔晶石",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 6:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,100)
				Sender.GiveItem("强化暗黑印记",1)
				Sender.TakeItem("暗黑印记（限时）",10)
				say = """恭喜你，升级成功。你的能力增强了！
								
				[结束:0]
				"""
	elif (Menu == 36):
		say = """注意：<font color=0xffFF00FF>失败后材料扣除，原升级材料和元宝不扣</font>
		强化幻影印记：幻影印记（限时）*10；炼制结晶*50；魔晶石*50；元宝500，几率50%！
        
		
		[请帮忙升级:361]
		[结束:0]
		"""
	elif (Menu == 361):
		#判断需要的金币	
		if (Sender.GameGold < 500):
			say= """世界上的事情没有免费的，升级也是同样的，下次不要忘了带手续费来。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("幻影印记（限时）") < 10):
			say ="""抱歉，无法为你升级，请问你带来了指定的升级物品了吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("炼制结晶") < 50):
			say ="""抱歉，无法为你升级，请问你带够了“炼制结晶”吗。
			
			[结束:0]
			"""
		elif(Sender.GetItemCount("魔晶石") < 50):
			say ="""抱歉，无法为你升级，你带够了“魔晶石”吗。
			
			[结束:0]
			"""

		else:
		#上面条件都达成，扣除费用和道具
			Sender.TakeItem("炼制结晶",50)
			Sender.TakeItem("魔晶石",50)
			select = random.randint(0,10)
			#设置获得物品的几率
			if select < 6:
				say ="""哦，非常抱歉！手抖了一下，升级失败，再来一次吧！
				
				[结束:0]
				"""
			else:
				SubGameGold(Sender,500)
				Sender.GiveItem("强化幻影印记",1)
				Sender.TakeItem("幻影印记（限时）",10)
				say = """恭喜你，升级成功。你的能力增强了！
								
				[结束:0]
				"""
		
#主菜单
	else:
		say = """印记是特殊能力的证明。我有提升它的方法。
		当然我的技术不是很成熟，有很大几率会失败。
		
		[打探各类印记增强的方法:1]
		
		[关闭:0]"""

	Dict['Say'] = say  # 定义聊天框对话内容
	return Dict

NpcEvent.add_listener(322, "OnClick", OnClick)
