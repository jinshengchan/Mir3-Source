# -*- coding: utf-8 -*-
#载入模块SYS引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import collections
import NpcEvent
import random
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
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
	say = "" 
#红名
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
		
		[关闭:0]"""
	elif Sender.Level < 3:
		say = """你还没有开始 乞丐 任务呢！
这个任务是去帮助在比奇省东海客栈工作的 客栈店员 遇到的麻烦。
可惜你现在还没有能力帮助她啊！先去把 等级 修炼提高到 3 以上再说吧！

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) < 38):
		say = """你还没有开始 乞丐 任务呢！
这个任务是去帮助在比奇省东海客栈工作的 客栈店员 遇到的麻烦。
可惜你还没有完成新手指引任务！先去把新手任务完成再说吧！

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 38):
		PlayerSetV(Sender,BV_NQ_MAIN,39)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """你还没有开始 乞丐 任务呢！
在比奇省东海客栈工作的 客栈店员（425:361） 最近好像有点棘手的事情， 去看看吧！

[结束:0]"""
		
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 49):
		if Sender.Level < 5:
			say = """你还没有开始 苍蝇拍 任务呢！
比奇省经营肉铺店的 金氏（446:405） 正在因为没有苍蝇拍的事儿而苦恼呢！去看看怎么回事吧！
可惜你现在还没有帮助他的能力。先去把 等级 提高到 5 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,50)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """现在可以接受 苍蝇拍 任务。
比奇省经营肉铺店的 金氏（446:405） 正在因为没有苍蝇拍的事儿而苦恼呢！去看看怎么回事吧！

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 55):
		if Sender.Level < 7:
			say = """你还没有开始 石母 任务呢！
				石母任务是安抚冤魂的任务。 可惜你现在还没有能力帮助她。
				先去把 等级 提高到 7 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,56)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """现在可以接受 石母 任务。
最近，在比奇省东边的公园常传出隐约的抽泣声。 
前去调查一番吧！

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 62):
		if Sender.Level < 9:
			say = """你还没有开始 王大人 任务呢！
王大人任务是去帮助王大人将比奇省商界掌握在比奇商会手中。
可惜你现在还没有帮助王大人的能力。
先去把 等级 提高到 9 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,63)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """现在可以接受 王大人 任务。
王大人任务就是帮王大人使比奇商会牢牢掌握比奇商界。
如果成功完成任务，会对今后的任务有所帮助。
首先去找 王大人 （389 : 396） 吧。

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 83):
		if Sender.Level < 11:
			say = """你还没有开始 轻型盔甲 任务呢！
轻型盔甲任务就是帮助比奇省的棉布商 怡美 解决困难。
可惜你现在还没有能力帮助怡美。
先去把 等级 提高到 9 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,84)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你还没有开始轻型盔甲任务呢！
去找一找在比奇省经营布店的 怡美（480 : 407），她会向你提出一个请求。
如果完成了她拜托你办的事情的话，你会得到她送给你的礼物哦。

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 86):
		if Sender.Level < 11:
			say = """你还没有开始 半兽人 任务呢！
半兽任务是制止以半兽勇士为中心集结起来的半兽人纠合势力使用古代魔法的阴谋。
可惜你现在还没有与半兽勇士和半兽人对抗的能力。
先去把 等级 提高到 11 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,87)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你还没有开始 半兽人 任务呢！
半兽任务是制止以半兽勇士为中心集结起来的半兽人纠合势力使用古代魔法的阴谋。
前往比奇省内城找 比奇城城主（472 : 361）看看，他好像要拜托你帮助他阻止半兽人的阴谋。

[结束:0]"""

	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 109):
		if Sender.Level < 16:
			say = """你还没有开始千年毒蛇任务呢！
毒蛇山谷出现了传说中的蛇，寻找这条传说中的蛇，取得解毒剂就是千年毒蛇任务。
可惜你现在还没有能力帮助毒蛇山谷的毒蛇山谷老太啊！ 
先去把 等级 提高到 16 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,110)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你还没有开始千年毒蛇任务呢！
毒蛇山谷中出现了传说中的蛇，叫做珍珍的小孩好像已经中毒了！当务之急就是找那条传说中的蛇取得解毒剂。
先去毒蛇山谷去见珍珍的 毒蛇山谷老太 （337 : 223） 吧！

[结束:0]"""


	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 114):
		if Sender.Level < 16:
			say = """你还没有开始被盗灵魂任务呢！
最近比奇省的贩牛商王小二的独生女王丽灵突然被发现一夕之间变成了白痴。
好像是最近盗取百姓灵魂的妖怪干的好事！灵魂任务就是揭开这个妖怪的真面目。
可惜你现在还没有能力完成灵魂任务。
先去把 等级 提高到 16 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,115)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你还没有开始被盗灵魂任务呢！
最近比奇省的贩牛商王小二的独生女王丽灵突然被发现一夕之间变成了白痴。
好像是最近盗取百姓灵魂的妖怪干的好事！灵魂任务就是揭开这个妖怪的真面目。
先去王小二的亲戚 王大人 家了解一些情况吧。

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) == 147):
		if Sender.Level < 22:
			say = """抱歉，对于这个任务几乎一无所知。
我只是听说过去曾经追随沃玛教主的沃玛教最后幸存者为了弥补过去的罪过而与邪恶势力在孤军奋战。 
去帮助他破坏沃玛教主在地上发挥力量的根源—灵魂明珠，并处决沃玛教主好让那些惨死的冤魂们升天。
同沃玛教主对抗需要很强的实力。 可惜你现在还没有这个能力，先去把 等级 提高到 22 以上吧！

[结束:0]"""
		else:
			PlayerSetV(Sender,BV_NQ_MAIN,148)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """抱歉，对于这个任务几乎一无所知。
我只是听说过去曾经追随沃玛教主的沃玛教最后幸存者为了弥补过去的罪过而与邪恶势力在孤军奋战。
去帮助他破坏沃玛教主在地上发挥力量的根源—灵魂明珠，并处决沃玛教主好让那些惨死的冤魂们升天。

[结束:0]"""
	else:
		MainTaskList = GetMainTaskList(Sender,PlayerGetV(Sender,BV_NQ_MAIN))
		if MainTaskList != None:
			a = MainTaskList[1]
			b = int(MainTaskList[2])
			c = MainTaskList[3]
			say = """你辛苦了。向您这样的好心人，一定有好报的…
您的江湖任务进度如下：
		
<font color=\"0xff00ff00\">任务名称</font>： {} 

<font color=\"0xff00ff00\">等级要求</font>： {} 级

<font color=\"0xff00ff00\">任务进度</font>： {} 

[结束:0]""".format(a,b,c)
				

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(294,"OnClick",OnClick)
