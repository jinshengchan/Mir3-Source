# -*- coding: utf-8 -*-
import Map.古墓3重置NPC as Gumu3


def OnKillGumuBoss1(Sender, MonsterInfo):
	if Sender is None or Sender.CurrentMap is None:
		return
	if Sender.CurrentMap.Info.Index != Gumu3.GUMU3_MAP:
		return
	if MonsterInfo is None or MonsterInfo.Index != Gumu3.MIDDLE_BOSS:
		return

	Gumu3.ShowGumu3Stone()
