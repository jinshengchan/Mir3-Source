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
import Server
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import collections
clr.AddReference("System.Core")
clr.AddReference('System')
clr.ImportExtensions(System.Linq)
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import unicodedata
import PlayerEvent
import MapEvent
from Utils.TimeUtil import *
import datetime
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
xinchunzhufuyu = [
"春节到了，千祥云集庆有余，百福骈臻贺新年！青山依旧在，祝福年年有！朋友，新的一年锦上添花！",
"春风舞翩翩，香花绽笑颜。心头情无限，短信来拜年。愿友爱情甜，事业翻新篇。幸福绕身边，健康到永远。愿你春节快乐！",
"春节，点亮吉祥的灯火，默念平安词；绽放五彩的礼花，默祈吉祥语；发送心灵的祝福，情谊洒满街。祝福你幸福安乐，好运久久，事事如意，开心永远！",
"烟花打开了新年的篇章，锣鼓敲响了春节的盛世，颂歌奏响了快乐的旋律，短信传递着万家的祥瑞，祝福注满了真挚的情谊，祝愿朋友在新的一年收获成功，享受幸福。春节快乐！",
"一桌团圆菜，二老喜望外，三瓶好酒开，四海聚归来，五谷山珍待，六亲话光彩，七情温馨爱，八方展风采，九杯痛饮快，十分乐开怀！春节祝你愉快！",
"幸福很简单，快乐加开心。春节到，新春始，我的祝福来报到，愿你春节新气象，找寻自己的快乐，属于自己的幸福，日子越来越甜蜜，春节快乐！",
"一杯清茶，一段经历；一朵鲜花，一冬明媚；一声祝福，一句问候，一条短信，一年真情。春节将至，祝你春节快乐，万事如意，幸福安康。",
"春节到，拜年早：一拜全家好；二拜困难少；三拜烦恼消；四拜不变老；五拜儿女孝；六拜幸福绕；七拜忧愁抛；八拜收入高；九拜平安罩；十拜乐逍遥。",
"新年佳节到，拜年要赶早，好运跟你跑，吉祥围你绕，财源进腰包，心想事就成，春节齐欢笑！我的祝福如此早，请你一定要收到。",
"辞旧岁，迎新春：更万象，换新颜：年年岁岁时无尽，岁岁年年福无边。此时送福福长驻，祝新的一年鸿运当头，洪福齐天。",
"祝大家在新的一年里，吉星照你，吉神护你，吉瑞找你，吉云跟你，吉月明亮，吉光闪现，吉人有吉相，新年吉时已到，祝你吉祥如意，岁岁大吉！",
"春节来临，欢声不断；电话打搅，多有不便；短信拜年，了我心愿；祝您全家，身体康健；生活幸福，来年多赚；提早拜年，免得占线！新年快乐！",
]

rewards888 = [
					('祝福油', 2, True, 500),
					('攻击神水（特）', 2, True, 1000),
					('自然神水（特）', 2, True, 1000),
					('灵魂神水（特）', 2, True, 1000),
					('体力强效神水（特）', 2, True, 1000),
					('魔力强效神水（特）', 2, True, 1000),
					('疾风神水（特）', 2, True, 1000),
					('攻击神水（大）', 2, True, 3000),
					('自然神水（大）', 2, True, 3000),
					('灵魂神水（大）', 2, True, 3000),
					('体力强效神水（大）', 2, True, 3000),
					('魔力强效神水（大）', 2, True, 3000),
					('疾风神水（大）', 2, True, 3000),
					]

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	say =''
	
	if (Menu == 1):
		say = """春节期间<font color=\"0xff00ff00\">（农历二十四开启到元宵节）</font>
		玩家每天可以花费<font color=\"0xff00ff00\">10万</font>金币进行一次许愿。
		随机获得经验、祝福油等相应道具，玩家许愿语将以走马灯形式播放。
		
		[我要许愿:11]
		
		[关闭:0]"""
	elif (Menu == 11):
		today = datetime.date.today()  #判断周几
		#日期是 15-下个月5号
		if (today.month == 1 and today.day >= 15) or (today.month == 2 and today.day <= 5):
			if (Sender.Gold > 100000):
				if(PlayerGetV(Sender,GV_PLAYER_XINCHUNZHUFU)==0):
					SubGold(Sender,100000)
					PlayerSetV(Sender,GV_PLAYER_XINCHUNZHUFU,1)
					GiveExperience(Sender,300000)     #给30万经验
					ServerUtils.SendMsgToAll("【{}】新春祝福：{}       ".format(Sender.Name, random.choice(xinchunzhufuyu)),MessageType.RollNotice)
					select = random.randint(0, 3)
					if select == 0:
					# 最终奖励
						converted_reward = []
						for item in rewards888:
							converted_item = (item[0], item[1], item[2])
							for i in range(item[3]):
								converted_reward.append(converted_item)
						# 抽取1个
						my_reward = random.sample(converted_reward, 1)
						# 发奖
						Sender.PYMailSend("新春祝福", "运营团队", "你获得随机奖励", my_reward)
						BroadChat('恭喜玩家 {} 新春送祝福，获得 {}'.format(Sender.Name, my_reward[0][0]))
				else:
					say = """你今天已经参与过新春许愿活动。
					
					[离开:0]"""
			else:
				say = """新春许愿需要花费10万金币，你的钱不够，无法许愿。
				
				[离开:0]"""
		else:
			say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
	elif (Menu == 2):
		say = """从<font color=\"0xff00ff00\">农历二十起到农历二十四结束（11-15号）</font>，为期<font color=\"0xff00ff00\">四天</font>时间，
		在神舰打怪，有一定概率获得<font color=\"0xff00ff00\">海鲜大礼包</font>。
		请获得<font color=\"0xff00ff00\">海鲜大礼包</font>的幸运玩家，联系客服兑换领取实物奖励。
		
		[关闭:0]"""
	elif (Menu == 3):
		say = """<font color=\"0xff00ff00\">大年三十到初六（每天晚上20点到22点）</font>，在庄园刷新各大教主以及相应小BOSS，庄园地图为安全区域。
		
		[进入庄园:31]
		
		[关闭:0]"""
	elif (Menu == 31):
		today = datetime.date.today()  #判断周几
		map = SEnvir.GetMap(553)  # 要传送的地图
		randomLocation = map.GetRandomLocation()      #取随机数坐标值
		#日期是 21-27号
		if today.day >= 21 and today.day <= 27:
			# 如果是晚上20点
			if current_time_is_between("20:00:00", "21:59:00"):
				Sender.TeleportByMapIndex(553,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
				return
		else:
			say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
	elif (Menu == 4):
		say = """<font color=\"0xff00ff00\">大年初一、初二全天</font>，异界幽灵船给GM拜年。
		玩家到船一的活动管理员处给GM拜年，可获得大量经验，
		并有几率获得绑定的<font color=\"0xff00ff00\">BOSS召唤卷</font>。
		
		[进入异界神舰:41]
		
		[关闭:0]"""
	elif (Menu == 41):
		today = datetime.date.today()  #判断周几
		map = SEnvir.GetMap(554)  # 要传送的地图
		#日期是 22号
		if today.month == 1 and (today.day == 22 or today.day == 23):
			if(PlayerGetV(Sender,GV_PLAYER_CUNJIEPAOCHUANG)==0):
				Sender.TeleportByMapIndex(554,23,81)          #飞地图ID X坐标 Y坐标
				return
			else:
				say = """你今天已经参与过一次活动，无法再次进入。
				
				[离开:0]"""
		else:
			say = """活动还没开启，请留意活动公告。
			
			[离开:0]"""
#主菜单
	else:
		say = """[新春许愿:1]            [海鲜大礼:2]
		
		[教主庄园:3]            [异界拜年:4]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#NpcEvent.add_listener(349,"OnClick",OnClick)