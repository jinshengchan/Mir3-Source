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

	say = """伟大的玛法大陆勇士，您总算找到这里来了。很久以前，我们受伟大的比奇城主派遣，前往诺玛开疆辟土，兴建了繁荣的诺玛村庄和诺玛城，但某一天，突然遭到了邪恶的诺玛怪物袭击。它们有着变幻莫测的魔法，把我们从诺玛赶出来，囚禁在这里。如果你能把我们解救出去，我们一定会重重感谢，当然，这里的守卫都非常强大，你们一定要报团起来，才有可能击败他们。"""


	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(356,"OnClick",OnClick)
NpcEvent.add_listener(357,"OnClick",OnClick)

