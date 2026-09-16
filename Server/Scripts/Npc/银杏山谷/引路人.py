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
		
		[关闭:0]"""	                             
#跳转菜单1				
	elif (Menu == 1):
		say = """在隐退的魔法师中具有较高声望的高手要数<font color=\"0xff00ff00\">化天先生</font>和<font color=\"0xff00ff00\">霹雳</font>
		<font color=\"0xff00ff00\">尊者</font>了。首先说霹雳尊者，他原来一门宗师，只给自己门派
		的门徒传授武功，不过所有人都可以向他学习具有中等威力
		的一般魔法。
		霹雳尊者住在<font color=\"0xff00ff00\">银杏山谷</font>，到<font color=\"0xff00ff00\">（265:145）</font>附近应该能找到他。
		据说是在村子北边山路上左边的那颗大树下。
		化天先生是一个很奇特的人。他曾经是武林至尊级高手，但
		是没有人了解他的身世和师门，知道现在，这仍然作为人们
		猜测的对象。化天先生住在离银杏山谷稍远的<font color=\"0xff00ff00\">魔法师高手居</font>
		里，从银杏山谷出来往右走，顺着山路一直向上就行了，他
		家就在山坡顶上。具体位置应该在<font color=\"0xff00ff00\">（353:212）</font>附近。
		
		[结束:0]
        
        
        """		
#主菜单
	else:	
		say = """战乱持续不断，江湖上的各类英雄们也不断角逐。但是有些
		超级武林高手反倒退出江湖，过着悠闲的生活。像他们这些
		高手已经把练武之人该得到的都得到了，然后就风风光光的
		退出。这些高手中有些人退出江湖以后还偶尔给那些年轻的
		晚辈们指导武功。
		你要是在修炼武功的过程中遇到什么困难，还是去找他们指
		导一下吧。以现在江湖上的人来看，虽然武功秘籍不难获得，
		但能给你讲解秘籍里蕴含的精髓的人可是少之又少啊。
	
		[询问有关魔法师高手的情况:1]
		[结束:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
	
NpcEvent.add_listener(133,"OnClick",OnClick)
