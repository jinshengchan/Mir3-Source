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
import collections
import Server.Envir.SEnvir as SEnvir
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Utils import ServerUtils
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
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		say = """还好。
		为什么要求见我？虽然钻了追踪者们的空子，但这地方不是
		久留之地。
		
		[我想了解前代大祭祀长的死亡和之后的情形。:11]"""
	elif (Menu == 11):
		say = """嗯，考虑到紫霞神女和占星术士安排你跟我见面，应该是有
		某些理由吧。我就相信他们，把我知道的事情都告诉你。
		大祭祀长神秘被杀的那一天，陪同那位的一行人当中也有我
		的师父。并且，在那个地方被杀的人，都有一个共同点，那
		就是，在那场战斗中死于非命的祭祀长和法老们，都是我们
		敢死组织的成员。
		... 但是，你为什么对这个事件感兴趣呢？那么久以前的事
		情，况且你也不是诺玛族人，只是个人类，真是令人费解啊
		。。
		
		<font color=\"0xffffff00\">最近有一位流亡的法老，看到阿龙怪掉落的尸骨项链后，</font>
		[就拜托我来调查此事。:12]"""
	elif (Menu == 12):
		say = """尸骨项链?! 难道，你现在带着那个项链吗？
		快让我看看！
		
		[拿出尸骨项链。:13]"""
	elif (Menu == 13):
		say = """这，这分明是扎马尔大人的项链。。
		为什么这个项链会在身为人类的你的手中？这分明是扎马尔
		大人牺牲的那天消失的呀？！
		
		<font color=\"0xffffff00\">难道这个项链拥有什么特殊的意义吗？</font>
		<font color=\"0xffffff00\">一个叫做拉贝卡的人，也说过故人曾经十分珍惜这个项链，</font>
		[因此他一直在寻找这个项链。。:14]"""
	elif (Menu == 14):
		say = """拉贝卡...? 你遇见了那个叛徒吗？
		那家伙没有追问你项链的来历，或者讨要那个项链吗？
		
		<font color=\"0xffffff00\">... 不是这样的。他只是说，回忆以前的事情，突然懂得了</font>
		<font color=\"0xffffff00\">一些事情，并说，作为“诺玛统领的走狗”存活着的那段时间</font>
		[并没有白费。:15]"""
	elif (Menu == 15):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10012):
			PlayerSetV(Sender,BV_NQ_NMKILL,10013)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """... 拉贝卡... 难道，当年背叛了我们去投靠诺玛统领的他
			，是为了查出事情的真相吗？这么说，我一直以来在误会着
			他？
			嗯，你问这个项链有什么意义是吧？那好，我就告诉你这个
			项链究竟是什么。
			... 这个项链并不是平凡之物。这是承载了我们敢死组织的
			盟约而制造的。你现在手里拿着的，就是只能由最高的勇士
			才能佩戴的项链。
			但是，为什么那个诺玛统领的养子－阿龙怪持有着这东西，
			可着实让人费解啊。。
			
			[阿龙怪出现:16]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 16):
		map = SEnvir.GetMap(567)
		cell = map.Cells[63,237]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		if map.GetAliveMonsterCount(100430) < 1:
			ServerUtils.SpawnMonsters(567, 100432, 10, 63, 237, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
			ServerUtils.SpawnMonsters(567, 100430, 1, 63, 237, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
		return
	elif (Menu == 2):
		say = """[再次叫您到这么危险的地方，实在是很抱歉。:21]"""
	elif (Menu == 21):
		say = """没关系。即使你不叫我，我也有几件想不通的事情，想再次
		和武士你碰面的
		
		[所谓想不通的事情，究竟是什么事情呢？:22]"""
	elif (Menu == 22):
		map = SEnvir.GetMap(567)
		if map.GetAliveMonsterCount(100430) < 1:
			ServerUtils.SpawnMonsters(567, 100432, 10, 212, 208, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
			ServerUtils.SpawnMonsters(567, 100430, 1, 212, 208, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
			talk=[
				{'m':"<阿龙怪> 哼，好像察觉到什么的样子嘛。不过已经晚了！虽然上次让你逃走了，这次就不用妄想了！出卖同族的叛徒啊，看我审判之剑！" ,'s': MessageType.System,'id': 0,'i': 601},
				{'m':"<大法老> 这是.. 阿龙怪的声音！正如我所预料，果然重新出现在这里了。人类武士啊，我有话跟阿龙怪说，请你帮忙打退其他的武将吧！",'s': MessageType.System,'id': 0,'i': 603},
				{'m':"<阿龙怪> 以为打倒了我们就能从这个地方溜走吗？呵哈哈哈，痴心妄想！ 半个小时后，我们的援兵会将这个地方围得水泄不通的！诺玛教主的战士们啊，先去干掉那个人类武士！",'s': MessageType.System,'id': 0,'i': 601},
				]
			DelayTalk((Sender,talk,0,TalkFinished1))
			return
	elif (Menu == 3):
		say = """...那就是使用了被禁止的力量的后遗症。长期使用魔剑力
		量的人，会逐渐被魔剑的力量所侵蚀，不止是肉体，连精神
		也会生病。阿龙怪在体力和精神力上都比常人要强，因此可
		以在不失去理智的基础上使用魔剑的力量。但是，看得出他
		的极限也快到了。
		对不起啊，武士。事实上，我是为了将阿龙怪引到这里来，
		才答应了武士你的邀请的。
		...感觉中，拜托武士来做此事的人，与阿龙怪似乎有什么
		联系。虽然一开始指示猜测，但是现在我可以确定了。再或
		许，也有可能是武士你正受到着与诺玛统领有关的某个人的
		监视。
		
		<font color=\"0xffffff00\">但是，这样差点就危及了帕斯卡大人的生命！</font>
		[究竟有没有这么做的必要？！:31]"""
	elif (Menu == 31):
		say = """值得这么做的。如果能抛出这条老命来换取未来的话，绝对
		值得这么做的！
		现在正在进行着的人类和诺玛族的战争，都是起因于魔族和
		魔教徒们的阴谋！想利用人类和诺玛们的贪婪和仇恨来消灭
		这两个善良民族的人，也是他们！虽然现在这场灾难开始于
		人类和诺玛族之间，但很快会席卷所有的善良民族的！
		
		
		[继续:32]"""
	elif (Menu == 32):
		say = """唯有将所有善良民族的力量拧成一股绳，才能改变世界。本想现在的诺玛统领会继承扎马尔大人的路线来协助这个奇迹的诞生，但是我们误算了。 唉，看来真的应该托付给像武士这样拥有精力和明亮双眸的年轻人才是，我们这些不识抬举的老头子们都要缩回去了。。
		......但是，武士你是否也想将毁灭之印据为己有呢？
		
		<font color=\"0xffffff00\">...作为武士，说对拥有巨大力量的法器没有兴趣的话，</font>
		[那肯定是骗人的。:33]"""
	elif (Menu == 33):
		say = """呵呵呵, 毁灭之印? 你居然知道了毁灭之印的事情？
		呵呵呵呵-这样啊。那好，如果你肯跟我这个老头子定一些
		誓约的话，我就告诉你有关毁灭之印的事情。
		
		[发誓遵守约定:34]
		[表示无法保证:35]"""
	elif (Menu == 34):
		say = """回答可真是爽快呀。。那好，就告诉你关于毁灭之印的事情。
		现在诺玛统领保管着的毁灭之印是假的。诺玛统领自己也知
		道，但是对自己部下和百姓们却是绝口不提。很可能，诺玛
		统领也在拼命地寻找真正的毁灭之印。因为那是可以唯一威
		胁到其生存的法器。
		我们的同志在当初诺玛统领为了攥取权力而有意造成混乱的
		时候，将那东西藏到了一个谁也不会想到的地方去了。因为
		我们想到，如果让真正的毁灭之印落入跟诺玛统领一样危险
		的人的手中的话，会发生多么可怕的事情。
		
		[那么，真正的毁灭之印藏在哪里呢？:36]"""
	elif (Menu == 35):
		say = """我告诉你毁灭之印的秘密吧。
		现在诺玛统领保管着的毁灭之印是假的。诺玛统领自己也知道
		，但是对自己的部下和百姓们却是绝口不提。很可能，诺玛统
		领也在拼命地寻找真正的毁灭之印。因为那是可以唯一威胁到
		其生存的法器。
		我们的同志在当初诺玛统领为了攥取权力而有意造成混乱的时
		候，将那东西藏到了一个谁也不会想到的地方去了。因为我们
		想到，如果让真正的毁灭之印落入跟诺玛统领一样危险的人的
		手中的话，会发生多么可怕的事情。
		
		[那么，真正的毁灭之印藏在哪里呢？:36]"""
	elif (Menu == 36):
		say = """真正的毁灭之印就藏在举行仪式的圣地的祭坛下面。我们在
		祭坛下面造了一个机关来隐藏了毁灭之印。要想启动这个机
		关，就一定要知道我们组织中流传下来的秘义。
		这个秘义不是以话语，而是以记忆传接着的。我为了自己的
		目的将你拉进了如此危险的境地，作为补偿，就传授给你那
		个秘义吧！虽然作为补偿，这个东西的确有点不伦不类。。
		闭上眼睛，以明心智吧，我就要传授给你我们的同志们代代
		流传下来的秘义。
		
		[闭上眼，集中精神。:37]"""
	elif (Menu == 37):
		say = """（看到很多诺玛法老们围攻一个诺玛武将的情形。虽然人数
		上占优，但是法老们好像是处于劣势，但他们最终还是打败
		了那个武将。同时，头脑中传来一个带有奇异颤音的说话声
		。）
		
		[记住我们的罪行～:38]"""
	elif (Menu == 38):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10019):
			PlayerSetV(Sender,BV_NQ_NMKILL,10020)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			map = SEnvir.GetMap(567)
			cell = map.Cells[210,206]
			if cell.Objects != None:
				for object in reversed(cell.Objects):
					if object != None and object.Race == ObjectType.NPC:
						object.Die()
						object.Despawn()
			say = """那就是我们的秘义。你绝对不能对任何人泄漏有关毁灭之印
			和这个秘义的秘密。特别是对请求你来调查的那个人，绝对
			不能告诉。
			藏有毁灭之印的祭坛所在的圣地，平时任何人都不能接近。
			那个地方只有在举行仪式的日子开放。恰好明天就是举办仪
			式的日子，你就趁此机会去取来毁灭之印吧。
			我们的圣地，可以通过这个<font color=\"0xff00ff00\">诺玛峡谷</font>来进入。很快那里就会
			举办仪式，但确切的时间我也不清楚。但是错过那个时间的
			话，近期内时无法进入圣地的，所以一定要把握住这次机会
			。愿神的祝福伴随你。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	else:
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10012) and Sender.GetItemCount("击退护身符") > 0 and Sender.GetItemCount("尸骨项链") > 0:
			say = """看来紫霞神女说的武士就是你了。有没有跟踪你的人？
			
			[好像没有。:1]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10017):
			say = """人类不应该来这里，快出去。这次睁一只眼闭一只眼放你们
			一马，如果下次再让我碰上你们，就没有这么好的运气了。
			
			[跟诺玛大法老搭话。:2]"""
		elif  (PlayerGetV(Sender,BV_NQ_NMKILL)==10019):
			say = """究竟，是怎么回事？
			
			[为什么阿龙怪突然感觉很痛苦，逃跑了？:3]"""
		else:
			say = """人类不应该来这里，快出去。这次睁一只眼闭一只眼放你们
			一马，如果下次再让我碰上你们，就没有这么好的运气了。
			
			[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def TalkFinished1(Sender):
	if(PlayerGetV(Sender,BV_NQ_NMKILL)==10017):
		PlayerSetV(Sender,BV_NQ_NMKILL,10018)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)

def DelayTalk(args):  #延迟调用播放
	Sender = args[0]
	talkContexts = args[1]
	talkIndex = args[2]
	talkFinishFunc = args[3]
	if talkIndex < len(talkContexts) and Sender is not None and Sender.Connection is not None:
		talkinfo = talkContexts[talkIndex]
		Sender.Connection.ReceiveChat(talkinfo['m'],talkinfo['s'],talkinfo['id'],talkinfo['i'])
		if talkIndex == len(talkContexts) - 1 :
			talkFinishFunc(Sender)
		else:
			Server.Envir.SEnvir.DelayCall("Npc.其他.帕斯卡.DelayTalk",5,(Sender,talkContexts,talkIndex + 1,talkFinishFunc))

NpcEvent.add_listener(372,"OnClick",OnClick)
