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
	
	if (Menu == 1):
		if (Sender.Gold < 500):
			say = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,500)
			Sender.TeleportByMapIndex(7,408,120)	#飞地图ID X坐标 Y坐标
			return
	elif(Menu == 2):
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

		
		[返回:99]
		[关闭:0]"""
	elif(Menu == 3):
		say = """你要了解的爆率都在下面,全国独创采用光通官方公布的隐藏属性解读，增加娱乐可玩性！
		
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
		震天魔神：噬魂级别武器
		神舰：45级别武器 魔灵 石榴级别首饰
		霸王教主：霹雳级别武器
		诺玛教主：诺玛首饰 四字首饰
		地天灭王：高级技能书 诺玛首饰 稀世武器
		
		[返回:99]
		[关闭:0]"""
#主菜单
	else:	
		say = """你好，我是传奇三服务员。
		希望你能在游戏里度过美好的时光，感受到满意的服务。
		<font color=\"0xff00ff00\">第一次来到这里请打开D键，并完成新手任务获得经验、声望、荣誉。。。</font>
	
		[回到道馆:1]    （路费：500金币）
		[游戏快捷键指南:2]
		[游戏爆率介绍:3]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(213,"OnClick",OnClick)
