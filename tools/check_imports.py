import sys
sys.path.append('.')

from src.entities.ball import Ball
from src.entities.brick import Brick
from src.entities.tornado import Tornado
from src.entities.balloon import Balloon
from src.entities.paddle import Paddle

print('imports ok')

b = Ball((255,255,255), 10, 50, 50)
print('radius', b.radius)
b.reset_to(100, 100)
print('reset', b.x, b.y)

brick = Brick(10, 10, 10, 20, (255,0,0))
print('brick initial is_hit', brick.is_hit)
print('brick check_collision', brick.check_collision(15,15))
print('brick after is_hit', brick.is_hit)
