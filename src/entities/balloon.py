######################載入套件######################
import math
import random
import pygame


######################物件類別######################
class Balloon:
    """
    氣球類別：用於慶祝遊戲勝利\n
    具有上升和左右搖擺的動畫效果
    """
    def __init__(self, x, y, color, size=20):
        """
        初始化氣球\n
        x, y: 氣球的初始座標\n
        color: 氣球的顏色\n
        size: 氣球的大小
        """
        self.x = x
        self.y = y
        self.original_y = y
        self.color = color
        self.size = size
        self.speed = random.uniform(1, 3)
        self.amplitude = random.uniform(10, 30)  # 左右搖擺幅度
        self.frequency = random.uniform(0.02, 0.05)  # 搖擺頻率
        self.time = 0
        
    def update(self, dt):
        """
        更新氣球位置\n
        dt: 時間增量
        """
        self.time += dt
        # 向上飄浮
        self.y -= self.speed
        # 左右搖擺
        self.x = self.x + math.sin(self.time * self.frequency * 100) * self.amplitude * dt
        
    def draw(self, screen):
        """
        繪製氣球\n
        screen: pygame 螢幕物件
        """
        # 畫氣球本體（橢圓形）
        balloon_rect = (int(self.x - self.size//2), int(self.y - self.size), self.size, int(self.size * 1.2))
        pygame.draw.ellipse(screen, self.color, balloon_rect)
        
        # 畫氣球繩子
        string_start = (int(self.x), int(self.y))
        string_end = (int(self.x), int(self.y + self.size))
        pygame.draw.line(screen, (100, 100, 100), string_start, string_end, 2)
        
        # 氣球上的高光
        highlight_x = int(self.x - self.size//4)
        highlight_y = int(self.y - self.size//2)
        highlight_size = max(3, self.size//4)
        pygame.draw.circle(screen, (255, 255, 255), (highlight_x, highlight_y), highlight_size)
    
    def is_off_screen(self):
        """
        檢查氣球是否已經飄出螢幕\n
        返回值：True 表示已飄出螢幕，False 表示仍在螢幕內
        """
        return self.y < -self.size * 2
