# -*- coding: utf-8 -*-
"""
物品补丁定位使用示例
演示如何在NPC对话或其他场景中使用ItemPatchLocator
"""

from Globals import *
from Defines import *
import sys
sys.path.append('Scripts/Utils')
from ItemPatchLocator import GetItemPatchInfo, SearchItemsByName

def CreateItemImageTag(itemName):
	"""
	根据物品名称创建<img>标签
	参数:
		itemName: 物品名称
	返回:
		完整的<img>标签字符串，如果物品不存在则返回物品名称
	"""
	patchInfo = GetItemPatchInfo(itemName)
	
	if patchInfo is None:
		# 物品不存在，返回原始名称
		return itemName
	
	# 创建完整的<img>标签
	# 格式: <img file=文件枚举 idx=图像索引 item=物品名称 />
	imgTag = "<img file={} idx={} item={} />".format(
		patchInfo["file"],
		patchInfo["image"],
		patchInfo["name"]
	)
	
	return imgTag

def CreateItemDisplayText(itemName, showDetails=False):
	"""
	创建物品显示文本（包含图标和名称）
	参数:
		itemName: 物品名称
		showDetails: 是否显示详细信息
	返回:
		格式化的显示文本
	"""
	patchInfo = GetItemPatchInfo(itemName)
	
	if patchInfo is None:
		return "[未知物品] {}".format(itemName)
	
	# 基础显示：图标 + 名称
	displayText = "{} {}".format(
		CreateItemImageTag(itemName),
		patchInfo["name"]
	)
	
	if showDetails:
		# 添加详细信息
		displayText += "\n补丁文件: {}\n图像索引: {}".format(
			patchInfo["patch_path"],
			patchInfo["image"]
		)
	
	return displayText

def GenerateItemListDialog(itemNames, title="物品列表"):
	"""
	生成包含物品列表的NPC对话文本
	参数:
		itemNames: 物品名称列表
		title: 对话标题
	返回:
		NPC对话格式的文本
	"""
	dialogText = "{}\n\n".format(title)
	
	for itemName in itemNames:
		patchInfo = GetItemPatchInfo(itemName)
		if patchInfo is not None:
			# 添加物品图标和名称
			dialogText += "{} {}\n".format(
				CreateItemImageTag(itemName),
				patchInfo["name"]
			)
		else:
			# 物品不存在
			dialogText += "[未找到] {}\n".format(itemName)
	
	dialogText += "\n[确定:0]"
	return dialogText

def FindItemsByType(itemType):
	"""
	根据物品类型查找物品（示例函数）
	注意：这需要遍历所有物品，性能开销较大
	"""
	try:
		matchedItems = []
		for i in range(SEnvir.ItemInfoList.Count):
			itemInfo = SEnvir.ItemInfoList[i]
			if itemInfo is not None and str(itemInfo.ItemType) == itemType:
				matchedItems.append(itemInfo.ItemName)
				if len(matchedItems) >= 10:  # 限制结果数量
					break
		
		return matchedItems
		
	except Exception as e:
		SEnvir.Log("查找物品类型时发生错误: {}".format(str(e)))
		return []

# 使用示例
def ExampleUsage():
	"""
	使用示例
	"""
	SEnvir.Log("=== 物品补丁定位工具使用示例 ===")
	
	# 示例1: 获取单个物品的补丁信息
	SEnvir.Log("\n1. 获取物品补丁信息:")
	itemName = "金币"
	patchInfo = GetItemPatchInfo(itemName)
	if patchInfo:
		SEnvir.Log("物品: {} -> 图像索引: {}, 补丁: {}".format(
			patchInfo["name"], patchInfo["image"], patchInfo["patch_path"]
		))
	
	# 示例2: 创建物品图标标签
	SEnvir.Log("\n2. 创建图标标签:")
	imgTag = CreateItemImageTag("铁剑")
	SEnvir.Log("铁剑的图标标签: {}".format(imgTag))
	
	# 示例3: 搜索物品
	SEnvir.Log("\n3. 搜索包含'药'的物品:")
	potionItems = SearchItemsByName("药")
	for item in potionItems[:3]:  # 只显示前3个
		SEnvir.Log("- {} (图像: {})".format(item["name"], item["image"]))
	
	# 示例4: 生成NPC对话
	SEnvir.Log("\n4. 生成NPC对话示例:")
	testItems = ["金币", "铁剑", "红药"]
	dialogText = GenerateItemListDialog(testItems, "商店物品")
	SEnvir.Log("对话文本:\n{}".format(dialogText))

if __name__ == "__main__":
	ExampleUsage()