# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import Server



# =============================================================================
# 定义商品配置字典
# =============================================================================
MERCHANT_CONFIG = {
    # 诺玛勋章配置
    'nuoma_medals': {
        11: '诺玛勋章（火）',
        12: '诺玛勋章（雷）', 
        13: '诺玛勋章（风）',
        14: '诺玛勋章（防御）',
        15: '诺玛勋章（魔御）'
    },
    
    # 勋章升级配置（10种完整勋章）
    'medal_upgrades': {
        311: ('破坏勋章', '强化破坏勋章', 2000000),
        312: ('自然勋章', '强化自然勋章', 2000000),
        313: ('灵魂勋章', '强化灵魂勋章', 2000000),
        314: ('火之勋章', '强化火之勋章', 2000000),
        315: ('冰之勋章', '强化冰之勋章', 2000000),
        316: ('雷之勋章', '强化雷之勋章', 2000000),
        317: ('风之勋章', '强化风之勋章', 2000000),
        318: ('神圣勋章', '强化神圣勋章', 2000000),
        319: ('暗黑勋章', '强化暗黑勋章', 2000000),
        3110: ('幻影勋章', '强化幻影勋章', 2000000)
    },
    
    # 诺玛书籍鉴定配置
    'nuoma_books': {
        'warrior': {
            21: {'name': '铁布衫', 'cost': 12880000},
            22: {'name': '十方斩', 'cost': 9980000},
            23: {'name': '破血狂杀', 'cost': 16880000},
            24: {'name': '乾坤大挪移', 'cost': 9980000},
            25: {'name': '斗转星移', 'cost': 9980000}
        },
        'wizard': {
            26: {'name': '魄冰刺', 'cost': 9980000},
            27: {'name': '怒神霹雳', 'cost': 12880000},
            28: {'name': '凝血离魂', 'cost': 16880000},
            29: {'name': '焰天火雨', 'cost': 12880000}
        },
        'taoist': {
            30: {'name': '云寂术', 'cost': 9980000},
            31: {'name': '妙影无踪', 'cost': 16880000},
            32: {'name': '阴阳法环', 'cost': 16880000},
            33: {'name': '移花接玉', 'cost': 9980000}
        }
    },
    
    # 特色称号配置
    'special_titles': {
        51: {'name': '幽灵船长', 'buff_id': 122, 'global_var': 'GV_PLAYER_BUFF1', 'description': '强元素雷+1，强元素暗黑+1，生命值+1%'},
        52: {'name': '诺玛苦僧', 'buff_id': 123, 'global_var': 'GV_PLAYER_BUFF2', 'description': '灵魂0-2，自然0-2，破坏0-3'},
        53: {'name': '撸牛博士', 'buff_id': 124, 'global_var': 'GV_PLAYER_BUFF3', 'description': '经验加成+10，背包负重+300'},
        54: {'name': '黑度烧客', 'buff_id': 125, 'global_var': 'GV_PLAYER_BUFF4', 'description': '攻击元素火+2，经验加成+20%，火墙伤害+10%'},
        55: {'name': '祖玛阁主', 'buff_id': 126, 'global_var': 'GV_PLAYER_BUFF5', 'description': '生命值+2%，暴击几率+1%，魔法躲避+1%'},
        56: {'name': '矿洞猎手', 'buff_id': 127, 'global_var': 'GV_PLAYER_BUFF6', 'description': '采矿成功率+50%'},
        57: {'name': '动物园长', 'buff_id': 128, 'global_var': 'GV_PLAYER_BUFF7', 'description': '宠物背包+10格，宠物负重+200'},
        501: {'name': '战天斗地', 'buff_id': 129, 'global_var': 'GV_PLAYER_BUFF8', 'class_required': 'Warrior', 'description': '破坏2-5，攻击速度+1'},
        502: {'name': '道骨仙风', 'buff_id': 130, 'global_var': 'GV_PLAYER_BUFF9', 'class_required': 'Taoist', 'description': '灵魂0-5，物防0-5，魔防0-5'},
        503: {'name': '法海无边', 'buff_id': 131, 'global_var': 'GV_PLAYER_BUFF10', 'class_required': 'Wizard', 'description': '自然0-5，生命+100，回蓝+20%'},
        504: {'name': '傲视群雄', 'buff_id': 133, 'global_var': 'GV_PLAYER_BUFF11', 'level_required': 60, 'description': '攻击速度+2，生命值+2%，暴击几率+2%，暴击伤害+2%，全系列魔法0-5，破坏0-2'}
    },
    
    # 武器幻化配置
    'weapon_illusion': {
        'normal': {
            621: '木剑幻化卷',
            622: '青铜斧幻化卷',
            623: '匕首幻化卷',
            624: '乌木剑幻化卷',
            625: '铁剑幻化卷',
            626: '半月幻化卷'
        },
        'advanced': {
            631: {'name': '霹雷幻化卷', 'cost': 38, 'global_var': 'GV_PLAYER_HUANHUAJUAN1'},
            632: {'name': '嗜魂法杖幻化卷', 'cost': 38, 'global_var': 'GV_PLAYER_HUANHUAJUAN2'},
            633: {'name': '龙纹剑幻化卷', 'cost': 38, 'global_var': 'GV_PLAYER_HUANHUAJUAN3'},
            634: {'name': '屠龙幻化卷', 'cost': 48, 'global_var': 'GV_PLAYER_HUANHUAJUAN4'},
            635: {'name': '铁轮幻化卷', 'cost': 48, 'global_var': 'GV_PLAYER_HUANHUAJUAN5'},
            636: {'name': '逍遥扇幻化卷', 'cost': 48, 'global_var': 'GV_PLAYER_HUANHUAJUAN6'},
            637: {'name': '破山剑幻化卷', 'cost': 58, 'global_var': 'GV_PLAYER_HUANHUAJUAN7'},
            638: {'name': '天神法杖幻化卷', 'cost': 58, 'global_var': 'GV_PLAYER_HUANHUAJUAN8'},
            639: {'name': '泰轮拂尘幻化卷', 'cost': 58, 'global_var': 'GV_PLAYER_HUANHUAJUAN9'}
        }
    },
    
    # 坐骑幻化配置
    'mount_illusion': {
        71: {'name': '烈焰幻化卷', 'cost': 888},
        72: {'name': '追风幻化卷', 'cost': 888},
        73: {'name': '雷霆幻化卷', 'cost': 888},
        74: {'name': '赤兔幻化卷', 'cost': 888}
    },
    
    # 衣服幻化配置
    'armor_illusion': {
        921: '布衣幻化卷',
        922: '轻型盔甲幻化卷',
        923: '重盔甲幻化卷',
        924: '魔法长袍幻化卷',
        925: '灵魂战衣幻化卷'
    },
    
    # 碎片合成配置
    'fragment_synthesis': {
        81: {'name': '白色口哨', 'fragment_name': '白色口哨碎片', 'fragment_count': 5, 'result_name': '白色口哨'},
        82: {'name': '幸运斗笠', 'fragment_name': '幸运斗笠碎片', 'fragment_count': 48, 'result_name': '幸运斗笠'},

    }
}

# =============================================================================
# 辅助函数
# =============================================================================

def check_inventory_space(sender):
    """检查背包空间 - 对于可叠加物品只需要一个空格"""
    return GetInventoryCount(sender) >= 1


def handle_nuoma_medal_purchase(sender, medal_id):
    """处理诺玛勋章购买"""
    if sender.GameGold < 10:
        return "你没有足够的元宝，无法购买。\n\n[返回主菜单:999]"
    
    if sender.GetItemCount("遗物") < 200:
        return "你没有足够的遗物，无法购买。\n\n[返回主菜单:999]"
    
    if not check_inventory_space(sender):
        return "你的包裹空间不足，需要至少一个空格。\n\n[返回主菜单:999]"
    
    try:
        medal_name = MERCHANT_CONFIG['nuoma_medals'][medal_id]
    except KeyError:
        return "未知的勋章ID。\n\n[返回主菜单:999]"
    
    SubGameGold(sender, 10)
    sender.TakeItem("遗物", 200)
    sender.GiveItem(medal_name, 1)
    return "购买成功。\n\n[返回主菜单:999]"


def handle_nuoma_book_purchase(sender, book_id):
    """处理诺玛书籍购买"""
    # 查找书籍配置
    book_config = None
    for class_type in ['warrior', 'wizard', 'taoist']:
        if book_id in MERCHANT_CONFIG['nuoma_books'][class_type]:
            book_config = MERCHANT_CONFIG['nuoma_books'][class_type][book_id]
            break
    
    if not book_config:
        return "未知的书籍ID。\n\n[返回主菜单:999]"
    
    if sender.Gold < book_config['cost']:
        return "喂！我没有说我不能免费传授武功吗？难道让我吃沙子活着吗？快点拿学费来！\n\n[返回主菜单:999]"
    
    if sender.GetItemCount(book_config['name']) < 1:
        return "请首先找到武功书......，不拿武功书来，却让我解释，真让人生气！\n\n[返回主菜单:999]"
    
    SubGold(sender, book_config['cost'])
    sender.TakeItem(book_config['name'], 1)
    sender.GiveItem(book_config['name'] + "（秘籍）", 1)
    return "还好成功了，下次请拿保存状态稍好的书来解释。\n\n[返回主菜单:999]"


def handle_special_title_purchase(sender, title_id):
    """处理特色称号购买"""
    try:
        title_config = MERCHANT_CONFIG['special_titles'][title_id]
    except KeyError:
        return "未知的称号ID。\n\n[返回主菜单:999]"
    
    # 检查职业要求
    if 'class_required' in title_config:
        if title_config['class_required'] == 'Warrior':
            if sender.Class != sender.Class.Warrior:
                return "你不是战士，无法购买。\n\n[返回主菜单:999]"
        elif title_config['class_required'] == 'Wizard':
            if sender.Class != sender.Class.Wizard:
                return "你不是法师，无法购买。\n\n[返回主菜单:999]"
        elif title_config['class_required'] == 'Taoist':
            if sender.Class != sender.Class.Taoist:
                return "你不是道士，无法购买。\n\n[返回主菜单:999]"
    
    # 检查等级要求
    if 'level_required' in title_config:
        if sender.Level < title_config['level_required']:
            return "你等级没有达到" + str(title_config['level_required']) + "级，无法购买。\n\n[返回主菜单:999]"
    
    if sender.Gold < 2880000:
        return "金币不足，无法购买。\n\n[返回主菜单:999]"
    
    if PlayerGetV(sender, GV_PLAYER_BUFFCOUNT) > 0:
        return "你已经购买过BUFF，无法重复购买。\n\n[返回主菜单:999]"
    
    # 获取全局变量ID
    if title_config['global_var'] == 'GV_PLAYER_BUFF1':
        global_var_id = GV_PLAYER_BUFF1
    elif title_config['global_var'] == 'GV_PLAYER_BUFF2':
        global_var_id = GV_PLAYER_BUFF2
    elif title_config['global_var'] == 'GV_PLAYER_BUFF3':
        global_var_id = GV_PLAYER_BUFF3
    elif title_config['global_var'] == 'GV_PLAYER_BUFF4':
        global_var_id = GV_PLAYER_BUFF4
    elif title_config['global_var'] == 'GV_PLAYER_BUFF5':
        global_var_id = GV_PLAYER_BUFF5
    elif title_config['global_var'] == 'GV_PLAYER_BUFF6':
        global_var_id = GV_PLAYER_BUFF6
    elif title_config['global_var'] == 'GV_PLAYER_BUFF7':
        global_var_id = GV_PLAYER_BUFF7
    elif title_config['global_var'] == 'GV_PLAYER_BUFF8':
        global_var_id = GV_PLAYER_BUFF8
    elif title_config['global_var'] == 'GV_PLAYER_BUFF9':
        global_var_id = GV_PLAYER_BUFF9
    elif title_config['global_var'] == 'GV_PLAYER_BUFF10':
        global_var_id = GV_PLAYER_BUFF10
    elif title_config['global_var'] == 'GV_PLAYER_BUFF11':
        global_var_id = GV_PLAYER_BUFF11
    else:
        return "未知的全局变量ID。\n\n[返回主菜单:999]"
    
    if GlobalGetV(global_var_id) > 0:
        return "你来晚一步，当前BUFF已被购买。\n\n[返回主菜单:999]"
    
    SubGold(sender, 2880000)
    sender.CustomBuffAdd(title_config['buff_id'])
    PlayerSetV(sender, GV_PLAYER_BUFFCOUNT, 1)
    GlobalSetV(global_var_id, 1)
    return "恭喜你购买成功，获得特色称号。\n\n[返回主菜单:999]"


def handle_special_title_remove(sender):
    """处理特色称号删除"""
    # 检查是否有buff
    if PlayerGetV(sender, GV_PLAYER_BUFFCOUNT) == 0:
        return "你没有特色称号，无法删除。\n\n[返回主菜单:999]"
    
    # 遍历所有可能的buff_id，找到当前玩家拥有的buff
    current_buff_id = None
    current_global_var_id = None
    
    for title_id, title_config in MERCHANT_CONFIG['special_titles'].items():
        # 获取对应的全局变量ID
        if title_config['global_var'] == 'GV_PLAYER_BUFF1':
            global_var_id = GV_PLAYER_BUFF1
        elif title_config['global_var'] == 'GV_PLAYER_BUFF2':
            global_var_id = GV_PLAYER_BUFF2
        elif title_config['global_var'] == 'GV_PLAYER_BUFF3':
            global_var_id = GV_PLAYER_BUFF3
        elif title_config['global_var'] == 'GV_PLAYER_BUFF4':
            global_var_id = GV_PLAYER_BUFF4
        elif title_config['global_var'] == 'GV_PLAYER_BUFF5':
            global_var_id = GV_PLAYER_BUFF5
        elif title_config['global_var'] == 'GV_PLAYER_BUFF6':
            global_var_id = GV_PLAYER_BUFF6
        elif title_config['global_var'] == 'GV_PLAYER_BUFF7':
            global_var_id = GV_PLAYER_BUFF7
        elif title_config['global_var'] == 'GV_PLAYER_BUFF8':
            global_var_id = GV_PLAYER_BUFF8
        elif title_config['global_var'] == 'GV_PLAYER_BUFF9':
            global_var_id = GV_PLAYER_BUFF9
        elif title_config['global_var'] == 'GV_PLAYER_BUFF10':
            global_var_id = GV_PLAYER_BUFF10
        elif title_config['global_var'] == 'GV_PLAYER_BUFF11':
            global_var_id = GV_PLAYER_BUFF11
        else:
            continue
        
        # 检查是否是当前玩家购买的buff
        if GlobalGetV(global_var_id) > 0:
            current_buff_id = title_config['buff_id']
            current_global_var_id = global_var_id
            break
    
    if current_buff_id is None:
        return "未找到你的特色称号信息。\n\n[返回主菜单:999]"
    
    # 删除buff
    sender.CustomBuffRemove(current_buff_id)
    PlayerSetV(sender, GV_PLAYER_BUFFCOUNT, 0)
    GlobalSetV(current_global_var_id, 0)
    
    return "特色称号删除成功。\n\n[返回主菜单:999]"


def handle_illusion_purchase(sender, illusion_id, illusion_type):
    """处理幻化购买"""
    try:
        if illusion_type == 'weapon_normal':
            item_name = MERCHANT_CONFIG['weapon_illusion']['normal'][illusion_id]
            cost = 10
        elif illusion_type == 'weapon_advanced':
            item_config = MERCHANT_CONFIG['weapon_illusion']['advanced'][illusion_id]
            item_name = item_config['name']
            cost = item_config['cost']
            
            # 检查限量
            if item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN1':
                global_var_id = GV_PLAYER_HUANHUAJUAN1
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN2':
                global_var_id = GV_PLAYER_HUANHUAJUAN2
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN3':
                global_var_id = GV_PLAYER_HUANHUAJUAN3
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN4':
                global_var_id = GV_PLAYER_HUANHUAJUAN4
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN5':
                global_var_id = GV_PLAYER_HUANHUAJUAN5
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN6':
                global_var_id = GV_PLAYER_HUANHUAJUAN6
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN7':
                global_var_id = GV_PLAYER_HUANHUAJUAN7
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN8':
                global_var_id = GV_PLAYER_HUANHUAJUAN8
            elif item_config['global_var'] == 'GV_PLAYER_HUANHUAJUAN9':
                global_var_id = GV_PLAYER_HUANHUAJUAN9
            else:
                return "未知的全局变量ID。\n\n[返回主菜单:999]"
            
            if GlobalGetV(global_var_id) > 2:
                return "你来晚一步，当前幻化卷已被购买一空。\n\n[返回主菜单:999]"
        elif illusion_type == 'mount':
            item_config = MERCHANT_CONFIG['mount_illusion'][illusion_id]
            item_name = item_config['name']
            cost = item_config['cost']
        elif illusion_type == 'armor':
            item_name = MERCHANT_CONFIG['armor_illusion'][illusion_id]
            cost = 28
        else:
            return "未知的幻化类型。\n\n[返回主菜单:999]"
    except KeyError:
        return "未知的幻化ID。\n\n[返回主菜单:999]"
    
    if sender.GetItemCount("幻化珠") < cost:
        return "你没有足够的幻化珠，无法兑换。\n\n[返回主菜单:999]"
    
    if not check_inventory_space(sender):
        return "你的包裹空间不足，需要至少一个空格。\n\n[返回主菜单:999]"
    
    sender.TakeItem("幻化珠", cost)
    sender.GiveItem(item_name, 1)
    
    # 如果是高级武器幻化，更新全局变量
    if illusion_type == 'weapon_advanced':
        GlobalSetV(global_var_id, GlobalGetV(global_var_id) + 1)
    
    # 弹出成功提示对话框
    sender.NPCConfirmationBox("兑换成功，获得" + item_name + "。", 999)
    return ""


def handle_medal_upgrade(sender, medal_id):
    """处理勋章升级"""
    try:
        medal_config = MERCHANT_CONFIG['medal_upgrades'][medal_id]
        original_name, upgraded_name, cost = medal_config
    except KeyError:
        return "未知的勋章ID。\n\n[返回主菜单:999]"
    
    # 查找符合条件的勋章
    found_item = None
    for i in range(Globals.InventorySize):
        item = sender.Inventory[i]
        if item and item.Info.ItemName == original_name and item.CurrentDurability > 14000:
            found_item = item
            break
    
    if not found_item:
        return "背包中没有未使用的" + original_name + "！\n\n[返回主菜单:999]"
    
    if sender.Gold < cost:
        return "金币不足，需要200万金币！\n\n[返回主菜单:999]"
    
    # 执行升级
    sender.TakeItem(found_item, 1)
    SubGold(sender, cost)
    sender.GiveItem(upgraded_name, 1)
    return upgraded_name + "强化成功！\n\n[返回主菜单:999]"


def handle_illusion_reset(sender, equipment_type):
    """处理幻化重置"""
    if sender.Gold < 880000:
        return "你没有足够的金币。\n\n[返回主菜单:999]"
    
    if equipment_type == 'weapon':
        item = sender.Equipment[int(EquipmentSlot.Weapon)]
        slot = 0
    elif equipment_type == 'armor':
        item = sender.Equipment[int(EquipmentSlot.Armour)]
        slot = 1
    else:
        return "未知的装备类型。\n\n[返回主菜单:999]"
    
    if not item:
        return "你没有装备" + ("武器" if equipment_type == 'weapon' else "衣服") + "。\n\n[返回主菜单:999]"
    
    if item.Stats[Stat.Illusion] == 0:
        return "你的" + ("武器" if equipment_type == 'weapon' else "衣服") + "没有幻化属性。\n\n[返回主菜单:999]"
    
    SubGold(sender, 880000)
    item.RemoveStat(Stat.Illusion, StatSource.Enhancement)
    sender.SendShapeUpdate()
    
    # 构建封包刷新装备
    itemStatsRefreshed = System.Activator.CreateInstance(Network.ServerPackets.ItemStatsRefreshed)
    stats = System.Activator.CreateInstance(Stats, item.Stats)
    itemStatsRefreshed.GridType = GridType.Equipment
    itemStatsRefreshed.Slot = slot
    itemStatsRefreshed.NewStats = stats
    itemStatsRefreshed.FullItemStats = item.ToClientInfo().FullItemStats
    sender.Enqueue(itemStatsRefreshed)
    
    return "你的幻化" + ("武器" if equipment_type == 'weapon' else "衣服") + "重置成功。\n\n[返回主菜单:999]"


def handle_fragment_synthesis(sender, synthesis_id):
    """处理碎片合成"""
    try:
        synthesis_config = MERCHANT_CONFIG['fragment_synthesis'][synthesis_id]
    except KeyError:
        return "未知的合成ID。\n\n[返回主菜单:999]"
    
    fragment_name = synthesis_config['fragment_name']
    fragment_count = synthesis_config['fragment_count']
    result_name = synthesis_config['result_name']
    
    # 检查碎片数量
    if sender.GetItemCount(fragment_name) < fragment_count:
        return "你的" + fragment_name + "不足，需要" + str(fragment_count) + "个，无法合成。\n\n[返回:8]"
    
    # 检查背包空间
    if not check_inventory_space(sender):
        return "你的包裹空间不足，需要至少一个空格。\n\n[返回:8]"
    
    # 执行合成
    sender.TakeItem(fragment_name, fragment_count)
    sender.GiveItem(result_name, 1)
    
    # 弹出成功提示对话框
    sender.NPCConfirmationBox("合成成功！获得" + result_name + "。", 8)
    return ""


# =============================================================================
# 主函数
# =============================================================================
def OnClick(args):
    """
    本函数为程序调用的固定格式 函数名和参数数量不要修改
    OnClick(Self, Sender, Menu)
    
    参数:
        Self：NPC的类
        Sender：玩家的类
        Menu：菜单的类
    """
    Self = args[0]
    Sender = args[1]
    Menu = args[2]
    Dict = {}
    
    say = ''

    # =============================================================================
    # 主菜单
    # =============================================================================
    if Menu == 0 or Menu == 999:
        say = """这里稀奇古怪的产品都有，欢迎光临。

[诺玛勋章:1]      [诺玛书籍鉴定:2]

[特色称号:5]      [武器幻化:6]

[坐骑幻化:7]      [衣服幻化:9]

[勋章升级:111]      [新春时装:10]

[碎片合成:8]"""
    
    # =============================================================================
    # 诺玛勋章系统
    # =============================================================================
    elif Menu == 1:
        say = """这里有各类诺玛勋章，需要消耗10元宝+200遗物，是否买个？

<font color=\"0xff00ff00\">诺玛勋章属性介绍：</font>

<font color=\"0xff00ff00\">诺玛勋章（火）</font>：强元素：火*1，光照范围+25
<font color=\"0xff00ff00\">诺玛勋章（雷）</font>：强元素：雷*1，光照范围+25
<font color=\"0xff00ff00\">诺玛勋章（风）</font>：强元素：风*1，光照范围+25
<font color=\"0xff00ff00\">诺玛勋章（防御）</font>：物理防御5-5，光照范围+25
<font color=\"0xff00ff00\">诺玛勋章（魔御）</font>：魔法防御5-5，光照范围+25

[诺玛勋章（火）:11]    [诺玛勋章（雷）:12]    [诺玛勋章（风）:13]
[诺玛勋章（防御）:14]  [诺玛勋章（魔御）:15]

[返回主菜单:999]"""
    
    elif Menu in [11, 12, 13, 14, 15]:
        say = handle_nuoma_medal_purchase(Sender, Menu)
    
    # =============================================================================
    # 勋章升级系统
    # =============================================================================
    elif Menu == 111:
        say = """勋章升级说明：
每种勋章升级需要200万金币，需要背包中有未使用的原勋章。

[破坏勋章:311]  [自然勋章:312]  [灵魂勋章:313]
[火之勋章:314]  [冰之勋章:315]  [雷之勋章:316]
[风之勋章:317]  [神圣勋章:318]  [暗黑勋章:319]
[幻影勋章:3110]

[返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['medal_upgrades']:
        say = handle_medal_upgrade(Sender, Menu)
    
    # =============================================================================
    # 诺玛书籍鉴定系统
    # =============================================================================
    elif Menu == 2:
        say = """花费大量的金币，可以百分百鉴定成功诺玛书籍，是否尝试下。

<font color="0xff00ff00">战士技能：</font>
[铁布衫:21]        需要花费<font color="0xff00ff00">1288万金币</font>
[十方斩:22]        需要花费<font color="0xff00ff00">998万金币</font>
[破血狂杀:23]      需要花费<font color="0xff00ff00">1688万金币</font>
[乾坤大挪移:24]    需要花费<font color="0xff00ff00">998万金币</font>
[斗转星移:25]      需要花费<font color="0xff00ff00">998万金币</font>

<font color="0xff00ff00">法师技能：</font>
[魄冰刺:26]        需要花费<font color="0xff00ff00">998万金币</font>
[怒神霹雳:27]      需要花费<font color="0xff00ff00">1288万金币</font>
[凝血离魂:28]      需要花费<font color="0xff00ff00">1688万金币</font>
[焰天火雨:29]      需要花费<font color="0xff00ff00">1288万金币</font>

<font color="0xff00ff00">道士技能：</font>
[云寂术:30]        需要花费<font color="0xff00ff00">998万金币</font>
[妙影无踪:31]      需要花费<font color="0xff00ff00">1688万金币</font>
[阴阳法环:32]      需要花费<font color="0xff00ff00">1688万金币</font>
[移花接玉:33]      需要花费<font color="0xff00ff00">998万金币</font>

[返回主菜单:999]"""
    
    elif Menu in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]:
        say = handle_nuoma_book_purchase(Sender, Menu)
    
    # =============================================================================
    # 特色称号系统
    # =============================================================================
    elif Menu == 5:
        say = """这里有各类特色称号，需要288万金币购买一个，
单BUFF只能单玩家获得，时效一星期。

<font color="0xff00ff00">称号属性介绍：</font>

幽灵船长：<font color="0xff00ff00">强元素雷+1，强元素暗黑+1，生命值+1%</font>
诺玛苦僧：<font color="0xff00ff00">灵魂0-2，自然0-2，破坏0-3</font>
撸牛博士：<font color="0xff00ff00">经验加成+10，背包负重+300</font>
黑度烧客：<font color="0xff00ff00">攻击元素火+2，经验加成+20%，火墙伤害+10%</font>
祖玛阁主：<font color="0xff00ff00">生命值+2%，暴击几率+1%，魔法躲避+1%</font>
矿洞猎手：<font color="0xff00ff00">采矿成功率+50%</font>
动物园长：<font color="0xff00ff00">宠物背包+10格，宠物负重+200</font>
战天斗地：<font color="0xff00ff00">破坏2-5，攻速+1</font>
道骨仙风：<font color="0xff00ff00">灵魂0-5，物防0-5，魔防0-5</font>
法海无边：<font color="0xff00ff00">自然0-5，生命+100，回蓝+20%</font>
傲视群雄：<font color="0xff00ff00">攻速+2，生命值+2%，暴击几率+2%，暴击伤害+2%，全系列魔法0-5，破坏0-2</font>

[幽灵船长:51]    [诺玛苦僧:52]    [撸牛博士:53]    [黑度烧客:54]
[祖玛阁主:55]    [矿洞猎手:56]    [动物园长:57]

[战天斗地（战士专用）:501]    [道骨仙风（道士专用）:502]
[法海无边（法师专用）:503]    [傲视群雄（60级专用）:504]

[删除特色称号:505]

[返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['special_titles']:
        say = handle_special_title_purchase(Sender, Menu)
    
    elif Menu == 505:
        say = handle_special_title_remove(Sender)
    
    # =============================================================================
    # 武器幻化系统
    # =============================================================================
    elif Menu == 6:
        say = """武器幻化说明：
幻化卷<font color=\"0xff00ff00\">消耗定量</font>幻化珠，幻化时效<font color=\"0xff00ff00\">1</font>个月，
普通幻化卷<font color=\"0xff00ff00\">不限量</font>，高级幻化卷每种每月限量购买<font color=\"0xff00ff00\">3</font>个。

<font color=\"0xff00ff00\">提示：</font>批量兑换幻化珠，输入数量即可！<font color=\"0xff00ff00\">价格：8.8万金币/个</font>

[幻化珠兑换:611]     [重置幻化:64]

[兑换普通幻化卷:62]

[兑换高级幻化卷:63]

[返回主菜单:999]"""
    

    
    elif Menu == 612:
        # 这个菜单已经不需要了，因为现在使用弹出对话框
        say = ""
    
    elif Menu == 611:
        # 显示输入提示
        say = """请输入要兑换的幻化珠数量（1-888）：

<font color=\"0xff00ff00\">点击下方按钮输入数量</font>

[输入兑换数量:611]

[返回:6]"""
        
        # 调用输入框功能
        Sender.PyInputBox("请输入要兑换的幻化珠数量（1-888）：", "Npc.比奇城.古怪学者.Input612")
    
    elif Menu == 613:
        # 显示确认对话框
        say = """确认兑换幻化珠：

<font color=\"0xff00ff00\">点击下方按钮确认兑换</font>

[确认兑换:614]

[返回:6]"""
        
        # 弹出确认对话框
        Sender.NPCConfirmationBox("确认要兑换幻化珠吗？", 614)
    
    elif Menu == 614:
        # 处理确认兑换 - 现在使用弹出对话框，不需要聊天框提示
        say = ""
    

    

    

    
    elif Menu == 62:
        say = """兑换价格:10个幻化珠

[木剑幻化卷:621]      [青铜斧幻化卷:622]    [匕首幻化卷:623]
[乌木剑幻化卷:624]    [铁剑幻化卷:625]      [半月幻化卷:626]

[返回:6]    [返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['weapon_illusion']['normal']:
        say = handle_illusion_purchase(Sender, Menu, 'weapon_normal')
    
    elif Menu == 63:
        say = """兑换限制:一种幻化卷每个月最多兑换3张

兑换价格:38个幻化珠
[霹雷幻化卷:631]      [嗜魂法杖幻化卷:632]    [龙纹剑幻化卷:633]

兑换价格:48个幻化珠
[屠龙幻化卷:634]      [铁轮幻化卷:635]        [逍遥扇幻化卷:636]

兑换价格:58个幻化珠
[破山剑幻化卷:637]    [天神法杖幻化卷:638]    [泰轮拂尘幻化卷:639]

[返回:6]    [返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['weapon_illusion']['advanced']:
        say = handle_illusion_purchase(Sender, Menu, 'weapon_advanced')
    
    elif Menu == 64:
        say = """你确定要重置已经幻化的武器吗？
重置幻化武器收费<font color=\"0xff00ff00\">88万</font>金币。

[确定重置:641]    [返回:6]    [返回主菜单:999]"""
    
    elif Menu == 641:
        say = handle_illusion_reset(Sender, 'weapon')
    
    # =============================================================================
    # 坐骑幻化系统
    # =============================================================================
    elif Menu == 7:
        say = """坐骑幻化说明：
对应<font color=\"0xff00ff00\">黑马坐骑</font>使用指定幻化卷，
幻化卷消耗<font color=\"0xff00ff00\">888</font>幻化珠，幻化时效<font color=\"0xff00ff00\">永久</font>。

<font color=\"0xff00ff00\">提示：</font>批量兑换幻化珠，输入数量即可！<font color=\"0xff00ff00\">价格：8.8万金币/个</font>

[幻化珠兑换:611]

[兑换烈焰幻化卷:71]    [兑换追风幻化卷:72]
[兑换雷霆幻化卷:73]    [兑换赤兔幻化卷:74]

[返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['mount_illusion']:
        say = handle_illusion_purchase(Sender, Menu, 'mount')
    
    # =============================================================================
    # 衣服幻化系统
    # =============================================================================
    elif Menu == 9:
        say = """衣服幻化说明：
幻化卷<font color=\"0xff00ff00\">消耗定量</font>幻化珠，幻化时效<font color=\"0xff00ff00\">1</font>个月。

<font color=\"0xff00ff00\">提示：</font>批量兑换幻化珠，输入数量即可！<font color=\"0xff00ff00\">价格：8.8万金币/个</font>

[幻化珠兑换:611]     [重置幻化:94]

[兑换衣服幻化卷:92]

[返回主菜单:999]"""
    
    elif Menu == 92:
        say = """兑换价格:28个幻化珠

[布衣幻化卷:921]        [轻型盔甲幻化卷:922]    [重盔甲幻化卷:923]
[魔法长袍幻化卷:924]    [灵魂战衣幻化卷:925]

[返回:9]    [返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['armor_illusion']:
        say = handle_illusion_purchase(Sender, Menu, 'armor')
    
    elif Menu == 94:
        say = """你确定要重置已经幻化的衣服吗？
重置幻化衣服收费<font color=\"0xff00ff00\">88万</font>金币。

[确定重置:941]    [返回:9]    [返回主菜单:999]"""
    
    elif Menu == 941:
        say = handle_illusion_reset(Sender, 'armor')
    
    # =============================================================================
    # 新春时装系统
    # =============================================================================
    elif Menu == 10:
        say = """特色新年时装限量供应:
限购男女各<font color=\"0xff00ff00\">5</font>件，单人最多只能购买<font color=\"0xff00ff00\">1</font>次。
每件价格<font color=\"0xff00ff00\">1288万</font>金币，限时<font color=\"0xff00ff00\">1</font>个月。

[购买新春时装男款:101]  [购买新春时装女款:102]

[返回主菜单:999]"""
    
    elif Menu == 101:
        if Sender.Gold < 12880000:
            say = "金币不足，无法购买。\n\n[返回主菜单:999]"
        elif PlayerGetV(Sender, GV_PLAYER_XINNIANSZ) > 0:
            say = "你已经购买过新春时装，无法重复购买。\n\n[返回主菜单:999]"
        elif GlobalGetV(GV_PLAYER_QJXINNIANSZN) > 4:
            say = "你来晚一步，当前新春时装已被抢购一空。\n\n[返回主菜单:999]"
        else:
            if check_inventory_space(Sender):
                SubGold(Sender, 12880000)
                Sender.GiveItem("新春时装（男）", 1)
                PlayerSetV(Sender, GV_PLAYER_XINNIANSZ, 1)
                GlobalSetV(GV_PLAYER_QJXINNIANSZN, GlobalGetV(GV_PLAYER_QJXINNIANSZN) + 1)
                say = "恭喜你购买成功，获得新春时装。\n\n[返回主菜单:999]"
            else:
                say = "你的包裹空间不足，需要至少一个空格。\n\n[返回主菜单:999]"
    
    elif Menu == 102:
        if Sender.Gold < 12880000:
            say = "金币不足，无法购买。\n\n[返回主菜单:999]"
        elif PlayerGetV(Sender, GV_PLAYER_XINNIANSZ) > 0:
            say = "你已经购买过新春时装，无法重复购买。\n\n[返回主菜单:999]"
        elif GlobalGetV(GV_PLAYER_QJXINNIANSZV) > 4:
            say = "你来晚一步，当前新春时装已被抢购一空。\n\n[返回主菜单:999]"
        else:
            if check_inventory_space(Sender):
                SubGold(Sender, 12880000)
                Sender.GiveItem("新春时装（女）", 1)
                PlayerSetV(Sender, GV_PLAYER_XINNIANSZ, 1)
                GlobalSetV(GV_PLAYER_QJXINNIANSZV, GlobalGetV(GV_PLAYER_QJXINNIANSZV) + 1)
                say = "恭喜你购买成功，获得新春时装。\n\n[返回主菜单:999]"
            else:
                say = "你的包裹空间不足，需要至少一个空格。\n\n[返回主菜单:999]"
    
    # =============================================================================
    # 碎片合成系统
    # =============================================================================
    elif Menu == 8:
        say = """碎片合成说明：
收集足够的碎片可以合成完整的装备，合成不需要消耗金币。

<font color="0xff00ff00">可合成物品：</font>

<font color="0xff00ff00">白色口哨</font>：需要5个白色口哨碎片
<font color="0xff00ff00">幸运斗笠</font>：需要48个幸运斗笠碎片  


[白色口哨合成:81]    [幸运斗笠合成:82]

[返回主菜单:999]"""
    
    elif Menu in MERCHANT_CONFIG['fragment_synthesis']:
        say = handle_fragment_synthesis(Sender, Menu)
    


    Dict['Say'] = say                         # 定义聊天框对话内容
    return Dict


# =============================================================================
# 注册事件监听器
# =============================================================================
NpcEvent.add_listener(385, "OnClick", OnClick)



# 注册输入框回调函数
def Input612(params):
    """处理幻化珠兑换输入框回调"""
    sender = params[0]
    user_input = params[1] if len(params) > 1 else None
    
    if not user_input:
        sender.PyInputBox("请输入要兑换的幻化珠数量（1-888）：", "Npc.比奇城.古怪学者.Input612")
        return
    
    try:
        quantity = int(user_input)
        
        # 限制最大兑换数量，避免刷金币
        if quantity > 888:
            sender.NPCConfirmationBox("错误：单次最多只能兑换888个幻化珠。", 611)
        elif quantity <= 0:
            sender.NPCConfirmationBox("错误：请输入有效的数量。", 611)
        else:
            # 直接处理购买逻辑
            total_cost = quantity * 88000
            
            if sender.Gold < total_cost:
                sender.NPCConfirmationBox("错误：你没有足够的金币，需要{}金币。".format(total_cost), 611)
            else:
                # 检查背包空间 - 幻化珠可以叠加，只需要一个空格
                if check_inventory_space(sender):
                    # 直接执行购买
                    SubGold(sender, total_cost)
                    sender.GiveItem("幻化珠", quantity)
                    # 弹出成功提示对话框
                    sender.NPCConfirmationBox("兑换成功！获得{}个幻化珠。".format(quantity), 614)
                else:
                    # 弹出错误提示对话框
                    sender.NPCConfirmationBox("错误：你的包裹空间不足，需要至少一个空格。", 611)
    except ValueError:
        sender.NPCConfirmationBox("错误：请输入有效的数字。", 611)