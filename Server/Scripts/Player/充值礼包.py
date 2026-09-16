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

# 充值奖励 注意RMB与元宝比例！
# 格式(累计充值元宝数量, (物品名称, 数量, 是否绑定))
# 请GM自行添加各种礼包
TopUpRewards = [
    #(10, "首充礼包"),
    #(50, "50元充值礼包"),
    #(100, "100元充值礼包"),
    (10, ("首充礼包", 1, True)),
    #(50, ("金手镯", 1, True)),
    #(100, ("紧急解毒药", 20, False)),
]



def OnTopUp(args):
    Sender = args[0]
    amount = args[1]

    if not Sender or amount < 1:
        return

    beforeTopUp = PlayerGetV(Sender, GK_LEIJICHONGZHI)
    afterTopUp = beforeTopUp + amount

    for reward in TopUpRewards:
        if beforeTopUp < reward[0] and afterTopUp >= reward[0]:
            Sender.PYMailSend("充值礼包", "运营团队", "感谢您对本服务器的支持!", [reward[1]])

    PlayerSetV(Sender, GK_LEIJICHONGZHI, afterTopUp)
    Sender.Connection.ReceiveChat("恭喜充值 {} 元宝成功！您已累计充值 {} 元宝".format(amount, afterTopUp), MessageType.System)

    return




#PlayerEvent.add_listener("OnTopUp", OnTopUp)
