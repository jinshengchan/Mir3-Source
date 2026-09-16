# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
import random
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
from 主线任务奖励 import *
from datetime import datetime, timedelta
import System
s1 = clr.Reference[System.Object]()
import Server
from Utils.TimeUtil import *
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
		say = """我可以指导你以下这些武功。
		
		（26-30 等级 修炼魔法）
		[野蛮冲撞:11]
		
		[不寻求武功指导:0]"""
	elif (Menu == 11):
		if Sender.Level < 27:
			say = """你的等级不够，无法给你武术指导。
			
			[结束:0]"""
		elif Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==0):
			say = """哦，年纪轻轻好像有相当实力的武功。现在还有这样的战士，找我有什么事情吗？
			
			[想了解新的武功。:12]"""
		else:
			say = """嗯。。战士的路即危险又艰辛。从你所带的工具看好像经历了无数的搏斗和考验。。
			首先将所持的武器刀刃磨光，每个村庄都有加工武器的商人，请他们给修理一下。那些人也许不知道你的心情。。。
			以后找机会再来！
			
			[好的，我知道了。:0]"""
	elif (Menu == 12):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """嗯，你好像在实战中也有些体会。虽然战士总是想在最前方战
			斗，但是没有这种<font color=\"0xff00ff00\">护身术</font>。魔法师可以利用瞬息移动魔法消失
			掉，道士也可以利用隐身术隐藏起自己的行踪，我们只有将敌
			人打倒后才可以脱身。如果被层层包围，真是死路一条。我也
			是经历了无数的生死考验，真是为了解决战士的困难才创造了
			<font color=\"0xff00ff00\">野蛮冲撞</font>。
			
			[野蛮冲撞是具有哪种功能的武功？:13]"""
	elif (Menu == 13):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """可以推开敌人，是一种简单而实用的武功。虽然表面看起来仅
			仅凭借力量将敌人推开，但不是使用肌肉的力量，而是集中<font color=\"0xff00ff00\">内</font>
			<font color=\"0xff00ff00\">力和外力</font>达到极限的高级武功。如果熟练地掌握了该武功，可
			以将比自身大几倍的巨物一下子推开。
			虽然不能给敌人更大的打击，在被敌人包围的状况下可以打出
			一条<font color=\"0xff00ff00\">血路</font>。对于在最前方和敌人正面战斗的战士来说是非常重
			要的武功。
			但是也不能认为该武功是简单的推挡技术。根据使用者的不同
			，可以作为<font color=\"0xff00ff00\">避免魔法或者连续器</font>使用，达到各种各样效果潜在力非常大的武功。
			
			[请传授野蛮冲撞武功！:14]"""
	elif (Menu == 14):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """好的，我的修炼方法非常严格。如果按照此方法学习，我将传授野蛮冲撞给你。
			
			[我应做的事情是什么？:15]"""
	elif (Menu == 15):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==0) and (Sender.GiveItem("书信",1)):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,1)
			say = """带着这个<font color=\"0xff00ff00\">书信</font>，穿越沙漠。找到隐居在<font color=\"0xff00ff00\">绿洲村</font>叫<font color=\"0xff00ff00\">‘王铁匠’</font>的武士，并将书信交给他，他就会告诉你某种秘诀。接受他的指教后再来！
		
			[结束:0]"""
		else:
			say = """你的背囊装满了。。请整理些位置再来！
			
			[结束:0]"""
	elif (Menu == 2):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """去沙漠走一趟如何？理解我为什么让你做这件事情吗？
			
			[嗯，没理解。:21]
			[嗯，好像理解了。:22]"""
	elif (Menu == 21):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """如此愚钝的人，到现在为止心理都在骂我吧。学习野蛮冲撞需要强大的力量和良好的内力，以及在非常艰苦的境况下也不放弃的体力和精力。为了培养这些功力，身体要处于极限的状态。因此让你横跨沙漠。
			
			[这是什么话？:3]"""
	elif (Menu == 22):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """比看起来理解快嘛。有一种将来可以成功的预感。
			
			[这是什么话？:3]"""
	elif (Menu == 3):
		if Sender.CheckMagic("野蛮冲撞"):
			PlayerSetV(Sender,GV_Warrior_ShoulderDash,99)
			say = """你不是已经掌握该武功吗？请到其它的地方搞恶做剧。
			
			[结束:0]"""
		else:
			say = """很正确哟。请拿着训练书，以后要帮助有困难的人。
			
			[下一步:4]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,GV_Warrior_ShoulderDash)==5):
			if (Sender.GiveItem("野蛮冲撞（秘籍）",1)):
				GiveGold(Sender,3000)
				PlayerSetV(Sender,GV_Warrior_ShoulderDash,6)
				say = """在哪儿、写了些什么？嗯，说你是不顾各种危险并找到药的优秀年轻人。对的，帮助有困难的人是我们有能力的人应该做的事情。非常好！你的行为提高了战士的声誉。
				像你一样的人，我也相信，可以将技术传授给你。
				你已经在其它地方得到了武功密集，我也没有再给你的必要了。我给你一些金币和东西，用在需要的地方。
				希望以后你多做有助于提高战士名誉的事情。
				
				[结束:0]"""
			else:
				say = """你的背囊装满了。。请整理些位置再来！
				
				[结束:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本警报：{} 任务序号变更使用封包挂".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本警报：{} 任务序号变更使用封包挂".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本警报：{} 任务序号变更使用封包挂".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	else:
		if Sender.Class == Sender.Class.Wizard:
			say = """人们都叫我黄河大侠，因为我专门指导那些想成为战士的年青
			人。
			不过，你不是战士。魔法师应该去银杏山谷。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Taoist:
			say = """人们都叫我黄河大侠，因为我专门指导那些想成为战士的年青
			人。
			不过，你不是战士。道士应该去道馆。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Assassin:
			say = """人们都叫我黄河大侠，因为我专门指导那些想成为战士的年青
			人。
			不过，你不是战士。刺客应该去比奇。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==1) and (Sender.GetItemCount("书信") > 0):
			say = """沙漠是很远的路。请快些到达！
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==1) and (Sender.GetItemCount("书信") < 1):
			if (Sender.GiveItem("书信",1)):
				say = """书信丢了？让人寒心！重新再给你一本，这次注意拿好。
				
				[结束:0]"""
			else:
				say = """你的背囊装满了。。请整理些位置再来！
				
				[结束:0]"""
		elif (PlayerGetV(Sender,GV_Warrior_ShoulderDash)==4):
			if (Sender.GetItemCount("书信") > 0):
				Sender.TakeItem("书信",1)
				PlayerSetV(Sender,GV_Warrior_ShoulderDash,5)
				say = """已经转交了书信？辛苦了。
				
				[下一步:2]"""
			else:
				say = """沙漠是很远的路。请快些转交书信！
				
				[结束:0]"""
		else:
			say = """每当我看到那些专心修炼武功的年轻人，我就觉得自己的工作很有意义。呵呵，你来找我干什么？
			
			[寻求武功指导:1]
			[结束:0]
			"""
			
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
		

NpcEvent.add_listener(310,"OnClick",OnClick)