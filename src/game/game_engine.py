######################載入套件######################
"""
遊戲引擎模組
負責管理整個遊戲的主循環、狀態更新和繪製
包含所有遊戲物件的初始化、更新和碰撞檢測邏輯
"""
import pygame
import sys
import random
from config import settings
from config import colors as game_colors
from src.entities.ball import Ball
from src.entities.brick import Brick
from src.entities.paddle import Paddle
from src.entities.tornado import Tornado
from src.entities.balloon import Balloon
from src.utils.resource_loader import load_image


######################物件類別######################
class GameEngine:
    """
    遊戲引擎類別\n
    
    這是整個遊戲的核心控制器，負責：\n
    1. 初始化所有遊戲物件（球、磚塊、底板等）\n
    2. 管理遊戲主循環和事件處理\n
    3. 處理物件間的碰撞檢測\n
    4. 控制遊戲狀態（進行中、勝利等）\n
    5. 管理特殊效果（龍捲風、慶祝氣球）
    """
    def __init__(self):
        """
        初始化遊戲引擎\n
        
        執行以下初始化步驟：\n
        1. 初始化 Pygame 系統\n
        2. 設定遊戲視窗和標題\n
        3. 載入遊戲資源（圖片等）\n
        4. 建立所有遊戲物件\n
        5. 設定遊戲狀態變數
        """
        # 初始化 Pygame 系統
        pygame.init()
        
        # 建立時鐘物件控制幀率
        self.clock = pygame.time.Clock()
        
        # 設定遊戲視窗
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Breaking the Block")

        # 載入資源：優先嘗試新的資源路徑，失敗則回退到舊版 'image/' 資料夾
        # 這種做法確保與舊版本的相容性
        ball_img = load_image('assets/images/ball/ball.png') or load_image('image/41QWjX05doL.png')

        # 創建磚塊陣列
        self.bricks = []
        
        # 磚塊配置參數
        brick_width = 75      # 每個磚塊的寬度
        brick_height = 25     # 每個磚塊的高度
        brick_spacing = 5     # 磚塊間的間距
        
        # 計算磚塊牆的位置（置中對齊）
        wall_width = 10 * brick_width + 9 * brick_spacing  # 10 個磚塊 + 9 個間距
        start_x = (settings.WIDTH - wall_width) // 2       # 水平置中
        start_y = 50                                        # 距離頂部的距離
        
        # 定義每排磚塊的顏色（由上到下）
        colors = [
            (255, 0, 0),    # 紅色
            (255, 165, 0),  # 橙色
            (255, 255, 0),  # 黃色
            (0, 255, 0),    # 綠色
            (0, 0, 255),    # 藍色
        ]
        
        # 建立 5 排 x 10 列的磚塊陣列
        for row in range(5):
            for col in range(10):
                # 計算每個磚塊的位置
                x = start_x + col * (brick_width + brick_spacing)
                y = start_y + row * (brick_height + brick_spacing)
                # 建立磚塊並加入陣列
                self.bricks.append(Brick(x, y, brick_height, brick_width, colors[row]))

        # 建立底板（玩家控制的板子）
        paddle_width = 120                           # 底板寬度
        paddle_height = 15                           # 底板高度
        paddle_y = settings.HEIGHT - 50              # 距離底部的距離
        paddle_x = (settings.WIDTH - paddle_width) // 2  # 水平置中
        self.paddle = Paddle(paddle_x, paddle_y, paddle_height, paddle_width, game_colors.WHITE)

        # 建立球物件
        # 初始位置在底板中央上方
        initial_ball_x = self.paddle.x + self.paddle.length / 2
        initial_ball_y = self.paddle.y - 12
        self.ball = Ball(game_colors.WHITE, 12, initial_ball_x, initial_ball_y, speed=6)
        self.ball.image = ball_img  # 設定球的圖片

        # 遊戲狀態控制
        self.game_won = False                    # 是否勝利
        self.victory_balloons = []               # 慶祝氣球列表
        self.balloon_spawn_timer = 0             # 氣球生成計時器
        self.balloon_spawn_interval = 0.1        # 氣球生成間隔（秒）

        # 龍捲風系統
        self.tornadoes = []                      # 龍捲風列表
        self.tornado_spawn_timer = 0             # 龍捲風生成計時器
        self.tornado_spawn_interval = random.uniform(5, 10)  # 隨機生成間隔 5-10 秒

    def check_victory(self):
        """
        檢查遊戲是否勝利\n
        
        遍歷所有磚塊，檢查是否都已被擊中\n
        返回值：True 表示所有磚塊都已被擊中（勝利），False 表示還有磚塊未被擊中
        """
        for brick in self.bricks:
            if not brick.is_hit:
                return False  # 發現未被擊中的磚塊
        return True  # 所有磚塊都被擊中

    def spawn_balloon(self):
        """
        生成勝利慶祝氣球\n
        
        在螢幕底部隨機位置生成一個彩色氣球\n
        氣球具有隨機的顏色和大小\n
        返回值：新創建的 Balloon 物件
        """
        # 隨機水平位置（避免太靠近邊緣）
        x = random.randint(50, settings.WIDTH - 50)
        # 從螢幕底部下方開始
        y = settings.HEIGHT + 50
        
        # 隨機選擇氣球顏色
        color = random.choice([
            (255, 100, 100),  # 淺紅色
            (100, 255, 100),  # 淺綠色
            (100, 100, 255),  # 淺藍色
            (255, 255, 100),  # 淺黃色
            (255, 100, 255),  # 淺紫色
            (100, 255, 255),  # 淺青色
            (255, 200, 100),  # 淺橙色
            (200, 100, 255),  # 淺紫羅蘭色
        ])
        
        # 隨機氣球大小
        size = random.randint(15, 25)
        
        return Balloon(x, y, color, size)

    def spawn_tornado(self):
        """
        生成龍捲風障礙物\n
        
        在螢幕頂部隨機位置生成一個龍捲風\n
        龍捲風會向下移動，碰到球時會重置遊戲\n
        返回值：新創建的 Tornado 物件
        """
        # 隨機水平位置
        x = random.randint(0, settings.WIDTH - 30)
        # 從螢幕頂部上方開始
        y = -80
        
        return Tornado(x, y)

    def restart_game(self):
        """
        重新開始遊戲\n
        
        重置所有遊戲狀態到初始狀態：\n
        1. 清除勝利狀態和慶祝氣球\n
        2. 恢復所有磚塊\n
        3. 將球重置到底板上方
        """
        # 重置遊戲狀態
        self.game_won = False
        self.victory_balloons.clear()
        
        # 恢復所有磚塊
        for brick in self.bricks:
            brick.is_hit = False
        
        # 將球重置到底板中央上方
        self.ball.reset_to(self.paddle.x + self.paddle.length / 2, self.paddle.y - self.ball.size)

    def run(self):
        """
        主遊戲循環\n
        
        這是遊戲的核心循環，負責：\n
        1. 控制遊戲幀率\n
        2. 處理使用者輸入（滑鼠、鍵盤）\n
        3. 更新所有遊戲物件狀態\n
        4. 檢查碰撞和遊戲狀態\n
        5. 繪製所有遊戲元素\n
        6. 管理特殊效果（龍捲風、慶祝氣球）
        """
        while True:
            # 控制遊戲幀率並計算時間差
            dt_ms = self.clock.tick(settings.FPS)  # 限制為設定的 FPS
            dt = dt_ms / 1000.0  # 轉換為秒數，用於物理運算

            # 檢查勝利條件
            if not self.game_won and self.check_victory():
                self.game_won = True
                print("恭喜！你贏了！🎉")

            # 滑鼠控制底板移動
            mouse_x, _ = pygame.mouse.get_pos()
            new_paddle_x = mouse_x - self.paddle.length // 2  # 滑鼠位置為底板中心
            
            # 限制底板不能移出螢幕邊界
            if new_paddle_x < 0:
                new_paddle_x = 0
            elif new_paddle_x + self.paddle.length > settings.WIDTH:
                new_paddle_x = settings.WIDTH - self.paddle.length
            
            self.paddle.x = new_paddle_x

            # 處理所有事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 使用者點擊關閉按鈕
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 滑鼠點擊事件（用於測試，點擊磚塊可直接擊中）
                    mx, my = pygame.mouse.get_pos()
                    for brick in self.bricks:
                        if brick.check_collision(mx, my):
                            print(f"磚塊被擊中！位置: ({mx}, {my})")
                elif event.type == pygame.KEYDOWN:
                    # 鍵盤按鍵事件
                    if event.key == pygame.K_SPACE:
                        # 空白鍵發射球
                        self.ball.launch()

            # 勝利狀態：管理慶祝氣球
            if self.game_won:
                # 更新氣球生成計時器
                self.balloon_spawn_timer += dt
                
                # 定期生成新氣球（最多 30 個）
                if self.balloon_spawn_timer >= self.balloon_spawn_interval and len(self.victory_balloons) < 30:
                    self.victory_balloons.append(self.spawn_balloon())
                    self.balloon_spawn_timer = 0
                
                # 更新所有氣球並移除飄出螢幕的氣球
                for balloon in self.victory_balloons[:]:  # 使用切片複製列表，避免迭代時修改
                    balloon.update(dt)
                    if balloon.is_off_screen():
                        self.victory_balloons.remove(balloon)

            # 遊戲進行中：管理龍捲風障礙物
            if not self.game_won:
                # 更新龍捲風生成計時器
                self.tornado_spawn_timer += dt
                
                # 達到生成間隔時建立新龍捲風
                if self.tornado_spawn_timer >= self.tornado_spawn_interval:
                    self.tornadoes.append(self.spawn_tornado())
                    self.tornado_spawn_timer = 0
                    # 設定下次生成的隨機間隔
                    self.tornado_spawn_interval = random.uniform(5, 10)

            # 更新所有龍捲風
            for tornado in self.tornadoes[:]:  # 使用切片複製列表
                tornado.update(dt)
                
                # 檢查龍捲風與球的碰撞
                if tornado.check_collision(self.ball):
                    # 龍捲風碰到球，重新開始遊戲
                    self.restart_game()
                    self.tornadoes.clear()  # 清除所有龍捲風
                    break  # 跳出迴圈
                
                # 移除離開螢幕的龍捲風
                if tornado.is_off_screen(settings.HEIGHT):
                    self.tornadoes.remove(tornado)

            # 繪製所有遊戲元素
            # 1. 清空螢幕（填入黑色背景）
            self.screen.fill(game_colors.BLACK)
            
            # 2. 繪製所有磚塊
            for brick in self.bricks:
                brick.draw(self.screen)
            
            # 3. 繪製底板
            self.paddle.draw(self.screen)
            
            # 4. 更新並繪製球
            self.ball.update(dt, settings.WIDTH, settings.HEIGHT, self.paddle, self.bricks)
            self.ball.draw(self.screen)
            
            # 5. 繪製勝利氣球（僅在勝利時）
            if self.game_won:
                for balloon in self.victory_balloons:
                    balloon.draw(self.screen)
            
            # 6. 繪製龍捲風
            for tornado in self.tornadoes:
                tornado.draw(self.screen)
            
            # 7. 更新螢幕顯示
            pygame.display.update()
