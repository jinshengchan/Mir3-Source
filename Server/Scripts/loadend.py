# -*- coding: utf-8 -*-
import Server
import ScheduledEvent
import ServerStartEvent

Server.Envir.SEnvir.Log("加载脚本成功")
Server.Envir.SEnvir.Log("开始注册定时脚本函数...")
ScheduledEvent.RegisterScheduledEvents()
Server.Envir.SEnvir.PeriodicCall("ServerEvent.AutoRecycleWeapons", Server.Envir.SEnvir.Now.AddSeconds(1), 1, 0)
Server.Envir.SEnvir.Log("开始执行服务器启动触发脚本...")
ServerStartEvent.OnServerStart()
