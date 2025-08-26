import math
import pygame


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
        plate: Paddle or Brick instance for the paddle
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
