######################載入套件######################
"""
資源載入工具模組
負責處理遊戲資源（如圖片、音效等）的載入
"""
import os
import pygame


######################定義函式區######################
def load_image(path, colorkey=None):
    """
    載入圖片檔案的通用函數\n
    此函數會嘗試載入指定路徑的圖片，如果載入失敗則返回 None\n
    支援所有 pygame 支援的圖片格式（PNG、JPG、GIF 等）\n
    
    參數說明：\n
    path: 圖片檔案的路徑（相對或絕對路徑）\n
    colorkey: 可選的透明色設定，用於處理沒有 alpha 通道的圖片\n
    
    返回值：\n
    成功時返回 pygame.Surface 物件\n
    失敗時返回 None（檔案不存在或格式不支援）
    """
    try:
        # 載入圖片檔案
        img = pygame.image.load(path)
        # 轉換為帶 alpha 通道的格式，提升效能並支援透明度
        return img.convert_alpha()
    except Exception:
        # 如果載入失敗（檔案不存在、格式錯誤等），返回 None
        return None
