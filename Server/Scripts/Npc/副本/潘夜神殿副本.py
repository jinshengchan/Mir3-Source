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
from Defines import *
from Defines import GV_PANYE_DUNGEON_COUNT
import random
import NpcEvent
from datetime import datetime, timedelta
import System
s1 = clr.Reference[System.Object]()
from Utils.TimeUtil import *
import Utils.ServerUtils as ServerUtils
from Utils import ServerUtils
from Npc import *
import Server.Envir.SEnvir as SEnvir



# 副本清理函数
def CloseFuben(args):
    """关闭副本"""
    map = args[0]
    if map is None:
        return
    
    # 清理副本
    if SEnvir.FubenMaps.Contains(map):
        SEnvir.CloseMap(map)
        SEnvir.FubenMaps.Remove(map)
    else:
        SEnvir.CloseMap(map)

def OnLeave(args):
    """玩家离开副本时调用"""
    map = args[0]
    player = args[1]
    
    if map is None or player is None:
        return
    
    # 检查副本内是否还有其他玩家
    if map.PlayerCount <= 1:  # 当前玩家还未完全离开，所以<=1表示没有其他玩家
        # 延迟3秒关闭副本，确保玩家完全离开
        SEnvir.DelayCall("Npc.潘夜岛.潘夜神殿副本.CloseFuben", 3, (map,))
    else:
        pass

# NPC事件监听器
def OnClick(args):
    Self = args[0]
    Sender = args[1]
    Menu = args[2]
    Links = args[3] if len(args) > 3 else None
    Dict = {}
    
    # 获取玩家当前副本进入次数
    current_count = PlayerGetV(Sender, GV_PANYE_DUNGEON_COUNT)
    max_count = 3  # 每日最大进入次数
    
    if Menu == 1:  # 进入副本
        # 检查玩家等级
        if Sender.Level < 40:
            Dict['Say'] = "你的等级不足40级，无法进入副本！\n\n[返回:0]"
            return Dict
        
        # 检查次数限制
        if current_count >= max_count:
            Dict['Say'] = "今日副本次数已用完！\n\n今日副本次数（{}/{}）\n\n[关闭:0]".format(current_count, max_count)
            return Dict
        
        # 创建副本地图
        map = SEnvir.CreateMap(298)
        if map is None:
            Dict['Say'] = "副本创建失败，请稍后再试。\n\n[关闭:0]"
            return Dict
            
        # 设置30分钟过期时间
        map.Expiry = datetime.now() + timedelta(minutes=30)
        
        # 生成怪物
        # 超级潘夜牛魔王
        map.CreateMon(51, 51, 3, "超级潘夜牛魔王", 1)
        
        # 普通怪物
        monsters = [
            ("潘夜战士", 20),
            ("潘夜冰魔", 20),
            ("潘夜右护卫", 20),
            ("潘夜云魔", 20),
            ("潘夜左护卫", 20),
            ("潘夜风魔", 20),
            ("潘夜火魔", 20)
        ]
        
        for name, count in monsters:
            map.CreateMon(51, 51, 100, name, count)
            
        # 潘夜鬼将8
        map.CreateMon(51, 51, 100, "潘夜鬼将8", 2)
        
        # 注册地图事件监听器（玩家离开事件）
        MapEvent.add_listener(map.Info.Index, "OnLeave", OnLeave)
        
        # 传送玩家
        DelayTeleport(Sender, map, 1, 91, 13)
        
        # 增加进入次数
        PlayerSetV(Sender, GV_PANYE_DUNGEON_COUNT, current_count + 1)
        return
    else:
        # 主对话界面
        Dict['Say'] = """<font color="0xffffff00">【每日副本】潘夜禁地</font>

<font color="0xffadd8e6">副本介绍：</font>
传说中的潘夜禁地，隐藏着无数珍贵的装备和宝物。
这里危机四伏，只有真正的勇士才能在此生存。
每日限制进入次数，挑战成功可获得丰厚奖励！

<font color="0xffffa500">挑战说明：</font>
• 每日可挑战次数：{}/{}
• 副本难度：★★★★☆
• 推荐等级：40级以上
• 挑战模式：单人副本

<font color="0xffff0000">副本产出：</font>
<img file=9 idx=1083 count=1 delay=1 item=潘夜血饮 /><img file=9 idx=1062 count=1 delay=1 item=潘夜无名刀 /><img file=9 idx=1066 count=1 delay=1 item=潘夜炼狱 />  <img file=9 idx=1343 count=1 delay=1 item=潘夜鬼将之魂 />  <img file=9 idx=1343 count=1 delay=1 item=潘夜牛魔王之魂 />

<font color="0xff00ff00">准备好接受挑战了吗？</font>

[进入副本:1]
[关闭:0]""".format(current_count, max_count)
        
        return Dict

# 注册NPC事件监听器
NpcEvent.add_listener(386, "OnClick", OnClick)