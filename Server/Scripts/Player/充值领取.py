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

from Player.充值礼包 import OnTopUp

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir
import glob, os


# 充值接口文件地址
FILE_PATH = u"D:\Server\Mir200\Envir\QuestDiary\充值元宝\元宝"

# 充值比例 1RMB = 10元宝
TOP_UP_RATIO = 100


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def OnCollectGameGoldClicked(args):
    Sender = args[0]
    if not Sender:
        return

    account = Sender.Character.Account.EMailAddress
    if not account:
        return

    # 充值接口只支持前10位
    account = account[:10]
    #Sender.Connection.ReceiveChat("当前账号 {} ！".format(account), MessageType.System)

    file_list = glob.glob(os.path.join(FILE_PATH, u'*.txt'))

    RMB_total = 0.0

    for file in file_list:
        amount = 0

        str_name = os.path.basename(file)[:-4]
        int_name = safe_cast(str_name, int)

        if not int_name:
            continue

        if str_name[0] == "0":
            amount = 0.1 * int_name
        else:
            amount = int_name

        # 打开文件寻找账号
        with open(file, "r") as f:
            lines = f.readlines()
        with open(file, "w") as f:
            for line in lines:
                if line.strip("\n")[:10] != account:
                    f.write(line)
                else:
                    RMB_total += amount

    gamegold_total = RMB_total * TOP_UP_RATIO
    Sender.Connection.ReceiveChat("恭喜充值 {} 元成功！您已获得充值 {} 元宝".format(RMB_total, gamegold_total), MessageType.System)
    GiveGameGold(Sender, gamegold_total)
    OnTopUp([Sender, gamegold_total])


PlayerEvent.add_listener("OnCollectGameGoldClicked", OnCollectGameGoldClicked)

