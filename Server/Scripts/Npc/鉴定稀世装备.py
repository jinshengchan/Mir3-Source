# -*- coding: utf-8 -*-
from Globals import *
import System
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Server.Models import ItemCheck


STONE_BY_TIER = {
	1: u"鉴定石一级",
	2: u"鉴定石二级",
	3: u"鉴定石三级",
	4: u"鉴定石四级",
	5: u"鉴定石五级",
}

IDENTIFY_MENU_BASE = 1000


def _get_inventory_item(sender, slot):
	if slot < 0 or slot >= sender.Inventory.Length:
		return None
	return sender.Inventory[slot]


def _get_inventory_count(sender, item_name):
	count = 0
	for item in sender.Inventory:
		if item is None or item.Info is None or item.Info.ItemName != item_name:
			continue
		count += int(item.Count)
	return count


def _get_preserved_flags(item):
	flags = getattr(UserItemFlags, "None")
	if (item.Flags & UserItemFlags.Bound) == UserItemFlags.Bound:
		flags |= UserItemFlags.Bound
	if (item.Flags & UserItemFlags.Worthless) == UserItemFlags.Worthless:
		flags |= UserItemFlags.Worthless
	return flags


def _get_unique_target_info(target_name):
	matches = [item for item in SEnvir.ItemInfoList.Binding if item.ItemName == target_name]
	if len(matches) != 1:
		return None

	target_info = SEnvir.GetItemInfo(target_name)
	if target_info is None or target_info.ItemName != target_name:
		return None
	if target_info.Rarity != Rarity.Elite:
		return None
	return matches[0]


def _give_item(sender, item_info, flags):
	check = ItemCheck(item_info, 1, flags, System.TimeSpan.Zero)
	if not sender.CanGainItems(False, check):
		return False
	item = SEnvir.CreateFreshItem(check)
	sender.GainItem(item)
	return True


def _build_item_menu(sender):
	links = []
	for slot in range(sender.Inventory.Length):
		item = sender.Inventory[slot]
		if item is None or item.Info is None:
			continue
		name = item.Info.ItemName
		if not name.startswith(u"未鉴定"):
			continue
		try:
			tier = int(item.Info.RequiredAmount)
		except:
			continue
		if tier not in STONE_BY_TIER:
			continue
		links.append(u"[{}（{}）:{}]".format(name, STONE_BY_TIER[tier], IDENTIFY_MENU_BASE + slot))

	if not links:
		return u"你的背包里没有可鉴定装备。\n\n[离开:0]"
	return u"请选择要鉴定的装备：\n\n{}\n\n[离开:0]".format(u"\n".join(links))


def _identify(sender, slot):
	source_item = _get_inventory_item(sender, slot)
	if source_item is None or source_item.Info is None or int(source_item.Count) < 1:
		return u"该位置已经没有装备。\n\n[返回:99]"

	source_name = source_item.Info.ItemName
	if not source_name.startswith(u"未鉴定"):
		return u"该物品不是未鉴定装备。\n\n[返回:99]"

	try:
		tier = int(source_item.Info.RequiredAmount)
	except:
		return u"该装备的鉴定等级无效。\n\n[返回:99]"
	if tier not in STONE_BY_TIER:
		return u"该装备的鉴定等级无效。\n\n[返回:99]"

	target_name = source_name[len(u"未鉴定"):]
	if not target_name:
		return u"找不到对应的稀世成品，请联系管理员。\n\n[返回:99]"
	target_info = _get_unique_target_info(target_name)
	if target_info is None:
		return u"找不到对应的稀世成品，请联系管理员。\n\n[返回:99]"

	stone_name = STONE_BY_TIER[tier]
	stone_info = SEnvir.GetItemInfo(stone_name)
	if stone_info is None:
		return u"找不到对应的鉴定石，请联系管理员。\n\n[返回:99]"
	if _get_inventory_count(sender, stone_name) < 1:
		return u"缺少{}。\n\n[返回:99]".format(stone_name)

	if not _give_item(sender, target_info, _get_preserved_flags(source_item)):
		return u"背包空间不足，鉴定未执行。\n\n[返回:99]"

	sender.TakeItem(source_item, 1)
	sender.TakeItem(stone_name, 1)
	return u"鉴定成功，获得{}。\n\n[继续鉴定:99]\n[离开:0]".format(target_name)


def OnClick(args):
	sender = args[1]
	menu = args[2]
	if menu >= IDENTIFY_MENU_BASE and menu < IDENTIFY_MENU_BASE + sender.Inventory.Length:
		say = _identify(sender, menu - IDENTIFY_MENU_BASE)
	else:
		say = _build_item_menu(sender)

	result = {}
	result['Say'] = say
	return result


NpcEvent.add_listener(215, "OnClick", OnClick)
