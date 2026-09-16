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
from Server.DBModels import *
from MirDB import *
import Server.Envir.SEnvir as SEnvir

EQUIPMENT_SLOTS = {'武器': 0, '衣服': 1, '头盔': 2, '火把': 3, '项链': 4, '左手镯': 5, '右手镯': 6, '左戒指': 7,
                   '右戒指': 8, '鞋子': 9, '毒': 10, '符': 11, '花': 12, '马甲': 13, '徽章': 14, '盾牌': 15, 
                   '声望称号': 16, '时装': 17, '自动药剂': 18}


def check_item_equipped(player, equip_type='', equip_name=''):

    if equip_type == '' and equip_name == '':
        raise Exception('At least one of equip_type and equip_name must be present')

    if equip_type == '':
        for _, value in EQUIPMENT_SLOTS.iteritems():
            checking_equip = player.Equipment[value]
            if checking_equip and checking_equip.Info.ItemName == equip_name:
                return True
    
    if equip_type not in EQUIPMENT_SLOTS.keys():
        raise Exception('Provided equip_type is illegal')

    if equip_name == '':
        if player.Equipment[EQUIPMENT_SLOTS[equip_type]]:
            return True
    
    if equip_type != '' and equip_name != '':
        checking_equip = player.Equipment[EQUIPMENT_SLOTS[equip_type]]
        if checking_equip and checking_equip.Info.ItemName == equip_name:
            return True
    
    return False


def deleteEquip(player, equip_type):
    player.RemoveEquippedItem(EQUIPMENT_SLOTS[equip_type])


def createThenPutOnEquipment(player, equip_name, equip_type):
    player.CreateThenPutOnItem(equip_name, EQUIPMENT_SLOTS[equip_type])

