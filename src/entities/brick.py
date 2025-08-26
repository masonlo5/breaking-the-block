import pygame


class Brick:
    def __init__(self, x, y, height, length, color):
        self.x = x
        self.y = y
        self.height = height
        self.length = length
        self.color = color
        self.is_hit = False  # 預設值為 not been hit

    def draw(self, screen):
        """繪製磚塊的方法"""
        if not self.is_hit:  # 只有在磚塊還沒被擊中時才繪製
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, self.height))

    def check_collision(self, pos_x, pos_y):
        """檢查指定位置是否擊中磚塊"""
        if (self.x <= pos_x <= self.x + self.length and 
            self.y <= pos_y <= self.y + self.height and 
            not self.is_hit):
            self.is_hit = True
            return True
        return False
