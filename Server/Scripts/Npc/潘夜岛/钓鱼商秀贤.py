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
#跳转菜单1衣服	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """我们有很多种钓鱼用品，你想买吗？
		
		[返回:99]
		[关闭:0]"""        
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """请放心吧，
		我会修理好这些护具的。
		
		[返回:99]
		[关闭:0]"""		
#跳转菜单4				
	elif (Menu == 4):
		say = """钓鱼前还是喝一杯酒比较好。
		潘夜岛对面有我那不听话的弟弟俊熙。
		如果这个钓鱼场人多的话，请往相反的方向走。
		
		[返回:99]"""			
#主菜单
	else:
		say = """钓鱼相关用品的购买，鱼类的出售，请到我这里来吧。
		
		[打开商店:1]
		[对话:4]
		[修理:2]
		
		[关闭:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的武器衣服类			
types =[ItemType.Weapon,ItemType.Armour]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goodslist=[
	('钓鱼服（男）',float(1)),
	('钓鱼服（女）',float(1)),
	('绿色鱼竿',float(1)),
	('鱼钩',float(1)),
	('高级鱼钩',float(1)),]
goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(216,"OnClick",OnClick)