# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import random

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir

clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)

# 不要改这个class
class PaoDianData():
    def __init__(self, CostType, Cost, RewardType, Reward, Interval):
        self.CostType = CostType
        self.Cost = Cost
        self.RewardType = RewardType
        self.Reward = Reward
        self.Interval = Interval

    def CheckCost(self, player):
    	if self.CostType == '金币':
    		if player.Gold >= self.Cost:
    			SubGold(player, self.Cost)
    			return True
    		return False
    	if self.CostType == '元宝':
    		if player.GameGold >= self.Cost:
    			SubGameGold(player, self.Cost)
    			return True
    		return False
    	return False

    def GiveReward(self, player):
    	if self.RewardType == '经验':
    		GiveExperience(player, self.Reward)
    		return
    	if self.RewardType == '金币':
    		GiveGold(player, self.Reward)
    		return
    	if self.RewardType == '元宝':
    		GiveGameGold(player, self.Reward)
    		return
    	if self.RewardType == '赏金':
    		GiveHuntGold(player, self.Reward)
    		return
    	if self.RewardType == '声望':
    		GivePrestige(player, self.Reward)
    		return
    	if self.RewardType == '贡献':
    		GiveContribute(player, self.Reward)
    		return



# 奖励表（自行修改）
# 可以扣除金币或者元宝
# 可以给 经验,金币,元宝,赏金,声望,荣誉
EXP_TABLE = {
	10: PaoDianData('金币', 0, '经验', 100, 60),                 # 1-10级    扣除0金币       100经验/60秒 
	21: PaoDianData('金币', 10000, '经验', 500, 300),               # 11-21级   扣除10000金币       500经验/300秒 
	29: PaoDianData('金币', 50000, '经验', 11000, 600),             # 22-29级  扣除50000金币       11000经验/600秒 
	34: PaoDianData('金币', 200000, '经验', 22000, 600),             # 30-34级  扣除200000金币       22000经验/600秒 
	39: PaoDianData('元宝', 100, '经验', 33000, 600),             # 35-39级  扣除100元宝       33000经验/600秒 
	44: PaoDianData('元宝', 200, '经验', 60000, 600),          # 40-44级  扣除200元宝    60000经验/600秒 
	47: PaoDianData('元宝', 200, '经验', 80000, 600),          # 45-47级  扣除200元宝    80000经验/600秒 
	51: PaoDianData('元宝', 200, '经验', 120000, 600),        # 48-51级  扣除200元宝   120000经验/600秒 
	57: PaoDianData('元宝', 500, '经验', 150000, 600),        # 52-57级  扣除500元宝   150000经验/600秒 
	64: PaoDianData('元宝', 500, '经验', 300000, 600),        # 58-64级  扣除500元宝   300000经验/600秒 
	70: PaoDianData('元宝', 500, '经验', 500000, 600),        # 65-70级  扣除500元宝   500000经验/600秒 
	75: PaoDianData('元宝', 500, '经验', 600000, 600),        # 71-75级  扣除500元宝   600000经验/600秒 
	80: PaoDianData('元宝', 500, '经验', 700000, 600),        # 76-80级  扣除500元宝   700000经验/600秒 
	999: PaoDianData('元宝', 500, '经验', 800000, 600),       # 81-999级 扣除500元宝   800000经验/600秒 
}
# 不要改这一行
EXP_TABLE = collections.OrderedDict(sorted(EXP_TABLE.items()))


# 允许泡点的地图index
# ALLOWED_MAPS = [] 为不限制地图
ALLOWED_MAPS = [1,6,7]


def StartPaoDian(player):
	for item in EXP_TABLE.items():
		if player.Level <= item[0]:
			data = item[1]
			player.Connection.ReceiveChat("已开启自动泡点，每{}秒扣除{}{}获得{}{}".format(data.Interval, data.Cost, data.CostType, data.Reward,data.RewardType), MessageType.System)
			SEnvir.PeriodicCall("Player.泡点.CheckPaoDian", SEnvir.Now.AddSeconds(data.Interval), data.Interval, [player, data], player)
			return


def CheckPaoDian(info):
	player = info[0]
	data = info[1]
	if not player or not data:
		return

	if player.CurrentMap.Info.Index not in ALLOWED_MAPS:
		StopPaoDian(player)
		player.Connection.ReceiveChat("不在指定地图, 自动泡点停止".format(data.CostType), MessageType.System)
		return

	if (player.Level >22) and (not player.InSafeZone):    #必须级别大于22级，不在安全区才会停止泡点
		StopPaoDian(player)
		player.Connection.ReceiveChat("不在安全区, 自动泡点停止".format(data.CostType), MessageType.System)
		return

	if data.CheckCost(player):
		data.GiveReward(player)
		player.Connection.ReceiveChat("自动泡点中...", MessageType.System)
	else:
		StopPaoDian(player)
		player.Connection.ReceiveChat("{}不足, 自动泡点停止".format(data.CostType), MessageType.System)



def StopPaoDian(player):
	if not player:
		return
	player.Connection.ReceiveChat("自动泡点停止", MessageType.System)
	SEnvir.RemoveScript("Player.泡点.CheckPaoDian", player)

