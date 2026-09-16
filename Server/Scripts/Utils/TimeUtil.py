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
from Server.Models import *
from MirDB import *
import Server.Envir.SEnvir as SEnvir

from datetime import datetime


# 时间格式 时:分:秒
# 24小时制 如 "23:01:00"是晚上11点1分0秒
# 判断当前时间是否在(开始时间, 结束时间)之间
def current_time_is_between(start_time, end_time):
    time_format = '%H:%M:%S'

    timeStart = datetime.strptime(start_time, time_format)
    timeEnd = datetime.strptime(end_time, time_format)
    now = datetime.now()

    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second = now.strftime('%S')

    timeNow = datetime.strptime('{}:{}:{}'.format(hour, minute, second), time_format)

    if timeStart < timeEnd:
        return timeStart <= timeNow <= timeEnd
    else:  # Over midnight
        return timeNow >= timeStart or timeNow <= timeEnd
