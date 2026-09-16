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
import Server
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
	
	say = ''

	if (Menu == 1):
		say = """这里有各类诺玛勋章，需要消耗10忠诚度，是否买个？
		
		[诺玛勋章（火）:11]    [诺玛勋章（雷）:12]    [诺玛勋章（风）:13]
		[诺玛勋章（防御）:14]  [诺玛勋章（魔御）:15]
		"""
	elif (Menu == 11):
		if (Sender.Character.RewardPoolCoin < 10):
			say = """你没有足够的忠诚度，无法购买。
			
			[离开:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				SEnvir.AdjustPersonalReward(Sender.Character,-10,CurrencySource.CashOutDeduct,"诺玛勋章脚本彩币扣除")
				Sender.GiveItem("诺玛勋章（火）",1)
				say="""购买成功。
				
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 12):
		if (Sender.Character.RewardPoolCoin < 10):
			say = """你没有足够的忠诚度，无法购买。
			
			[离开:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				SEnvir.AdjustPersonalReward(Sender.Character,-10,CurrencySource.CashOutDeduct,"诺玛勋章脚本彩币扣除")
				Sender.GiveItem("诺玛勋章（雷）",1)
				say="""购买成功。
				
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 13):
		if (Sender.Character.RewardPoolCoin < 10):
			say = """你没有足够的忠诚度，无法购买。
			
			[离开:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				SEnvir.AdjustPersonalReward(Sender.Character,-10,CurrencySource.CashOutDeduct,"诺玛勋章脚本彩币扣除")
				Sender.GiveItem("诺玛勋章（风）",1)
				say="""购买成功。
				
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 14):
		if (Sender.Character.RewardPoolCoin < 10):
			say = """你没有足够的忠诚度，无法购买。
			
			[离开:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				SEnvir.AdjustPersonalReward(Sender.Character,-10,CurrencySource.CashOutDeduct,"诺玛勋章脚本彩币扣除")
				Sender.GiveItem("诺玛勋章（防御）",1)
				say="""购买成功。
				
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 15):
		if (Sender.Character.RewardPoolCoin < 10):
			say = """你没有足够的忠诚度，无法购买。
			
			[离开:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
				SEnvir.AdjustPersonalReward(Sender.Character,-10,CurrencySource.CashOutDeduct,"诺玛勋章脚本彩币扣除")
				Sender.GiveItem("诺玛勋章（魔御）",1)
				say="""购买成功。
				
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 2):
		say = """花费大量的金币，可以百分百鉴定成功诺玛书籍，是否尝试下。
		
		[战士技能:41]   [法师技能:42]   [道士技能:43]
		
		[离开:0]"""
	elif (Menu == 41):
		say = """[铁布衫:21]        需要花费1288万金币
		[十方斩:22]        需要花费998万金币
		[破血狂杀:23]      需要花费1688万金币
		[乾坤大挪移:24]    需要花费998万金币
		[斗转星移:25]      需要花费998万金币
		
		[离开:0]"""
	elif (Menu == 42):
		say = """[魄冰刺:26]        需要花费998万金币
		[怒神霹雳:27]      需要花费1288万金币
		[凝血离魂:28]      需要花费1688万金币
		[焰天火雨:29]      需要花费1288万金币
		
		[离开:0]"""
	elif (Menu == 43):
		say = """[云寂术:30]        需要花费998万金币
		[妙影无踪:31]      需要花费1688万金币
		[阴阳法环:32]      需要花费1688万金币
		[移花接玉:33]      需要花费998万金币
		
		[离开:0]"""
	elif (Menu == 21):
		say = """如果想学铁布衫，请支付12880000金币。
		想得到指教吗？
		
		[请写武功秘籍:211]
		[结束:0]
		"""
	elif (Menu == 211):
		#判断需要的金币
		if (Sender.Gold < 12880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("铁布衫") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,12880000)
			Sender.TakeItem("铁布衫",1)
			Sender.GiveItem("铁布衫（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 22):
		say = """如果想学十方斩，请支付9980000金币。
		想得到指教吗？
		
		[请写武功秘籍:221]
		[结束:0]
		"""
	elif (Menu == 221):
		#判断需要的金币	
		if (Sender.Gold < 9980000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("十方斩") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,9980000)
			Sender.TakeItem("十方斩",1)
			Sender.GiveItem("十方斩（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 23):
		say = """如果想学破血狂杀，请支付16880000金币。
		想得到指教吗？
		
		[请写武功秘籍:231]
		[结束:0]
		"""
	elif (Menu == 231):
		#判断需要的金币	
		if (Sender.Gold < 16880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("破血狂杀") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,16880000)
			Sender.TakeItem("破血狂杀",1)
			Sender.GiveItem("破血狂杀（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 24):
		say = """如果想学乾坤大挪移，请支付9980000金币。
		想得到指教吗？
		
		[请写武功秘籍:241]
		[结束:0]
		"""
	elif (Menu == 241):
		#判断需要的金币	
		if (Sender.Gold < 9980000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("乾坤大挪移") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,9980000)
			Sender.TakeItem("乾坤大挪移",1)
			Sender.GiveItem("乾坤大挪移（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 25):
		say = """如果想学斗转星移，请支付9980000金币。
		想得到指教吗？
		
		[请写武功秘籍:251]
		[结束:0]
		"""
	elif (Menu == 251):
		#判断需要的金币
		if (Sender.Gold < 9980000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("斗转星移") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,9980000)
			Sender.TakeItem("斗转星移",1)
			Sender.GiveItem("斗转星移（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""

	elif (Menu == 26):
		say = """如果想学魄冰刺，请支付9980000金币。
		想得到指教吗？
		
		[请写武功秘籍:261]
		[结束:0]
		"""
	elif (Menu == 261):
		#判断需要的金币	
		if (Sender.Gold < 9980000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("魄冰刺") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,9980000)
			Sender.TakeItem("魄冰刺",1)
			Sender.GiveItem("魄冰刺（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 27):
		say = """如果想学怒神霹雳，请支付12880000金币。
		想得到指教吗？
		
		[请写武功秘籍:271]
		[结束:0]
		"""
	elif (Menu == 271):
		#判断需要的金币	
		if (Sender.Gold < 12880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("怒神霹雳") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,12880000)
			Sender.TakeItem("怒神霹雳",1)
			Sender.GiveItem("怒神霹雳（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 28):
		say = """如果想学凝血离魂，请支付16880000金币。
		想得到指教吗？
		
		[请写武功秘籍:281]
		[结束:0]
		"""
	elif (Menu == 281):
		#判断需要的金币	
		if (Sender.Gold < 16880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("凝血离魂") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,16880000)
			Sender.TakeItem("凝血离魂",1)
			Sender.GiveItem("凝血离魂（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 29):
		say = """如果想学焰天火雨，请支付12880000金币。
		想得到指教吗？
		
		[请写武功秘籍:291]
		[结束:0]
		"""
	elif (Menu == 291):
		#判断需要的金币	
		if (Sender.Gold < 12880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("焰天火雨") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,12880000)
			Sender.TakeItem("焰天火雨",1)
			Sender.GiveItem("焰天火雨（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""

	elif (Menu == 30):
		say = """如果想学云寂术，请支付9980000金币。
		想得到指教吗？
		
		[请写武功秘籍:301]
		[结束:0]
		"""
	elif (Menu == 301):
		#判断需要的金币	
		if (Sender.Gold < 9980000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("云寂术") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,9980000)
			Sender.TakeItem("云寂术",1)
			Sender.GiveItem("云寂术（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 31):
		say = """如果想学妙影无踪，请支付16880000金币。
		想得到指教吗？
		
		[请写武功秘籍:311]
		[结束:0]
		"""
	elif (Menu == 311):
		#判断需要的金币	
		if (Sender.Gold < 16880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("妙影无踪") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,16880000)
			Sender.TakeItem("妙影无踪",1)
			Sender.GiveItem("妙影无踪（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 32):
		say = """如果想学阴阳法环，请支付16880000金币。
		想得到指教吗？
		
		[请写武功秘籍:321]
		[结束:0]
		"""
	elif (Menu == 321):
		#判断需要的金币	
		if (Sender.Gold < 16880000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("阴阳法环") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,16880000)
			Sender.TakeItem("阴阳法环",1)
			Sender.GiveItem("阴阳法环（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 33):
		say = """如果想学移花接玉，请支付9980000金币。
		想得到指教吗？
		
		[请写武功秘籍:331]
		[结束:0]
		"""
	elif (Menu == 331):
		#判断需要的金币	
		if (Sender.Gold < 9980000):
			say= """喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("移花接玉") < 1):
			say ="""请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGold(Sender,9980000)
			Sender.TakeItem("移花接玉",1)
			Sender.GiveItem("移花接玉（秘籍）",1)
			say = """还好成功了，下次请拿保存状态稍好的书来解释。
				
				[结束:0]
				"""
	elif (Menu == 5):
		say = """这里有各类特色称号，需要288万金币购买一个，
		单BUFF只能单玩家获得，时效一星期。
		是否买个？
		
		[幽灵船长:51]    [诺玛苦僧:52]    [撸牛博士:53]    [黑度烧客:54]
		[祖玛阁主:55]    [矿洞猎手:56]    [动物园长:57]
		[战天斗地（战士专用）:501]
		[道骨仙风（道士专用）:502]
		[法海无边（法师专用）:503]
		[傲视群雄（60级专用）:504]
		"""
	elif (Menu == 51):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF1) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(122)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF1,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 52):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF2) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(123)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF2,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 53):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF3) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(124)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF3,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 54):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF4) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(125)
			PlayerSetV(Sender,GV_PLYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF4,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 55):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF5) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(126)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF5,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 56):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF6) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(127)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF6,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 57):
		if (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF7) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(128)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF7,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 501):
		if Sender.Class != Sender.Class.Warrior:
			say = """你不是战士，无法购买。
			
			[结束:0]"""
		elif (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF8) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(129)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF8,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 502):
		if Sender.Class != Sender.Class.Taoist:
			say = """你不是道士，无法购买。
			
			[结束:0]"""
		elif (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF9) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(130)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF9,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 503):
		if Sender.Class != Sender.Class.Wizard:
			say = """你不是法师，无法购买。
			
			[结束:0]"""
		elif (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF10) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(131)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF10,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 504):
		if Sender.Level < 60:
			say = """你等级没有达到60级，无法购买。
			
			[结束:0]"""
		elif (Sender.Gold < 2880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_BUFFCOUNT) > 0):
			say = """你已经购买过BUFF，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_BUFF11) > 0):
			say = """你来晚一步，当前BUFF已被购买。
			
			[结束:0]"""
		else:
			SubGold(Sender,2880000)
			Sender.CustomBuffAdd(133)
			PlayerSetV(Sender,GV_PLAYER_BUFFCOUNT,1)
			GlobalSetV(GV_PLAYER_BUFF11,1)
			say = """恭喜你购买成功，获得特色称号。
			
			[结束:0]"""
	elif (Menu == 6):
		say = """武器幻化说明：
		幻化卷<font color=\"0xff00ff00\">消耗定量</font>幻化珠，幻化时效<font color=\"0xff00ff00\">1</font>个月，
		普通幻化卷<font color=\"0xff00ff00\">不限量</font>，高级幻化卷每种每月限量购买<font color=\"0xff00ff00\">3</font>个。
		
		[幻化珠兑换:61]     [重置幻化:64]
		
		[兑换普通幻化卷:62]
		
		[兑换高级幻化卷:63]"""
	elif (Menu == 61):
		say = """[8.8万金币兑换幻化珠:611]
		
		[技能残页兑换幻化珠:612]"""
	elif (Menu == 611):
		if (Sender.Gold < 88000):
			say= """你没有足够的金币，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,88000)
				Sender.GiveItem("幻化珠",1)
				say="""兑换成功，获得幻化珠。
				
				[继续兑换:611]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 612):
		say = """两张残页兑换一个幻化珠
		
		[凝血离魂（残页）:6121]  [阴阳法环（残页）:6122]  [破血狂杀（残页）:6123]
		[焰天火雨（残页）:6124]  [妙影无踪（残页）:6125]  [铁布衫（残页）:6126]
		[怒神霹雳（残页）:6127]  [魄冰刺（残页）:6128]    [云寂术（残页）:6129]
		[十方斩（残页）:61210]    [移花接玉（残页）:61211]  [斗转星移（残页）:61212]
		[乾坤大挪移（残页）:61213]"""
	elif (Menu == 6121):
		if(Sender.GetItemCount("凝血离魂（残页）") < 2):
			say= """你没有凝血离魂（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("凝血离魂（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6121]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6122):
		if(Sender.GetItemCount("阴阳法环（残页）") < 2):
			say= """你没有阴阳法环（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("阴阳法环（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6122]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6123):
		if(Sender.GetItemCount("破血狂杀（残页）") < 2):
			say= """你没有破血狂杀（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("破血狂杀（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6123]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6124):
		if(Sender.GetItemCount("焰天火雨（残页）") < 2):
			say= """你没有焰天火雨（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("焰天火雨（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6124]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6125):
		if(Sender.GetItemCount("妙影无踪（残页）") < 2):
			say= """你没有妙影无踪（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("妙影无踪（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6125]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6126):
		if(Sender.GetItemCount("铁布衫（残页）") < 2):
			say= """你没有铁布衫（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("铁布衫（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6126]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6127):
		if(Sender.GetItemCount("怒神霹雳（残页）") < 2):
			say= """你没有怒神霹雳（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("怒神霹雳（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6127]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6128):
		if(Sender.GetItemCount("魄冰刺（残页）") < 2):
			say= """你没有魄冰刺（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("魄冰刺（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6128]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 6129):
		if(Sender.GetItemCount("云寂术（残页）") < 2):
			say= """你没有云寂术（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("云寂术（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:6129]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 61210):
		if(Sender.GetItemCount("十方斩（残页）") < 2):
			say= """你没有十方斩（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("十方斩（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:61210]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 61211):
		if(Sender.GetItemCount("移花接玉（残页）") < 2):
			say= """你没有移花接玉（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("移花接玉（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:61211]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 61212):
		if(Sender.GetItemCount("斗转星移（残页）") < 2):
			say= """你没有斗转星移（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("斗转星移（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:61212]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 61213):
		if(Sender.GetItemCount("乾坤大挪移（残页）") < 2):
			say= """你没有乾坤大挪移（残页），无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("乾坤大挪移（残页）",2)
				Sender.GiveItem("幻化珠",1)
				say = """兑换成功。
				
				[继续兑换:61213]
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 62):
		say = """兑换价格:10个幻化珠
		
		[木剑幻化卷:621]      [青铜斧幻化卷:622]    [匕首幻化卷:623]
		[乌木剑幻化卷:624]    [铁剑幻化卷:625]      [半月幻化卷:626]"""
	elif (Menu == 621):
		if(Sender.GetItemCount("幻化珠") < 10):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",10)
				Sender.GiveItem("木剑幻化卷",1)
				say="""兑换成功，获得木剑幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 622):
		if(Sender.GetItemCount("幻化珠") < 10):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",10)
				Sender.GiveItem("青铜斧幻化卷",1)
				say="""兑换成功，获得青铜斧幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 623):
		if(Sender.GetItemCount("幻化珠") < 10):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",10)
				Sender.GiveItem("匕首幻化卷",1)
				say="""兑换成功，获得匕首幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 624):
		if(Sender.GetItemCount("幻化珠") < 10):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",10)
				Sender.GiveItem("乌木剑幻化卷",1)
				say="""兑换成功，获得乌木剑幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 625):
		if(Sender.GetItemCount("幻化珠") < 10):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",10)
				Sender.GiveItem("铁剑幻化卷",1)
				say="""兑换成功，获得铁剑幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 626):
		if(Sender.GetItemCount("幻化珠") < 10):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",10)
				Sender.GiveItem("半月幻化卷",1)
				say="""兑换成功，获得半月幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 63):
		say = """兑换限制:一种幻化卷每个月最多兑换3张
		
		兑换价格:38个幻化珠
		[霹雷幻化卷:631]      [嗜魂法杖幻化卷:632]    [龙纹剑幻化卷:633]
		
		兑换价格:48个幻化珠
		[屠龙幻化卷:634]      [铁轮幻化卷:635]        [逍遥扇幻化卷:636]
		
		兑换价格:58个幻化珠
		[破山剑幻化卷:637]    [天神法杖幻化卷:638]    [泰轮拂尘幻化卷:639]"""
	elif (Menu == 631):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN1) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 38):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",38)
				Sender.GiveItem("霹雷幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN1,GlobalGetV(GV_PLAER_HUANHUAJUAN1) + 1)
				say="""兑换成功，获得霹雷幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 632):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN2) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 38):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",38)
				Sender.GiveItem("嗜魂法杖幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN2,GlobalGetV(GV_PLAER_HUANHUAJUAN2) + 1)
				say="""兑换成功，获得嗜魂法杖幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 633):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN3) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 38):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",38)
				Sender.GiveItem("龙纹剑幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN3,GlobalGetV(GV_PLAER_HUANHUAJUAN3) + 1)
				say="""兑换成功，获得龙纹剑幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 634):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN4) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 48):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",48)
				Sender.GiveItem("屠龙幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN4,GlobalGetV(GV_PLAER_HUANHUAJUAN4) + 1)
				say="""兑换成功，获得屠龙幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 635):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN5) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 48):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",48)
				Sender.GiveItem("铁轮幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN5,GlobalGetV(GV_PLAER_HUANHUAJUAN5) + 1)
				say="""兑换成功，获得铁轮幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 636):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN6) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 48):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",48)
				Sender.GiveItem("逍遥扇幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN6,GlobalGetV(GV_PLAER_HUANHUAJUAN6) + 1)
				say="""兑换成功，获得逍遥扇幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 637):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN7) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 58):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",58)
				Sender.GiveItem("破山剑幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN7,GlobalGetV(GV_PLAER_HUANHUAJUAN7) + 1)
				say="""兑换成功，获得破山剑幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 638):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN8) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 58):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",58)
				Sender.GiveItem("天神法杖幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN8,GlobalGetV(GV_PLAER_HUANHUAJUAN8) + 1)
				say="""兑换成功，获得天神法杖幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 639):
		if (GlobalGetV(GV_PLAER_HUANHUAJUAN9) > 2):
			say = """你来晚一步，当前幻化卷已被购买一空。
			
			[结束:0]"""
		elif(Sender.GetItemCount("幻化珠") < 58):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",58)
				Sender.GiveItem("泰轮拂尘幻化卷",1)
				GlobalSetV(GV_PLAER_HUANHUAJUAN9,GlobalGetV(GV_PLAER_HUANHUAJUAN9) + 1)
				say="""兑换成功，获得泰轮拂尘幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 64):
		say = """你确定要重置已经幻化的武器吗？
		重置幻化武器收费<font color=\"0xff00ff00\">88万</font>金币。
		
		[确定重置:641]"""
	elif (Menu == 641):
		item = Sender.Equipment[int(EquipmentSlot.Weapon)]
		if (not (item)):
			say = """你没有装备武器。
			
			[结束:0]"""
		elif (item.Stats[Stat.Illusion] == 0):
			say = """你的武器没有幻化属性。
			
			[结束:0]"""
		elif (Sender.Gold < 880000):
			say= """你没有足够的金币。
			
			[结束:0]"""
		else:
			SubGold(Sender,880000)
			item.RemoveStat(Stat.Illusion, StatSource.Enhancement)
			Sender.SendShapeUpdate()
			#构建封包刷新武器
			itemStatsRefreshed  = System.Activator.CreateInstance(Network.ServerPackets.ItemStatsRefreshed)
			stats = System.Activator.CreateInstance(Stats,Sender.Equipment[0].Stats)
			itemStatsRefreshed.GridType = GridType.Equipment
			itemStatsRefreshed.Slot = 0 #装备框架位置序号
			itemStatsRefreshed.NewStats = stats
			itemStatsRefreshed.FullItemStats = Sender.Equipment[0].ToClientInfo().FullItemStats
			Sender.Enqueue(itemStatsRefreshed)
			say = """你的幻化武器重置成功。
			
			[结束:0]"""
	elif (Menu == 7):
		say = """坐骑幻化说明：
		对应<font color=\"0xff00ff00\">黑马坐骑</font>使用指定幻化卷，
		幻化卷消耗<font color=\"0xff00ff00\">888</font>幻化珠，幻化时效<font color=\"0xff00ff00\">永久</font>。
		
		[幻化珠兑换:61]
		
		[兑换烈焰幻化卷:71]
		[兑换赤兔幻化卷:74]"""
#[兑换追风幻化卷:72]
#[兑换雷霆幻化卷:73]
	elif (Menu == 71):
		if(Sender.GetItemCount("幻化珠") < 888):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",888)
				Sender.GiveItem("烈焰幻化卷",1)
				say="""兑换成功，获得烈焰幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 72):
		if(Sender.GetItemCount("幻化珠") < 888):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",888)
				Sender.GiveItem("追风幻化卷",1)
				say="""兑换成功，获得追风幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 73):
		if(Sender.GetItemCount("幻化珠") < 888):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",888)
				Sender.GiveItem("雷霆幻化卷",1)
				say="""兑换成功，获得雷霆幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 74):
		if(Sender.GetItemCount("幻化珠") < 888):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",888)
				Sender.GiveItem("赤兔幻化卷",1)
				say="""兑换成功，获得赤兔幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 8):
		if(Sender.GameGold < 1000):
			say = """你的赞助币不足，无法购买。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGameGold(Sender,10)
				Sender.GiveItem('净化水',30)
				say = """购买成功。
				
				[关闭:0]"""
			else:
				say = """你的包裹没有空间，无法购买。
				
				[关闭:0]"""
	elif (Menu == 9):
		say = """衣服幻化说明：
		幻化卷<font color=\"0xff00ff00\">消耗定量</font>幻化珠，幻化时效<font color=\"0xff00ff00\">1</font>个月，
		普通幻化卷<font color=\"0xff00ff00\">不限量</font>，高级幻化卷每种每月限量购买<font color=\"0xff00ff00\">3</font>个。
		
		[幻化珠兑换:61]     [重置幻化:94]
		
		[兑换普通幻化卷:92]"""
	elif (Menu == 92):
		say = """兑换价格:28个幻化珠
		
		[布衣幻化卷:921]        [轻型盔甲幻化卷:922]    [重盔甲幻化卷:923]
		[魔法长袍幻化卷:924]    [灵魂战衣幻化卷:925]"""
	elif (Menu == 921):
		if(Sender.GetItemCount("幻化珠") < 28):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",28)
				Sender.GiveItem("布衣幻化卷",1)
				say="""兑换成功，获得布衣幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 922):
		if(Sender.GetItemCount("幻化珠") < 28):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",28)
				Sender.GiveItem("轻型盔甲幻化卷",1)
				say="""兑换成功，获得轻型盔甲幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 923):
		if(Sender.GetItemCount("幻化珠") < 28):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",28)
				Sender.GiveItem("重盔甲幻化卷",1)
				say="""兑换成功，获得重盔甲幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 924):
		if(Sender.GetItemCount("幻化珠") < 28):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",28)
				Sender.GiveItem("魔法长袍幻化卷",1)
				say="""兑换成功，获得魔法长袍幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 925):
		if(Sender.GetItemCount("幻化珠") < 28):
			say= """你没有足够的幻化珠，无法兑换。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				Sender.TakeItem("幻化珠",28)
				Sender.GiveItem("灵魂战衣幻化卷",1)
				say="""兑换成功，获得灵魂战衣幻化卷。
				
				[结束:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[结束:0]"""
	elif (Menu == 94):
		say = """你确定要重置已经幻化的衣服吗？
		重置幻化衣服收费<font color=\"0xff00ff00\">88万</font>金币。
		
		[确定重置:941]"""
	elif (Menu == 941):
		item = Sender.Equipment[int(EquipmentSlot.Armour)]
		if (not (item)):
			say = """你没有装备衣服。
			
			[结束:0]"""
		elif (item.Stats[Stat.Illusion] == 0):
			say = """你的衣服没有幻化属性。
			
			[结束:0]"""
		elif (Sender.Gold < 880000):
			say= """你没有足够的金币。
			
			[结束:0]"""
		else:
			SubGold(Sender,880000)
			item.RemoveStat(Stat.Illusion, StatSource.Enhancement)
			Sender.SendShapeUpdate()
			#构建封包刷新衣服
			itemStatsRefreshed  = System.Activator.CreateInstance(Network.ServerPackets.ItemStatsRefreshed)
			stats = System.Activator.CreateInstance(Stats,Sender.Equipment[1].Stats)
			itemStatsRefreshed.GridType = GridType.Equipment
			itemStatsRefreshed.Slot = 1 #装备框架位置序号
			itemStatsRefreshed.NewStats = stats
			itemStatsRefreshed.FullItemStats = Sender.Equipment[1].ToClientInfo().FullItemStats
			Sender.Enqueue(itemStatsRefreshed)
			say = """你的幻化衣服重置成功。
			
			[结束:0]"""
	elif (Menu == 10):
		say = """特色新年时装限量供应:
		限购男女各<font color=\"0xff00ff00\">5</font>件，单人最多只能购买<font color=\"0xff00ff00\">1</font>次。
		每件价格<font color=\"0xff00ff00\">1288万</font>金币，限时<font color=\"0xff00ff00\">1</font>个月。
		
		[购买新春时装男款:101]  [购买新春时装女款:102]
		"""
	elif (Menu == 101):
		if (Sender.Gold < 12880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_XINNIANSZ) > 0):
			say = """你已经购买过新春时装，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_QJXINNIANSZN) > 4):
			say = """你来晚一步，当前新春时装已被抢购一空。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,12880000)
				Sender.GiveItem("新春时装（男）",1)
				PlayerSetV(Sender,GV_PLAYER_XINNIANSZ,1)
				GlobalSetV(GV_PLAYER_QJXINNIANSZN,GlobalGetV(GV_PLAYER_QJXINNIANSZN)+1)
				say = """恭喜你购买成功，获得新春时装。
				
				[结束:0]"""
			else:
				say = """你的包裹没有空间，无法购买。
				
				[结束:0]"""
	elif (Menu == 102):
		if (Sender.Gold < 12880000):
			say = """金币不足，无法购买。
			
			[结束:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_XINNIANSZ) > 0):
			say = """你已经购买过新春时装，无法重复购买。
			
			[结束:0]"""
		elif (GlobalGetV(GV_PLAYER_QJXINNIANSZV) > 4):
			say = """你来晚一步，当前新春时装已被抢购一空。
			
			[结束:0]"""
		else:
			if (GetInventoryCount(Sender) >= 1):
				SubGold(Sender,12880000)
				Sender.GiveItem("新春时装（女）",1)
				PlayerSetV(Sender,GV_PLAYER_XINNIANSZ,1)
				GlobalSetV(GV_PLAYER_QJXINNIANSZV,GlobalGetV(GV_PLAYER_QJXINNIANSZV)+1)
				say = """恭喜你购买成功，获得新春时装。
				
				[结束:0]"""
			else:
				say = """你的包裹没有空间，无法购买。
				
				[结束:0]"""
#主菜单
	else:
		say = """这里稀奇古怪的产品都有，欢迎光临。
		
		[诺玛勋章:1]      [诺玛书籍鉴定:2]
		
		[特色称号:5]      [武器幻化:6]
		
		[坐骑幻化:7]      [衣服幻化:9]
		
		[购买净化水:8]    [新春时装:10]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


NpcEvent.add_listener(351,"OnClick",OnClick)