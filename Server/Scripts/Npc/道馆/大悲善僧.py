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
import random
from 主线任务奖励 import *
clr.AddReference('System')
from System import DateTime
import System
s1 = clr.Reference[System.Object]()
from Defines import *
import Server
import unicodedata
from Utils import ServerUtils
from Npc import *
from Utils.PlayerUtils import *
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
ALLOWED_ITEM_TYPES = [ItemType.Torch]

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	if (Menu == 100):
		say = """我可以指导你以下这些武功。
		（26 - 30 等级 修炼魔法）
		[困魔咒:101]
		（31 - 40 等级 修炼魔法）
		[群体治愈术:102]
		
		[不寻求武功指导:0]"""
	elif (Menu == 101):
		say = """困魔咒是<font color=\"0xff00ff00\">在一定的空间施魔法，使沾有魔气的生物被隔离的魔</font>
		<font color=\"0xff00ff00\">法</font>。带有邪气的生物如果进入困魔咒之内，会因自身体内气体
		不顺而陷入迷惑之中。
		他们直到受到外部的刺激从魔法中苏醒过来为止，不断地在困
		魔咒中打转转。但是如果带有正气的人进入，他们将摆脱困魔
		咒的力量。
		
		[结束:0]"""
	elif (Menu == 102):
		say = """群体治愈术是同时可以治疗很多人的<font color=\"0xff00ff00\">水平很高的恢复术</font>。除了
		同时可以治疗很多人以外，与恢复术没有很大的不同，因此有
		人认为群体治愈术不是很了不起的技术。
		但是每个人体内的气流都不同，可以同时掌握了解几个人气流
		的事情<font color=\"0xff00ff00\">需要非同一般的精神力</font>。同时治疗几个人气的消耗非常
		大，因此该武功是没有经过相当水平的训练完全无法修炼的武功。
		
		[结束:0]"""
	
#####群体治愈术
	elif (Menu == 21):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """想起你第一次请求我传授的时候了。
			那时候我真没有想到你会成为这么优秀的道士。我认为你和一般的训练生一样停留在某个阶段，满足于自己的力量并中断了训练。
			但是你忍受了很困难的训练过程，超出了我的期望。
			我现在好像没有什么可以传授给你。
			
			[毫无道理的话。我现在依然需要大飞圣僧的指教。:22]"""
	elif (Menu == 22):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """不是这样的。
			通过学习可以掌握的知识你已经掌握很充分。
			你认为不足的部分是你以后一边修炼一边要补充的部分。
			不满足于现状，而且以后也进行专心修炼，终究有一天可以填补
			上这个部分的。
			但是不要忘记<font color=\"0xff00ff00\">真正的武功修炼是从现在开始</font>的名言。
			嘿嘿，老人的废话很多哦。
			但是以后修炼武功的过程中，如果有难点，请随时来找我。老
			人我将尽全力帮助你。
			这么看来。。
			有一个很重要的<font color=\"0xff00ff00\">委托</font>。
			
			[什么事情？:23]"""
	elif (Menu == 23):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """我每年这个时候都要<font color=\"0xff00ff00\">去某个村庄祭祖</font>，但是今年有其它的事情不能直接参加祭祖。由于是很重要的祭祖，不能随便委托别人正在苦闷中。如果是你，我信得过好像可以委托你。
			不是很困难的事情。将我给的<font color=\"0xff00ff00\">威魂深怨护身符</font>贴到 祭坛 上，然后背诵祭文，仪式就结束了。可以吗？
			
			[好的，我将参加祭祖。:24]
			[我还不具备办理这种仪式的能力。:25]"""
	elif (Menu == 24):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		elif (GetInventoryCount(Sender) >= 1): #格子大于等于1格
			PlayerSetV(Sender,GV_Taoist_MassHeal,1)
			Sender.GiveItem("威魂深怨护身符",1)
			say = """哦哦。。。
			可以吗？
			那个村庄位于<font color=\"0xff00ff00\">盟重县东北方向绝命谷入口的附近</font>。
			这是<font color=\"0xff00ff00\">威魂深怨护身符</font>，将它贴在 祭坛 上后，请上香。
			那么就拜托了... 
			
			[结束:0]"""
		else:
			say = """背囊里没有位置了，整理出位置后，请再来！
			
			[结束:0]"""
	elif (Menu == 241):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		elif(Sender.GetItemCount("威魂深怨护身符") > 0):
			say = """你身上不是有威魂深怨护身符吗？还想买？
			
			[结束:0]"""
		else:
			say = """哈哈，是说将那么重要的威魂深怨护身符丢失了？如果重新制作护身符，要使用非常贵的颜料。那么可以筹备50000两费用吗？
			
			[即使很贵也要重新买到:242]
			[钱不够，无法买。:243]"""
	elif (Menu == 242):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		elif (Sender.Gold < 50000):
			say = """你钱都没有，还要威魂深怨护身符？准备好做护身符的材料费，再来 ！
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于1格
				SubGold(Sender,50000)
				Sender.GiveItem("威魂深怨护身符",1)
				say = """这是威魂深怨护身符。
				小心不要重新再丢失了。
				
				[结束:0]"""
			else:
				say = """背囊里没有位置了，整理出位置后，请再来！
				
				[结束:0]"""
	elif (Menu == 243):
		say = """那么是说钱不够？
		那么准备好钱，再来！
		直到等到你找来钱。
		
		[结束:0]"""
	elif (Menu == 25):
		say = """啧啧。。过分谦虚了哟。现在你应该充满自信心的时候还没有
		到吗？知道了吗？很遗憾，只好找其他的人了。
		
		[结束:0]"""
	elif (Menu == 261):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """知道了。那个村子是<font color=\"0xff00ff00\">百年之前由于传染病而消失了的村子</font>。自
			从作为那个村子乳汁的溪水被污染后，人们都生病而死。
			
			[真是无法相信的事情。我分别和那个地方的人们谈话了，他们:262]
			[都是活人。:262]"""
	elif (Menu == 262):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """我以前没有讲过吗？世上的事情中无法说明道理的更多。你遇
			见的事情也是其中的一种。有可能由于对蜈蚣的憎恨和拯救村
			子的坚定意志使得<font color=\"0xff00ff00\">那些人的灵魂</font>继续留在那个地方。
			你看到的东西是他们的灵魂。。你没有感觉到他们不像活着的
			人吗？
			
			[虽然没有感觉到他们生的很好看。。。感觉到他们有很强的意:263]
			[志，无论如何不能认为是亡灵。:263]"""
	elif (Menu == 263):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """有才干哟.你看到的那些东西都是因为你和他们有缘分。你终究做成了我没有做成的事情，哈哈。。
			
			[什么话儿？:264]"""
	elif (Menu == 264):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """听说这个村子开始流行传染病消息的时候，我还不能给他们任何帮助。我认为世界上没有任何事情比拯救一个村子更有价值的事情了。
			哈哈，我又在讲废话了。
			
			[是的，曾经有过这个事情。。。:265]"""
	elif (Menu == 265):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		else:
			say = """嗯。。那样了，现在可以还给我以前委托你事情的时候给你的
			<font color=\"0xff00ff00\">威魂深怨护身符</font>吗？
			
			[好的，在这儿。:266]
			[这个，好像落在哪儿了。:267]"""
	elif (Menu == 266):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		elif (Sender.GetItemCount("威魂深怨护身符") > 0):
			if(PlayerGetV(Sender,GV_Taoist_MassHeal)==5):
				PlayerSetV(Sender,GV_Taoist_MassHeal,6)
				Sender.TakeItem("威魂深怨护身符",1)
				Sender.GiveItem("神圣铂金戒指",1)
				GiveGold(Sender,4300)
				say = """谢谢！虽然现在不需要，为了以后要好好地保管。
				好吧，拿着吧。接受这么困难的委托，将贵重的威魂深怨护身符再重新送给你。
				但是你身上的<font color=\"0xff00ff00\">书籍</font>是什么？
				
				不对, 这是群体治愈术的秘诀？
				[这个东西怎么在这儿。。。:268]"""
			else:
				SEnvir.Log("-----------------------------------")
				SEnvir.Log("脚本报错：{} 技能任务群体治愈术出错".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本报错：{} 技能任务群体治愈术出错".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本报错：{} 技能任务群体治愈术出错".format(Sender.Character.CharacterName))
				SEnvir.Log("-----------------------------------")
		else:
			say = """噢，听说年轻朋友想笼络老人。。。你没有威魂深怨护身符吗？
			
			[结束:0]"""
	elif (Menu == 267):
		if Sender.CheckMagic("群体治愈术"):
			PlayerSetV(Sender,GV_Taoist_MassHeal,99)
			say = """你已经练成了群体治愈术，我再没有什么魔法可以教你了，以后再来找我吧。
			
			[结束:0]"""
		elif (GetInventoryCount(Sender) >= 1):
			if(PlayerGetV(Sender,GV_Taoist_MassHeal)==5):
				PlayerSetV(Sender,GV_Taoist_MassHeal,6)
				Sender.GiveItem("神圣铂金戒指",1)
				GiveGold(Sender,3300)
				say = """也没有办法。你也不是故意弄丢的，我再买一个。。。
				接着，这是接受困难委托的<font color=\"0xff00ff00\">谢礼？？</font>。
				但是你身上的<font color=\"0xff00ff00\">书籍</font>是什么？
				
				不对, 这是群体治愈术的秘诀？
				[这个东西怎么在这儿。。。:268]"""
			else:
				SEnvir.Log("-----------------------------------")
				SEnvir.Log("脚本报错：{} 技能任务群体治愈术出错".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本报错：{} 技能任务群体治愈术出错".format(Sender.Character.CharacterName))
				SEnvir.Log("脚本报错：{} 技能任务群体治愈术出错".format(Sender.Character.CharacterName))
				SEnvir.Log("-----------------------------------")
		else:
			say ="""你的包裹没有空格。
			
			[离开:0]"""
	elif (Menu == 268):
		PlayerSetV(Sender,GV_Taoist_MassHeal,99)
		say = """哦，这个世界上还有不少莫名其妙的事，用这个将解了那些人的怨恨。。。
		你真的做了好事。将成为其他道士们<font color=\"0xff00ff00\">的很好谈资</font>。一路顺风。
		
		[结束:0]"""

#困魔咒
	elif (Menu == 3):
		if Sender.CheckMagic("困魔咒"):
			PlayerSetV(Sender,GV_Taoist_TrapOctagon,99)
			say = """你不是已经掌握困魔咒嘛？如果到了可以修炼更高水平武功的时候，请重新再来。
			
			[结束:0]"""
		else:
			say = """困魔咒原来是先人为了封闭邪气而创造的古代魔法。过去称为
			困魔咒的技术和现在的形态有些不同。过去困魔咒的媒体不是
			护身符，而是叫做<font color=\"0xff00ff00\">困魔石</font>带有新鲜气体的石头。如果使用该种
			石头，比我们现在称为困魔咒的技术可以在更广泛的区域永久
			性地压制邪气。
			现在到处都剩有相同的困魔咒，但是最近这些困魔咒中发生了
			<font color=\"0xff00ff00\">不一般的事情</font>。
			
			[什么不一般的事情？:31]"""
	elif (Menu == 31):
		if Sender.CheckMagic("困魔咒"):
			PlayerSetV(Sender,GV_Taoist_TrapOctagon,99)
			say = """你不是已经掌握困魔咒嘛？如果到了可以修炼更高水平武功的时候，请重新再来。
			
			[结束:0]"""
		else:
			say = """据某人说<font color=\"0xff00ff00\">困魔咒中有几处被破坏了</font>。现在只能推测是谁故意搞
			的，但是究竟是谁以什么理由搞的还不是很清楚。现在道馆的
			很多道士和修炼生正在对此事<font color=\"0xff00ff00\">进行调查或者恢复困魔咒</font>。
			但是。。。做此事的人手真的很不够，像你一样的有实力者可
			以成为很大的<font color=\"0xff00ff00\">帮助</font>，你要帮助我们的事情吗？
			
			[好的，我将试试。:311]
			[我还没有担当此事的能力。:312]"""
	elif (Menu == 311):
		if Sender.CheckMagic("困魔咒"):
			PlayerSetV(Sender,GV_Taoist_TrapOctagon,99)
			say = """你不是已经掌握困魔咒嘛？如果到了可以修炼更高水平武功的时候，请重新再来。
			
			[结束:0]"""
		else:
			PlayerSetV(Sender,GV_Taoist_TrapOctagon,1)
			say = """哈哈哈，我看人还是很有眼力的。
			你将要担任恢复的困魔咒在<font color=\"0xff00ff00\">沃玛神殿2层的里侧</font>。首先要找到<font color=\"0xff00ff00\">将</font>
			<font color=\"0xff00ff00\">要恢复的5个困魔祭坛所用的困魔石</font>。从第一困魔石开始到最后
			一个共5个困魔石，分散在各处的火焰怪兽有可能握有困魔石。
			如果5种困魔石都找到了，<font color=\"0xff00ff00\">从第1个困魔咒房间开始按照顺序使</font>
			<font color=\"0xff00ff00\">用困魔石通过每个房间</font>即可。困魔石在进入需要自己房间的瞬
			间受到气的感应，将自动修复祭坛。你只要将那个地方<font color=\"0xff00ff00\">破坏祭</font>
			<font color=\"0xff00ff00\">坛的怪兽都处理掉</font>即可。
			
			有一个<font color=\"0xff00ff00\">注意事项</font>，在新鲜的困魔咒房间里<font color=\"0xff00ff00\">不可以召唤自己的白</font>
			<font color=\"0xff00ff00\">骨</font>。如果召唤，在进入下个困魔咒房间之前一定要解除召唤。
			那么请小心身体，快点回来！
			
			[结束:0]"""
	elif (Menu == 312):
		say = """现在还有些不相信自己能力的样子。那么做些准备，再来！
		
		[结束:0]"""


#主菜单
	else:
		if Sender.Class == Sender.Class.Warrior:
			say = """贫道人称大悲先生，专门指导来这里修行的道士。
			不过你是战士，你应该去边境城市。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Wizard:
			say = """贫道人称大悲先生，专门指导来这里修行的道士。
			不过你是魔法师，你应该去银杏山谷。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Assassin:
			say = """贫道人称大悲先生，专门指导来这里修行的道士。
			不过你是刺客，你应该去比奇。
			
			[结束:0]"""
		else:
			if(PlayerGetV(Sender,GV_Taoist_MassHeal)==1):
				say = """还没有去那个村庄哟。
				那个村庄位于<font color=\"0xff00ff00\">盟重县东北方向绝命谷入口的附近</font>。
				快去快回。
				
				[由于失误，弄丢了护身符:241]
				[结束:0]"""
			elif (PlayerGetV(Sender,GV_Taoist_MassHeal)==5):
				say ="""啊，是你哟。回来了？
				
				[那个。。。在大飞圣僧所讲的地方经历了非常怪异的事情。:261]"""
#困魔咒
			elif((Sender.Level >= 27) and (PlayerGetV(Sender,GV_Taoist_TrapOctagon)==0)):
				say = """困魔咒是<font color=\"0xff00ff00\">在一定的空间施魔法，使沾有魔气的生物被隔离的魔</font>
				<font color=\"0xff00ff00\">法</font>。带有邪气的生物如果进入困魔咒之内，会因自身体内气体
				不顺而陷入迷惑之中。
				他们直到受到外部的刺激从魔法中苏醒过来为止，不断地在困
				魔咒中打转转。但是如果带有正气的人进入，他们将摆脱困魔
				咒的力量。
				你知道<font color=\"0xff00ff00\">困魔咒的由来</font>吗？
				
				[不知道，请讲。:3]"""
			elif((Sender.Level >= 31) and (PlayerGetV(Sender,GV_Taoist_MassHeal)==0)):
				say = """群体治愈术是同时可以治疗很多人的<font color=\"0xff00ff00\">水平很高的恢复术</font>。除了
				同时可以治疗很多人以外，与恢复术没有很大的不同，因此有
				人认为群体治愈术不是很了不起的技术。
				但是每个人体内的气流都不同，可以同时掌握了解几个人气流
				的事情<font color=\"0xff00ff00\">需要非同一般的精神力</font>。同时治疗几个人气的消耗非常
				大，因此该武功是没有经过相当水平的训练完全无法修炼的武功。
				
				[请传授我群体治愈术吧！:21]"""
			else:
				say = """贫道人称大悲先生。
				那，你来找我有什么事？
				
				[寻求武功指导:100]
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(322,"OnClick",OnClick)

