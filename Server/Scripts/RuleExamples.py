# -*- coding: utf-8 -*-
"""
规则应用示例
展示如何在各种游戏事件中应用规则
"""

from GameRules import get_game_rules

def on_player_level_up(player, new_level):
    """玩家升级事件"""
    rules = get_game_rules()
    
    # 检查等级限制
    if not rules.check_level_rule(new_level):
        return False, f"等级 {new_level} 超过服务器限制"
    
    # 应用经验倍率
    base_exp = 1000  # 基础经验
    actual_exp = rules.apply_exp_rate(base_exp)
    
    # 检查等级奖励
    level_rewards = rules.get_rule("level", "level_rewards", {})
    if str(new_level) in level_rewards:
        reward = level_rewards[str(new_level)]
        # 给予等级奖励
        pass
    
    return True, f"升级成功，获得经验 {actual_exp}"

def on_player_gain_gold(player, gold_amount):
    """玩家获得金币事件"""
    rules = get_game_rules()
    
    # 检查金币上限
    if not rules.check_gold_rule(player.gold + gold_amount):
        return False, "金币数量超过服务器限制"
    
    # 应用金币倍率
    gold_rate = rules.get_rule("economy", "gold_rate", 1.0)
    actual_gold = int(gold_amount * gold_rate)
    
    return True, f"获得金币 {actual_gold}"

def on_player_pk(player, target):
    """玩家PK事件"""
    rules = get_game_rules()
    
    # 检查PK规则
    pk_allowed, message = rules.check_pk_rule(player.name, target.name)
    if not pk_allowed:
        return False, message
    
    # 应用PK惩罚
    pk_penalty = rules.get_rule("combat", "pk_penalty", 0.1)
    # 处理PK惩罚逻辑
    pass
    
    return True, "PK成功"

def on_item_drop(player, item, base_drop_rate):
    """物品掉落事件"""
    rules = get_game_rules()
    
    # 应用掉落倍率
    actual_drop_rate = rules.apply_drop_rate(base_drop_rate)
    
    # 检查耐久度规则
    max_durability = rules.get_rule("items", "max_durability", 100)
    if hasattr(item, 'durability'):
        item.durability = min(item.durability, max_durability)
    
    return True, f"掉落率: {actual_drop_rate}"

def on_player_trade(player1, player2, item, price):
    """玩家交易事件"""
    rules = get_game_rules()
    
    # 检查交易是否允许
    allow_trade = rules.get_rule("social", "allow_trade", True)
    if not allow_trade:
        return False, "交易功能已禁用"
    
    # 应用交易税率
    trade_tax = rules.get_rule("economy", "trade_tax", 0.05)
    tax_amount = int(price * trade_tax)
    actual_price = price - tax_amount
    
    return True, f"交易成功，税率: {trade_tax*100}%，实际价格: {actual_price}"

def on_guild_create(guild_name, leader):
    """创建行会事件"""
    rules = get_game_rules()
    
    # 检查行会功能是否允许
    allow_guild = rules.get_rule("social", "allow_guild", True)
    if not allow_guild:
        return False, "行会功能已禁用"
    
    return True, "行会创建成功"

def on_guild_join(guild, player):
    """加入行会事件"""
    rules = get_game_rules()
    
    # 检查行会成员上限
    max_members = rules.get_rule("social", "max_guild_members", 50)
    if len(guild.members) >= max_members:
        return False, "行会成员已满"
    
    return True, "加入行会成功"

def check_event_status():
    """检查活动状态"""
    rules = get_game_rules()
    
    # 检查双倍经验活动
    double_exp = rules.get_rule("events", "double_exp_weekend", False)
    if double_exp:
        # 临时提高经验倍率
        rules.set_rule("level", "exp_rate", 2.0)
    
    # 检查特殊掉落活动
    special_drop = rules.get_rule("events", "special_drop_event", False)
    if special_drop:
        # 临时提高掉落倍率
        rules.set_rule("items", "drop_rate", 2.0)
    
    return True, "活动状态检查完成"

def reload_game_rules():
    """重新加载游戏规则"""
    from GameRules import reload_rules
    rules = reload_rules()
    return True, "规则重新加载成功" 