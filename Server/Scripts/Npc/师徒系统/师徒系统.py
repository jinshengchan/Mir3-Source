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
import xlwt
import xlrd
from xlutils.copy import copy
from 变量.默认变量 import *
from Utils.PlayerUtils import *
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import Server.Envir.SEnvir as SEnvir
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
#最低拜师等级
MinBaishiLevel = 1
#最高拜师等级
MaxBaishiLevel = 45
#出师等级
ChushiLevel = 48
#收徒等级
BeMasterLevel = 50
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	bg = {}
	font={}
	Dict={}
	student1 = ''
	StudentLevel1 = ''
	StudentOnline1 = ''
	MasterOnline = '离线'
	ShituJieshao = """<font color=\"0xff00ff00\">师徒系统介绍：</font>
				
				1、玩家可以在游戏内拜师，拜师的最低等级为 <font color=\"0xff00ff00\"> {} </font> 级，
				   最高 <font color=\"0xff00ff00\"> {} </font> 级，超出之后则不能拜师。
				2、玩家等级达到 <font color=\"0xff00ff00\"> {} </font> 级可以招收徒弟，
				   每个玩家只能招收 <font color=\"0xff00ff00\"> 1 </font> 名徒弟。
				3、成为师父的玩家，可以获得 <font color=\"0xff00ff00\"> 师尊牌 </font> 道具，
				   可双击传送到不受地图传送限制的徒弟面前，
				   使用冷却延迟三十分钟，必须存在师徒关系才可以使用。
				4、徒弟等级达到 <font color=\"0xff00ff00\"> {} </font> 级自动出师。
				5、每出师一位徒弟，师徒均会获得一定的授业值奖励，
				   完成主线剧情任务，也可以获得一定的授业值奖励。
				6、师父因特殊原因解除师徒关系，双方的授业值都会清零，
				   请玩家谨慎拜师。
				7、玩家拜师后获得 <font color=\"0xff00ff00\"> 师徒令 </font> 道具，
				   可双击传送到不受地图传送限制的师傅面前，
				   使用冷却延迟三十分钟，玩家出师后自动收回。

				""".format(MinBaishiLevel,MaxBaishiLevel,BeMasterLevel,ChushiLevel)
	if (Menu == 1):
		if Sender.GetItemCount('师尊牌') > 0:
			say = """你已经领取过师尊牌，请勿重复领取。
			
			[返回:99]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				Sender.GiveItem("师尊牌",1)
				say = """成功领取师尊牌，快去收徒吧。
				
				[我要收徒:2]
				
				[返回:99]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
			
	elif (Menu == 2):
		for student_value in [BV_CURRENT_STUDENT1]:
			if PlayerGetV(Sender,student_value) == 0:
				Sender.PyInputBox("请输入对方角色名。", "Npc.师徒系统.师徒系统.Admissions", "Npc.师徒系统.师徒系统.InputCanceled",)
				return
		else:
			say = """<font color=\"0xff00ff00\">你的徒弟位置已满，无法招收。</font> 
			
			[逐出师门:3]
			
			[关闭:0]"""
	elif (Menu == 3):
		StudentName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_CURRENT_STUDENT1))
		say = """将你的徒弟 {} （{}级）逐出师门，会扣除你和徒弟所获得的授业值，
		确定要逐出师门吗？
		
		[逐出师门:31]
		
		[关闭:0]""".format(StudentName,StudentName.Level)
	elif (Menu == 31):
		say = KickStudent(Sender,BV_CURRENT_STUDENT1)
	elif (Menu == 4):
		# 师徒值兑换商店功能
		current_shitu_bonus = PlayerGetV(Sender, BV_SHITU_BONUS)
		
		say = """<font color=\"0xff00ff00\">师徒值兑换商店</font>

你当前的师徒值：<font color=\"0xff00ff00\"> {} </font>

请选择要兑换的物品：

[祝福油:41] 20师徒值
[钢玉石:43] 50师徒值
[100万金币:45] 10师徒值
[200万金币:46] 20师徒值
[500万金币:47] 50师徒值

[返回主菜单:99]""".format(current_shitu_bonus)
		
		Dict['Say'] = say
		return Dict
	elif (Menu == 41):
		# 兑换祝福油
		current_shitu_bonus = PlayerGetV(Sender, BV_SHITU_BONUS)
		if current_shitu_bonus >= 20:
			if GetInventoryCount(Sender) >= 1:
				PlayerSetV(Sender, BV_SHITU_BONUS, current_shitu_bonus - 20)
				Sender.GiveItem("祝福油", 1)
				say = """<font color=\"0xff00ff00\">兑换成功！</font>

你花费了20师徒值，获得了祝福油。

[继续兑换:4]
[返回主菜单:99]"""
			else:
				say = """<font color=\"0xffff0000\">背包空间不足！</font>

请整理背包后再来兑换。

[返回兑换菜单:4]"""
		else:
			say = """<font color=\"0xffff0000\">师徒值不足！</font>

你需要20师徒值才能兑换祝福油，
当前只有 {} 师徒值。

[返回兑换菜单:4]""".format(current_shitu_bonus)
		
		Dict['Say'] = say
		return Dict
	elif (Menu == 43):
		# 兑换钢玉石
		current_shitu_bonus = PlayerGetV(Sender, BV_SHITU_BONUS)
		if current_shitu_bonus >= 50:
			if GetInventoryCount(Sender) >= 1:
				PlayerSetV(Sender, BV_SHITU_BONUS, current_shitu_bonus - 50)
				Sender.GiveItem("钢玉石", 1)
				say = """<font color=\"0xff00ff00\">兑换成功！</font>

你花费了50师徒值，获得了钢玉石。

[继续兑换:4]
[返回主菜单:99]"""
			else:
				say = """<font color=\"0xffff0000\">背包空间不足！</font>

请整理背包后再来兑换。

[返回兑换菜单:4]"""
		else:
			say = """<font color=\"0xffff0000\">师徒值不足！</font>

你需要50师徒值才能兑换钢玉石，
当前只有 {} 师徒值。

[返回兑换菜单:4]""".format(current_shitu_bonus)
		
		Dict['Say'] = say
		return Dict
	elif (Menu == 45):
		# 兑换100万金币
		current_shitu_bonus = PlayerGetV(Sender, BV_SHITU_BONUS)
		if current_shitu_bonus >= 10:
			PlayerSetV(Sender, BV_SHITU_BONUS, current_shitu_bonus - 10)
			GiveGold(Sender, 1000000)
			say = """<font color=\"0xff00ff00\">兑换成功！</font>

你花费了10师徒值，获得了100万金币。

[继续兑换:4]
[返回主菜单:99]"""
		else:
			say = """<font color=\"0xffff0000\">师徒值不足！</font>

你需要10师徒值才能兑换100万金币，
当前只有 {} 师徒值。

[返回兑换菜单:4]""".format(current_shitu_bonus)
		
		Dict['Say'] = say
		return Dict
	elif (Menu == 46):
		# 兑换200万金币
		current_shitu_bonus = PlayerGetV(Sender, BV_SHITU_BONUS)
		if current_shitu_bonus >= 20:
			PlayerSetV(Sender, BV_SHITU_BONUS, current_shitu_bonus - 20)
			GiveGold(Sender, 2000000)
			say = """<font color=\"0xff00ff00\">兑换成功！</font>

你花费了20师徒值，获得了200万金币。

[继续兑换:4]
[返回主菜单:99]"""
		else:
			say = """<font color=\"0xffff0000\">师徒值不足！</font>

你需要20师徒值才能兑换200万金币，
当前只有 {} 师徒值。

[返回兑换菜单:4]""".format(current_shitu_bonus)
		
		Dict['Say'] = say
		return Dict
	elif (Menu == 47):
		# 兑换500万金币
		current_shitu_bonus = PlayerGetV(Sender, BV_SHITU_BONUS)
		if current_shitu_bonus >= 50:
			PlayerSetV(Sender, BV_SHITU_BONUS, current_shitu_bonus - 50)
			GiveGold(Sender, 5000000)
			say = """<font color=\"0xff00ff00\">兑换成功！</font>

你花费了50师徒值，获得了500万金币。

[继续兑换:4]
[返回主菜单:99]"""
		else:
			say = """<font color=\"0xffff0000\">师徒值不足！</font>

你需要50师徒值才能兑换500万金币，
当前只有 {} 师徒值。

[返回兑换菜单:4]""".format(current_shitu_bonus)
		
		Dict['Say'] = say
		return Dict

#主菜单
	#玩家等级小于最低拜师等级
	elif Sender.Level < MinBaishiLevel:
		say = ShituJieshao
		say += """<font color=\"0xff00ff00\">你未达到拜师所需等级，请继续加油升级吧！</font>
		
		[关闭:0]"""
	#玩家等级小于或者等于最高拜师等级
	elif Sender.Level <= MaxBaishiLevel:
		#已经有师傅了，显示对应的信息
		if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
			MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
			if SEnvir.GetPlayerByCharacter(str(MasterName)):
				MasterOnline = '<font color=\"0xff00ff00\"> 在线 </font>'
			else:
				MasterOnline = '<font color=\"0xffff0000\"> 离线 </font>'
			say = ShituJieshao
			say += """当前 <font color=\"0xff00ff00\"> {} </font> 授业值      可使用授业值： <font color=\"0xff00ff00\"> {} </font> 
				
				<font color=\"0xff00ff00\">你的师父：</font> {}  {} 
				
				[师徒值兑换商店:4]
				[关闭:0]""".format(PlayerGetV(Sender,BV_TU_BONUSCOUNT),PlayerGetV(Sender,BV_SHITU_BONUS),MasterName,MasterOnline)
		else:
			say = ShituJieshao
			say += """<font color=\"0xff00ff00\">你还没有拜师，快去找个师父吧！</font>
				
				[关闭:0]"""
	#玩家等级小于出师等级
	elif Sender.Level < ChushiLevel:
		#已经有师傅了，显示对应的信息
		if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
			MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
			if SEnvir.GetPlayerByCharacter(str(MasterName)):
				MasterOnline = '<font color=\"0xff00ff00\"> 在线 </font>'
			else:
				MasterOnline = '<font color=\"0xffff0000\"> 离线 </font>'
			say = ShituJieshao
			say += """当前 <font color=\"0xff00ff00\"> {} </font> 授业值      可使用授业值： <font color=\"0xff00ff00\"> {} </font> 
				
				<font color=\"0xff00ff00\">你的师父：</font> {}  {} 
				
				[师徒值兑换商店:4]
				[关闭:0]""".format(PlayerGetV(Sender,BV_TU_BONUSCOUNT),PlayerGetV(Sender,BV_SHITU_BONUS),MasterName,MasterOnline)
		else:
			say = ShituJieshao
			say += """<font color=\"0xff00ff00\">很抱歉，你已经无法拜师。</font>
				
				[关闭:0]"""
	#玩家等级小于收徒等级
	elif Sender.Level < BeMasterLevel:
		#已经有师傅了，显示对应的信息
		if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
			MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
			if SEnvir.GetPlayerByCharacter(str(MasterName)):
				MasterOnline = '<font color=\"0xff00ff00\"> 在线 </font>'
			else:
				MasterOnline = '<font color=\"0xffff0000\"> 离线 </font>'
			say = ShituJieshao
			say += """<font color=\"0xff00ff00\">恭喜，你已经是一名合格的勇士了！请继续加油吧！</font>
				
				当前 <font color=\"0xff00ff00\"> {} </font> 授业值      可使用授业值： <font color=\"0xff00ff00\"> {} </font> 
				
				<font color=\"0xff00ff00\">你的师父：</font> {}  {} 
				
				[师徒值兑换商店:4]
				[关闭:0]""".format(PlayerGetV(Sender,BV_TU_BONUSCOUNT),PlayerGetV(Sender,BV_SHITU_BONUS),MasterName,MasterOnline)
		else:
			say = ShituJieshao
			say += """<font color=\"0xff00ff00\">你没有师父，请加油升级收徒吧。</font>
				
				[关闭:0]"""
	else:
		say = ShituJieshao
		#已经有师傅了，显示对应的信息
		if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
			# 验证师徒关系有效性
			if not ValidateMasterStudentRelation(Sender):
				# 关系无效，重新检查
				if PlayerGetV(Sender,BV_MASTER_INDEX) == 0:
					say += """<font color=\"0xffff0000\">师徒关系异常，已自动清理。</font>
					
					[关闭:0]"""
					Dict['Say'] = say
					return Dict
			
			MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
			if MasterName and SEnvir.GetPlayerByCharacter(str(MasterName)):
				MasterOnline = '<font color=\"0xff00ff00\"> 在线 </font>'
			else:
				MasterOnline = '<font color=\"0xffff0000\"> 离线 </font>'
			say += """当前 <font color=\"0xff00ff00\"> {} </font> 授业值      可使用授业值： <font color=\"0xff00ff00\"> {} </font> 
				
				<font color=\"0xff00ff00\">你的师父：</font> {}  {} 
				
				[师徒值兑换商店:4]
				
				""".format(PlayerGetV(Sender,BV_TU_BONUSCOUNT),PlayerGetV(Sender,BV_SHITU_BONUS),MasterName,MasterOnline)
		#有师尊牌道具，显示师傅信息
		if Sender.GetItemCount('师尊牌') > 0:
			say += """当前 <font color=\"0xff00ff00\"> {} </font> 授业值   可使用授业值： <font color=\"0xff00ff00\"> {} </font>
				
				[招收徒弟:2] （已出师： <font color=\"0xff00ff00\"> {} </font> 个）
				[师徒值兑换商店:4]
				
				""".format(PlayerGetV(Sender,BV_SHI_BONUSCOUNT),PlayerGetV(Sender,BV_SHITU_BONUS),PlayerGetV(Sender,BV_SHITU_COUNT))
			say += """<font color=\"0xff00ff00\">你已招收的徒弟列表如下：</font>
				
				"""
			if SEnvir.GetCharacter(PlayerGetV(Sender,BV_CURRENT_STUDENT1)):
				student1 = SEnvir.GetCharacter(PlayerGetV(Sender,BV_CURRENT_STUDENT1))
				StudentLevel1 = str(student1.Level)+'级'
				if SEnvir.GetPlayerByCharacter(str(student1)):
					StudentOnline1 = '<font color=\"0xff00ff00\"> 在线 </font>'
				else:
					StudentOnline1 = '<font color=\"0xffff0000\"> 离线 </font>'
				say += """{}   {}   {}       [逐出师门:3]
					""".format(student1,StudentLevel1,StudentOnline1,)
		else:
			say = ShituJieshao
			#已经有师傅了，显示对应的信息
			if PlayerGetV(Sender,BV_MASTER_INDEX) > 0:
				MasterName = SEnvir.GetCharacter(PlayerGetV(Sender,BV_MASTER_INDEX))
				if SEnvir.GetPlayerByCharacter(str(MasterName)):
					MasterOnline = '<font color=\"0xff00ff00\"> 在线 </font>'
				else:
					MasterOnline = '<font color=\"0xffff0000\"> 离线 </font>'
				say += """当前 <font color=\"0xff00ff00\"> {} </font> 授业值      可使用授业值： <font color=\"0xff00ff00\"> {} </font> 
					
					<font color=\"0xff00ff00\">你的师父：</font> {}  {} 
					
					[师徒值兑换商店:4]
					
					""".format(PlayerGetV(Sender,BV_TU_BONUSCOUNT),PlayerGetV(Sender,BV_SHITU_BONUS),MasterName,MasterOnline)
			say += """<font color=\"0xff00ff00\">未领取师尊牌，无法查看收徒情况。</font>
					
					[领取师尊牌:1]
					
					[关闭:0]"""

	Dict['Say'] = say                         #定义聊天框对话内容
	return Dict

#点击邀请界面
def Admissions(params):
	Sender = params[0]
	userInput = params[1] if len(params) > 1 else None
	# 验证用户输入
	if not userInput:
		Sender.Connection.ReceiveChat("请输入对方角色名，然后点击确定。".format(userInput),MessageType.System)
		Sender.PyInputBox("请输入对方角色名。", "Npc.师徒系统.师徒系统.Admissions", "Npc.师徒系统.师徒系统.InputCanceled",)
	else:
		#判断能收几个徒弟
		for student_value in [BV_CURRENT_STUDENT1]:
			#判断没收过徒弟
			if PlayerGetV(Sender,student_value) == 0:
				#对方不在线或者名字不对
				if SEnvir.GetPlayerByCharacter(userInput):
					player = SEnvir.GetPlayerByCharacter(userInput)
					#对方等级不对，不符合收徒条件
					if MinBaishiLevel <= player.Level <= MaxBaishiLevel:
						#TODO 对方是否开启师徒开关
						
						#对方已经有师傅
						if PlayerGetV(player,BV_MASTER_INDEX) > 0:
							Sender.Connection.ReceiveChat("玩家 {} 已经拜师，请选择其他玩家。".format(userInput),MessageType.System)
							return
						else:
							#设置双方目前进行收徒中变量
							PlayerSetV(Sender,BV_ON_ADMISSION,player.Character.Index)
							PlayerSetV(player,BV_ON_ADMISSION,Sender.Character.Index)
							#对方弹出邀请界面
							mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
							mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(363)
							mynpc.NPCCall(player)
							Sender.Connection.ReceiveChat("已发送邀请，等待玩家 {} 响应。".format(userInput),MessageType.System)
							return
					else:
						Sender.Connection.ReceiveChat("玩家 {} 等级不符合条件，无法拜师。".format(userInput),MessageType.System)
						return
				else:
					Sender.PyInputBox("请输入对方角色名。", "Npc.师徒系统.师徒系统.Admissions", "Npc.师徒系统.师徒系统.InputCanceled",)
					Sender.Connection.ReceiveChat("无法定位到 {} ,请检查后重新输入。".format(userInput),MessageType.System)
					return
		else:
			Sender.Connection.ReceiveChat("位置已满，无法收徒。",MessageType.System)
			return

#点击邀请界面时 取消邀请
def InputCanceled(params):
	Sender = params[0]
	Sender.Connection.ReceiveChat("取消收徒邀请。",MessageType.System)

#逐出师门
def KickStudent(Sender,num):
	if SEnvir.GetCharacter(PlayerGetV(Sender,num)):
		StudentName = SEnvir.GetCharacter(PlayerGetV(Sender,num))
		if SEnvir.GetPlayerByCharacter(str(StudentName)):
			player = SEnvir.GetPlayerByCharacter(str(StudentName))
			
			# 清理师傅的徒弟相关变量
			PlayerSetV(Sender,num,0)                    # 清理徒弟索引
			PlayerSetV(Sender,BV_SHI_BONUSCOUNT,0)      # 清理师傅临时授业值
			
			# 清理徒弟的师傅相关变量
			PlayerSetV(player,BV_MASTER_INDEX,0)        # 清理师傅索引
			PlayerSetV(player,BV_TU_BONUSCOUNT,0)       # 清理徒弟临时授业值
			PlayerSetV(player,BV_LEVEL_REWARD,0)        # 清理徒弟等级奖励
			PlayerSetV(player,BV_SHITU_BONUS,0)         # 清理徒弟总授业值（重要！）
			PlayerSetV(player,BV_ON_ADMISSION,0)        # 清理收徒进行中状态
			
			# 收回师徒令道具
			player.TakeItem('师徒令',player.GetItemCount('师徒令'))
			
			# 通知徒弟被逐出师门
			player.Connection.ReceiveChat("你已被你的师父 {} 逐出师门。".format(Sender.Name),MessageType.System)
			
			# 记录日志（可选）
			print "师徒关系解除：师傅 %s 逐出徒弟 %s" % (Sender.Name, player.Name)
			
			return """已经将你的徒弟 {} （{}级）逐出师门。
				
				[关闭:0]""".format(StudentName,StudentName.Level)
		else:
			# 徒弟不在线的情况，也要清理变量
			PlayerSetV(Sender,num,0)                    # 清理徒弟索引
			PlayerSetV(Sender,BV_SHI_BONUSCOUNT,0)      # 清理师傅临时授业值
			
			# 记录日志（可选）
			print "师徒关系解除：师傅 %s 逐出离线徒弟 %s" % (Sender.Name, StudentName)
			
			return """已经将你的徒弟 {} （{}级）逐出师门。
				
				[关闭:0]""".format(StudentName,StudentName.Level)
	else:
		# 无效的徒弟索引，清理师傅变量
		PlayerSetV(Sender,num,0)                        # 清理无效的徒弟索引
		PlayerSetV(Sender,BV_SHI_BONUSCOUNT,0)          # 清理师傅临时授业值
		
		return """徒弟信息无效，已清理相关数据。
			
			[关闭:0]"""


# 师徒关系验证函数
def ValidateMasterStudentRelation(player):
	"""
	验证师徒关系的一致性，清理无效的师徒关系
	"""
	try:
		# 检查徒弟是否有师傅
		master_index = PlayerGetV(player, BV_MASTER_INDEX)
		if master_index > 0:
			master = SEnvir.GetCharacter(master_index)
			if not master:
				# 师傅角色不存在，清理师徒关系
				PlayerSetV(player, BV_MASTER_INDEX, 0)
				PlayerSetV(player, BV_TU_BONUSCOUNT, 0)
				PlayerSetV(player, BV_LEVEL_REWARD, 0)
				PlayerSetV(player, BV_SHITU_BONUS, 0)
				PlayerSetV(player, BV_ON_ADMISSION, 0)
				print "清理无效师徒关系：徒弟 %s 的师傅不存在" % player.Name
				return False
			
			# 检查师傅是否有这个徒弟
			student_index = PlayerGetV(master, BV_CURRENT_STUDENT1)
			if student_index != player.Character.Index:
				# 师徒关系不一致，清理徒弟的师傅信息
				PlayerSetV(player, BV_MASTER_INDEX, 0)
				PlayerSetV(player, BV_TU_BONUSCOUNT, 0)
				PlayerSetV(player, BV_LEVEL_REWARD, 0)
				PlayerSetV(player, BV_SHITU_BONUS, 0)
				PlayerSetV(player, BV_ON_ADMISSION, 0)
				print "清理不一致师徒关系：徒弟 %s 与师傅 %s 关系不匹配" % (player.Name, master.Name)
				return False
		
		# 检查是否同时是师傅和徒弟（不应该发生）
		if PlayerGetV(player, BV_MASTER_INDEX) > 0 and PlayerGetV(player, BV_CURRENT_STUDENT1) > 0:
			# 清理徒弟身份，保留师傅身份
			PlayerSetV(player, BV_MASTER_INDEX, 0)
			PlayerSetV(player, BV_TU_BONUSCOUNT, 0)
			PlayerSetV(player, BV_LEVEL_REWARD, 0)
			PlayerSetV(player, BV_SHITU_BONUS, 0)
			PlayerSetV(player, BV_ON_ADMISSION, 0)
			print "清理冲突身份：玩家 %s 不能同时是师傅和徒弟" % player.Name
			return False
			
		return True
	except Exception as e:
		print "验证师徒关系时出错：%s" % str(e)
		return False

NpcEvent.add_listener(362,"OnClick",OnClick)
