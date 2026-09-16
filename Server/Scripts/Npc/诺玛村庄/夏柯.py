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
from 主线任务奖励 import *
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
REFINE_REQUIREMENTS={'万里碧海':{'Gold':18880000,'Item':{'万里碧海（万）':1,'万里碧海（里）':1,'万里碧海（碧）':1,'万里碧海（海）':1},},
			'九宫云雾':{'Gold':18880000,'Item':{'九宫云雾（九）':1,'九宫云雾（宫）':1,'九宫云雾（云）':1,'九宫云雾（雾）':1},},
			'黑天暗云':{'Gold':18880000,'Item':{'黑天暗云（黑）':1,'黑天暗云（天）':1,'黑天暗云（暗）':1,'黑天暗云（云）':1},},
			'血花落照':{'Gold':18880000,'Item':{'血花落照（血）':1,'血花落照（花）':1,'血花落照（落）':1,'血花落照（照）':1},},
			'破血魔镜':{'Gold':18880000,'Item':{'破血魔镜（破）':1,'破血魔镜（血）':1,'破血魔镜（魔）':1,'破血魔镜（镜）':1},}}

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	say = ''
	
	if (Menu == 1):
		say = """在玛法大陆，相传一位北方的勇士利用魔剑的强大力量打败了魔族，把我们民族从危机中拯救了出来。
		但他被魔剑的力量引诱住，走火入魔了，失去了同族爱和正义
		感，变成了怪物。我们的祖先大法老们竭尽全力打败了他，把
		他封印在地下深处，然后把项链的4个眼挖出来，各一分为四，
		藏到了16个方向。
		霸群大怪利用强大的魔力吸附住4个眼睛的碎片，变成了自
		己身体的一部分。
		
		[关闭:0]"""
	elif (Menu == 2):
		say = """诺玛统领陀大怪利用霸群大怪的力量搜集到了项链的碎片。打败陀大怪的话，或许能得到部分项链碎片。
		项链碎片共有16片，搜集每条项链的4个碎片，便可得到4条项
		链万里碧海、九宫云雾、黑天暗云、血花落照。
		把项链碎片搜集过来交给我，我会利用我们诺玛族代代相传的
		秘传解除项链里的籀文，那么项链就会恢复到原来的状态。
		
		[制作项链:21]
		
		[关闭:0]"""
	elif (Menu == 21):
		say = """真棒！终于凑齐了项链的碎片。你想制造什么样的项链？我只收你材料费1888万。
		
		[血花落照:211]
		[黑天暗云:212]
		[九宫云雾:213]
		[万里碧海:214]"""
	elif(Menu == 211):
		say = Refine(Sender,'血花落照')
	elif(Menu == 212):
		say = Refine(Sender,'黑天暗云')
	elif(Menu == 213):
		say = Refine(Sender,'九宫云雾')
	elif(Menu == 214):
		say = Refine(Sender,'万里碧海')
	elif (Menu == 3):
		say = """您想打开毁灭之印的秘密吗？
		
		[关闭:0]"""
	elif (Menu == 4):
		say = """相传古时候的诺玛大法老们为了防止魔剑被魔族或者心怀不轨之徒拿到，在那把剑上面下了强力的咒语。
		
		[继续:41]"""
	elif (Menu == 41):
		say = """实际上，若想解开咒语的话需要另外一个东西。
		那东西就是一个叫做<font color=\"0xff00ff00\">毁灭之印</font>的东西。 <font color=\"0xff00ff00\">毁灭之印</font>是一个拥有强大魔法的高级法器，只能由大祭祀长代代相传，现在应该在那个篡权为教主之前担任大祭祀长位置的诺玛统领手里。
		
		[继续:42]"""
	elif (Menu == 42):
		say = """（难道说毁灭之印也在那家伙手中吗？）
		
		[这么说来，若想获得毁灭之印，就一定要先打败诺玛统领了？:43]"""
	elif (Menu == 43):
		say = """嗯，想得到毁灭之印，也并不非得要去诺玛城。
		毁灭之印是个很重要的东西，诺玛统领是不会轻易地将那东西
		带出城的，这很清楚。但是，即使是诺玛统领，有时候也不得
		阻止毁灭之印到外面去。
		我们诺玛族，自古以来就是拥有着虔诚信仰的民族，会定期举
		办宗教活动或者是仪式。在这样的活动中，成为核心内容的，
		就是那个毁灭之印。
		
		[继续:44]"""
	elif (Menu == 44):
		say = """即使诺玛统领是凭借邪恶的力量来篡夺大族长位置的凶暴之徒
		，但还是无法违反我们强大的传统。在他掌权之后，宗教活动
		也在继续。无法离开诺玛城的诺玛统领在每次活动的时候，也
		只好将毁灭之印送往仪式场所。
		
		[继续:45]"""
	elif (Menu == 45):
		if Sender.Level >= 48 and (PlayerGetV(Sender,BV_NQ_NMKILL)==0) and Sender.GetItemCount("勇士的证明") > 0: #(PlayerGetV(Sender,BV_NQ_SJKILL)==5015) and 
			Sender.TakeItem("勇士的证明",1)
			PlayerSetV(Sender,BV_NQ_NMKILL,10000)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """嗯，不久后会有一个很大的宗教活动。但估计毁灭之印已经运
			到了祭祀场所，所以还是等待下次机会会比较好。
			那应该是在星期二夜间的什么时候，如果你想知道详细的信息
			的话，你就在<font color=\"0xff00ff00\">星期一晚上7点到10点之间</font>来找我吧。我会
			打听他们的动向，给你提供一些有用的信息的。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 5):
		say = """呵呵，我说了失礼的话呢。若早就知道你是这么一个勇猛的
		人，我也不会试图多费唇舌去说服你了。
		好的！那我就帮助你去获得你想要的物品吧！
		但是，这之前有件事情你要铭记在心。每个人都有天命一说
		，世间的事情，都有合适去做和不合适去做的时候。据我分
		析天象，解除咒语的最佳时机是在阳衰阴盛的最高峰时间，
		也就是在<font color=\"0xff00ff00\">星期一夜晚11点到0点之间</font>。
		
		[继续:51]"""
	elif (Menu == 51):
		say = """你必须要在星期一的夜晚11点到午夜之间得到毁灭之印，若是错过了这个时机，天象就会发声变化，你也只好等到下一个合适的时候。
		
		[我明白。请告诉我毁灭之印运送的路径。我不想浪费时间了。:52]"""
	elif (Menu == 52):
		say = """毁灭之印是个十分重要的东西，因此运送的路线是极端机密
		的，除了几个大法老之外无人知晓。但是，在我流亡此地之
		前得到的消息，那条路径一般是在<font color=\"0xff00ff00\">诺玛峡谷的四处地点中的</font>
		<font color=\"0xff00ff00\">一处</font>那个时间是在<font color=\"0xff00ff00\">星期一夜晚11点钟</font>。
		究竟会选择哪个道路，是每次随机决定的，因此最好去打听
		他们的移动路线来进行埋伏。刚才也说了，护送的队伍是十
		分强大的，所以你不能有单枪匹马去争夺的想法，一定要<font color=\"0xff00ff00\">进</font>
		<font color=\"0xff00ff00\">行充分的准备并集结同伴</font>后前往。
		那四个地点就是<font color=\"0xff00ff00\">诺玛峡谷中距离49:54的地点。</font>
		
		[继续:53]"""
	elif (Menu == 53):
		if(PlayerGetV(Sender,BV_NQ_NMKILL)==10000):
			PlayerSetV(Sender,BV_NQ_NMKILL,10001)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """一定要做好万全的准备，也希望你能够取得成功。还有，不
			要让此事连累的无辜的人，也不要让诺玛统领或者沃尔阁知
			道，消息是从我这里传出去的。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 6):
		say = """嗯？真的是阿龙怪来阻止你吗？
		好奇怪啊。阿龙怪应该不会护送假的搬运队伍的... 那家伙
		如果想阻止你，应该不会很容易就放过你的。究竟那时候是
		怎样一个情形？
		
		[叙述遇见阿龙怪时的状况。:61]"""
	elif (Menu == 61):
		say = """... 居然有这种事情啊，会是怎么回事呢？
		阿龙怪很少会到诺玛城周围去巡视，你应该是不巧跟他碰见
		的吧。
		
		[继续:62]"""
	elif (Menu == 62):
		say = """呵呵，错过了一次难得的机会啊。。
		
		[没有其他办法来寻找吗？比如等毁灭之印下次搬运的机会？:63]"""
	elif (Menu == 63):
		say = """很不幸，埋伏在毁灭之印搬运的另外一条道路上来袭击的成
		功可能性几乎没有。由于此次事件，他们肯定会改变运送路
		径的。并且不管是真的还是假的护送队伍，肯定会伴随有很
		强大的护卫兵力，不会像这次这么容易地打退他们的。
		干脆去打听保管毁灭之印的秘密所在，潜入该地偷出来，可行一些。
		
		[保管毁灭之印的秘密场所是哪里？:64]"""
	elif (Menu == 64):
		if(PlayerGetV(Sender,BV_NQ_NMKILL)==10003):
			PlayerSetV(Sender,BV_NQ_NMKILL,10004)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """我也不知道确切的信息。关于此事我会进行调查的，你在<font color=\"0xff00ff00\">星</font>
			<font color=\"0xff00ff00\">期二晚上19点至22点之间</font>来找我吧。一定要记住，来打听情
			报就要准时，不然的话就会错过袭击秘密场所的时间的。你
			要铭记。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 7):
		say = """嗯，这是个护身符项链啊... 等等！这不是个寻常的项链。
		
		你究竟是从什么地方得到的？
		
		<font color=\"0xffffff00\">我也不太清楚。在和阿龙怪进行战斗后，就在那周围拣到了这东西。</font>
		[或许，这东西跟毁灭之印有关系吗？:71]"""
	elif (Menu == 71):
		say = """哦，说实话，这东西跟毁灭之印没有关系。但是，这明明是
		叫做扎马尔勇士的东西。但扎马尔是在沙漠区域死亡的呀？
		为什么这东西会在诺玛城那里呢？真是令人费解。
		
		[那个叫做扎马尔的人到底是谁？您为什么这么关心呢？:72]"""
	elif (Menu == 72):
		say = """扎马尔是我们诺玛族最高的勇士。他是我们大祭祀长的护卫
		武士，是拥有高超武艺的人。但是，就是这么一个人，在沙
		漠离奇地死亡了！那时候他所护卫的大祭祀长和很多法老们
		都死了，我们的宗教体系也遭受了剧烈的振荡。虽然有点羞
		于启齿，在那场权力斗争中，很多有望成为祭祀官的法老们
		相互消耗并消失了。
		
		[继续:73]"""
	elif (Menu == 73):
		say = """现在的诺玛统领就是利用那时的混乱在宗教领域中确立了自己的稳固地位，并以此为基础，篡取了大族长的位置，最后到了自称诺玛统领的地步。
		若是大祭祀长没有遭受横死，扎马尔也健在的话，即使诺玛
		统领拥有再大的本领，也没有可能那么容易篡夺所有权力的
		。若说大祭祀长是我们的精神支柱，那么扎马尔就是支撑这
		个支柱的坚实底座。
		
		[继续:74]"""
	elif (Menu == 74):
		say = """但是，事实上这两个人都在西部沙漠遭受了横死，我们也陷
		入了巨大的混乱之中。并且，那时候散落在事发地点周围的
		兵器和脚印都是人类的，我们当时就想，杀害大祭祀长一行
		人的有可能就是比奇人。
		诺玛统领就诱导了这种怀疑，在民众之中掀起了对比奇人的
		仇恨。虽然现在已经清楚了那些是诺玛统领的手段，但是，
		那时候为什么会有人类的痕迹，现在也是想不明白。
		
		[难到您现在还认为比奇人跟那件事情有牵连吗？:75]"""
	elif (Menu == 75):
		say = """嗯，虽说比奇人没有直接介入那个事件，但是那时候留在该
		处的，确确实实就是人类的痕迹。
		嗯，又让你白跑一趟了，真的对不起啊。我会帮你收集有关
		毁灭之印的其他信息，你可以答应我一个请求吗？
		
		[您要我做什么事情？:76]"""
	elif (Menu == 76):
		say = """我想拜托你去查一下，为什么据称被比奇人杀死了的扎马尔
		的项链会在诺玛统领的心腹阿龙怪的身上？
		当时的遗物们都是交给了死者的遗族们的，没有家庭的扎马
		尔的遗物，是由法老们暂时保管后送给他亲友拉贝卡的。我
		记得当时的遗物中就已经没有这个项链了。嗯，也有可能是
		我没有记清楚那时候的事情。
		所以我想请你去见当时接受遗物的拉贝卡，去调查一下那件
		事。通过他，有可能得到很多我不曾知道的事情。
		
		[那么，在哪里可以遇见那个叫做拉贝卡的人呢？:77]"""
	elif (Menu == 77):
		say = """拉贝卡现在在诺玛统领手下当一名侦察队长。唉，想安静的
		找他说话不会是件容易的事情。他是个十分外向和固执的人
		，并且对人类有很深的偏见。若是条件允许的话，应该是我
		直接去找他来问的，只是，我现在也只是个流亡之身 。。
		唉。
		也没有办法将他叫到这里来，只有在他巡视诺玛城的时候跟
		她碰头吧。
		当然，这是件非常危险的事情，我也不想强人所难。请仔细
		考虑一下，然后决定究竟可不可以帮我这个忙吧。
		
		[同意帮忙。:78]
		[拒绝帮忙。:79]"""
	elif (Menu == 78):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10006):
			#PlayerSetV(Sender,BV_NQ_NMKILL,10007)
			MainQuestRewards(Sender,BV_NQ_NMKILL)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """重新考虑之后还是决定帮我的忙吗？
			那好，你能替我去见拉贝卡，调查那个尸骨项链的事情吗？
			那个人会穿着一件平凡的侦察队长的服装，想要认出他来不
			会很容易。将出现的<font color=\"0xff00ff00\">侦察队长</font>都抓起来讯问好了。若有结
			果的话，就在<font color=\"0xff00ff00\">星期四晚上7点到10点之前</font>过来告诉我吧。
			
			拉贝卡主要在<font color=\"0xff00ff00\">星期三晚上11点左右巡视诺玛峡谷</font>，他主要巡视
			的区域是<font color=\"0xff00ff00\">49:54附近</font>。在那附近埋伏并等待的话，就可以遇见
			拉贝卡了。
			他武功很强，想击倒他会很难。虽然我知道你的武功也是十分
			高强，但还是希望你能做好准备后前往。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 79):
		say = """也罢。本来就不是想强求的事情嘛。。不过，若是你改变想
		法的话，就来找我吧。
		
		[关闭:0]"""
	elif (Menu == 8):
		say = """嗯，如果你得到的信息都是真实的话，诺玛统领的计划远早于别人所猜想的时候就开始了。
		还有，帕斯卡啊。。果然那家伙也与此事有牵连啊。帕斯卡
		被放逐也不是无关的事情啊。。
		。。。虽然很无理，但是我想再拜托你一件事情。
		
		[这次又是什么事情？:81]"""
	elif (Menu == 81):
		say = """呵呵，不要板着脸嘛，这次不是叫你去和诺玛武将们进行战
		斗。我想拜托你去见一下<font color=\"0xff00ff00\">帕斯卡</font>。
		他被放逐，已经是好久以前的事情了，所以对他的行踪并不
		是很清楚。但是很久以前，好像听说过他曾在<font color=\"0xff00ff00\">绿洲村庄周围</font>
		徘徊。去搜寻一下绿洲村庄周围的话，有可能就能找到那家
		伙，但那是人类居住的地方，我不能随便接近。
		所以请你替我去查一下。或许<font color=\"0xff00ff00\">询问绿洲村庄的居民</font>的话，能
		够得到有用的信息也说不定啊。
		若是得到了有关那家伙的信息的话，请你在<font color=\"0xff00ff00\">星期五9点至9点</font>
		<font color=\"0xff00ff00\">半之间</font>来告诉我有关情况吧。记住，不要错过时间。
		
		[我明白了。但是...:82]"""
	elif (Menu == 82):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10008):
			PlayerSetV(Sender,BV_NQ_NMKILL,10009)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """嗯，有什么想进一步了解的吗？
			
			[啊，没有。我这就出发。:0]
			
			（好奇怪啊。。为什么大法老夏柯会对当时的事情这么执着呢？ 还有，为什么拉贝卡说不要太相信这个大法老呢？）"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 9):
		say = """这么说来，扎马尔的儿子果真就是阿龙怪吗? 真是造化弄人
		啊，誓死反对诺玛统领的父亲和正在效忠或许是杀害父亲的
		凶手的儿子... 呵呵呵。
		果然，诺玛统领制造这些过分的事情可真是有一手啊。
		但是，事件发生地周围的痕迹明明就是人类的啊。。
		跟人类进行着战争的诺玛统领不会与人类进行勾结的吧？或
		者有没有能够解答这个问题的信息呢？
		
		<font color=\"0xffffff00\">由于阿龙怪突然出现了，证人要急于转移，</font>
		[就没能知道进一步的信息。:91]"""
	elif (Menu == 91):
		say = """... 嗯。。这样啊。
		你需要的有关毁灭之印的信息我也正在收集之中。不久我就
		可以给你足够的信息了吧。因此，请你也多帮我一下吧。
		但是，我对当时的事件周围留有人类的痕迹，确实一直不能
		够释怀。若诺玛统领果真是真凶的话，为什么那地方留有人
		类的脚印呢？
		请你再去帕斯卡打听一下为什么那周围会留有人类的痕迹好
		吗？我想，那里面也一定有什么其他内幕的。哦，这是为了
		表示我的心意给你的东西。
		遇见帕斯卡的方法，你应该比我更清楚。你就再去找那个<font color=\"0xff00ff00\">安</font>
		<font color=\"0xff00ff00\">排了与帕斯卡的会面的人</font>不就行了吗？
		
		[继续:92]"""
	elif (Menu == 92):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10014):
			PlayerSetV(Sender,BV_NQ_NMKILL,10015)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """从帕斯卡那里得到的消息，请你立即回来告诉我。最晚要在
			<font color=\"0xff00ff00\">星期日11点</font>来找我。如果错过这个时间，所有的事情都会泡
			汤的。
			
			[关闭:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 10):
		say = """若想打破那个咒语，需要另外一个东西。
		那东西就是一个叫做<font color=\"0xff00ff00\">毁灭之印</font>的东西。<font color=\"0xff00ff00\">毁灭之印</font>是个拥有
		强大魔法的高级法器，只能由大祭祀长代代相传，现
		在应该在那个篡权为教主之前担任大祭祀长位置的诺
		玛统领手里。
		
		[继续:101]"""
	elif (Menu == 101):
		say = """（难道说毁灭之印也在那家伙手中吗？）
		
		<font color=\"0xffffff00\">这么说来，若想获得毁灭之印的话，</font>
		[就一定要先打败诺玛统领了？:102]"""
	elif (Menu == 102):
		say = """嗯，想得到毁灭之印，得去诺玛城。
		毁灭之印是个很重要的东西，诺玛统领是会不会轻易地将那
		东西带出城的，这很清楚。但是，即使是诺玛统领，有时候
		也不得阻止毁灭之印到外面去。
		我们诺玛族，自古以来就是拥有着虔诚信仰的民族，会定期
		举办宗教活动或者是仪式。在这样的活动中，成为核心内容
		的，就是那个毁灭之印。若说角笛是大族长的象征，那毁灭
		之印就是大祭祀长的象征，在所有的宗教活动中，它是不可
		或缺的。
		
		[继续:103]"""
	elif (Menu == 103):
		if (PlayerGetV(Sender,BV_NQ_NMKILL)==10020):
			if (GetInventoryCount(Sender) >= 1):
				if Sender.Class == Sender.Class.Warrior: #战士
					Sender.GiveItemsByStat([{'name':'十方斩（残页）','bound':True,'count':80,},])
				elif Sender.Class == Sender.Class.Taoist: #道士
					Sender.GiveItemsByStat([{'name':'移花接玉（残页）','bound':True,'count':100,},])
				else:
					Sender.GiveItemsByStat([{'name':'魄冰刺（残页）','bound':True,'count':100,},])
				#PlayerSetV(Sender,BV_NQ_NMKILL,10021)
				MainQuestRewards(Sender,BV_NQ_NMKILL)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """嗯，不久后会有一个很大的宗教活动。但估计毁灭之印已经
				运到了祭祀场所，所以还是等待下次机会会比较好。
				我会打听他们的动向，给你提供一些有用的信息的。
				[关闭:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
		else:
			SEnvir.Log("-----------------------------------")
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("脚本报错：{} 诺玛任务序号不匹配".format(Sender.Character.CharacterName))
			SEnvir.Log("-----------------------------------")
	elif (Menu == 11):
		say = """飞龙剑需要集齐150个碎片，并花费888万金币，才能合成。
		
		[合成飞龙剑（火）:111]
		[合成飞龙剑（冰）:112]
		[合成飞龙剑（雷）:113]
		[合成飞龙剑（风）:114]
		[合成飞龙剑（神圣）:115]
		[合成飞龙剑（暗黑）:116]
		[合成飞龙剑（幻影）:117]"""
	elif (Menu == 111):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（火）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（火）",150)
				Sender.GiveItem("飞龙剑（火）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
	elif (Menu == 112):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（冰）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（冰）",150)
				Sender.GiveItem("飞龙剑（冰）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
	elif (Menu == 113):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（雷）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（雷）",150)
				Sender.GiveItem("飞龙剑（雷）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
	elif (Menu == 114):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（风）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（风）",150)
				Sender.GiveItem("飞龙剑（风）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
	elif (Menu == 115):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（神圣）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（神圣）",150)
				Sender.GiveItem("飞龙剑（神圣）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
	elif (Menu == 116):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（暗黑）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（暗黑）",150)
				Sender.GiveItem("飞龙剑（暗黑）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
	elif (Menu == 117):
		if (Sender.Gold < 8880000):
			say= """你没有足够的金币，无法合成。
			
			[关闭:0]"""
		elif(Sender.GetItemCount("飞龙剑碎片（幻影）") < 150):
			say ="""你没有足够的碎片，无法合成。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,8880000)
				Sender.TakeItem("飞龙剑碎片（幻影）",150)
				Sender.GiveItem("飞龙剑（幻影）",1)
				say="""祝贺你，合成成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法合成。
				
				[关闭:0]"""
#主菜单
	else:
		#完成神舰任务 并且 等级大于或等于48级 并且没接过任务
		if Sender.Level >= 48 and (PlayerGetV(Sender,BV_NQ_NMKILL)==0) and Sender.GetItemCount("勇士的证明") > 0: #(PlayerGetV(Sender,BV_NQ_SJKILL)==5015) and 
			say = """我是诺玛族正统的大法老。
			人类勇士,你要打听什么？
			
			[打听组合项链碎片的方法:2]
			[打听复活飞龙剑的方法:11]
			[跟夏柯进行对话:4]
			
			[关闭:0]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10000):
			say = """你来得正好。不久之后就会有个很隆重的宗教活动，为了举
			办那个活动，毁灭之印很快就会运到那里去的。如果能够成
			功地将毁灭之印从搬运队伍那里抢夺过来的话，就可以不用
			进入诺玛城就能得到毁灭之印的。如果袭击成功的话，就不
			用与诺玛统领或者阿龙怪对抗了。但是，搬运那东西的，也
			是一批最为厉害的诺玛武将，因此也不要掉以轻心。
			
			他们的力量十分强大，一个不好，非但得不到毁灭之印，还
			会付出自己的生命的。即使这样，你也要去争取<font color=\"0xff00ff00\">毁灭之印</font>吗
			？
			
			[是的。我已做好心里准备。现在临时改变想法，不是我的作风。:5]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10002) and Sender.GetItemCount("藏宝箱") > 0:
			Sender.TakeItem("藏宝箱",1)
			Sender.Connection.ReceiveChat("藏宝箱物品消失了。", MessageType.System)
			PlayerSetV(Sender,BV_NQ_NMKILL,10003)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """终于找来了毁灭之印了呀！因为施加在箱子上面的咒语没能
			打开箱子啊？
			我知道了。就由我来解开咒语吧，请你拿过来。
			
			<font color=\"0xffffff00\">大法老念了奇怪的咒语，箱子上面的诺玛文字们泛起光芒后消失了。</font>
			
			好了。但是好像这箱子里什么东西也没有啊。。
			
			[不可能吧？！抢夺箱子的时候，阿龙怪分明是全力阻止我的。:6]"""
		elif PlayerGetV(Sender,BV_NQ_NMKILL)==10003:
			say = """终于找来了毁灭之印了呀！因为施加在箱子上面的咒语没能
			打开箱子啊？
			我知道了。就由我来解开咒语吧，请你拿过来。
			
			好了。但是好像这箱子里什么东西也没有啊。。
			
			[不可能吧？！抢夺箱子的时候，阿龙怪分明是全力阻止我的。:6]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10004):
			PlayerSetV(Sender,BV_NQ_NMKILL,10005)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """实在很抱歉，我没能打听出来那个秘密场所的位置。
			但是，那个秘密场所肯定在诺玛峡谷的某个角落，我听到了
			<font color=\"0xff00ff00\">诺玛峡谷的诺玛大司令中的一个</font>知道关于此事的消息。
			若是太明显的话，那家伙可能找机会隐藏踪迹，因此必须要
			在<font color=\"0xff00ff00\">今天午夜之前</font>将那个家伙找出来。请你到诺玛峡谷去抓些
			<font color=\"0xff00ff00\">诺玛大司令们</font>，询问此事吧。嗯，如果觉得一个人干不来的话
			，就带上同伴们一起去吧。
			若是找到了那个家伙，得到了某些<font color=\"0xff00ff00\">能够成为线索的东西</font>的话
			，你在<font color=\"0xff00ff00\">星期三晚上19点至22点之间</font>来找我吧。"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10006) and Sender.GetItemCount("尸骨项链") > 0:
			say = """那好，找到了什么线索吗？
			
			[不知道能不能成为线索，但是我得到了这个东西。:7]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10008):
			say = """嗯，有什么打听到的消息吗？
			快告诉我。
			
			[我听到了这样的故事。:8]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10014):
			say = """啊，得到什么有用的信息了吗？
			
			[叙述其间听到的消息。:9]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10020):
			say = """看你询问毁灭之印的事情。古时候的诺玛大法老们为了防止魔剑被魔族或者心怀不轨之徒拿到，在那把剑上面下了强力的咒语。
			
			[继续:10]"""
		elif (PlayerGetV(Sender,BV_NQ_NMKILL)==10022) and Sender.GetItemCount("毁灭之印") > 0:
			Sender.TakeItem("毁灭之印",1)
			Sender.Connection.ReceiveChat("毁灭之印物品消失了。", MessageType.System)
			#PlayerSetV(Sender,BV_NQ_NMKILL,10023)
			MainQuestRewards(Sender,BV_NQ_NMKILL)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """以后你需要帮助的话，就尽管过来找我吧，我会尽力帮助你的。还有，这是我的一点心意，作为我的补偿，你就收下吧。
			像你这样既智慧又正直的人，一定能够达成心中的大志的。"""
		else:
			say = """我是诺玛族正统的大法老。
			人类勇士,你要打听什么？
			
			[打听组合项链碎片的方法:2]
			[打听复活飞龙剑的方法:11]
			
			[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def Refine(Sender,RefineName):
	requirements = REFINE_REQUIREMENTS[RefineName]

	if (Sender.Gold < requirements['Gold']):
			return """你还没准备齐全呢，需要200万的材料费。
			
			[关闭:0]"""
	if(requirements['Item']):
		for m,n in requirements['Item'].items():
			if (Sender.GetItemCount(m)<n):
				return """你还没准备齐全呢，需要对应的材料各一个。
				
				[关闭:0]"""
	if (requirements['Item']):
		for m,n in requirements['Item'].items():
			Sender.TakeItem(m,n)
		SubGold(Sender,requirements['Gold'])
		Sender.GiveItem(RefineName,1)
		return """用我们诺玛族的秘方，帮你修复 {} 项链。
		做好了……这可是珍宝啊。
		
		[关闭:0]""".format(RefineName)

NpcEvent.add_listener(370,"OnClick",OnClick)

