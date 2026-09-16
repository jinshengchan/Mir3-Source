# -*- coding: utf-8 -*-
from Globals import *
from Defines import *
import clr
import NpcEvent
import Utils
import Server.Envir.SEnvir as SEnvir

clr.AddReference("Library")
clr.AddReference('System')
from Library import *

GUMU3_MAP = 1643
SWITCH_NPCS = [400,401,402,403]
WAVE_MONSTERS = [100653,100654,100655,100656,100657,100658,100659]
MIDDLE_BOSS = 100660
STONE_NPC = 404
CENTER_REGION = 44988
BOSS_REGION = 56595
RESET_SECONDS = 300
SPAWN_RANGE = 5

ActivatedSwitches = set()
MiddleBossSpawned = False
StoneActive = False


def _InGumu3(Sender):
	return Sender is not None and Sender.CurrentMap is not None and Sender.CurrentMap.Info.Index == GUMU3_MAP


def _GetRegion(index):
	for region in SEnvir.MapRegionList.Binding:
		if region.Index == index:
			return region
	return None


def _CreateAtRegion(target_map, region_index, monster_index, count):
	region = _GetRegion(region_index)
	if target_map is None or region is None or region.PointList is None or region.PointList.Count == 0:
		return False

	point = region.PointList[SEnvir.Random.Next(region.PointList.Count)]
	target_map.CreateMon(point.X, point.Y, SPAWN_RANGE, monster_index, count)
	return True


def _SpawnMiddleBoss():
	global MiddleBossSpawned
	if MiddleBossSpawned:
		return

	target_map = SEnvir.GetMap(GUMU3_MAP)
	if target_map is None:
		return

	MiddleBossSpawned = True
	if not _CreateAtRegion(target_map, CENTER_REGION, MIDDLE_BOSS, 1):
		# 中央区域缺失时使用当前地图中央坐标，避免机关完成后没有中BOSS
		target_map.CreateMon(202,199,2,MIDDLE_BOSS,1)


def _ActivateSwitch(Self, Sender):
	if not _InGumu3(Sender):
		return

	npc_index = Self.NPCInfo.Index
	if npc_index not in SWITCH_NPCS:
		return

	if StoneActive or MiddleBossSpawned:
		Sender.Connection.ReceiveChat("本轮古墓3层机关已经完成，请等待石像机关重置。", MessageType.System)
		return

	if npc_index in ActivatedSwitches:
		Sender.Connection.ReceiveChat("这个机关已经开启。", MessageType.System)
		return

	target_map = SEnvir.GetMap(GUMU3_MAP)
	if target_map is None:
		Sender.Connection.ReceiveChat("古墓3层地图尚未准备好。", MessageType.System)
		return

	ActivatedSwitches.add(npc_index)
	SEnvir.ToggleNpcVisibility(npc_index, False)
	for monster_index in WAVE_MONSTERS:
		target_map.CreateMon(Self.CurrentLocation.X, Self.CurrentLocation.Y, SPAWN_RANGE, monster_index, 1)

	Utils.ServerUtils.SendMsgToMapOneArg([GUMU3_MAP, "古墓3层机关已开启，每种怪物刷新1只。", MessageType.System])
	if len(ActivatedSwitches) == len(SWITCH_NPCS):
		_SpawnMiddleBoss()
		Utils.ServerUtils.SendMsgToMapOneArg([GUMU3_MAP, "四个机关全部开启，中间房出现了中BOSS。", MessageType.System])


def OnSwitchClick(args):
	Self = args[0]
	Sender = args[1]
	_ActivateSwitch(Self, Sender)


def ShowGumu3Stone():
	global StoneActive
	if StoneActive or not MiddleBossSpawned:
		return

	StoneActive = True
	SEnvir.ToggleNpcVisibility(STONE_NPC, True)
	npc = SEnvir.GetNpcObject(STONE_NPC)
	if npc is not None:
		SEnvir.AddEffect(npc.ObjectID, Effect.Repulsion)

	Utils.ServerUtils.SendMsgToMapOneArg([GUMU3_MAP, "中BOSS已被击败，中央召唤阵出现了石像，点击石像可前往古墓4层。", MessageType.System])
	SEnvir.ScheduledCall("Map.古墓3重置NPC.ResetGumu3", SEnvir.Now.AddSeconds(RESET_SECONDS), 'dont_care')


def OnStoneClick(args):
	Sender = args[1]
	if not _InGumu3(Sender):
		return

	if not StoneActive:
		Sender.Connection.ReceiveChat("石像尚未开启。", MessageType.System)
		return

	region = _GetRegion(BOSS_REGION)
	if region is None:
		Sender.Connection.ReceiveChat("古墓4层大BOSS区域不存在。", MessageType.System)
		return

	if not Sender.Teleport(region):
		Sender.Connection.ReceiveChat("当前无法传送到古墓4层大BOSS区域。", MessageType.System)


def ResetGumu3(dont_care):
	global ActivatedSwitches, MiddleBossSpawned, StoneActive

	for npc_index in SWITCH_NPCS:
		SEnvir.ToggleNpcVisibility(npc_index, True)
	SEnvir.ToggleNpcVisibility(STONE_NPC, False)

	npc = SEnvir.GetNpcObject(STONE_NPC)
	if npc is not None:
		SEnvir.RemoveEffects(npc.ObjectID)

	ActivatedSwitches = set()
	MiddleBossSpawned = False
	StoneActive = False
	Utils.ServerUtils.SendMsgToMapOneArg([GUMU3_MAP, "古墓3层的机关和石像恢复了原状。", MessageType.System])


# 404 在数据库中是古墓3层默认隐藏的石像 NPC
SEnvir.ToggleNpcVisibility(STONE_NPC, False)

NpcEvent.add_listener(400,"OnClick",OnSwitchClick)
NpcEvent.add_listener(401,"OnClick",OnSwitchClick)
NpcEvent.add_listener(402,"OnClick",OnSwitchClick)
NpcEvent.add_listener(403,"OnClick",OnSwitchClick)
NpcEvent.add_listener(404,"OnClick",OnStoneClick)

