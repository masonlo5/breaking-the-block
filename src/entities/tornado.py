import math
import random
import pygame


class Tornado:
    """龍捲風類別：碰到球時重新開始遊戲"""
    def __init__(self, x, y, width=30, height=80):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = random.uniform(1, 3)  # 下降速度
        self.rotation = 0  # 旋轉角度
        self.rotation_speed = random.uniform(5, 10)  # 旋轉速度
        self.color = (150, 150, 150)  # 灰色
        
    def update(self, dt):
        """更新龍捲風位置和旋轉"""
        self.y += self.speed
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation = 0
    
    def draw(self, screen):
        """繪製龍捲風"""
        # 畫龍捲風的螺旋形狀
        center_x = self.x + self.width // 2
        
        # 畫多個圓圈形成龍捲風效果
        for i in range(0, self.height, 8):
            # 計算每層的寬度（上窄下寬）
            layer_width = self.width * (i / self.height) * 0.8 + 5
            # 計算旋轉偏移
            offset = math.sin(math.radians(self.rotation + i * 10)) * (layer_width / 4)
            
            # 繪製龍捲風的每一層
            layer_x = center_x + offset - layer_width // 2
            layer_y = self.y + i
            
            # 顏色漸變（上淺下深）
            gray_value = int(200 - (i / self.height) * 100)
            color = (gray_value, gray_value, gray_value)
            
            pygame.draw.ellipse(screen, color, 
                              (int(layer_x), int(layer_y), int(layer_width), 6))
    
    def check_collision(self, ball):
        """檢查是否與球碰撞"""
        # 簡單的矩形碰撞檢測
        ball_left = ball.x - ball.radius
        ball_right = ball.x + ball.radius
        ball_top = ball.y - ball.radius
        ball_bottom = ball.y + ball.radius
        
        tornado_left = self.x
        tornado_right = self.x + self.width
        tornado_top = self.y
        tornado_bottom = self.y + self.height
        
        return (ball_right > tornado_left and ball_left < tornado_right and
                ball_bottom > tornado_top and ball_top < tornado_bottom)
    
    def is_off_screen(self, height):
        """檢查龍捲風是否離開螢幕"""
        return self.y > height
