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


class GameEngine:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Breaking the Block")

        # load resources: try new assets path first, fallback to legacy 'image/' folder
        ball_img = load_image('assets/images/ball/ball.png') or load_image('image/41QWjX05doL.png')

        # create bricks
        self.bricks = []
        brick_width = 75
        brick_height = 25
        brick_spacing = 5
        wall_width = 10 * brick_width + 9 * brick_spacing
        start_x = (settings.WIDTH - wall_width) // 2
        start_y = 50
        colors = [
            (255, 0, 0),
            (255, 165, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
        ]
        for row in range(5):
            for col in range(10):
                x = start_x + col * (brick_width + brick_spacing)
                y = start_y + row * (brick_height + brick_spacing)
                self.bricks.append(Brick(x, y, brick_height, brick_width, colors[row]))

        # paddle
        plate_width = 120
        plate_height = 15
        plate_y = settings.HEIGHT - 50
        plate_x = (settings.WIDTH - plate_width) // 2
        self.plate = Paddle(plate_x, plate_y, plate_height, plate_width, game_colors.WHITE)

        # ball
        self.ball = Ball(game_colors.WHITE, 12, self.plate.x + self.plate.length / 2, self.plate.y - 12, speed=6)
        self.ball.image = ball_img

        # game state
        self.game_won = False
        self.victory_balloons = []
        self.balloon_spawn_timer = 0
        self.balloon_spawn_interval = 0.1

        # tornado
        self.tornadoes = []
        self.tornado_spawn_timer = 0
        self.tornado_spawn_interval = random.uniform(5, 10)

    def check_victory(self):
        for brick in self.bricks:
            if not brick.is_hit:
                return False
        return True

    def spawn_balloon(self):
        x = random.randint(50, settings.WIDTH - 50)
        y = settings.HEIGHT + 50
        color = random.choice([
            (255, 100, 100),
            (100, 255, 100),
            (100, 100, 255),
            (255, 255, 100),
            (255, 100, 255),
            (100, 255, 255),
            (255, 200, 100),
            (200, 100, 255),
        ])
        size = random.randint(15, 25)
        return Balloon(x, y, color, size)

    def spawn_tornado(self):
        x = random.randint(0, settings.WIDTH - 30)
        y = -80
        return Tornado(x, y)

    def restart_game(self):
        self.game_won = False
        self.victory_balloons.clear()
        for brick in self.bricks:
            brick.is_hit = False
        self.ball.reset_to(self.plate.x + self.plate.length / 2, self.plate.y - self.ball.size)

    def run(self):
        while True:
            dt_ms = self.clock.tick(settings.FPS)
            dt = dt_ms / 1000.0

            if not self.game_won and self.check_victory():
                self.game_won = True
                print("恭喜！你贏了！🎉")

            mouse_x, _ = pygame.mouse.get_pos()
            new_plate_x = mouse_x - self.plate.length // 2
            if new_plate_x < 0:
                new_plate_x = 0
            elif new_plate_x + self.plate.length > settings.WIDTH:
                new_plate_x = settings.WIDTH - self.plate.length
            self.plate.x = new_plate_x

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for brick in self.bricks:
                        if brick.check_collision(mx, my):
                            print(f"磚塊被擊中！位置: ({mx}, {my})")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.launch()

            if self.game_won:
                self.balloon_spawn_timer += dt
                if self.balloon_spawn_timer >= self.balloon_spawn_interval and len(self.victory_balloons) < 30:
                    self.victory_balloons.append(self.spawn_balloon())
                    self.balloon_spawn_timer = 0
                for balloon in self.victory_balloons[:]:
                    balloon.update(dt)
                    if balloon.is_off_screen():
                        self.victory_balloons.remove(balloon)

            if not self.game_won:
                self.tornado_spawn_timer += dt
                if self.tornado_spawn_timer >= self.tornado_spawn_interval:
                    self.tornadoes.append(self.spawn_tornado())
                    self.tornado_spawn_timer = 0
                    self.tornado_spawn_interval = random.uniform(5, 10)

            for tornado in self.tornadoes[:]:
                tornado.update(dt)
                if tornado.check_collision(self.ball):
                    self.restart_game()
                    self.tornadoes.clear()
                    break
                if tornado.is_off_screen(settings.HEIGHT):
                    self.tornadoes.remove(tornado)

            self.screen.fill(game_colors.BLACK)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.plate.draw(self.screen)
            self.ball.update(dt, settings.WIDTH, settings.HEIGHT, self.plate, self.bricks)
            self.ball.draw(self.screen)
            if self.game_won:
                for balloon in self.victory_balloons:
                    balloon.draw(self.screen)
            for tornado in self.tornadoes:
                tornado.draw(self.screen)
            pygame.display.update()
