import os
import pygame


def load_image(path, colorkey=None):
    """載入圖片，path 可以是相對於專案根目錄或 assets 的路徑

    返回 pygame.Surface 或 None（找不到或載入失敗時）
    """
    try:
        img = pygame.image.load(path)
        return img.convert_alpha()
    except Exception:
        return None
