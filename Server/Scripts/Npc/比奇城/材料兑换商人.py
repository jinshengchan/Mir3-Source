# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
from 主线任务奖励 import *
from Npc.商店列表 import *

# 兑换配置字典
EXCHANGE_CONFIG = {
    101: {'material': '僵尸骨头', 'count': 1000, 'reward': '黑铁', 'reward_count': 1},
    102: {'material': '号角', 'count': 1000, 'reward': '黑铁', 'reward_count': 1},
    103: {'material': '牙齿', 'count': 1000, 'reward': '黑铁', 'reward_count': 1},
    104: {'material': '皮', 'count': 1000, 'reward': '黑铁', 'reward_count': 1},
    105: {'material': '指甲', 'count': 1000, 'reward': '黑铁', 'reward_count': 1},
    106: {'material': '宝玉', 'count': 1000, 'reward': '黑铁', 'reward_count': 1},
    107: {'material': '潘夜之泪', 'count': 500, 'reward': '黑铁', 'reward_count': 1},
    108: {'material': '夜明珠', 'count': 500, 'reward': '黑铁', 'reward_count': 1},
    109: {'material': '神灵雕像', 'count': 500, 'reward': '黑铁', 'reward_count': 1},
    110: {'material': '震天魔印', 'count': 500, 'reward': '黑铁', 'reward_count': 1},
    111: {'material': '遗物', 'count': 200, 'reward': '钢玉石', 'reward_count': 1},
    112: {'material': '魔光片', 'count': 200, 'reward': '钢玉石', 'reward_count': 1},
}
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
	
	# 使用字典配置处理兑换
	elif Menu in EXCHANGE_CONFIG:
		config = EXCHANGE_CONFIG[Menu]
		material = config['material']
		count = config['count']
		reward = config['reward']
		reward_count = config['reward_count']
		
		if Sender.GetItemCount(material) >= count:
			Sender.TakeItem(material, count)
			Sender.GiveItem(reward, reward_count)
			say = """兑换成功！
			
你花费了{}个{}，获得了{}个{}。

[继续兑换:{}]
[结束:0]""".format(count, material, reward_count, reward, Menu)
		else:
			say = """材料不足！
			
你需要{}个{}才能兑换{}个{}。
当前拥有：{}个{}

[返回兑换菜单:100]
[结束:0]""".format(count, material, reward_count, reward, Sender.GetItemCount(material), material)
	


#主菜单
	else:
		say = """<font color=\"0xff00ff00\">材料兑换商人</font>

欢迎来到材料兑换商店！
我可以帮你将收集到的材料兑换成珍贵的矿石。

<font color=\"0xffffff00\">兑换黑铁材料：</font>
[僵尸骨头:101]        兑换1个黑铁
[号角:102]            兑换1个黑铁
[牙齿:103]            兑换1个黑铁
[皮:104]              兑换1个黑铁
[指甲:105]            兑换1个黑铁
[宝玉:106]            兑换1个黑铁
[潘夜之泪:107]        兑换1个黑铁
[夜明珠:108]          兑换1个黑铁
[神灵雕像:109]        兑换1个黑铁
[震天魔印:110]        兑换1个黑铁

<font color=\"0xffffff00\">兑换钢玉石材料：</font>
[遗物:111]            兑换1个钢玉石
[魔光片:112]          兑换1个钢玉石

[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(383,"OnClick",OnClick)

