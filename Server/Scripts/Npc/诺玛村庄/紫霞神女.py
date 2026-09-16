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
		say = """人类和诺玛族之间正发生一场残酷无情的战争。
		只要陀大怪还没有被消失，这场战争就永远不会划上终止符。
		
		[关闭:0]"""
	elif (Menu == 2):
		say = """帕斯卡...?
		您是从什么地方听到这个名字的？
		
		[您应该知道叫做帕斯卡的诺玛法老吧。:21]"""
	elif (Menu == 21):
		say = """... 我不想说谎，我是认识他。但是我不能告诉您关于他的
		事情。
		这不是因为我信不过您，而是这位跟我所在的帮会的事情有
		关系。
		嗯，但是如果你能够证明自己是可以信赖的人，我倒是可以
		引荐给他。
		
		[要怎么证明呢？:22]"""
	elif (Menu == 22):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10009):
			PlayerSetV(Sender,BV_NQ_NMKILL,10010)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """很简单。绿洲的<font color=\"0xff00ff00\">占星术士 梅山侠</font>拥有着可以辨别人的善恶
			的一双慧眼。请到她那里去弄一张证明你是好人的证票吧。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 3):
		say = """呵呵，您拿到了正确的东西呀。从占星术士给了您那么贵重
		的符咒看来，您应该是值得那么做的人物啊。
		请将那符咒时时刻刻带在身上吧。占星术士大人的法力会保
		护您的生命的。
		既然您已经拿来了证票，我也要履行我的承诺了。我会安排
		您和帕斯卡大人见面的。只是由于那位现在在被追击当中，
		不能够在公开场合会面，我会安排一个隐秘的场所的。但是
		，跟那位取得联系，可能需要一些时间。请您明天再来，我
		会告诉您确切的时间和地点。
		
		[继续:31]"""
	elif (Menu == 31):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10011):
			PlayerSetV(Sender,BV_NQ_NMKILL,10012)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """那位大人现在所处的位置是<font color=\"0xff00ff00\">诺玛峡谷东边的63:237</font>附近。为了
			引开那些追击者，将会面的地点设在了追击者们的据点。但是
			由于危险，并不能在那里久留，所以请您在最晚<font color=\"0xff00ff00\">星期五晚10点</font>
			<font color=\"0xff00ff00\">之前</font>去于那位会面。如果过了<font color=\"0xff00ff00\">星期五晚10点</font>的话，就请放弃与
			那位大人碰面吧，请注意不要让人盯了尾哨。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 4):
		say = """我并不是想指责您，所以不必道歉。我所怀疑的不是您，而
		是托付您做这件事情的那个人。
		受人之托，不能拒绝，您肯定是接受了什么人的委托了吧？
		请求您来找帕斯卡大人的人是谁？
		
		[说出夏柯的名字。:41]
		[不说出夏柯的名字。:42]"""
	elif (Menu == 41):
		say = """... 夏柯啊，就是那么最近流亡的大法老是吧。。
		可是很奇怪啊，能够升到大法老位置的人，肯定在寺院里面经
		历国很长的修练生活，怎会那么不清楚内部事务呢？况且，他
		执着于前任大祭祀长的死因，也太奇怪了。曾在诺玛统领属下
		过着安稳生活的他会突然流亡，还有他居然派一个外族的人来
		调查相关人员，这些都透着一点奇怪呢。
		请务必对那家伙保持警觉心，没准他会是诺玛统领派过来的间
		谍呢。
		由于不是别人，而是您的请求，我就重新给帕斯卡大人发送消
		息过去。
		
		[继续:43]"""
	elif (Menu == 42):
		say = """我也并没有指望您一定会说出那个名字。。嗯，好吧，对托付
		之人进行负责的意思我懂得。但是，也请您多加小心那个人。
		从阿龙怪知道确切的会面场所发动袭击的这一点来看，好像
		是阿龙怪的间谍在监视着您。
		考虑到您的义气，我再次安排一下与帕斯卡大人的会面吧。
		但是，请务必避免上次所发生的那种事情。
		
		[继续:43]"""
	elif (Menu == 43):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10015):
			PlayerSetV(Sender,BV_NQ_NMKILL,10016)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """请明天再来获取答复吧。但是，那位大人是否会愿意冒着风险重新出现在隐居处之外，我也不太好说。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
#主菜单
	else:
		today = datetime.datetime.now().weekday() + 1  #判断周几
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10009):
			say = """徘徊于村庄周围的诺玛吗？嗯。。不太清楚。几天前倒是看
			到过阿龙怪在周围进行侦察，但也没有过什么危险的行动，
			就不见了。
			
			[有没有在附近见到过一个老诺玛法老？名字叫做帕斯卡..:2]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10011) and Sender.GetItemCount("击退护身符") > 0:
			say = """你好像去过占星术士那里了，请问拿到了证票了吗？
			
			[证票没有给我，不过给了这么一个东西。:3]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10015):
			say = """看来您还想会见那位大人啊。。
			请问您像与他见面的理由是什么，这件事情跟阿龙怪有什么
			关系吗？
			
			<font color=\"0xffffff00\">上次的事情，实在是很抱歉。</font>
			[但是真的没有想过阿龙怪会袭击那里。:4]"""
		elif today == 6 and current_time_is_between("19:00:00", "22:00:00") and (PlayerGetV(Sender,BV_NQ_NMKILL)==10016):
			PlayerSetV(Sender,BV_NQ_NMKILL,10017)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """您很幸运，帕斯卡大人答应再次见您了。
			那位大人现在所处的位置是<font color=\"0xff00ff00\">诺玛峡谷的210:206</font>附近。
			但是如同那上次的惊险事故，这次也不能等您很长时间。所
			以请您务必在<font color=\"0xff00ff00\">星期六晚11点之前</font>去与那位会面吧。
			请注意不要让人盯了尾哨。
			
			[关闭:0]"""
		else:
			say = """灾难即将来临，可人类只顾眼前的利益互相争斗。这该怎么办
			才好？
			
			[进行对话:1]
			
			[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(371,"OnClick",OnClick)
