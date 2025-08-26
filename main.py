
######################載入套件######################
import pygame 
import sys
import math
import random
######################類別物件######################
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


class Balloon:
    """氣球類別：用於慶祝遊戲勝利"""
    def __init__(self, x, y, color, size=20):
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
        """更新氣球位置"""
        self.time += dt
        # 向上飄浮
        self.y -= self.speed
        # 左右搖擺
        self.x = self.x + math.sin(self.time * self.frequency * 100) * self.amplitude * dt
        
    def draw(self, screen):
        """繪製氣球"""
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
        """檢查氣球是否已經飄出螢幕"""
        return self.y < -self.size * 2


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


class Ball:
    """球的類別：包含顏色、大小(直徑)、初始位置、速度以及是否已發射的旗標

    屬性:
        color: (r,g,b)
        size: 直徑 (int)
        x, y: 中心座標 (float)
        vx, vy: 速度向量 (float)
        is_launched: bool
    """
    def __init__(self, color, size, init_x, init_y, speed=5, is_launched=False):
        self.color = color
        self.size = size
        # using center coordinates
        self.x = float(init_x)
        self.y = float(init_y)
        # initial velocities (vx, vy) - start stationary until launched
        self.vx = 0.0
        self.vy = 0.0
        self.speed = float(speed)
        self.is_launched = bool(is_launched)
        # optional pygame surface to draw the ball
        self.image = None

    @property
    def radius(self):
        return self.size // 2

    def draw(self, screen):
        if self.image:
            # scale image to ball size if needed
            img = pygame.transform.smoothscale(self.image, (self.size, self.size))
            screen.blit(img, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def launch(self, angle=None):
        """發射球。如果提供 angle (rad) 則以該方向發射，否則用預設斜上方向。"""
        if not self.is_launched:
            if angle is None:
                # 預設朝左上 60 度
                angle = -math.radians(60)
            # 以 speed 和角度設定速度向量
            self.vx = self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)
            self.is_launched = True

    def reset_to(self, x, y):
        """把球放回某個位置（通常是板子上方），並設定為未發射。"""
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.is_launched = False

    def update(self, dt, width, height, plate, bricks):
        """更新球的位置並處理與牆壁、板子、磚塊的碰撞。

        dt: seconds elapsed since last frame (float)
        width/height: screen size
        plate: Brick instance for the paddle
        bricks: list of Brick instances
        """
        # if not launched, stick to plate
        if not self.is_launched:
            # center horizontally on plate and sit just above it
            self.x = plate.x + plate.length / 2
            self.y = plate.y - self.radius - 1
            return

        # move
        self.x += self.vx * dt * 60.0  # scale to frame-rate neutral (approx)
        self.y += self.vy * dt * 60.0

        # wall collisions (left/right)
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.vx = -self.vx

        # ceiling collision
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy

        # plate collision (simple)
        # check if ball is over the plate horizontally and touching it vertically
        if (plate.x <= self.x <= plate.x + plate.length and
            self.y + self.radius >= plate.y and self.vy > 0):
            # move ball to top of plate
            self.y = plate.y - self.radius - 1
            # reflect Y
            self.vy = -abs(self.vy)
            # adjust vx based on where it hit the plate
            plate_center = plate.x + plate.length / 2
            relative_hit = (self.x - plate_center) / (plate.length / 2)  # -1 .. 1
            # change horizontal speed proportionally
            self.vx += relative_hit * 2.5

        # brick collisions: if center point inside a brick, mark brick hit and reflect
        for brick in bricks:
            if not brick.is_hit:
                if brick.check_collision(self.x, self.y):
                    # simple response: invert y velocity
                    self.vy = -self.vy
                    # small speed increase for challenge
                    self.vx *= 1.02
                    self.vy *= 1.02
                    break

        # if ball falls below screen, reset to plate
        if self.y - self.radius > height:
            # place back on plate and mark as not launched
            self.reset_to(plate.x + plate.length / 2, plate.y - self.radius - 1)




######################定義函式區######################

######################初始化設定######################
pygame.init() # 啟動pygame
clock = pygame.time.Clock() # create a clock object to manage the frame rate

######################載入圖片######################

# 載入球的圖片（如果存在）
ball_image = None
try:
    ball_image = pygame.image.load("image/41QWjX05doL.png").convert_alpha()
except Exception:
    ball_image = None


######################遊戲視窗設定######################
width = 800 # create a width variable
height = 600 # create a height variable
# create window's size
screen = pygame.display.set_mode((width, height))
# create window's title
pygame.display.set_caption("Breaking the Block")

######################磚塊######################
# 建立 5x10 磚塊牆
bricks = []
brick_width = 75
brick_height = 25
brick_spacing = 5

# 計算磚塊牆的總寬度並置中
wall_width = 10 * brick_width + 9 * brick_spacing  # 10個磚塊 + 9個間隔
start_x = (width - wall_width) // 2  # 置中
start_y = 50  # 距離頂部50像素

# 定義不同行的顏色
colors = [
    (255, 0, 0),    # 紅色
    (255, 165, 0),  # 橙色
    (255, 255, 0),  # 黃色
    (0, 255, 0),    # 綠色
    (0, 0, 255)     # 藍色
]

# 創建 5 行 x 10 列的磚塊牆
for row in range(5):
    for col in range(10):
        x = start_x + col * (brick_width + brick_spacing)
        y = start_y + row * (brick_height + brick_spacing)
        color = colors[row]  # 每一行使用不同顏色
        brick = Brick(x, y, brick_height, brick_width, color)
        bricks.append(brick)

######################顯示文字設定######################

######################底板設定######################
# 創建可控制的底板
plate_width = 120  # 比一般磚塊更長
plate_height = 15
plate_y = height - 50  # 固定在螢幕底部附近
plate_color = (255, 255, 255)  # 白色
# 初始位置在螢幕中央
plate_x = (width - plate_width) // 2
plate = Brick(plate_x, plate_y, plate_height, plate_width, plate_color)

######################球設定######################
# 建立球，初始放在板子上方
ball_color = (255, 255, 255)
ball_size = 12
ball_speed = 6
ball = Ball(ball_color, ball_size, plate.x + plate.length / 2, plate.y - ball_size, speed=ball_speed, is_launched=False)
# 如果有載入到圖片就指定給 ball
ball.image = ball_image

######################遊戲結束設定######################
# 遊戲狀態
game_won = False
victory_balloons = []
balloon_spawn_timer = 0
balloon_spawn_interval = 0.1  # 每0.1秒生成一個氣球

# 氣球顏色列表
balloon_colors = [
    (255, 100, 100),  # 紅色
    (100, 255, 100),  # 綠色
    (100, 100, 255),  # 藍色
    (255, 255, 100),  # 黃色
    (255, 100, 255),  # 紫色
    (100, 255, 255),  # 青色
    (255, 200, 100),  # 橙色
    (200, 100, 255),  # 紫藍色
]

######################龍捲風設定######################
tornadoes = []
tornado_spawn_timer = 0
tornado_spawn_interval = random.uniform(5, 10)  # 每5-10秒生成一個龍捲風

def check_victory():
    """檢查是否所有磚塊都被擊中"""
    for brick in bricks:
        if not brick.is_hit:
            return False
    return True

def spawn_balloon():
    """生成一個氣球"""
    x = random.randint(50, width - 50)
    y = height + 50  # 從螢幕底部開始
    color = random.choice(balloon_colors)
    size = random.randint(15, 25)
    return Balloon(x, y, color, size)

def restart_game():
    """重新開始遊戲"""
    global game_won, victory_balloons, bricks, ball
    
    # 重置遊戲狀態
    game_won = False
    victory_balloons.clear()
    
    # 重新創建所有磚塊
    bricks.clear()
    for row in range(5):
        for col in range(10):
            x = start_x + col * (brick_width + brick_spacing)
            y = start_y + row * (brick_height + brick_spacing)
            color = colors[row]
            brick = Brick(x, y, brick_height, brick_width, color)
            bricks.append(brick)
    
    # 重置球的位置
    ball.reset_to(plate.x + plate.length / 2, plate.y - ball.size)
    
    print("遊戲重新開始！")

def spawn_tornado():
    """生成一個龍捲風"""
    x = random.randint(0, width - 30)
    y = -80  # 從螢幕頂部開始
    return Tornado(x, y)

######################主程式######################
while True:
    # 計算 delta time (秒)
    dt_ms = clock.tick(60)  # limit the frame rate to 60 FPS
    dt = dt_ms / 1000.0
    
    # 檢查遊戲勝利
    if not game_won and check_victory():
        game_won = True
        print("恭喜！你贏了！🎉")
    
    # 取得滑鼠位置並更新板子位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # 計算板子的新 x 位置（以滑鼠為中心）
    new_plate_x = mouse_x - plate_width // 2
    # 確保板子不會移出螢幕邊界
    if new_plate_x < 0:
        new_plate_x = 0
    elif new_plate_x + plate_width > width:
        new_plate_x = width - plate_width
    # 更新板子位置
    plate.x = new_plate_x
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if user clicked [x] button
            pygame.quit()
            sys.exit() # quit the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 取得滑鼠點擊位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 檢查是否擊中任何磚塊
            for brick in bricks:
                if brick.check_collision(mouse_x, mouse_y):
                    print(f"磚塊被擊中！位置: ({mouse_x}, {mouse_y})")
        elif event.type == pygame.KEYDOWN:
            # 空白鍵發射
            if event.key == pygame.K_SPACE:
                ball.launch()
    
    # 如果遊戲勝利，生成氣球
    if game_won:
        balloon_spawn_timer += dt
        if balloon_spawn_timer >= balloon_spawn_interval and len(victory_balloons) < 30:
            victory_balloons.append(spawn_balloon())
            balloon_spawn_timer = 0
        
        # 更新氣球位置
        for balloon in victory_balloons[:]:  # 使用切片複製來避免修改列表時的問題
            balloon.update(dt)
            if balloon.is_off_screen():
                victory_balloons.remove(balloon)
    
    # 龍捲風生成和更新（只在遊戲進行中，不在勝利時生成）
    if not game_won:
        tornado_spawn_timer += dt
        if tornado_spawn_timer >= tornado_spawn_interval:
            tornadoes.append(spawn_tornado())
            tornado_spawn_timer = 0
            # 重新設定下次生成時間
            tornado_spawn_interval = random.uniform(5, 10)
    
    # 更新龍捲風位置
    for tornado in tornadoes[:]:
        tornado.update(dt)
        # 檢查與球的碰撞
        if tornado.check_collision(ball):
            restart_game()
            tornadoes.clear()  # 清除所有龍捲風
            break
        # 移除離開螢幕的龍捲風
        if tornado.is_off_screen(height):
            tornadoes.remove(tornado)
    
    # fill the screen with black color
    screen.fill((0, 0, 0))
    
    # 繪製所有磚塊
    for brick in bricks:
        brick.draw(screen)
    
    # 繪製底板
    plate.draw(screen)

    # 更新與繪製球
    ball.update(dt, width, height, plate, bricks)
    ball.draw(screen)
    
    # 繪製勝利氣球
    if game_won:
        for balloon in victory_balloons:
            balloon.draw(screen)
    
    # 繪製龍捲風
    for tornado in tornadoes:
        tornado.draw(screen)
    
    # update the window
    pygame.display.update() 