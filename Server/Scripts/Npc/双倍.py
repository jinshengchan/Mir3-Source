# -*- coding: utf-8 -*-
# 载入模块SYS
import datetime
import os
import sys
# 引用模块的地址
from Globals import *
from Defines import *
import clr
import Server

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir
import collections
import NpcEvent

'''
点NPC 如果落后排行榜第一名2级 可以领取2小时双倍经验buff
'''

# 数据库需要新建一个自定义buff, 作为新人buff
# 注意设定自定义buff的属性以及持续时间
# 此变量设为这个自定义buff的序号
NEW_PLAYER_EXP_BUFF_INDEX = 146


def OnClick(args):
    Self = args[0]
    Sender = args[1]
    Menu = args[2]
    say = "123"
    res = {}

    if Menu == 2:
        user = SEnvir.Rankings.First.Value
        if user:
            if (int)(user.Level - Sender.Level) < 2 and user.Rebirth <= Sender.Character.Rebirth:
                say = """你当前不具备领取条件。
                         排行榜第一名为 {} 等级 {}


                    	 [关闭:0]""".format(user.CharacterName, user.Level)
            else:
                # 判断领取次数
                if (int) (PlayerGetV(Sender, GV_NEW_PLAYER_EXP_BUFF_COUNT)) >= 1:
                    say = """今天已经没有双倍次数了
                             
                             [关闭:0]"""
                else:
                    # 判断是否已经有了buff
                    if Sender.HasCustomBuff(NEW_PLAYER_EXP_BUFF_INDEX):
                        say = """上一次领取的buff消失之前，无法重复领取

                                 [关闭:0]"""
                    else:
                        PlayerSetV(Sender, GV_NEW_PLAYER_EXP_BUFF_COUNT, PlayerGetV(Sender, GV_NEW_PLAYER_EXP_BUFF_COUNT) + 1)
                        Sender.CustomBuffAdd(NEW_PLAYER_EXP_BUFF_INDEX)
                        say = """领取成功！

                                 [关闭:0]"""
    else:
            say =   """          如果你的等级低于排行榜第一名2级或以上
          每天可以在我这里领取 1 次双倍经验

          <font color=\"0xffff0000\">你已经领取了 {} 次。</font>

      注意：
          必须等上次领取的双倍失效后才可以再领。


                     [领取:2]


                     [关闭:0]""".format(PlayerGetV(Sender, GV_NEW_PLAYER_EXP_BUFF_COUNT))
    res['Say'] = say  # 定义聊天框对话内容
    return res


NpcEvent.add_listener(352, "OnClick", OnClick)
