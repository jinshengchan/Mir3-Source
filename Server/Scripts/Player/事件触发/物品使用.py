
# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import random
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir
import System
s1 = clr.Reference[System.Object]()
import NpcEvent
from Utils.TimeUtil import *
import os

def sendMsgToAll(msg):
	for con in SEnvir.Connections:
		con.ReceiveChat(msg,MessageType.System)

# ！！！注意！！！
# 数据库道具必须为消耗品 且Shape值范围是 [27,1000], 以及2000以上, 不要重复
# ！！！注意！！！
def OnUseItem(args):  #双击使用的道具
	Sender=args[0]
	Item = args[1]

	#消耗品 从27开始扩展  道具数据库Shape 设置对应值
	if(Item.Info.ItemType == ItemType.Consumable):  #背包格子判断
		if(Item.Info.Shape == 27):  #道具数据库Shape值  从27起    欢迎礼包     
			goods1=[{'name':'太阳水（绑定）',
					'count':100,},
					]
			goods2=[{'name':'太阳水（绑定）',
					'count':100,},
					]
			goods3=[{'name':'太阳水（绑定）',
					'count':50,},
					]
			goods4=[{'name':'太阳水（绑定）',
					'count':50,},
					]
			goods5=[{'name':'太阳水（绑定）',
					'count':50,},
					]
			goods6=[{'name':'太阳水（绑定）',
					'count':50,},
					]
			goods7=[{'name':'太阳水（绑定）',
					'count':100,},
					]
			goods8=[{'name':'太阳水（绑定）',
					'count':100,},
					]
					
			mapping_table = {
			MirGender.Male: {MirClass.Warrior: goods1,MirClass.Wizard: goods3,
							MirClass.Taoist: goods5,MirClass.Assassin: goods7},
			MirGender.Female: {MirClass.Warrior: goods2,MirClass.Wizard: goods4,
							MirClass.Taoist: goods6,MirClass.Assassin: goods8},
							}
							
			if(Sender.GiveItemsByStat(mapping_table[Sender.Gender][Sender.Class])):#给多种物品 返回值为FALSE 表示给物品失败 True 成功 goods 必须是如上的dictionary结构 
				return True
			else:
				Sender.Connection.ReceiveChat("你的背包空间不足。",MessageType.System)
			return False
		elif(Item.Info.Shape == 129): #道具数据库Shape值       充值礼包
			goods10=[{'name':'坐标传送符',
					'count':10,},
					{'name':'金条',
					'count':2,},
					{'name':'BOSS探查符',
					'count':2,},
					{'name':'带刺的玫瑰花',
					'count':5,},
					]
			goods11=[{'name':'坐标传送符',
					'count':10,},
					{'name':'金条',
					'count':2,},
					{'name':'BOSS探查符',
					'count':2,},
					{'name':'带刺的玫瑰花',
					'count':5,},
					]
					
			mapping_table = {
			MirGender.Male: {MirClass.Warrior: goods10,MirClass.Wizard: goods10,
							MirClass.Taoist: goods10,MirClass.Assassin: goods10},
			MirGender.Female: {MirClass.Warrior: goods11,MirClass.Wizard: goods11,
							MirClass.Taoist: goods11,MirClass.Assassin: goods11},
							}
							
			if(Sender.GiveItemsByStat(mapping_table[Sender.Gender][Sender.Class])):#给多种物品 返回值为FALSE 表示给物品失败 True 成功 goods 必须是如上的dictionary结构 
				return True
			else:
				Sender.Connection.ReceiveChat("你的背包空间不足。",MessageType.System)
			return False
		elif(Item.Info.Shape == 29): #道具数据库Shape值     彩票 
			select = random.randint(0,10000)
			if select < 2:
				amount = 5000000
				Sender.Connection.ReceiveChat('祝贺你，中了特等奖，获得{}金币！'.format(amount),MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}彩票抽中特等奖，获得{}金币！'.format(Sender.Name, amount),MessageType.System)
			elif select < 5:
				amount = 500000
				Sender.Connection.ReceiveChat('祝贺你，中了 1 等奖，获得{}金币！'.format(amount),MessageType.System)
			elif select < 10:
				amount = 100000
				Sender.Connection.ReceiveChat('祝贺你，中了 2 等奖，获得{}金币！'.format(amount),MessageType.System)
			elif select < 25:
				amount = 50000
				Sender.Connection.ReceiveChat('祝贺你，中了 3 等奖，获得{}金币！'.format(amount),MessageType.System)
			elif select < 100:
				amount = 10000
				Sender.Connection.ReceiveChat('祝贺你，中了 4 等奖，获得{}金币！'.format(amount),MessageType.System)
			elif select < 200:
				amount = 5000
				Sender.Connection.ReceiveChat('祝贺你，中了 5 等奖，获得{}金币！'.format(amount),MessageType.System)
			elif select < 500:
				amount = 1000
				Sender.Connection.ReceiveChat('祝贺你，中了 6 等奖，获得{}金币！'.format(amount),MessageType.System)
			else:
				amount = 0
				Sender.Connection.ReceiveChat('没有中奖，祝你下次好运...'.format(Sender.Name, amount),MessageType.System)
				return True
			goods={'金币':amount}
			if(Sender.GiveItems(goods)):#给多种物品 返回值为FALSE 表示给物品失败 True 成功 goods 必须是如上的dictionary结构 
				return True
			else:
				Sender.Connection.ReceiveChat("你的背包空间不足。",MessageType.System)
			return False
			
		elif(Item.Info.Shape == 30): #道具数据库Shape值     特殊首饰冶炼石		
			my_npc = System.Activator.CreateInstance(Server.Models.NPCObject)         #调用NPC面板
			my_npc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(190)                      #调用NPC序号
			my_npc.NPCCall(Sender)
			return False	
			
		elif(Item.Info.Shape == 31): #道具数据库Shape值     特殊武器制炼石				
			my_npc = System.Activator.CreateInstance(Server.Models.NPCObject)         #调用NPC面板
			my_npc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(191)                      #调用NPC序号
			my_npc.NPCCall(Sender)
			return False
			
		elif(Item.Info.Shape == 32): #道具数据库Shape值     新手祝福油
			#判断手上是否有武器	
			if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
				Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
				return False
			#判断手上的武器是否新手武器	
			if(Sender.Equipment[int(EquipmentSlot.Weapon)].Info.Index not in [2196,2197,2198,2199]):
				Sender.Connection.ReceiveChat("你的武器不是新手武器",MessageType.System)
				return False
			#判断手上的武器是否幸运+6以上
			if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck] > 6):
				Sender.Connection.ReceiveChat("你的新手武器已经幸运+7",MessageType.System)
				return False
			#判断手上的武器是否幸运+5以上
			if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck] < 7):
				select = random.randint(0,10000)
				if select < 5:
					Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)  #按几率给武器加1点幸运并刷新属性值
				elif select < 50:
					Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)  #按几率给武器加1点幸运并刷新属性值
				elif select > 50 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck]  < 5:             #前5点几乎必成
					Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)  #按几率给武器加1点幸运并刷新属性值
				else:
					Sender.Connection.ReceiveChat('你的新手武器没发生任何改变',MessageType.Hint)
				return True

		elif(Item.Info.Shape == 33): #道具数据库Shape值     点化石：合成高级稀世技能书				
			my_npc = System.Activator.CreateInstance(Server.Models.NPCObject)         #调用NPC面板
			my_npc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(378)                      #调用NPC序号
			my_npc.NPCCall(Sender)
			return False
		elif(Item.Info.Shape == 34): #道具数据库Shape值     破空石：破碎虚空，特殊副本传送石				
			my_npc = System.Activator.CreateInstance(Server.Models.NPCObject)         #调用NPC面板
			my_npc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(394)                      #调用NPC序号
			my_npc.NPCCall(Sender)
			return False


		elif(Item.Info.Shape == 35): #道具数据库Shape值     元宝类
			GiveGameGold(Sender,10)   #增加元宝
			Sender.Connection.ReceiveChat('增加10个元宝',MessageType.System)
			return True
		elif(Item.Info.Shape == 36): #道具数据库Shape值     元宝类
			GiveGameGold(Sender,20)   #增加元宝
			Sender.Connection.ReceiveChat('增加20个元宝',MessageType.System)
			return True
		elif(Item.Info.Shape == 37): #道具数据库Shape值     元宝类
			GiveGameGold(Sender,50)   #增加元宝
			Sender.Connection.ReceiveChat('增加50个元宝',MessageType.System)
			return True
		elif(Item.Info.Shape == 38): #道具数据库Shape值     元宝类
			GiveGameGold(Sender,100)   #增加元宝
			Sender.Connection.ReceiveChat('增加100个元宝',MessageType.System)
			return True
		elif(Item.Info.Shape == 39): #道具数据库Shape值     元宝类
			GiveGameGold(Sender,500)   #增加元宝
			Sender.Connection.ReceiveChat('增加500个元宝',MessageType.System)
			return True
		elif(Item.Info.Shape == 40): #道具数据库Shape值     元宝类
			GiveGameGold(Sender,1000)   #增加元宝
			Sender.Connection.ReceiveChat('增加1000个元宝',MessageType.System)
			return True
		elif Item.Info.Shape == 41:
			# 带权重的抽取物品
			# (物品名，数量，是否绑定，权重)
			# 奖池
			rewards = [
					('五倍经验卷（绑定）', 1, False, 16),
					('双倍经验卷（绑定）', 1, False, 130),
					#('麻痹戒指', 1, False, 1),
					#('复活戒指', 1, False, 1),
					#('护身戒指', 1, False, 1),
					#('传送戒指', 1, False, 1),
					('探测项链', 1, False, 1),
					#('隐身戒指', 1, False, 1),
					('防御戒指', 1, False, 1),
					('技巧项链', 1, False, 3),
					('金条', 1, False, 259),
					('金条包', 1, False, 130),
					('金盒', 1, False, 65),
					('结晶', 1, False, 259),
					('高级碎片', 1, False, 259),
					('钢玉石', 1, False, 259),
					('黄色的饰品', 1, False, 65),
					('蓝色的饰品', 1, False, 65),
					('红色的饰品', 1, False, 65),
					('紫色的饰品', 1, False, 65),
					('绿色的饰品', 1, False, 65),
					('灰色的饰品', 1, False, 65),
					('初级准确石', 1, False, 65),
					('初级生命石', 1, False, 259),
					('初级敏捷石', 1, False, 65),
					('初级魔防下限石', 1, False, 65),
					('初级防御下限石', 1, False, 65),
					#('装备特殊属性修炼石', 1, False, 65),
					#('武器特殊属性修炼石', 1, False, 65),
					#('首饰特殊属性修炼石', 1, False, 65),
					('黑龙宝珠', 1, False, 259),
					('炼制结晶', 1, False, 518),
					('1元红包', 1, False, 518),
					('2元红包', 1, False, 259),
					('5元红包', 1, False, 259),
					('10元红包', 1, False, 65),
					('50元红包', 1, False, 16),
					('100元红包', 1, False, 8),
					('经验珠（1000万）', 1, False, 8),
					('经验珠（500万）', 1, False, 16),
					('经验珠（100万）', 1, False, 32),
					('经验珠（50万）', 1, False, 128),
					('宠物召唤券', 1, False, 8),
					('回生丸', 1, False, 6),
					]
			# 最终奖励
			converted_reward = []
			for item in rewards:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)

			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("BOSS宝箱", "惊喜团队", "你打开了BOSS宝箱, 请领取你的奖励", my_reward)
			return True
		elif Item.Info.Shape == 42:
			# 带权重的抽取物品
			# (物品名，数量，是否绑定，权重)
			# 奖池
			rewards = [
					('50W经验', 1, False, 1035),
					('100W经验', 1, False, 876),
					('BOSS宝箱', 1, False, 500),
					('100元红包', 1, False, 259),
					('500W经验', 1, False, 518),
					]
			# 最终奖励
			converted_reward = []
			for item in rewards:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)

			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("霸王教主雕像", "经验奖励", "你打开了霸王教主雕像, 请领取你的奖励", my_reward)
			return True
		elif(Item.Info.Shape == 43): #道具数据库Shape值     金条类
			GiveGold(Sender,995000)   #增加金币
			Sender.Connection.ReceiveChat('增加995000金币',MessageType.System)
			return True
		elif(Item.Info.Shape == 44): #道具数据库Shape值     金盒类
			GiveGold(Sender,9950000)   #增加金币
			Sender.Connection.ReceiveChat('增加9950000金币',MessageType.System)
			return True

		elif(Item.Info.Shape == 47): #道具数据库Shape值     金条包
			GiveGold(Sender,4975000)   #增加金币
			Sender.Connection.ReceiveChat('增加4975000金币',MessageType.System)
			return True
		elif(Item.Info.Shape == 45): #召唤宠物脚本范例
			if(Sender.Pets.Count > 0):
				say = "你已经有宠物了"
				return False    #判断已经有角色了，就无法使用道具了，跳出并不消耗道具
			else:
				# 怪物名 数目 多久叛变(秒)
				Sender.AddPet("地狱炎魔", 1, 18000)
				return True
		elif(Item.Info.Shape == 46): #物品解包
			Sender.GiveItem("强效太阳水",6)
			return True
		elif(Item.Info.Shape == 48): #召唤宠物脚本范例
			if(Sender.Pets.Count > 0):
				say = "你已经有宠物了"
				return False    #判断已经有角色了，就无法使用道具了，跳出并不消耗道具
			else:
				# 怪物名 数目 多久叛变(秒)
				Sender.AddPet("精灵猫", 1, 18000)
				return True
		elif(Item.Info.Shape == 49): #召唤宠物脚本范例
			if(Sender.Pets.Count > 0):
				say = "你已经有宠物了"
				return False    #判断已经有角色了，就无法使用道具了，跳出并不消耗道具
			else:
				# 怪物名 数目 多久叛变(秒)
				Sender.AddPet("田园犬", 1, 18000)
				return True
		elif(Item.Info.Shape == 50): #召唤宠物脚本范例
			if(Sender.Pets.Count > 0):
				say = "你已经有宠物了"
				return False    #判断已经有角色了，就无法使用道具了，跳出并不消耗道具
			else:
				# 怪物名 数目 多久叛变(秒)
				Sender.AddPet("机灵鼠", 1, 18000)
				return True

		elif(Item.Info.Shape == 52): #骷髅教主召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([299,300,301,302]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30002,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用骷髅教主召唤卷，潘夜石窟随机地图刷新骷髅教主一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了骷髅教主召唤卷，潘夜石窟随机地图刷新骷髅教主一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 53): #触龙神召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([149,150,151,152,153,154,155,156]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30003,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用触龙神召唤卷，万年谷随机地图刷新触龙神一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了触龙神召唤卷，万年谷随机地图刷新触龙神一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 54): #赤月恶魔召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([270,271,272,273,274,275,276]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30005,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用赤月恶魔召唤卷，赤月山谷随机地图刷新赤月恶魔一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了赤月恶魔召唤卷，赤月山谷随机地图刷新赤月恶魔一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 55): #祖玛教主召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([131,133,135,136,137,139,140,141]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30007,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用祖玛教主召唤卷，祖玛寺庙随机地图刷新祖玛教主一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了祖玛教主召唤卷，祖玛寺庙随机地图刷新祖玛教主一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 56): #潘夜牛魔王召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([285,286,287,288,289,290,292,293,294,295,296,297]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30006,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用潘夜牛魔王召唤卷，潘夜神殿随机地图刷新潘夜牛魔王一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了潘夜牛魔王召唤卷，潘夜神殿随机地图刷新潘夜牛魔王一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 57): #震天魔神召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([340,341,342,343,344,345,346,347,348,349,350,351,352,353,354]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30010,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用震天魔神召唤卷，真天宫随机地图刷新震天魔神一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了震天魔神召唤卷，真天宫随机地图刷新震天魔神一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 58): #霸王教主召唤卷
			if(PlayerGetV(Sender,GV_PLAYER_ZHAOHUANJUAN) > 0):                #定义个人全局变量
				Sender.Connection.ReceiveChat('你今天已经使用过，无法再次使用',MessageType.System)
				return False    #判断已经用过了，就无法使用道具了，跳出并不消耗道具
			else:
				PlayerSetV(Sender,GV_PLAYER_ZHAOHUANJUAN,1)                  #赋值个人全局变量为1，代表使用过
				refreshMap = random.choice([247,248,249,250]) #刷新地图
				map = SEnvir.GetMap(refreshMap) #获取随机的地图序号
				randomLocation = map.GetRandomLocation() #拿到一个随机的坐标
				map.CreateMon(randomLocation.X,randomLocation.Y,1,30009,1) #随机地图，随机坐标，随机范围，刷沃玛教主1只
				Sender.Connection.ReceiveChat('使用霸王教主召唤卷，神舰随机地图刷新霸王教主一只！',MessageType.System)
				for player in SEnvir.Players:
					if(player is None):
						continue
					player.Connection.ReceiveChat('{}使用了霸王教主召唤卷，神舰随机地图刷新霸王教主一只！'.format(Sender.Name),MessageType.System)
				return True
		elif(Item.Info.Shape == 59): #道具数据库Shape值     时空符文
			select = random.randint(0,100)
			if select < 10:   
				Sender.TeleportByMapIndex(1503,33,38)
				Sender.Connection.ReceiveChat("上天眷顾，你进入了一位传奇隐士居住地。。。",MessageType.System)
			elif select < 30:
				Sender.TeleportByMapIndex(1526,15,26)
			else:
				Sender.TeleportByMapIndex(2,40,33)

		elif(Item.Info.Shape == 60): #祝福罐
			#判断手上是否有武器	
			if (not (Sender.Equipment[int(EquipmentSlot.Weapon)])):
				Sender.Connection.ReceiveChat("你没有装备武器",MessageType.System)
				return False
			#判断手上的武器是否幸运+6以上
			if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck] > 6):
				Sender.Connection.ReceiveChat("你的武器已经幸运+7",MessageType.System)
				return False
			#判断手上的武器是否幸运+5以上
			if(Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck] < 7):
				select = random.randint(0,1000)
				if select < 150:
					Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)  #按几率给武器加1点幸运并刷新属性值
				elif select < 250 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck]  < 5:
					Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)  #按几率给武器加1点幸运并刷新属性值
				elif select > 50 and Sender.Equipment[int(EquipmentSlot.Weapon)].Stats[Stat.Luck]  < 3:             #前3点几乎必成
					Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)  #按几率给武器加1点幸运并刷新属性值
				else:
					Sender.Connection.ReceiveChat('你的武器没发生任何改变',MessageType.Hint)
				return True
		elif(Item.Info.Shape == 61): #道具数据库Shape值     新手礼包
			GiveGold(Sender,5000)    #增加金币
			Sender.Connection.ReceiveChat('增加5000金币',MessageType.System)
			GiveHuntGold(Sender,1200)   #增加赏金
			Sender.Connection.ReceiveChat('增加1200个赏金',MessageType.System)
			
			if Sender.Class == Sender.Class.Warrior:
				Sender.GiveItem("基本剑术（秘籍）",1)
				Sender.GiveItem("攻杀剑术（秘籍）",1)
				Sender.GiveItem("刺杀剑术（秘籍）",1)
			elif Sender.Class == Sender.Class.Wizard:
				Sender.GiveItem("火球术（秘籍）",1)
				Sender.GiveItem("冰月神掌（秘籍）",1)
				Sender.GiveItem("风掌（秘籍）",1)
				Sender.GiveItem("诱惑之光（秘籍）",1)
			else:
				Sender.GiveItem("治愈术（秘籍）",1)
				Sender.GiveItem("精神力战法（秘籍）",1)
				Sender.GiveItem("施毒术（秘籍）",1)
				Sender.GiveItem("灵魂火符（秘籍）",1)
			return True
#		elif(Item.Info.Shape == 62): #道具数据库Shape值     推广礼包
			Sender.GiveItem("攻击神水（新手）",1)
			Sender.GiveItem("自然神水（新手）",1)
			Sender.GiveItem("灵魂神水（新手）",1)
			Sender.GiveItem("体力强效神水（新手）",1)
			GiveGold(Sender,20000)    #增加金币
			Sender.Connection.ReceiveChat('增加20000金币',MessageType.System)
			GiveGameGold(Sender,10)   #增加元宝
			Sender.Connection.ReceiveChat('增加10个元宝',MessageType.System)
			return True
		elif(Item.Info.Shape == 62): #道具数据库Shape值     50W经验
			GiveExperience(Sender,500000)   #增加经验
			Sender.Connection.ReceiveChat('增加500000经验',MessageType.System)
			return True
		elif(Item.Info.Shape == 63): #道具数据库Shape值     100W经验
			GiveExperience(Sender,1000000)   #增加经验
			Sender.Connection.ReceiveChat('增加1000000经验',MessageType.System)
			return True
		elif(Item.Info.Shape == 64): #道具数据库Shape值     500W经验
			GiveExperience(Sender,5000000)    #增加经验
			Sender.Connection.ReceiveChat('增加5000000经验',MessageType.System)
			return True
		elif(Item.Info.Shape == 65): #道具数据库Shape值     1000W经验
			GiveExperience(Sender,10000000)   #增加经验
			Sender.Connection.ReceiveChat('增加10000000经验',MessageType.System)
			return True
		elif Item.Info.Shape == 66: #道具数据库Shape值       声望贡献盲盒
			# 带权重的抽取物品
			# (物品名，数量，是否绑定，权重)
			# 奖池
			rewards = [
					('贡献', 10, False, 5500),
					('声望', 10, False, 5500),
					('贡献', 20, False, 3000),
					('声望', 20, False, 3000),
					('贡献', 50, False, 1000),
					('声望', 50, False, 1000),
					]
			# 最终奖励
			converted_reward = []
			for item in rewards:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("声望贡献盲盒", "运营团队", "你打开了声望贡献盲盒, 请领取你的奖励", my_reward)
			return True
	else:
		return True
	
	return True

PlayerEvent.add_listener("OnUseItem",OnUseItem)#注册使用消耗类物品 如果注册函数返回True 则扣除物品 返回False则不扣除物品

