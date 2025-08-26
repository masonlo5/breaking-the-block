######################載入套件######################
import pygame


######################物件類別######################
class Brick:
    """
    磚塊類別\n
    負責處理磚塊的繪製和碰撞檢測
    """
    def __init__(self, x, y, height, length, color):
        """
        初始化磚塊\n
        x, y: 磚塊的左上角座標\n
        height, length: 磚塊的高度和寬度\n
        color: 磚塊的顏色\n
        """
        self.x = x
        self.y = y
        self.height = height
        self.length = length
        self.color = color
        self.is_hit = False  # 預設值為 not been hit

    def draw(self, screen):
        """
        繪製磚塊的方法\n
        screen: pygame 螢幕物件
        """
        if not self.is_hit:  # 只有在磚塊還沒被擊中時才繪製
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, self.height))

    def check_collision(self, pos_x, pos_y):
        """
        檢查指定位置是否擊中磚塊\n
        pos_x, pos_y: 檢查的座標位置\n
        返回值：True 表示擊中，False 表示未擊中
        """
        if (self.x <= pos_x <= self.x + self.length and 
            self.y <= pos_y <= self.y + self.height and 
            not self.is_hit):
            self.is_hit = True
            return True
        return False
