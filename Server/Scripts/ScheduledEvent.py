# -*- coding: utf-8 -*-
import Server.Envir.SEnvir as SEnvir

'''
用法说明：
SEnvir.DelayCallMS(py函数名, 多少毫秒后执行，参数项, 绑定的玩家（可以不写）) 
--- 告诉服务端x毫秒后执行1次指定的py函数，参数项会被传入此py函数
SEnvir.DelayCall(py函数名, 多少秒后执行，参数项) 
--- 告诉服务端x秒后执行1次指定的py函数，参数项会被传入此py函数
SEnvir.ScheduledCall(py函数名, 执行时间，参数项，绑定的玩家（可以不写) 
--- 告诉服务端在指定时间，执行1次指定的py函数，参数项会被传入此py函数
SEnvir.PeriodicCall(py函数名, 执行时间，间隔多少秒后重复执行，参数项，绑定的玩家（可以不写) 
--- 告诉服务端在指定时间执行指定的py函数，此后每x秒重复执行一次，参数项会被传入此py函数

注意：参数项仅限一个 当想要执行的py函数需要大于1个参数的时候，需要用List或者Tuple包装一下，确保其仅接受1个参数
注意：执行时间的类型 是C#的DateTime类型，不可以用Python的Datetime
'''

'''
例子：
SEnvir.DelayCall("Utils.ServerUtils.SendMsgToAll", 3, "延迟测试")
 --- 3秒后 运行一次Utils.ServerUtils.SendMsgToAll函数 传入"延迟测试"作为其参数
SEnvir.PeriodicCall("Utils.ServerUtils.SendMsgToAll", SEnvir.Now, 3, "重复测试")
 --- 立即运行一次Utils.ServerUtils.SendMsgToAll函数 此后每3秒执行一次 传入"延迟测试"作为其参数
'''

def RegisterScheduledEvents():
	#清理已注册的延迟函数
	SEnvir.ScriptList.Clear()

    #这里注册所有需要的延迟函数

	# 游方货郎 600秒刷新一次位置
	#SEnvir.PeriodicCall("Npc.游方货郎.Refresh", SEnvir.Now, 600, 0)

	# 攻城战提前通知 
	# 每600秒检查一次是否需要通知
	SEnvir.PeriodicCall("Ser.发送攻城战通知.SendMsgBeforeConquestWar", SEnvir.Now, 600, 0)

	#桃园活动地图刷怪
	SEnvir.PeriodicCall("Mon.桃园活动.RefreshMonster", SEnvir.Now, 3600, 0)

	#古墓2层每5分钟轮换一次前往古墓3层的出口，首次在服务器启动5分钟后执行
	SEnvir.PeriodicCall("Map.古墓2定时开关门.ChangeGumuEntrance", SEnvir.Now.AddSeconds(300), 300, 0)
	
	# 定时发送公告 延迟5分钟
	SEnvir.DelayCall("Ser.系统公告.SendMsg", 60, 0)
	
	SEnvir.Log("注册定时脚本函数完成")
