from .brick import Brick


class Paddle(Brick):
    """底板類別，繼承 Brick 並可擴充行為"""
    def __init__(self, x, y, height, length, color):
        super().__init__(x, y, height, length, color)
