# coding=utf-8
"""
作者:yan lei yu
日期：2022年 10月 24日
"""
import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""
    # 参数引进来，便于与主文件相关联
    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        # 得到了屏幕的尺寸
        self.screen = ai_game.screen
        # 引入settings 外星人可以使用alien_speed
        self.settings = ai_game.settings
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        """向右移动外星人"""
        # 更新的是外星人的坐标，得到坐标后，再在画板上将其画出
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
