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
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单1
	elif (Menu == 1):
		say = """我什么都不知道，你还是去问别人吧！
			
			[递给他100钱:2]
			[递给他1000钱:3]
			[放弃询问这个人:0]"""
	elif (Menu == 2):
		say = """哎？这是干什么？
			
			[以后买点酒喝什么的吧！:21]"""
	elif (Menu == 21):
		say = """你…你这是做什么？ 竟敢和保护比奇省治安的我开这种玩笑？
			看来和你是做不了朋友了！要和我比试比试吗…
			我长这么大还是头一次受到这种污辱！
			
			[你千万别误会啊…我真的不是这个意思！:22]"""
	elif (Menu == 22):
		say = """你还狡辩什么啊？这个混蛋！
			
			[你千万不要误会呀！:23]"""
	elif (Menu == 23):
		say = """呵呵…没有别的意思！真的吗？
			
			[对不起，是我错了，请原谅！:24]"""
	elif (Menu == 24):
		PlayerSetV(Sender,BV_NQ_MAIN,68)
		GiveGold(Sender,1)
		Sender.Connection.ReceiveChat("得到 1 金币", MessageType.System)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """唉！没办法，谁让我年纪大来着呢，原谅一下你吧！这里有1钱！
			快去买5瓶烧酒来，喝了酒才能消了我的肚子里的火气。
			别忘了把找还的零钱带回来！
			
			[结束:0]"""
	elif (Menu == 3):
		if (Sender.Gold < 1000):
			say = """你在摸索什么？？？
				
				[结束:0]"""
		else:
			say = """哎？这是干什么？
				
				[以后买点酒喝什么的吧！:31]"""
	elif (Menu == 31):
		say = """你…你这是做什么？ 竟敢和保护比奇省治安的我开这种玩笑？
			看来和你是做不了朋友了！要和我比试比试吗…
			我长这么大还是头一次受到这种污辱！
			
			[你千万别误会啊…我真的不是这个意思！:32]"""
	elif (Menu == 32):
		PlayerSetV(Sender,BV_NQ_MAIN,69)
		SubGold(Sender,1000)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """唔... 谢谢啦。 我就给你讲讲吧！
			
			[拜托啦:10]"""
	elif (Menu == 10):
		say = """哦？是嘛，好吧，我来讲给你听。
			祖先们修建了这比奇省和里面的城镇村庄之后，就开始反复的在周边勘查并拓展自己的根据地。但是这附近值得利用的土地非常的少。很难足够的支持别的地方的农事生产需要。
			随着人口逐渐的增加，人们为了寻找更加宽阔的土地和更多的资源开始拓宽自己的领土。
			于是人们向沃玛、蛇谷、盟众一步一步的扩大土地，开拓没有人烟到达过的沼泽地，也遇到了生活在森林、灌木丛和山洞中其它各种各样的怪物并与它们发生战争，就这样一点一点的扩大了领土，可以说每一寸土地都是用鲜血换来的啊！
			尽管我们现在占据了宽广的领土，但在比奇土地上各处都仍存在着怪物的势力，加上大部分地区全都是深山和茂密的灌木丛，仍然会发生种种阻断村庄之间道路的事情……
			唔…这已经是我所知道的全部故事啦！
			就说到这里吧！酒喝得很爽啊！
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==65):
			say = """喂！……我可是卫士中资历最深的……你先去跟其他的人打听之后再来找我吧！
				不能让人小瞧了我…
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==66):
			say = """喂！……我可是卫士中资历最深的……你先去跟其他的人打听之后再来找我吧！
				不能让人小瞧了我…
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==67):
			say = """哦！你也是来问我关于比奇省历史的吗？
				
				[是的，请给我讲讲比奇省历史的故事吧！:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==68):
			if(Sender.GetItemCount('烧酒') < 1):
				say = """快去买啊！一钱不够吗？
					
					[结束:0]"""
			elif(Sender.GetItemCount('烧酒') < 5):
				say = """我是说五瓶，快去再买点。
					竟敢不听我的！
					
					[结束:0]"""
			else:
				Sender.TakeItem('烧酒',5)
				PlayerSetV(Sender,BV_NQ_MAIN,69)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """零钱啊！ 
					咕噜…咕噜…啊！现在舒服多了。
					对了，你是找我来问什么的来着？
					
					[我想知道关于比奇省历史的事:10]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==69):
			say = """哦？那我就再给你讲一遍吧！
				祖先们修建了这比奇省和里面的城镇村庄之后，就开始反复的在周边勘查并拓展自己的根据地。但是这附近值得利用的土地非常的少。很难足够的支持别的地方的农事生产需要。
				随着人口逐渐的增加，人们为了寻找更加宽阔的土地和更多的资源开始拓宽自己的领土。
				于是人们向沃玛、蛇谷、盟众一步一步的扩大土地，开拓没有人烟到达过的沼泽地，也遇到了生活在森林、灌木丛和山洞中其它各种各样的怪物并与它们发生战争，就这样一点一点的扩大了领土，可以说每一寸土地都是用鲜血换来的啊！
				尽管我们现在占据了宽广的领土，但在比奇土地上各处都仍存在着怪物的势力，加上大部分地区全都是深山和茂密的灌木丛，仍然会发生种种阻断村庄之间道路的事情……
				
				[结束:0]"""
		else:
			say = """要我帮忙吗？
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(258,"OnClick",OnClick)
