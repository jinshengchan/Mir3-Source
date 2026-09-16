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
import Utils.Colors as Colors

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir


# 需要显示的图标以及功能
# 格式为 (LibraryFile.Interface文件中图标编号, 宽, 高, 对应NPC编号)
ShortcutList = [(160, 165, 20, 51),
                (161, 70, 20, 51),
                (162, 70, 20, 51),
                (163, 70, 20, 51),
                (164, 70, 20, 333),]


def OnShortcutDialogClicked(args):
    Sender = args[0]
    return ShortcutList



PlayerEvent.add_listener("OnShortcutDialogClicked",OnShortcutDialogClicked)
