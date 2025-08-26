
######################載入套件######################
"""
Breaking the Block - 打磚塊遊戲主程式
一款使用 Pygame 開發的經典打磚塊遊戲，具有以下特色：
- 球與磚塊的碰撞檢測
- 滑鼠控制底板
- 龍捲風障礙物
- 勝利氣球慶祝效果

執行方式：python main.py
"""
import sys


######################定義函式區######################
def main():
    """
    主程式函數\n
    
    此函數是整個遊戲的入口點，負責：\n
    1. 動態匯入 GameEngine 類別（避免靜態分析問題）\n
    2. 建立遊戲引擎實例\n
    3. 啟動遊戲主循環\n
    
    使用動態匯入的好處：\n
    - 避免某些 IDE 或執行環境的匯入路徑問題\n
    - 確保在執行時才載入遊戲引擎，提供更好的錯誤處理
    """
    try:
        # 動態匯入遊戲引擎類別
        # 這樣做可以避免在某些環境下的路徑問題
        from src.game.game_engine import GameEngine
    except Exception as e:
        # 如果匯入失敗，提供清楚的錯誤訊息
        raise RuntimeError("無法匯入 GameEngine，請確認專案根目錄已在 PYTHONPATH，或使用 `python main.py` 從專案根目錄執行。") from e

    # 建立遊戲引擎實例並開始遊戲
    engine = GameEngine()
    engine.run()


######################主程式######################
# 直接呼叫主函數執行遊戲
main()