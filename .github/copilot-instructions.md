# Breaking the Block - AI Coding Instructions

一個使用 Pygame 開發的打磚塊遊戲，具有龍捲風障礙物和勝利氣球慶祝效果。

## 專案架構

### 核心結構

- **main.py**: 入口點，動態匯入 `GameEngine` 避免靜態分析問題
- **src/game/game_engine.py**: 主要遊戲循環和狀態管理
- **src/entities/**: 遊戲物件類別（Ball、Brick、Paddle、Tornado、Balloon）
- **config/**: 遊戲設定和顏色常數
- **assets/images/**: 新版資源路徑，`image/` 為舊版相容路徑

### 執行方式

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 執行遊戲
python main.py
```

## 關鍵設計模式

### 遊戲物件繼承

- `Paddle` 繼承自 `Brick`，共享基本碰撞檢測
- 所有實體都有 `update(dt)` 和 `draw(screen)` 方法
- 使用 delta time (dt) 確保幀率無關的物理運算

### 資源載入模式

```python
# 優先載入新路徑，失敗時回退舊路徣
ball_img = load_image('assets/images/ball/ball.png') or load_image('image/41QWjX05doL.png')
```

### 狀態管理

- `GameEngine.game_won`: 控制勝利狀態和氣球生成
- `Ball.is_launched`: 控制球是否黏在板子上
- `Brick.is_hit`: 磚塊消失狀態

## 物理系統

### 球的行為

- 未發射時黏在板子中央上方
- 發射角度預設 -60° (左上方)
- 與板子碰撞時根據撞擊位置調整水平速度
- 磚塊碰撞後速度微增 1.02x

### 龍捲風系統

- 隨機生成間隔 5-10 秒
- 螺旋形視覺效果使用 `math.sin` 和漸變灰色
- 碰到球時觸發遊戲重啟

### 勝利慶祝

- 所有磚塊消失後生成上升氣球
- 氣球具有左右搖擺動畫和高光效果

## 開發約定

### 座標系統

- 球使用中心座標 (`ball.x`, `ball.y`)
- 其他物件使用左上角座標
- 碰撞檢測混合使用中心點和邊界框

### 匯入規範

- 相對匯入： `from src.entities.ball import Ball`
- 配置匯入： `from config import settings`
- 使用 `sys.path.append('.')` 確保根目錄可見

### 測試工具

- `tools/check_imports.py`: 驗證所有匯入和基本物件創建
- 手動測試：滑鼠控制板子、空白鍵發射球、點擊磚塊

## 常見任務

### 新增遊戲實體

1. 在 `src/entities/` 創建類別，實作 `update(dt)` 和 `draw(screen)`
2. 在 `GameEngine.__init__()` 初始化
3. 在主循環中更新和繪製
4. 更新 `tools/check_imports.py` 驗證

### 調整遊戲平衡

- 球速度：`Ball.__init__(speed=6)`
- 磚塊佈局：`GameEngine.__init__()` 中的巢狀迴圈
- 龍捲風頻率：`tornado_spawn_interval`

### 資源管理

- 優先使用 `assets/images/` 新路徑
- `resource_loader.load_image()` 處理載入失敗
- 支援 colorkey 透明色（雖然目前未使用）
