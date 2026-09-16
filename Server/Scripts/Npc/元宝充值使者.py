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
	bg = {}
	font={}
	Dict={}
	
	if (Menu == 1):
		Sender.TopUp()
		say = """您已经领取成功。
			
		[关闭:0]"""
	elif (Menu == 2):
		say = """您好，欢迎来到 <font color=\"0xff00ff00\">逍遥传奇3</font> 很高兴为您服务
		
		①本系统支持网上银行、手机充值卡、各类游戏点卡。
		②当前充值比例为1:10
		
		
		
		<link  color=0xffffff00  hcolor=0xffff0000  dcolor=0xffff0000  text=点击联系管理员  x=1  y=90  data=|url:tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=3107412015  />
		<link  color=0xffffff00  hcolor=0xffff0000  dcolor=0xffff0000  text=点击联系管理员  x=100  y=90  data=|url:tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=3107412015  />
		<link  color=0xffffff00  hcolor=0xffff0000  dcolor=0xffff0000  text=点击联系管理员  x=200  y=90  data=|url:tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=3107412015  />
		
		[退出:0]"""
	elif (Menu == 3):
		say = """我可以帮你把红包兑换成元宝，需要兑换吗？
		
		[兑换1元红包:11]           1元红包兑换100个元宝
		[兑换2元红包:16]           2元红包兑换200个元宝
		[兑换5元红包:12]           5元红包兑换500个元宝
		[兑换10元红包:13]       10元红包兑换1000个元宝
		[兑换50元红包:14]       50元红包兑换5000个元宝
		[兑换100元红包:15]   100元红包兑换10000个元宝

		[返回:99]		
		[退出:0]"""
	elif(Menu == 11):
#判断是否有要求的道具			
		if(Sender.GetItemCount("1元红包") < 1):
			say ="""你都没有红包。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("1元红包",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("兑换元宝成功！你已增加100个元宝",MessageType.System)
			say="""成功兑换100个元宝
			
			[继续兑换:11]
			[离开:0]"""
	elif(Menu == 12):
#判断是否有要求的道具			
		if(Sender.GetItemCount("5元红包") < 1):
			say ="""你都没有红包。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("5元红包",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("兑换元宝成功！你已增加500个元宝",MessageType.System)
			say="""成功兑换500个元宝
			
			[继续兑换:12]
			[离开:0]"""
	elif(Menu == 13):
#判断是否有要求的道具			
		if(Sender.GetItemCount("10元红包") < 1):
			say ="""你都没有红包。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("10元红包",1)
			GiveGameGold(Sender,1000)
			Sender.Connection.ReceiveChat("兑换元宝成功！你已增加1000个元宝",MessageType.System)
			say="""成功兑换1000个元宝
			
			[继续兑换:13]
			[离开:0]"""
	elif(Menu == 14):
#判断是否有要求的道具			
		if(Sender.GetItemCount("50元红包") < 1):
			say ="""你都没有红包。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("50元红包",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("兑换元宝成功！你已增加5000个元宝",MessageType.System)
			say="""成功兑换5000个元宝
			
			[继续兑换:14]
			[离开:0]"""
	elif(Menu == 15):
#判断是否有要求的道具			
		if(Sender.GetItemCount("100元红包") < 1):
			say ="""你都没有红包。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("100元红包",1)
			GiveGameGold(Sender,10000)
			Sender.Connection.ReceiveChat("兑换元宝成功！你已增加10000个元宝",MessageType.System)
			say="""成功兑换10000个元宝
			
			[继续兑换:15]
			[离开:0]"""
	elif(Menu == 16):
#判断是否有要求的道具			
		if(Sender.GetItemCount("2元红包") < 1):
			say ="""你都没有红包。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("2元红包",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("兑换元宝成功！你已增加200个元宝",MessageType.System)
			say="""成功兑换200个元宝
			
			[继续兑换:16]
			[离开:0]"""

	elif(Menu == 4):
#判断是否有要求的道具			
		if(Sender.GetItemCount("霸王教主雕像") < 1):
			say ="""你都没有霸王教主雕像。

			[返回:99]
			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("霸王教主雕像",1)
			GiveExperience(Sender,1000000)
			Sender.Connection.ReceiveChat("霸王教主雕像兑换元宝成功！你已增加1000000经验",MessageType.System)
			say="""成功增加了1000000经验
			
			[继续兑换:4]
			[离开:0]"""

	elif(Menu == 5):
		say = """游戏快捷键非常重要！您可以通过键盘<font color=\"0xff00ff00\">O</font>键打开
		游戏配置-游戏-按键设置 查看！
		
<font color=\"0xff00ff00\">D</font>：D键功能菜单
<font color=\"0xff00ff00\">Y</font>：商城
<font color=\"0xff00ff00\">Q</font>：人物面板
<font color=\"0xff00ff00\">W</font>：背包
<font color=\"0xff00ff00\">F</font>：行会（新人第一次来，要打开它进入新手行会获得Buff）
<font color=\"0xff00ff00\">G</font>：组队
<font color=\"0xff00ff00\">HOME</font>：大补贴内置辅助
<font color=\"0xff00ff00\">P</font>：宠物
<font color=\"0xff00ff00\">E</font>：技能栏
<font color=\"0xff00ff00\">Z</font>：药品快捷栏
<font color=\"0xff00ff00\">S</font>：大地图
<font color=\"0xff00ff00\">O</font>：游戏配置
<font color=\"0xff00ff00\">Ctrl+R</font>：排行榜
<font color=\"0xff00ff00\">Ctrl+W</font>：爆率查询
		
		[返回:99]
		[关闭:0]"""
	elif(Menu == 6):
		say = """隐藏属性解读，增加娱乐可玩性！
		
		蚂蚁洞穴：祝福油 强化油 金币
		绝命谷：祈祷散件
		触龙神：祈祷散件 战神头 虎面头 心魔戒 强化油 祝福油 武神鞋
		沃玛神殿：狂风项链 狂风戒指
		沃玛教主：狂风项链 狂风戒指 记忆散件 沃玛号角
		猪洞：大量金币 战神头 虎面头 虚空道环 无影靴
		失乐园：金刚散件 33武器
		潘夜岛：大量金币
		石窟：稀释靴子
		骷髅教主：战神头 虎面头 六棱戒指
		灌木林：魔血散件 神谕项链 猫眼 复血
		赤月山谷：魔血散件 神谕项链 猫眼 复血
		祖玛神殿：祖玛牌武器 怨恨项链 昏暗风印 七彩金环 流星项链 破坏项链 武圣 天机 紫金环
		潘夜神殿：潘夜武器 心灵 骑士 龙之手镯 五行 乾坤
		黑度真天宫：38级别武器 雷神级别首饰 黑铁头
		震天魔神：嗜魂法杖、龙纹剑、霹雷等武器
		神舰：45级别武器 魔灵 石榴级别首饰
		霸王教主：铁轮、逍遥扇、屠龙等武器
		诺玛教主：诺玛首饰 四字首饰
		地天灭王：高级技能书 诺玛首饰 稀世武器
		黎明女王：天神法杖、泰轮拂尘、破山剑等稀世武器
		
		[返回:99]
		[关闭:0]"""




#主菜单
	else:	
		say = """您好，欢迎来到 <font color=\"0xff00ff00\">逍遥传奇3</font> 
		 <font color=\"0xff00ff00\">QQ群：123456789</font> 很高兴为您服务		

		
				[红包兑换元宝:3]

				[游戏快捷键指南:5]

				[游戏爆率介绍:6]

				[霸王教主雕像换经验:4] 

	<font color=\"0xff00ff00\">霸王教主雕像是霸王教主灵魂精华，可以兑换100万经验。　</font>								
				
		[退出:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(212,"OnClick",OnClick)