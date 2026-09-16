# -*- coding: utf-8 -*-
"""
游戏规则管理系统
用于定义和管理各种游戏规则
"""

import os
import json
import time
from datetime import datetime

class GameRules:
    def __init__(self):
        self.rules = {}
        self.load_rules()
    
    def load_rules(self):
        """加载规则配置"""
        rules_file = "Scripts/rules_config.json"
        if os.path.exists(rules_file):
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    self.rules = json.load(f)
            except:
                self.create_default_rules()
        else:
            self.create_default_rules()
    
    def create_default_rules(self):
        """创建默认规则"""
        self.rules = {
            "level": {
                "max_level": 50,
                "exp_rate": 1.0,
                "level_rewards": {}
            },
            "economy": {
                "max_gold": 999999999,
                "max_game_gold": 999999,
                "gold_rate": 1.0,
                "trade_tax": 0.05
            },
            "combat": {
                "pk_mode": 1,
                "allow_pk": True,
                "pk_penalty": 0.1,
                "safe_zones": []
            },
            "items": {
                "drop_rate": 1.0,
                "max_durability": 100,
                "repair_cost_rate": 1.0
            },
            "social": {
                "allow_trade": True,
                "allow_mail": True,
                "allow_guild": True,
                "max_guild_members": 50
            },
            "events": {
                "double_exp_weekend": False,
                "special_drop_event": False,
                "event_start_time": "",
                "event_end_time": ""
            }
        }
        self.save_rules()
    
    def save_rules(self):
        """保存规则配置"""
        rules_file = "Scripts/rules_config.json"
        try:
            with open(rules_file, 'w', encoding='utf-8') as f:
                json.dump(self.rules, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存规则配置失败: {e}")
    
    def get_rule(self, category, key, default=None):
        """获取规则值"""
        return self.rules.get(category, {}).get(key, default)
    
    def set_rule(self, category, key, value):
        """设置规则值"""
        if category not in self.rules:
            self.rules[category] = {}
        self.rules[category][key] = value
        self.save_rules()
    
    def check_level_rule(self, player_level):
        """检查等级规则"""
        max_level = self.get_rule("level", "max_level", 50)
        return player_level <= max_level
    
    def check_gold_rule(self, gold_amount):
        """检查金币规则"""
        max_gold = self.get_rule("economy", "max_gold", 999999999)
        return gold_amount <= max_gold
    
    def check_pk_rule(self, player_name, target_name):
        """检查PK规则"""
        allow_pk = self.get_rule("combat", "allow_pk", True)
        safe_zones = self.get_rule("combat", "safe_zones", [])
        
        if not allow_pk:
            return False, "PK功能已禁用"
        
        # 检查安全区
        # 这里需要根据实际地图信息来判断
        return True, "PK检查通过"
    
    def apply_exp_rate(self, base_exp):
        """应用经验倍率"""
        exp_rate = self.get_rule("level", "exp_rate", 1.0)
        return int(base_exp * exp_rate)
    
    def apply_drop_rate(self, base_drop_rate):
        """应用掉落倍率"""
        drop_rate = self.get_rule("items", "drop_rate", 1.0)
        return base_drop_rate * drop_rate

# 全局规则实例
game_rules = GameRules()

def get_game_rules():
    """获取游戏规则实例"""
    return game_rules

def reload_rules():
    """重新加载规则"""
    global game_rules
    game_rules = GameRules()
    return game_rules 