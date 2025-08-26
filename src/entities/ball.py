######################載入套件######################
import math
import pygame


######################物件類別######################
class Ball:
    """
    球的類別：包含顏色、大小(直徑)、初始位置、速度以及是否已發射的旗標\n
    \n
    屬性說明：\n
    color: 球的顏色 (r,g,b) 元組\n
    size: 球的直徑（整數）\n
    x, y: 球心座標（浮點數）\n
    velocity_x, velocity_y: 速度向量（浮點數）\n
    speed: 球的移動速度（浮點數）\n
    is_launched: 是否已發射（布林值）\n
    image: 球的圖片物件（可選）
    """
    def __init__(self, color, size, init_x, init_y, speed=5, is_launched=False):
        """
        初始化球物件\n
        \n
        參數:\n
        color (tuple): 球的顏色 (r,g,b)，每個值範圍 0-255\n
        size (int): 球的直徑，範圍 > 0\n
        init_x (float): 初始位置的中心 x 座標\n
        init_y (float): 初始位置的中心 y 座標\n
        speed (float): 球的移動速度，範圍 > 0\n
        is_launched (bool): 是否已發射，預設為 False\n
        \n
        初始化說明:\n
        - 球使用中心座標系統\n
        - 未發射時速度為 0\n
        - 可選擇性設定球的圖片
        """
        self.color = color
        self.size = size
        # 使用中心座標記錄球的位置
        self.x = float(init_x)
        self.y = float(init_y)
        # 初始速度向量（velocity_x, velocity_y）- 未發射前為靜止狀態
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = float(speed)
        self.is_launched = bool(is_launched)
        # 可選的 pygame 圖片物件用於繪製球
        self.image = None

    @property
    def radius(self):
        """
        取得球的半徑\n
        返回值：球的半徑（直徑的一半）
        """
        return self.size // 2

    def draw(self, screen):
        """
        繪製球的方法\n
        \n
        參數:\n
        screen (pygame.Surface): pygame 螢幕物件\n
        \n
        繪製邏輯:\n
        - 如果有設定圖片，則繪製圖片並縮放到球的大小\n
        - 如果沒有圖片，則繪製純色圓形\n
        - 繪製位置以球心座標為準
        """
        if self.image:
            # 如果需要的話將圖片縮放到球的大小
            img = pygame.transform.smoothscale(self.image, (self.size, self.size))
            screen.blit(img, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def launch(self, angle=None):
        """
        發射球\n
        \n
        參數:\n
        angle (float): 發射角度（弧度），預設為 None\n
        \n
        發射邏輯:\n
        - 如果提供 angle（弧度）則以該方向發射\n
        - 如果 angle 為 None，使用預設的左上 60 度角\n
        - 根據速度和角度設定速度向量\n
        - 將球標記為已發射狀態
        """
        if not self.is_launched:
            if angle is None:
                # 預設朝左上 60 度發射
                angle = -math.radians(60)
            # 以 speed 和角度設定速度向量
            self.velocity_x = self.speed * math.cos(angle)
            self.velocity_y = self.speed * math.sin(angle)
            self.is_launched = True

    def reset_to(self, x, y):
        """
        重置球到指定位置\n
        \n
        參數:\n
        x (float): 重置後的球心 x 座標\n
        y (float): 重置後的球心 y 座標\n
        \n
        重置操作:\n
        - 將球移動到指定位置（通常是底板上方）\n
        - 停止球的移動（速度歸零）\n
        - 設定為未發射狀態，球會黏在底板上
        """
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.is_launched = False

    def update(self, dt, width, height, paddle, bricks):
        """
        更新球的位置並處理碰撞檢測\n
        \n
        參數:\n
        dt (float): 距離上一幀的時間差（秒）\n
        width (int): 螢幕寬度，範圍 > 0\n
        height (int): 螢幕高度，範圍 > 0\n
        paddle (Paddle): 底板物件，包含位置和尺寸資訊\n
        bricks (list): 磚塊陣列，包含所有未被擊中的磚塊\n
        \n
        更新邏輯:\n
        1. 如果未發射，球會跟隨底板移動\n
        2. 如果已發射，執行物理移動和碰撞檢測\n
        3. 處理牆壁、底板、磚塊的碰撞\n
        4. 球掉出螢幕底部時重置到底板上方
        """
        # 如果球還沒發射，就讓它黏在底板上方
        if not self.is_launched:
            # 水平置中在底板上，垂直位置在底板正上方
            self.x = paddle.x + paddle.length / 2
            self.y = paddle.y - self.radius - 1
            return

        # 更新球的位置（使用時間差進行幀率無關的移動）
        self.x += self.velocity_x * dt * 60.0  # 縮放到與幀率無關（大約值）
        self.y += self.velocity_y * dt * 60.0

        # 牆壁碰撞檢測（左邊和右邊）
        if self.x - self.radius <= 0:
            # 撞到左牆，限制位置並反彈
            self.x = self.radius
            self.velocity_x = -self.velocity_x
        elif self.x + self.radius >= width:
            # 撞到右牆，限制位置並反彈
            self.x = width - self.radius
            self.velocity_x = -self.velocity_x

        # 天花板碰撞檢測
        if self.y - self.radius <= 0:
            # 撞到天花板，限制位置並反彈
            self.y = self.radius
            self.velocity_y = -self.velocity_y

        # 底板碰撞檢測（簡單版本）
        # 檢查球是否在底板的水平範圍內且垂直位置接觸底板
        if (paddle.x <= self.x <= paddle.x + paddle.length and
            self.y + self.radius >= paddle.y and self.velocity_y > 0):
            # 將球移動到底板頂部
            self.y = paddle.y - self.radius - 1
            # 反彈 Y 方向速度
            self.velocity_y = -abs(self.velocity_y)
            # 根據撞擊底板的位置調整水平速度
            paddle_center = paddle.x + paddle.length / 2
            relative_hit = (self.x - paddle_center) / (paddle.length / 2)  # 範圍 -1 到 1
            # 根據撞擊位置成比例地改變水平速度
            self.velocity_x += relative_hit * 2.5

        # 磚塊碰撞檢測：如果球心在磚塊內，標記磚塊被擊中並反彈
        for brick in bricks:
            if not brick.is_hit:
                if brick.check_collision(self.x, self.y):
                    # 簡單反應：反轉 y 方向速度
                    self.velocity_y = -self.velocity_y
                    # 小幅增加速度以增加挑戰性
                    self.velocity_x *= 1.02
                    self.velocity_y *= 1.02
                    break

        # 如果球掉到螢幕底部，重置到底板上
        if self.y - self.radius > height:
            # 將球放回底板中央上方並標記為未發射
            self.reset_to(paddle.x + paddle.length / 2, paddle.y - self.radius - 1)
