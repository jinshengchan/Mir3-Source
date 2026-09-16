# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
from Defines import *
import random
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

	if (Menu == 1):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """作为一名魔法师，你<font color=\"0xff00ff00\">上一个台阶</font>的时机终于来了。
			
			[下一步:2]"""
	elif (Menu == 2):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """想听对该武功的说明吗？
			
			[是的，想听。:31]
			[不需要。:32]
			"""
	elif (Menu == 31):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """魔法师在1对1的斗争中是最强的，但是遇到多数敌人的包围马
			上就变成了守势。即使不遭到包围，体力和气力很快地消耗，
			因此不能进行长期战。为了弥补这种魔法师的缺点而产生的
			武功正是<font color=\"0xff00ff00\">'爆裂火焰'</font>。
			“爆裂火焰“是在<font color=\"0xff00ff00\">一定范围之内可以产生火焰大爆炸</font>的技术。
			这周围所在的敌人将受到很大的破坏。虽然能源的消耗大，如
			果熟练的话反而可以节省能源。
			对于分散开的敌人没有什么作用。虽然有在使用该技术之前要
			将<font color=\"0xff00ff00\">敌人引诱到一个地方的缺点</font>，<font color=\"0xff00ff00\">对移动快捷的敌人进行攻击</font>还是很
			有效。效果显著，是任何武功都比不上的。
			
			[请教我该武功吧！:4]"""
	elif (Menu == 32):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """那样？你对我的希望是什么？
			
			[请教我该武功吧！:4]"""
	elif (Menu == 4):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """嗯，虽然不可以，也不得不这样了！
			我看你练习该武功<font color=\"0xff00ff00\">内力</font>还是有些不足，练习武功之前，内力不
			能抑制火气的话，将走火入魔。失去武功固然不好，有时候有
			可能丧失生命。那还要练习吗？
			
			[即使有失去生命的遗憾，也要练习。:51]
			[现在好象有些勉强。:52]"""
	elif (Menu == 51):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """已经下了这么大的决心，我教你一种防御方法。
			
			[下一步:6]"""
	elif (Menu == 52):
		say = """没有办法。如果认为很勉强，不做也是其中的一个方法。。。
		
		[结束:0]"""
	elif (Menu == 6):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """你沿着这条路去<font color=\"0xff00ff00\">毒蛇山村</font>，找到七点白蛇，并拿到它的胆汁。
			用<font color=\"0xff00ff00\">七点白蛇的胆汁</font>制成药，服下此药，内力可以大增，而且可
			以抑制火气逆行。
			而且有重要的注意事项，<font color=\"0xff00ff00\">在抓七点白蛇时千万不可以使用魔法</font>。
			如果使用了魔法，蛇胆被破坏将破坏药效，一定要直接进攻捕
			到毒蛇。
			你如果找来七点白蛇胆汁，我将给你制作增强内力的<font color=\"0xff00ff00\">仙丹</font>还传
			授给你武功。
			还有疑问吗？
			
			[毒蛇山村在哪里？:7]"""
	elif (Menu == 7):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """过了银杏山谷、比奇县，毒蛇山村就到了。
			坐标？已经达到像你一样的等级了，还不知道吗？
			
			[为什么需要七点白蛇的胆汁？:8]"""
	elif (Menu == 8):
		if Sender.CheckMagic("爆裂火焰"):
			PlayerSetV(Sender,GV_Wizard_FireStorm,99)
			say = """你不是已经修炼了该武功吗..请找寻其它的武功吧！
			
			[结束:0]"""
		else:
			say = """爆裂火焰的火力非常强大。在修炼不足的情况下修炼该武功，
			体内的火魔将逆行，从而伤害内脏器官。我年轻的时候也是抑
			制不住冲动，仓促修炼该武功，从而受到内伤，到现在为止还
			受到伤痛的折磨。
			用七点白蛇的胆汁制成药，吃了以后可以增强内力，抑制体内
			的火气逆行。
			
			[知道了。:9]"""
	elif (Menu == 9):
		PlayerSetV(Sender,GV_Wizard_FireStorm,1)
		PlayerSetV(Sender,BV_NQ_SKILL,10005)
		PlayerSetV(Sender,BV_NQ_SKILLMON,1)
		say = """那么，快点去找到<font color=\"0xff00ff00\">七点白蛇胆汁</font>吧。这期间我准备其他的药材。
		
		[结束:0]"""
	elif (Menu == 10):
		if (Sender.GetItemCount("七点白蛇胆汁") > 0):
			PlayerSetV(Sender,GV_Wizard_FireStorm,2)
			Sender.TakeItem("七点白蛇胆汁",1)
			Sender.GiveItem("胆汁",1)
			say = """喂，这里有药水。这个药水是用你拿来的<font color=\"0xff00ff00\">胆汁制成的</font>。你吃药的过程中，我将准备武功秘籍。
			
			[下一步:11]"""
		else:
			say = """时间很重要。不好慢腾腾的，快点找来<font color=\"0xff00ff00\">七点白蛇胆汁</font>吧。。。
			
			[结束:0]"""
	elif (Menu == 11):
		if (PlayerGetV(Sender,GV_Wizard_FireStorm)==3):
			if (GetInventoryCount(Sender) >= 2): #格子大于等于2格
				PlayerSetV(Sender,GV_Wizard_FireStorm,4)
				Sender.GiveItem("爆裂火焰（秘籍）",1)
				Sender.GiveItem("流星天玉",1)
				GiveGold(Sender,9900)
				say = """喝完这个药后，掌握了可以解毒的武功书就不会出现走火入魔的事情了。
				希望你可以将武功用在有用的事情上。
				
				[谢谢！:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
		else:
			say = """你现在还没有吃<font color=\"0xff00ff00\">药</font>，如果这样我也不能把书给你。
			
			[结束:0]"""
	
#主菜单
	else:
		if (Sender.Class == Sender.Class.Wizard) and (PlayerGetV(Sender,GV_Wizard_FireStorm)==0):
			if((Sender.Level >= 32) and (PlayerGetV(Sender,GV_Wizard_FireStorm)==0)):
				say = """你有什么事吗？说说看。。
				嗯，想学称为“爆裂火焰”的武功？
				
				[下一步:1]"""
			else:
				say = """如果需要帮忙，请随时来找我！"""
		elif (PlayerGetV(Sender,GV_Wizard_FireStorm)==1):
			if(Sender.GetItemCount("七点白蛇胆汁") > 0):
				say = """嗯,很幸运地找来了。好的，现在该我制药了。请等一下！
				
				[下一步:10]"""
			else:
				say = """时间很重要。不好慢腾腾的，快点找来<font color=\"0xff00ff00\">七点白蛇胆汁</font>吧。。。
				
				[结束:0]"""
		elif (PlayerGetV(Sender,GV_Wizard_FireStorm)==3):
			say = """喂，这里有药水。这个药水是用你拿来的<font color=\"0xff00ff00\">胆汁制成的</font>。你吃药的过程中，我将准备武功秘籍。
			
			[下一步:11]"""
		else:
			say = """如果需要帮忙，请随时来找我！"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#类型为 Enums里的普通类
types =[ItemType.Nothing]
	
NpcEvent.add_listener(319,"OnClick",OnClick)
