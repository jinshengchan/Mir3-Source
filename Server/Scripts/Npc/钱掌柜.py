# -*- coding: utf-8 -*-
# 传奇3 Zircon引擎 - 终极兑换脚本
# 包含10种勋章强化和赞助币兑换功能

import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
from Globals import *

# 菜单ID定义
MAIN_MENU = 10      # 主菜单ID改为10避免冲突
EXCHANGE_MENU = 21

# 兑换配置
EXCHANGE_OPTIONS = {
    211: ("1赞助币", 1000000, 1),      # 100万金币=1赞助币
    212: ("10赞助币", 10000000, 10),   # 1000万金币=10赞助币
    213: ("100赞助币", 100000000, 100) # 1亿金币=100赞助币
}



def OnClick(args):
    Self = args[0]
    Sender = args[1]
    Menu = args[2]
    userInput = args[3] if len(args) > 3 else ""
    
    Dict = {'Say': "", 'Input': ""}
    
    # 主菜单（Menu=0是初始打开，Menu=MAIN_MENU是返回）
    if Menu == 0 or Menu == MAIN_MENU:
        green_start = "<font color=\"0xff00ff00\">"
        green_end = "</font>"
        Dict['Say'] = """{}欢迎来到钱掌柜兑换中心！{}

{}赞助币兑换{}
兑换比例：1赞助币 = 100万金币

[兑换1赞助币:211] (需要100万金币)
[兑换10赞助币:212] (需要1000万金币)
[兑换100赞助币:213] (需要1亿金币)

[关闭窗口:-1]""".format(green_start, green_end, green_start, green_end)
    
    # 处理赞助币兑换
    elif Menu in EXCHANGE_OPTIONS:
        name, cost, gain = EXCHANGE_OPTIONS[Menu]
        
        if Sender.Gold < cost:
            needed = cost//10000
            unit = "万" if cost < 100000000 else "亿"
            Dict['Say'] = "金币不足，需要{}{}金币\n\n[返回主菜单:{}]".format(
                needed//10000 if unit == "亿" else needed, 
                unit,
                MAIN_MENU
            )
        else:
            SubGold(Sender, cost)
            GiveGameGold(Sender, gain)
            # 发送成功消息到聊天框
            Sender.Connection.ReceiveChat("成功兑换{}！".format(name), MessageType.System)
            # 兑换成功后直接显示主菜单，不进行跳转
            green_start = "<font color=\"0xff00ff00\">"
            green_end = "</font>"
            Dict['Say'] = """{}欢迎来到钱掌柜兑换中心！{}

{}赞助币兑换{}
兑换比例：1赞助币 = 100万金币

[兑换1赞助币:211] (需要100万金币)
[兑换10赞助币:212] (需要1000万金币)
[兑换100赞助币:213] (需要1亿金币)

[关闭窗口:-1]""".format(green_start, green_end, green_start, green_end)
    

    
    return Dict

# 注册NPC事件
NpcEvent.add_listener(342, "OnClick", OnClick)