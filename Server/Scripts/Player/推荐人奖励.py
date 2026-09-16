# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
import datetime
import os
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

'''
发送推荐人和被推荐人奖励
可以自定义是否检查推荐人和被推荐人拥有不同IP
'''

# 是否检查建号IP
CHECK_SAME_CREATION_IP = True
# 是否检查登录IP
CHECK_SAME_LOGIN_IP = True

# 是否记录IP相同的情况，如果相同就写入文本文件里面
RECORD_SAME_IP = True
# 记录IP相同数据存储位置
# 可以修改 但是需要手动创建好文件夹
FILE_PATH = u"D:\Server\推荐系统记录"
#---------------------------------------------------------------------------------------
# 推荐人奖励 （上家）
# 被推荐人达到对应等级后，上家获得的奖励
#---------------------------------------------------------------------------------------
ReferrerRewards = {
    35: [("5元红包", 1, True)],
}

'''
带权重的随机抽取 - 简单的写法
(物品名, 数量, 是否绑定, 权重)
'''
redpacket_weighted1 = [
         ('5元红包', 2, True, 100000),
         ('5元红包', 3, True, 500),
         ('5元红包', 4, True, 10),
         ('5元红包', 6, True, 1)
         ]
'''
抽中某一物品的概率是 物品权重/总权重
然后构造一个新的列表
'''
converted_redpacket_weighted1 = []
for item in redpacket_weighted1:
    converted_item = (item[0], item[1], item[2])
    for i in range(item[3]):
        converted_redpacket_weighted1.append(converted_item)

# 40级以后随机给1红包
ReferrerRewards[40] = random.sample(converted_redpacket_weighted1, 1)
ReferrerRewards[45] = random.sample(converted_redpacket_weighted1, 1)
ReferrerRewards[50] = random.sample(converted_redpacket_weighted1, 1)

#-------------------------------------------------------------------------------------

# 被推荐人奖励 （自己）
# 自己达到对应等级后，自己获得的奖励
RefereeRewards = {
    10: [("挂机卷3小时", 2, True)],
    20: [("传奇宝箱", 1, True)],
    30: [("传奇宝箱", 3, True)],
    35: [("5元红包", 1, True)],
}

# 额外随机物品
# 列表中是所有备选的物品
books = [
         ('魄冰刺(秘籍)', 1, False),
         ('焰天火雨(秘籍)', 1, False),
         ('怒神霹雳(秘籍)', 1, False),
         ('龙卷风(秘籍)', 1, False),
         ('凝血离魂(秘籍)', 1, False),
         ('莲月剑法(秘籍)', 1, False),
         ('乾坤大挪移(秘籍)', 1, False),
         ('铁布衫(秘籍)', 1, False),
         ('斗转星移(秘籍)', 1, False),
         ('破血狂杀(秘籍)', 1, False),
         ('十方斩(秘籍)', 1, False),
         ('云寂术(秘籍)', 1, False),
         ('阴阳法环(秘籍)', 1, False),
         ('妙影无踪(秘籍)', 1, False),
         ('移花接玉(秘籍)', 1, False),
         ('回生术(秘籍)', 1, False),
         ('翔空剑法(秘籍)', 1, False),
         ('新月爆炎龙(秘籍)', 1, False),
         ('心机一转(秘籍)', 1, False),
         ('鹰击(秘籍)', 1, False),
         ('黄泉旅者(秘籍)', 1, False),
         ('狂涛涌泉(秘籍)', 1, False),
         ('修罗降临(秘籍)', 1, False),
         ]
#potions = [
#           ('金创药(小)', 10, False),
#           ('金创药(中)', 5, False),
#           ('金创药(大)', 1, False),
#           ('魔法药(小)', 10, False),
#           ('魔法药(中)', 5, False),
#           ('魔法药(大)', 1, False)
#           ]

# 例子：被推荐人5级随机给2本书 1种药
#if 5 not in RefereeRewards:
    # 如果奖励列表没有5级奖励 先创建个空列表
#    RefereeRewards[5] = []
#RefereeRewards[5].append(random.sample(books, 2))
#RefereeRewards[5].append(random.sample(potions, 1))

# 40级随机给3本书
RefereeRewards[40] = random.sample(books, 3)


'''
带权重的随机抽取 - 简单的写法
(物品名, 数量, 是否绑定, 权重)
'''
redpacket_weighted3 = [
         ('5元红包', 2, True, 100000),
         ('5元红包', 3, True, 500),
         ('5元红包', 4, True, 50),
         ('5元红包', 6, True, 1)
         ]
'''
抽中某一物品的概率是 物品权重/总权重
然后构造一个新的列表
'''
converted_redpacket_weighted3 = []
for item in redpacket_weighted3:
    converted_item = (item[0], item[1], item[2])
    for i in range(item[3]):
        converted_redpacket_weighted3.append(converted_item)

# 45级随机给1红包
RefereeRewards[45] = random.sample(converted_redpacket_weighted3, 1)
RefereeRewards[50] = random.sample(converted_redpacket_weighted3, 1)



def CheckReferral(myself):
    if not myself:
        return None
    # 本人
    myself_level = myself.Level
    myself_creation_IP = myself.Character.Account.CreationIP
    myself_last_IP = myself.Character.Account.LastIP
    myself_current_IP = myself.Character.Account.Connection.IPAddress

    # 我的上家
    my_referrer = myself.Character.Account.Referral
    if not my_referrer:
        return None

    referrer_creation_IP = my_referrer.CreationIP
    referrer_last_IP = my_referrer.LastIP

    #myself.Connection.ReceiveChat("my ip = {}, referal ip = {}".format(myself_last_IP, referrer_last_IP), MessageType.System)

    # 如果两个账号出现IP相同 则记录到文件里面
    file_name = '推荐系统校验记录-' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"

    if CHECK_SAME_CREATION_IP:
        if myself_creation_IP == referrer_creation_IP:
            # 我的建号IP == 推荐人的建号IP
            if RECORD_SAME_IP:
                with open(os.path.join(FILE_PATH, file_name), "a") as the_file:
                    the_file.write("被推荐人账号: {}\n".format(myself.Character.Account.EMailAddress).encode('utf8'))
                    the_file.write("推荐人账号: {}\n".format(my_referrer.EMailAddress).encode('utf8'))
                    the_file.write("记录到相同建号IP\n".encode('utf8'))

            return None

    if CHECK_SAME_LOGIN_IP:
        if myself_last_IP == referrer_last_IP or myself_current_IP == referrer_last_IP:
            # 我的上次登录IP == 推荐人的上次登录IP 或者 我的当前登录IP == 推荐人的上次登录IP
            if RECORD_SAME_IP:
                with open(os.path.join(FILE_PATH, file_name), "a") as the_file:
                    the_file.write("被推荐人账号: {}\n".format(myself.Character.Account.EMailAddress).encode('utf8'))
                    the_file.write("推荐人账号: {}\n".format(my_referrer.EMailAddress).encode('utf8'))
                    the_file.write("被推荐人上次登录IP: {}\n".format(myself_last_IP).encode('utf8'))
                    the_file.write("推荐人上次登录IP: {}\n".format(referrer_last_IP).encode('utf8'))
                    the_file.write("被推荐人当前IP: {}\n".format(myself_current_IP).encode('utf8'))
                    the_file.write("记录到相同登录IP\n".encode('utf8'))

            return None

        # 如果上家在线 则对比当前IP
        if my_referrer.Connection:
            if my_referrer.Connection.IPAddress == myself_last_IP or my_referrer.Connection.IPAddress == myself_current_IP:
                if RECORD_SAME_IP:
                    with open(os.path.join(FILE_PATH, file_name), "a") as the_file:
                        the_file.write("被推荐人账号: {}\n".format(myself.Character.Account.EMailAddress).encode('utf8'))
                        the_file.write("推荐人账号: {}\n".format(my_referrer.EMailAddress).encode('utf8'))
                        the_file.write("被推荐人上次登录IP: {}\n".format(myself_last_IP).encode('utf8'))
                        the_file.write("推荐人当前IP: {}\n".format(my_referrer.Connection.IPAddress).encode('utf8'))
                        the_file.write("被推荐人当前IP: {}\n".format(myself_current_IP).encode('utf8'))
                        the_file.write("记录到相同登录IP\n".encode('utf8'))

                return None

    # 检查给上家的奖励
    if myself_level in ReferrerRewards:
        referrer_reward = ReferrerRewards[myself_level]
        # 发送给上家 my_referrer.LastCharacter.CharacterName是上家角色名
        myself.PYMailSend("推荐人礼包", "运营团队",
                               "您推荐的玩家 {} 已经达到了 {} 级, 这是给您的奖励！".format(myself.Name, myself.Level),
                               referrer_reward, my_referrer.LastCharacter.CharacterName)

    # 检查给自己的奖励
    if myself_level in RefereeRewards:
        my_reward = RefereeRewards[myself_level]
        myself.PYMailSend("被推荐人礼包", "运营团队",
                               "感谢您填写了推荐人并且达到了 {} 级, 这是给您的奖励！".format(myself.Level),
                               my_reward)

