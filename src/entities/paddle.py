######################載入套件######################
from .brick import Brick


######################物件類別######################
class Paddle(Brick):
    """
    底板類別，繼承 Brick 並可擴充行為\n
    用於控制玩家操作的底板
    """
    def __init__(self, x, y, height, length, color):
        """
        初始化底板\n
        x, y: 底板的左上角座標\n
        height, length: 底板的高度和寬度\n
        color: 底板的顏色
        """
        super().__init__(x, y, height, length, color)
