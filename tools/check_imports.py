######################載入套件######################
"""
匯入檢查工具
用於驗證專案的所有模組匯入是否正常運作
並測試基本物件的創建和功能
"""
import sys
# 將專案根目錄加入 Python 路徑，確保可以匯入專案模組
sys.path.append('.')

# 匯入所有遊戲實體類別
from src.entities.ball import Ball
from src.entities.brick import Brick
from src.entities.tornado import Tornado
from src.entities.balloon import Balloon
from src.entities.paddle import Paddle

######################測試匯入######################
print('✅ 所有模組匯入成功')

######################測試球物件######################
# 建立一個白色球物件進行測試
b = Ball((255,255,255), 10, 50, 50)
print('球的半徑:', b.radius)

# 測試重置功能
b.reset_to(100, 100)
print('重置後球的位置:', b.x, b.y)

######################測試磚塊物件######################
# 建立一個紅色磚塊進行測試
brick = Brick(10, 10, 10, 20, (255,0,0))
print('磚塊初始狀態 is_hit:', brick.is_hit)

# 測試碰撞檢測
collision_result = brick.check_collision(15, 15)
print('碰撞檢測結果:', collision_result)
print('碰撞後磚塊狀態 is_hit:', brick.is_hit)

print('🎉 所有基本功能測試完成')
