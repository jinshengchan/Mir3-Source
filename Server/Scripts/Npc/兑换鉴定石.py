# -*- coding: utf-8 -*-
from Globals import *
import System
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Server.Models import ItemCheck


STONE_PURCHASES = {
	u"鉴定石一级": (1, 50),
	u"鉴定石二级": (2, 100),
	u"鉴定石三级": (3, 150),
	u"鉴定石四级": (4, 200),
	u"鉴定石五级": (5, 250),
}

PURCHASE_MENU = {
	101: u"鉴定石一级",
	102: u"鉴定石二级",
	103: u"鉴定石三级",
	104: u"鉴定石四级",
	105: u"鉴定石五级",
}

DECOMPOSE_TO = {
	u"鉴定石五级": u"鉴定石四级",
	u"鉴定石四级": u"鉴定石三级",
	u"鉴定石三级": u"鉴定石二级",
	u"鉴定石二级": u"鉴定石一级",
}

DECOMPOSE_MENU_BASE = 2000


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


def _give_item(sender, item_info, flags):
	check = ItemCheck(item_info, 1, flags, System.TimeSpan.Zero)
	if not sender.CanGainItems(False, check):
		return False
	item = SEnvir.CreateFreshItem(check)
	sender.GainItem(item)
	return True


def _build_main_menu():
	return u"""请选择服务：

[购买鉴定石一级:101]  高级碎片x1 + 元宝x50
[购买鉴定石二级:102]  高级碎片x2 + 元宝x100
[购买鉴定石三级:103]  高级碎片x3 + 元宝x150
[购买鉴定石四级:104]  高级碎片x4 + 元宝x200
[购买鉴定石五级:105]  高级碎片x5 + 元宝x250

[鉴定石分解:2]
[离开:0]"""


def _build_decompose_menu(sender):
	links = []
	for slot in range(sender.Inventory.Length):
		item = sender.Inventory[slot]
		if item is None or item.Info is None:
			continue
		source_name = item.Info.ItemName
		if source_name not in DECOMPOSE_TO:
			continue
		links.append(u"[{} → {}:{}]".format(source_name, DECOMPOSE_TO[source_name], DECOMPOSE_MENU_BASE + slot))

	if not links:
		return u"你的背包里没有可向下分解的鉴定石。\n\n[返回:0]"
	return u"每次按 1:1 向下分解一颗：\n\n{}\n\n[返回:0]".format(u"\n".join(links))


def _purchase(sender, stone_name):
	if stone_name not in STONE_PURCHASES:
		return u"无效的鉴定石。\n\n[返回:0]"

	fragment_count, game_gold = STONE_PURCHASES[stone_name]
	stone_info = SEnvir.GetItemInfo(stone_name)
	if stone_info is None:
		return u"找不到对应的鉴定石，请联系管理员。\n\n[返回:0]"
	if sender.GameGold < game_gold:
		return u"你的元宝不足。\n\n[返回:0]"
	if _get_inventory_count(sender, u"高级碎片") < fragment_count:
		return u"你的高级碎片不足。\n\n[返回:0]"

	if not sender.GiveItems({stone_name: 1}):
		return u"背包空间不足，兑换未执行。\n\n[返回:0]"

	SubGameGold(sender, game_gold)
	sender.TakeItem(u"高级碎片", fragment_count)
	return u"兑换成功，获得{}。\n\n[继续购买:1]\n[鉴定石分解:2]\n[离开:0]".format(stone_name)


def _decompose(sender, slot):
	source_item = _get_inventory_item(sender, slot)
	if source_item is None or source_item.Info is None or int(source_item.Count) < 1:
		return u"该位置已经没有鉴定石。\n\n[返回:2]"

	source_name = source_item.Info.ItemName
	if source_name not in DECOMPOSE_TO:
		return u"该物品不能向下分解。\n\n[返回:2]"

	target_name = DECOMPOSE_TO[source_name]
	target_info = SEnvir.GetItemInfo(target_name)
	if target_info is None:
		return u"找不到对应的低级鉴定石，请联系管理员。\n\n[返回:2]"

	if not _give_item(sender, target_info, _get_preserved_flags(source_item)):
		return u"背包空间不足，分解未执行。\n\n[返回:2]"

	sender.TakeItem(source_item, 1)
	return u"分解成功，获得{}。\n\n[继续分解:2]\n[返回:0]".format(target_name)


def OnClick(args):
	sender = args[1]
	menu = args[2]
	if menu == 2:
		say = _build_decompose_menu(sender)
	elif menu in PURCHASE_MENU:
		say = _purchase(sender, PURCHASE_MENU[menu])
	elif menu >= DECOMPOSE_MENU_BASE and menu < DECOMPOSE_MENU_BASE + sender.Inventory.Length:
		say = _decompose(sender, menu - DECOMPOSE_MENU_BASE)
	else:
		say = _build_main_menu()

	result = {}
	result['Say'] = say
	return result


NpcEvent.add_listener(216, "OnClick", OnClick)
