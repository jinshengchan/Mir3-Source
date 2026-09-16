# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from datetime import datetime, timedelta
import datetime
import random

MONBOSSLIST = [
"诺玛骑兵55",
"诺玛司令55",
"诺玛抛石兵55",
"诺玛斧兵55",
"诺玛装甲兵55",
]

def RefreshMonster(dont_care):
	serverNow = SEnvir.Now.AddDays(1) # 获取服务器当前时间
	select = random.randint(0 , 23)
	select1 = random.randint(0 , 59)
	spawnTime = datetime.datetime(serverNow.Year, serverNow.Month, serverNow.Day, select, select1, 0)
	SEnvir.ScheduledCall("Mon.诺玛必爆怪.RefreshMonster", spawnTime, 0)

	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(362, selected, 1, 197, 184, 1000) #刷怪 地图名 怪物名 数量 X Y 范围
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(363, selected, 1, 196, 188, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(364, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(365, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(366, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(367, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(368, selected, 1, 205, 183, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(369, selected, 1, 166, 173, 1000)
	
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(362, selected, 1, 197, 184, 1000) #刷怪 地图名 怪物名 数量 X Y 范围
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(363, selected, 1, 196, 188, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(364, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(365, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(366, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(367, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(368, selected, 1, 205, 183, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(369, selected, 1, 166, 173, 1000)
	
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(362, selected, 1, 197, 184, 1000) #刷怪 地图名 怪物名 数量 X Y 范围
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(363, selected, 1, 196, 188, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(364, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(365, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(366, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(367, selected, 1, 198, 198, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(368, selected, 1, 205, 183, 1000)
	selected = random.choice(MONBOSSLIST)
	ServerUtils.SpawnMonsters(369, selected, 1, 166, 173, 1000)
	
	return