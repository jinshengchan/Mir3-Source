# -*- coding: utf-8 -*-
# 导入所需模块和依赖
import sys
from datetime import datetime, timedelta
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import Server
import NpcEvent
import MapEvent
from Utils import ServerUtils
import Server.Envir.SEnvir as SEnvir
import random
import time

# 定义副本核心常量
LIMIT_TIME = 1800
BUFFER_TIME = 10

# 副本核心配置
BADA_FUBEN_MAP_INDEX = 387
BADA_FUBEN_X = 19
BADA_FUBEN_Y = 34
BADA_ENTER_COST = ("元宝", 500)
BADA_LEVEL_COST = ("元宝", 50)
BADA_MONSTER_SPAWN_X = 21
BADA_MONSTER_SPAWN_Y = 30
BADA_MONSTER_SPAWN_RANGE = 10

# 地图临时变量
TEMPV_WAVE_NUM = 1
TEMPV_MON_SPAWNED = 2
TEMPV_FUBEN_TYPE = 3
TEMPV_SCRIPT_ID = 4

# 不限次数Name列表
EXCLUDE_PLAYER_NAME = ["999", "梦无魂", "梦无霜", "梦无雨", "专治不服", "因媛而毅"]
#EXCLUDE_PLAYER_NAME = ["aasssdddafafasda"]

# 同时最大副本进程数
MAX_ACTIVE_FUBEN_COUNT = 2

# 等待队列最大长度
MAX_WAITING_QUEUE = 10

# 等待超时时间（秒）
WAIT_TIMEOUT = 300  # 5分钟

# 进程池定时检查间隔（秒），用于清理超时活跃玩家和等待者
POOL_CHECK_INTERVAL = 120  # 2分钟

# 刷新状态按钮配置（新增）
REFRESH_LOCK_DURATION = 30  # 刷新点击锁时长（秒）
refresh_lock = {}  # 刷新锁存储：{player_id: 上次刷新时间戳}

# 进程池管理（优化：解决资源泄露问题）
class FubenProcessPool:
    def __init__(self):
        self.active_players = {}  # 活跃玩家：{player_id: 进入时间}
        self.waiting_queue = []   # 等待队列：[{player_id: xxx, join_time: xxx}, ...]
        self.pool_lock = clr.Reference[System.Object]()
        self.pool_lock.Value = System.Object()
        # 启动进程池定时检查（核心优化：主动清理超时资源）
        self.start_pool_check()
    
    # 启动进程池定时检查，清理超时活跃玩家和等待者
    def start_pool_check(self):
        try:
            # 每POOL_CHECK_INTERVAL秒调用一次检查方法，循环执行
            SEnvir.DelayCall("Npc.BOSS副本.八大暗影.PoolCheck", POOL_CHECK_INTERVAL, (self,), None)
        except Exception as e:
            # 移除进程池相关日志
            pass
    
    # 进程池定时检查核心方法（优化：主动清理超时资源）
    def pool_check(self):
        try:
            System.Threading.Monitor.Enter(self.pool_lock.Value)
            try:
                # 1. 清理超时等待者（原逻辑仅在玩家离开时清理，优化后定时清理）
                self._clean_expired_waiters()
                
                # 2. 清理超时活跃玩家（核心优化：解决活跃玩家异常未释放问题）
                self._clean_expired_active_players()
                
                # 3. 再次启动定时检查，形成循环
                self.start_pool_check()
            finally:
                System.Threading.Monitor.Exit(self.pool_lock.Value)
        except Exception as e:
            # 移除进程池相关日志
            pass
            # 异常后重新启动定时检查，避免检查中断
            self.start_pool_check()
    
    # 获取当前活跃进程数
    def get_active_count(self):
        return len(self.active_players)
    
    # 获取等待队列长度
    def get_waiting_count(self):
        return len(self.waiting_queue)
    
    # 尝试进入副本（成功返回True，需要等待返回False，队列已满返回None）（优化：增加player_id校验）
    def try_enter_fuben(self, player_id):
        System.Threading.Monitor.Enter(self.pool_lock.Value)
        try:
            # 优化：校验player_id有效性，无效ID直接返回None，避免占用资源
            if not player_id or player_id <= 0:
                return None
            
            # 如果已经在活跃列表中，直接返回成功
            if player_id in self.active_players:
                return True
            
            # 如果活跃进程数未满，加入活跃列表
            if len(self.active_players) < MAX_ACTIVE_FUBEN_COUNT:
                self.active_players[player_id] = SEnvir.Now
                return True
            
            # 如果已经在等待队列中，返回需要等待
            for item in self.waiting_queue:
                if item['player_id'] == player_id:
                    return False
            
            # 如果等待队列未满，加入等待队列
            if len(self.waiting_queue) < MAX_WAITING_QUEUE:
                self.waiting_queue.append({
                    'player_id': player_id,
                    'join_time': SEnvir.Now
                })
                return False
            else:
                # 等待队列已满
                return None
        finally:
            System.Threading.Monitor.Exit(self.pool_lock.Value)
    
    # 离开副本（优化：确保玩家从活跃列表移除，同时处理等待队列）
    def leave_fuben(self, player_id):
        System.Threading.Monitor.Enter(self.pool_lock.Value)
        try:
            # 核心修复1：强制从活跃列表移除（无论是否存在）
            if player_id in self.active_players:
                del self.active_players[player_id]
            
            # 核心修复2：同时从等待队列移除（防止玩家既在活跃又在等待）
            for i, item in enumerate(self.waiting_queue):
                if item['player_id'] == player_id:
                    del self.waiting_queue[i]
                    break
            
            # 清理过期的等待者
            self._clean_expired_waiters()
            
            # 如果有等待者，让队列中的第一个玩家进入
            if self.waiting_queue and len(self.active_players) < MAX_ACTIVE_FUBEN_COUNT:
                next_player = self.waiting_queue.pop(0)
                next_player_id = next_player['player_id']
                wait_time = (SEnvir.Now - next_player['join_time']).TotalSeconds
                
                # 加入活跃列表
                self.active_players[next_player_id] = SEnvir.Now
                
                # 尝试通知玩家（需要找到玩家对象）
                return next_player_id
            
            return None
        finally:
            System.Threading.Monitor.Exit(self.pool_lock.Value)
    
    # 清理过期的等待者（原逻辑保留，新增定时调用）
    def _clean_expired_waiters(self):
        current_time = SEnvir.Now
        
        # 从后往前遍历，避免索引问题
        for i in range(len(self.waiting_queue) - 1, -1, -1):
            waiter = self.waiting_queue[i]
            wait_time = (current_time - waiter['join_time']).TotalSeconds
            
            if wait_time > WAIT_TIMEOUT:
                # 等待超时，移除
                self.waiting_queue.pop(i)
    
    # 核心优化：清理超时活跃玩家（解决异常离线/崩溃导致的进程泄露）
    def _clean_expired_active_players(self):
        current_time = SEnvir.Now
        expired_player_ids = []
        
        # 遍历活跃玩家，判断是否超时（超过副本时限LIMIT_TIME）
        for player_id, enter_time in self.active_players.items():
            active_time = (current_time - enter_time).TotalSeconds
            # 超过副本时限，标记为过期（预留10秒缓冲）
            if active_time > LIMIT_TIME + 10:
                expired_player_ids.append(player_id)
        
        # 移除所有过期活跃玩家，释放进程名额
        for player_id in expired_player_ids:
            del self.active_players[player_id]
        
        # 清理过期后，检查等待队列，补充活跃玩家
        self._refill_active_players()
    
    # 辅助优化：清理超时活跃玩家后，补充等待队列中的玩家进入活跃列表
    def _refill_active_players(self):
        # 循环补充，直到活跃进程数满或等待队列为空
        while self.waiting_queue and len(self.active_players) < MAX_ACTIVE_FUBEN_COUNT:
            next_player = self.waiting_queue.pop(0)
            next_player_id = next_player['player_id']
            
            self.active_players[next_player_id] = SEnvir.Now
            # 通知玩家可以进入
            NotifyWaitingPlayer(next_player_id)
    
    # 获取玩家等待位置
    def get_wait_position(self, player_id):
        System.Threading.Monitor.Enter(self.pool_lock.Value)
        try:
            for i, item in enumerate(self.waiting_queue):
                if item['player_id'] == player_id:
                    return i + 1  # 返回位置（从1开始）
            return 0  # 不在等待队列中
        finally:
            System.Threading.Monitor.Exit(self.pool_lock.Value)
    
    # 获取玩家等待时间
    def get_wait_time(self, player_id):
        System.Threading.Monitor.Enter(self.pool_lock.Value)
        try:
            for item in self.waiting_queue:
                if item['player_id'] == player_id:
                    wait_time = (SEnvir.Now - item['join_time']).TotalSeconds
                    return int(wait_time)
            return 0
        finally:
            System.Threading.Monitor.Exit(self.pool_lock.Value)
    
    # 检查玩家是否在活跃列表中
    def is_player_active(self, player_id):
        System.Threading.Monitor.Enter(self.pool_lock.Value)
        try:
            return player_id in self.active_players
        finally:
            System.Threading.Monitor.Exit(self.pool_lock.Value)
    
    # 获取状态信息
    def get_status_info(self):
        System.Threading.Monitor.Enter(self.pool_lock.Value)
        try:
            return {
                'active_count': len(self.active_players),
                'waiting_count': len(self.waiting_queue),
                'active_players': list(self.active_players.keys()),
                'waiting_players': [item['player_id'] for item in self.waiting_queue]
            }
        finally:
            System.Threading.Monitor.Exit(self.pool_lock.Value)

# 创建全局进程池实例
fuben_pool = FubenProcessPool()

# 进程池定时检查入口（供SEnvir.DelayCall调用）
def PoolCheck(args):
    try:
        # 获取进程池实例
        pool = args[0]
        if pool and hasattr(pool, 'pool_check'):
            pool.pool_check()
    except Exception as e:
        # 移除进程池相关日志
        pass

# 定义怪物索引获取函数
def get_monster_index(mon_name):
    mon_info = SEnvir.GetMonsterInfo(mon_name)
    if mon_info:
        return mon_info.Index
    else:
        return -1

# BOSS配置列表
BADA_MON_LIST = {
    1: [("沃玛教主", 1, get_monster_index("沃玛教主"))],
    2: [("骷髅教主", 1, get_monster_index("骷髅教主"))],
    3: [("触龙神", 1, get_monster_index("触龙神"))],
    4: [("赤月恶魔", 1, get_monster_index("赤月恶魔"))],
    5: [("祖玛教主", 1, get_monster_index("祖玛教主"))],
    6: [("潘夜牛魔王", 1, get_monster_index("潘夜牛魔王"))],
    7: [("震天魔神", 1, get_monster_index("震天魔神"))],
    8: [("霸王教主", 1, get_monster_index("霸王教主"))],
    9: [("诺玛教主", 1, get_monster_index("诺玛教主"))],
    10: [("地天灭王", 1, get_monster_index("地天灭王"))],
    11: [("火影", 1, get_monster_index("火影"))],
    12: [("冥血魔王", 1, get_monster_index("冥血魔王"))],
    13: [("囚禁的魔王", 1, get_monster_index("囚禁的魔王"))],
    14: [("黎明女王", 1, get_monster_index("黎明女王"))],
    15: [("朱雀天王1", 1, get_monster_index("朱雀天王1"))],
    16: [("幽灵船长", 1, get_monster_index("幽灵船长"))],
    17: [("黑风寨寨主", 1, get_monster_index("黑风寨寨主"))],
    18: [("赤龙魔王", 1, get_monster_index("赤龙魔王"))],
    19: [("黑羽教主-钺皇", 1, get_monster_index("黑羽教主-钺皇"))],
    20: [("黎明教主", 1, get_monster_index("黎明教主"))],
    21: [("八腕魔", 1, get_monster_index("八腕魔"))],
    22: [("魔灵神主", 1, get_monster_index("魔灵神主"))],
}

# 安全移除脚本函数
def SafeRemoveScript(script_name, player):
    try:
        if player and hasattr(player, 'ObjectID'):
            SEnvir.RemoveScript(script_name, player)
    except Exception as e:
        SEnvir.Log("SafeRemoveScript-脚本移除异常：" + str(e))
        pass

# 通知等待玩家函数
def NotifyWaitingPlayer(player_id):
    try:
        # 查找玩家对象
        all_players = SEnvir.Players
        for p in all_players:
            if hasattr(p, 'ObjectID') and int(p.ObjectID or 0) == player_id:
                if hasattr(p, 'Connection'):
                    # 发送通知消息
                    p.Connection.ReceiveChat("副本进程已空闲，您可以进入副本了！", MessageType.System)
                    
                    # 获取状态信息
                    status = fuben_pool.get_status_info()
                    active_count = status['active_count']
                    waiting_count = status['waiting_count']
                    
                    tip = "当前状态：活跃进程" + str(active_count) + "/" + str(MAX_ACTIVE_FUBEN_COUNT) + \
                          "，等待人数" + str(waiting_count)
                    p.Connection.ReceiveChat(tip, MessageType.System)
                break
    except Exception as e:
        # 移除进程池相关日志
        pass

# 辅助函数：判断玩家是否可进入副本（用于控制对话框按钮显示）
def can_enter_fuben(player_id):
    # 1. 活跃进程未满，且玩家不在活跃列表、不在等待队列 → 可进入
    status = fuben_pool.get_status_info()
    if status['active_count'] < MAX_ACTIVE_FUBEN_COUNT:
        if not fuben_pool.is_player_active(player_id) and fuben_pool.get_wait_position(player_id) == 0:
            return True
    # 2. 其他情况（活跃满、在活跃列表、在等待队列、队列满）→ 不可进入
    return False

# 辅助函数：检查刷新锁（新增），返回剩余冷却时间（秒），0表示可刷新
def check_refresh_lock(player_id):
    current_time = time.time()
    # 玩家无刷新记录或已过冷却时间，可刷新
    if player_id not in refresh_lock or (current_time - refresh_lock[player_id]) >= REFRESH_LOCK_DURATION:
        return 0
    # 计算剩余冷却时间
    remaining = int(REFRESH_LOCK_DURATION - (current_time - refresh_lock[player_id]))
    return remaining

# 辅助函数：更新刷新锁（新增）
def update_refresh_lock(player_id):
    refresh_lock[player_id] = time.time()

# NPC点击核心函数 - 优化：对话框按钮显示（可进入显示进入按钮，不可进入隐藏）+ 刷新锁+倒计时
def OnClick(args):
    Self = None
    player = None
    Menu = 0
    Dict = {}
    Say = ""
    
    try:
        try:
            Self = args[0]
            player = args[1]
            Menu = args[2]
        except Exception as e:
            SEnvir.Log("OnClick-参数获取异常：" + str(e))
            Dict['Say'] = "参数错误"
            return Dict

        player_id = getattr(player, "ObjectID", 0)
        player_name = getattr(player, "Name", 0)
        try:
            player_id = int(player_id)
        except:
            player_id = 0

        # 判断玩家是否可进入副本（控制进入按钮显示）
        enter_available = can_enter_fuben(player_id)
        # 检查刷新锁状态，获取剩余冷却时间
        refresh_remaining = check_refresh_lock(player_id)

        if Menu == 11:
            if not player or not hasattr(player, 'Connection'):
                Say = "玩家状态异常"
                Dict['Say'] = Say
                return Dict

            if hasattr(player, 'CurrentMap') and player.CurrentMap and hasattr(player.CurrentMap, 'Index'):
                if player.CurrentMap.Index == BADA_FUBEN_MAP_INDEX:
                    player.Connection.ReceiveChat("您已经在副本中，无法重复进入。", MessageType.System)
                    Dict['Say'] = Say
                    return Dict

            # 检查每日次数限制
            if player_name not in EXCLUDE_PLAYER_NAME:
                bada_count = int(PlayerGetV(player, GV_BADA_COUNT) or 0)
                if bada_count > 0:
                    player.Connection.ReceiveChat("每天只能挑战一次...", MessageType.Combat)
                    Dict['Say'] = Say
                    return Dict

            # 检查费用
            paid = False
            if BADA_ENTER_COST[0] == "元宝":
                if hasattr(player, 'GameGold') and int(player.GameGold or 0) >= BADA_ENTER_COST[1]:
                    SubGameGold(player, BADA_ENTER_COST[1])
                    paid = True

            if not paid:
                Say = "你的钱不够"
                Dict['Say'] = Say
                return Dict

            # 尝试进入进程池
            result = fuben_pool.try_enter_fuben(player_id)
            
            if result is True:
                # 成功获得副本权限，创建副本
                if hasattr(player, 'GroupMembers') and player.GroupMembers:
                    player.GroupLeave()

                fuben = SEnvir.CreateMap(BADA_FUBEN_MAP_INDEX)
                if fuben:
                    fuben.MapTime = SEnvir.Now.AddSeconds(LIMIT_TIME)
                    MapSetTempV(fuben, TEMPV_FUBEN_TYPE, "八大")
                    player.Teleport(fuben, BADA_FUBEN_X, BADA_FUBEN_Y)

                    if player_name not in EXCLUDE_PLAYER_NAME:
                        PlayerSetV(player, GV_BADA_COUNT, 1)
                    
                    # 发送进入成功消息
                    player.Connection.ReceiveChat("成功进入副本！祝您挑战顺利！", MessageType.System)
                    SEnvir.Log(str(player_name) + "成功进入八大暗影副本")
                else:
                    # 优化核心：副本创建失败，除了退还费用，必须释放进程池名额（解决资源泄露）
                    fuben_pool.leave_fuben(player_id)
                    if BADA_ENTER_COST[0] == "元宝":
                        GiveGameGold(player, BADA_ENTER_COST[1])
                    player.Connection.ReceiveChat("副本创建失败，费用已退还。", MessageType.System)
            
            elif result is False:
                # 需要等待
                wait_position = fuben_pool.get_wait_position(player_id)
                wait_time = fuben_pool.get_wait_time(player_id)
                
                status = fuben_pool.get_status_info()
                active_count = status['active_count']
                waiting_count = status['waiting_count']
                
                # 发送等待消息
                player.Connection.ReceiveChat("当前副本进程已满，您已加入等待队列。", MessageType.System)
                tip = "您的等待位置：第" + str(wait_position) + "位," + \
                      "已等待时间：" + str(wait_time) + "秒," + \
                      "当前状态：活跃进程" + str(active_count) + "/" + str(MAX_ACTIVE_FUBEN_COUNT) + \
                      "，等待人数" + str(waiting_count) + "/" + str(MAX_WAITING_QUEUE) + "," + \
                      "请耐心等待，或稍后再试。"
                player.Connection.ReceiveChat(tip, MessageType.System)
            
            else:
                # 等待队列已满
                status = fuben_pool.get_status_info()
                active_count = status['active_count']
                waiting_count = status['waiting_count']
                
                player.Connection.ReceiveChat("抱歉，等待队列已满，请稍后再试。", MessageType.System)
                tip = "当前状态：活跃进程" + str(active_count) + "/" + str(MAX_ACTIVE_FUBEN_COUNT) + \
                      "，等待人数" + str(waiting_count) + "/" + str(MAX_WAITING_QUEUE)
                player.Connection.ReceiveChat(tip, MessageType.System)
                
                # 退还费用
                if BADA_ENTER_COST[0] == "元宝":
                    GiveGameGold(player, BADA_ENTER_COST[1])

        elif Menu == 12:
            # 优化3：刷新状态按钮点击锁，限制每30s一次
            if refresh_remaining > 0:
                # 冷却中，提示不可刷新
                player.Connection.ReceiveChat("刷新过于频繁，请等待" + str(refresh_remaining) + "秒后再试！", MessageType.System)
                # 刷新对话框，显示当前冷却状态
                Menu = 1  # 重置菜单，重新渲染对话框
            else:
                # 可刷新，更新刷新锁，重新判断可进入状态
                update_refresh_lock(player_id)
                # 重新获取可进入状态（同步进程池最新状态）
                enter_available = can_enter_fuben(player_id)
                
            # 刷新状态信息（无论是否冷却，均重新渲染状态）
            status = fuben_pool.get_status_info()
            active_count = status['active_count']
            waiting_count = status['waiting_count']
            
            wait_position = fuben_pool.get_wait_position(player_id)
            wait_time = fuben_pool.get_wait_time(player_id)
            
            # 重新获取刷新锁状态（刷新后可能进入冷却）
            refresh_remaining = check_refresh_lock(player_id)
            # 刷新按钮显示（冷却/正常）
            if refresh_remaining > 0:
                refresh_button = "[刷新状态:82] 刷新状态信息（剩余" + str(refresh_remaining) + "秒）\r\n\r\n"
            else:
                refresh_button = "[刷新状态:82] 刷新状态信息\r\n\r\n"
            # 进入按钮显示（刷新后同步更新）
            enter_button = "[开始挑战:81] \r\n\r\n" if enter_available else ""
            
            Say = "副本状态信息：\r\n\r\n" + \
                  "活跃进程：" + str(active_count) + "/" + str(MAX_ACTIVE_FUBEN_COUNT) + "\r\n\r\n" + \
                  enter_button + \
                  refresh_button + \
                  "[返回:1] 返回上级菜单\r\n\r\n" + \
                  "[离开:0]"

        else:
            status = fuben_pool.get_status_info()
            active_count = status['active_count']
            waiting_count = status['waiting_count']
            
            # 检查玩家是否在等待队列中
            wait_position = fuben_pool.get_wait_position(player_id)
            wait_time = fuben_pool.get_wait_time(player_id)
            
            # 优化1：可进入显示进入按钮，不可进入隐藏；优化2：不可进入时必显刷新按钮（带倒计时）
            enter_button = "[开始挑战:81] \r\n\r\n" if enter_available else ""
            # 刷新按钮显示（冷却/正常）
            if refresh_remaining > 0:
                refresh_button = "[刷新状态:82] 刷新状态信息（剩余" + str(refresh_remaining) + "秒）\r\n\r\n"
            else:
                refresh_button = "[刷新状态:82] 刷新状态信息\r\n\r\n"
            
            # 修复核心：注释移到拼接完成后
            Say = "这里可以进入八大暗影教主副本\r\n\r\n" + \
                  "体验挑战BOOS的快感\r\n\r\n" + \
                  "每层1个大BOOS,一共" + str(len(BADA_MON_LIST)) + "层, 击杀教主方可进入下一层\r\n\r\n" + \
                  "进入门票需要" + str(BADA_ENTER_COST[1]) + BADA_ENTER_COST[0] + "。\r\n\r\n" + \
                  "每层扣除" + str(BADA_LEVEL_COST[1]) + BADA_LEVEL_COST[0] + "。\r\n\r\n" + \
                  "当前状态：活跃进程" + str(active_count) + "/" + str(MAX_ACTIVE_FUBEN_COUNT) + "。\r\n\r\n" + \
                  enter_button + \
                  refresh_button + "[离开:0]"  # 必显刷新按钮（修正：移除多余反斜杠，避免语法错误）

    except Exception as e:
        SEnvir.Log("OnClick-核心逻辑异常：" + str(e))
        Say = "操作失败，请稍后重试"

    Dict['Say'] = Say
    return Dict

# 副本创建事件函数
def OnCreate(args):
    try:
        try:
            fuben_map = args[0]
        except Exception as e:
            SEnvir.Log("OnCreate-参数获取异常：" + str(e))
            return
        
        if not fuben_map:
            return
        
        MapSetTempV(fuben_map, TEMPV_WAVE_NUM, 1)
        MapSetTempV(fuben_map, TEMPV_MON_SPAWNED, 0)
        MapSetTempV(fuben_map, TEMPV_FUBEN_TYPE, "八大")
        MapSetTempV(fuben_map, TEMPV_SCRIPT_ID, 0)
    except Exception as e:
        SEnvir.Log("OnCreate-创建副本异常：" + str(e))

# 副本新层初始化函数
def InitNewLevel(args):
    try:
        try:
            fuben_map = args[0]
            player = args[1]
        except Exception as e:
            SEnvir.Log("InitNewLevel-参数获取异常：" + str(e))
            return
        
        if not (player and fuben_map):
            return

        if int(getattr(player, 'GameGold', 0) or 0) < BADA_LEVEL_COST[1]:
            player.Connection.ReceiveChat("元宝不足，无法进入本层副本。", MessageType.System)
            TeleportBackToTown(player)
            return
        SubGameGold(player, BADA_LEVEL_COST[1])

        SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
        wave = int(MapGetTempV(fuben_map, TEMPV_WAVE_NUM) or 0)
        MapSetTempV(fuben_map, TEMPV_MON_SPAWNED, 0)
        fuben_map.ClearAllMonsters()

        # 修复：每层限时应为基础时间，而非叠加60秒（原逻辑会导致层数越高时间越长，不符合常规副本设计）
        current_limit = LIMIT_TIME
        tip = "您进入了副本第" + str(wave) + "层，本层限时" + str(current_limit) + "秒"
        player.Connection.ReceiveChat(tip, MessageType.System)
        
        script_id = SEnvir.DelayCall("Npc.BOSS副本.八大暗影.CheckFuben", 3, (fuben_map, wave, player), player)
        MapSetTempV(fuben_map, TEMPV_SCRIPT_ID, script_id)
    except Exception as e:
        SEnvir.Log("InitNewLevel-初始化新层异常：" + str(e))

# 副本进入事件函数
def OnEnter(args):
    try:
        InitNewLevel(args)
    except Exception as e:
        SEnvir.Log("OnEnter-进入副本异常：" + str(e))

# 副本离开事件函数 - 修改为释放进程（核心修复）
def OnLeave(args):
    player = None
    try:
        try:
            fuben_map = args[0]
            player = args[1]
        except Exception as e:
            SEnvir.Log("OnLeave-参数获取异常：" + str(e))
            return

        player_id = getattr(player, "ObjectID", 0)
        try:
            player_id = int(player_id)
        except:
            player_id = 0

        # 核心修复2：提前移除脚本，避免重复执行
        SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
        SafeRemoveScript("Npc.BOSS副本.八大暗影.TeleportBackToTown", player)
        SafeRemoveScript("Npc.BOSS副本.八大暗影.TeleportToNextLevel", player)

        # 核心修复3：强制释放进程池（无论是否正常离开）
        if player_id > 0:
            fuben_pool.leave_fuben(player_id)
        
        # 如果有等待的玩家，通知他们
        next_player_id = fuben_pool.leave_fuben(player_id)
        if next_player_id:
            NotifyWaitingPlayer(next_player_id)

        CloseFuben((fuben_map,))

        if player and hasattr(player, 'Connection'):
            player.Connection.ReceiveChat("你离开了副本地图，副本已关闭", MessageType.System)
    except Exception as e:
        SEnvir.Log("OnLeave-离开副本异常：" + str(e))
        # 兜底：即使出现异常，也要尝试释放进程
        try:
            if player and getattr(player, "ObjectID", 0) > 0:
                fuben_pool.leave_fuben(int(getattr(player, "ObjectID", 0)))
        except:
            pass

# 副本关闭函数
def CloseFuben(args):
    try:
        try:
            fuben_map = args[0]
        except Exception as e:
            SEnvir.Log("CloseFuben-参数获取异常：" + str(e))
            return
        
        if not fuben_map:
            return

        MapSetTempV(fuben_map, TEMPV_WAVE_NUM, 0)
        MapSetTempV(fuben_map, TEMPV_MON_SPAWNED, 0)
        MapSetTempV(fuben_map, TEMPV_FUBEN_TYPE, "")
        MapSetTempV(fuben_map, TEMPV_SCRIPT_ID, 0)

        fuben_map.ClearAllMonsters()
        SEnvir.CloseMap(fuben_map)
    except Exception as e:
        SEnvir.Log("CloseFuben-关闭副本异常：" + str(e))

# 统计副本当前层目标怪物，排除玩家租用的怪物
def GetAliveFubenMonsterCount(fuben_map, mon_index):
    count = 0
    for obj in fuben_map.Objects:
        if not obj or getattr(obj, 'Dead', True):
            continue
        if getattr(obj, 'PetOwner', None):
            continue
        monster_info = getattr(obj, 'MonsterInfo', None)
        if monster_info and monster_info.Index == mon_index:
            count += 1
    return count

# 刷怪函数 - 核心修复：添加怪物生成标记设置
def SpawnMonsters(fuben_map):
    try:
        if not fuben_map:
            return

        wave = int(MapGetTempV(fuben_map, TEMPV_WAVE_NUM) or 0)
        fuben_type = "八大"

        if fuben_type == "八大":
            if wave not in BADA_MON_LIST:
                wave = 1
                MapSetTempV(fuben_map, TEMPV_WAVE_NUM, wave)

            mon_info = BADA_MON_LIST[wave][0]
            mon_name = mon_info[0]
            mon_count = mon_info[1]
            mon_index = mon_info[2]

            if mon_index > 0:
                fuben_map.CreateMon(BADA_MONSTER_SPAWN_X, BADA_MONSTER_SPAWN_Y, BADA_MONSTER_SPAWN_RANGE, mon_name, mon_count)
                # 核心修复：生成怪物后标记为已生成
                MapSetTempV(fuben_map, TEMPV_MON_SPAWNED, 1)
    except Exception as e:
        SEnvir.Log("SpawnMonsters-刷怪异常：" + str(e))

# 传送回城函数
def TeleportBackToTown(player):
    try:
        if not player or not player.CurrentMap:
            return
        player.TeleportByMapIndex(1, 450, 390)
        player.Connection.ReceiveChat("恭喜通关所有层数！传送回城。", MessageType.System)
        # 核心修复4：回城时也释放进程
        player_id = getattr(player, "ObjectID", 0)
        if player_id > 0:
            fuben_pool.leave_fuben(int(player_id))
    except Exception as e:
        SEnvir.Log("TeleportBackToTown-传送回城异常：" + str(e))

# 传送下一层函数
def TeleportToNextLevel(args):
    try:
        try:
            player = args[0]
            fuben_map = args[1]
        except Exception as e:
            SEnvir.Log("TeleportToNextLevel-参数获取异常：" + str(e))
            return

        if not (player and fuben_map):
            return

        fuben_type = "八大"
        if fuben_type == "八大":
            player.Teleport(fuben_map, BADA_FUBEN_X, BADA_FUBEN_Y)
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            InitNewLevel((fuben_map, player))
    except Exception as e:
        SEnvir.Log("TeleportToNextLevel-传送下一层异常：" + str(e))

# 副本状态检查函数（优化：玩家死亡时释放进程）
def CheckFuben(args):
    try:
        try:
            fuben_map = args[0]
            wave = args[1]
            player = args[2]
        except Exception as e:
            SEnvir.Log("CheckFuben-参数获取异常：" + str(e))
            return
        player_id = getattr(player, "ObjectID", 0)
        player_name = getattr(player, "Name", 0)
        try:
            player_id = int(player_id)
        except:
            player_id = 0

        if not (player and fuben_map):
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            CloseFuben((fuben_map,))
            # 优化：玩家/地图异常时，释放进程池名额
            if player_id and player_id > 0:
                fuben_pool.leave_fuben(player_id)
            return

        # 优化：玩家死亡时，触发离开逻辑，释放进程
        if hasattr(player, 'IsAlive') and not player.IsAlive:
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            # 核心修复5：死亡时直接调用进程释放
            if player_id > 0:
                fuben_pool.leave_fuben(player_id)
            OnLeave((fuben_map, player))
            return

        if not hasattr(player, 'CurrentMap') or not player.CurrentMap or player.CurrentMap != fuben_map:
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            CloseFuben((fuben_map,))
            if hasattr(player, 'Connection'):
                player.Connection.ReceiveChat("你已离开副本，副本关闭。", MessageType.System)
            # 优化：玩家离开副本时，确保释放进程
            if player_id and player_id > 0:
                fuben_pool.leave_fuben(player_id)
            return

        if int(getattr(fuben_map, 'PlayerCount', 0) or 0) < 1:
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            CloseFuben((fuben_map,))
            # 优化：副本无玩家时，释放所有相关进程（防止残留）
            if player_id and player_id > 0:
                fuben_pool.leave_fuben(player_id)
            return

        current_wave = int(MapGetTempV(fuben_map, TEMPV_WAVE_NUM) or 0)
        
        if current_wave not in BADA_MON_LIST:
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            player.Connection.ReceiveChat("副本层数错误", MessageType.System)
            TeleportBackToTown(player)
            # 优化：层数异常时，释放进程池名额
            if player_id and player_id > 0:
                fuben_pool.leave_fuben(player_id)
            return

        current_mon_info = BADA_MON_LIST[current_wave][0]
        current_boss_name = current_mon_info[0]
        current_boss_index = current_mon_info[2]

        if int(current_boss_index) <= 0:
            player.Connection.ReceiveChat("怪物配置错误：" + current_boss_name, MessageType.System)
            return

        mon_spawned = int(MapGetTempV(fuben_map, TEMPV_MON_SPAWNED) or 0) > 0

        alive_count = int(GetAliveFubenMonsterCount(fuben_map, current_boss_index) or 0)
        
        if alive_count < 1:
            if mon_spawned:
                next_wave = current_wave + 1
                
                if next_wave > len(BADA_MON_LIST):
                    SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
                    tip = "恭喜成功通关所有" + str(len(BADA_MON_LIST)) + "层！" + str(BUFFER_TIME) + "秒后传送回城"
                    player.Connection.ReceiveChat(tip, MessageType.System)
                    player.GiveItem("100元红包", 2)
                    #player.GiveItem("蓝玫瑰", 1)
                    SEnvir.Log(str(player_name) + "通关八大暗影副本")
                    SEnvir.ScheduledCall("Npc.BOSS副本.八大暗影.TeleportBackToTown", SEnvir.Now.AddSeconds(BUFFER_TIME), player)
                else:
                    MapSetTempV(fuben_map, TEMPV_WAVE_NUM, next_wave)
                    SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
                    tip = "成功通过第" + str(current_wave) + "层！" + str(BUFFER_TIME) + "秒后传送到下一层"
                    player.Connection.ReceiveChat(tip, MessageType.System)
                    SEnvir.ScheduledCall("Npc.BOSS副本.八大暗影.TeleportToNextLevel", SEnvir.Now.AddSeconds(BUFFER_TIME), (player, fuben_map))
            else:
                SpawnMonsters(fuben_map)
                SEnvir.DelayCall("Npc.BOSS副本.八大暗影.CheckFuben", 5, (fuben_map, current_wave, player), player)
        else:
            SEnvir.DelayCall("Npc.BOSS副本.八大暗影.CheckFuben", 5, (fuben_map, current_wave, player), player)
            
    except Exception as e:
        SEnvir.Log("CheckFuben-副本检查异常：" + str(e))
        try:
            player = args[2]
            SafeRemoveScript("Npc.BOSS副本.八大暗影.CheckFuben", player)
            # 优化：异常时，释放进程池名额
            player_id = getattr(player, "ObjectID", 0)
            try:
                player_id = int(player_id)
            except:
                player_id = 0
            if player_id and player_id > 0:
                fuben_pool.leave_fuben(player_id)
        except:
            pass

# 注册事件
try:
    MapEvent.add_listener(BADA_FUBEN_MAP_INDEX, "OnEnter", OnEnter)
    MapEvent.add_listener(BADA_FUBEN_MAP_INDEX, "OnLeave", OnLeave)
    MapEvent.add_listener(BADA_FUBEN_MAP_INDEX, "OnCreate", OnCreate)
except Exception as e:
    SEnvir.Log("事件注册异常：" + str(e))
