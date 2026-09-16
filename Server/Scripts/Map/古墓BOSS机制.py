# -*- coding: utf-8 -*-
import MonsterEvent
import Server.Envir.SEnvir as SEnvir

from Library import *

GUMU4_MAP = 1644
BIG_BOSS = 100661
MIDDLE_BOSS = 100660
DOOR_IDS = [3251, 3252, 3253, 3254, 3255, 3256]
EXIT_MAP = 1576
EXIT_X = 41
EXIT_Y = 74
EVICT_DELAY_SECONDS = 300

PHASE_KEY = "Gumu4BossPhase"
CLEANUP_KEY = "Gumu4BossCleanup"
MIDDLE_MARKER = "Gumu4PhaseMiddle"

DIRECTIONS = [
	("7点", 30, 125, 3253, 3254),
	("11点", 33, 35, 3251, 3252),
	("2点", 120, 30, 3255, 3256),
]


def _IsGumu4Boss(monster):
	return monster is not None and monster.CurrentMap is not None and monster.CurrentMap.Info.Index == GUMU4_MAP


def _GetTemp(monster, key, default):
	try:
		return int(monster.TempVariables[key])
	except:
		monster.TempVariables[key] = default
		return default


def _SetTemp(monster, key, value):
	monster.TempVariables[key] = value


def _SetDoorState(state):
	for movement_index in DOOR_IDS:
		movement = SEnvir.GetMovementInfo(movement_index)
		if movement is not None:
			movement.ExtraInfo = state


def CloseGumuBossDoors():
	_SetDoorState("关闭")


def _SetDirectionDoors(direction, state):
	found = False
	for movement_index in direction[3:5]:
		movement = SEnvir.GetMovementInfo(movement_index)
		if movement is None:
			continue
		movement.ExtraInfo = state
		found = True
	return found


def _GetAlivePhaseMiddleBosses(target_map):
	count = 0
	for obj in list(target_map.Objects):
		try:
			if obj.MonsterInfo is None or obj.MonsterInfo.Index != MIDDLE_BOSS or obj.Dead:
				continue
			if _GetTemp(obj, MIDDLE_MARKER, 0) == 1:
				count += 1
		except:
			pass
	return count


def _DisableLegacyMiddleBossRespawns():
	for spawn in list(SEnvir.Spawns):
		try:
			if spawn.CurrentMap is None or spawn.CurrentMap.Info.Index != GUMU4_MAP:
				continue
			if spawn.Info is None or spawn.Info.Monster is None or spawn.Info.Monster.Index != MIDDLE_BOSS:
				continue
			# 地图4中BOSS只允许按血量阶段刷新，禁止数据库旧复活点自动补刷。
			spawn.Info.Count = 0
		except:
			pass


def _CleanupLegacyMiddleBosses(target_map):
	for obj in list(target_map.Objects):
		try:
			if obj.MonsterInfo is None or obj.MonsterInfo.Index != MIDDLE_BOSS or obj.Dead:
				continue
			if _GetTemp(obj, MIDDLE_MARKER, 0) == 1:
				continue
			if obj.SpawnInfo is not None:
				obj.SpawnInfo.AliveCount = max(0, obj.SpawnInfo.AliveCount - 1)
				obj.SpawnInfo = None
			obj.Despawn()
		except:
			pass


def _GetTargetPhase(monster):
	health = float(monster.Stats[Stat.Health])
	if health <= 0:
		return 0

	hp_lost_percent = (health - float(monster.CurrentHP)) * 100.0 / health
	if hp_lost_percent >= 80:
		return 3
	if hp_lost_percent >= 60:
		return 2
	if hp_lost_percent >= 40:
		return 1
	return 0


def _SpawnPhaseMiddleBoss(monster, direction):
	created = monster.CurrentMap.CreateMon(direction[1], direction[2], 2, MIDDLE_BOSS, 1)
	if created is None or len(created) == 0:
		return False

	for middle in created:
		_SetTemp(middle, MIDDLE_MARKER, 1)
	return True


def _StartNextPhase(monster, phase):
	if phase < 1 or phase > len(DIRECTIONS):
		return False
	direction = DIRECTIONS[phase - 1]
	if not _SpawnPhaseMiddleBoss(monster, direction):
		return False

	_SetDirectionDoors(direction, "开启")
	_SetTemp(monster, PHASE_KEY, phase)
	monster.CurrentMap.MapMsg("古墓土偶护卫武士已刷新在：{}".format(direction[0]), MessageType.Hint)
	return True


def _DisableLegacyBossPhaseFlags(monster):
	try:
		# 阻止旧C# AI按旧编号389和旧门点重复处理，统一由本脚本接管。
		monster.CanFirstInvincibility = False
		monster.CanSecondInvincibility = False
		monster.CanThirdInvincibility = False
	except:
		pass


def _ProcessPhase(monster):
	phase = _GetTemp(monster, PHASE_KEY, 0)
	target_phase = _GetTargetPhase(monster)
	if target_phase > phase and _GetAlivePhaseMiddleBosses(monster.CurrentMap) == 0:
		_StartNextPhase(monster, phase + 1)


def ApplyGumuBossInvincibility(monster):
	if not _IsGumu4Boss(monster) or monster.Dead:
		return

	if _GetAlivePhaseMiddleBosses(monster.CurrentMap) > 0:
		monster.Stats[Stat.Invincibility] = 1
	else:
		monster.Stats[Stat.Invincibility] = 0


def EvictGumu4Players(args):
	tomb_map = SEnvir.GetMap(GUMU4_MAP)
	if tomb_map is None:
		return

	for player in list(tomb_map.Players):
		if player is None or player.CurrentMap is None:
			continue
		if player.CurrentMap.Info.Index != GUMU4_MAP:
			continue
		player.TeleportByMapIndex(EXIT_MAP, EXIT_X, EXIT_Y)


def OnProcessAI(args):
	monster = args[0]
	if not _IsGumu4Boss(monster) or monster.Dead:
		return

	_DisableLegacyBossPhaseFlags(monster)
	if _GetTemp(monster, CLEANUP_KEY, 0) == 0:
		_DisableLegacyMiddleBossRespawns()
		_CleanupLegacyMiddleBosses(monster.CurrentMap)
		_SetTemp(monster, CLEANUP_KEY, 1)

	_ProcessPhase(monster)
	# 旧C# AI在本回合后仍会按旧编号清一次无敌，延迟到本回合结束后校正。
	SEnvir.ScheduledCall("Map.古墓BOSS机制.ApplyGumuBossInvincibility", SEnvir.Now.AddMilliseconds(1), monster)


def OnKillGumuBoss(Sender, MonsterInfo):
	if MonsterInfo is None or MonsterInfo.Index != BIG_BOSS:
		return
	if Sender is None or Sender.CurrentMap is None or Sender.CurrentMap.Info.Index != GUMU4_MAP:
		return

	CloseGumuBossDoors()
	SEnvir.DelayCall("Map.古墓BOSS机制.EvictGumu4Players", EVICT_DELAY_SECONDS, ())


SEnvir.AddWatchingMonster(BIG_BOSS)
MonsterEvent.add_listener(BIG_BOSS, "OnProcessAI", OnProcessAI)
