# coding=utf-8
"""
作者:yan lei yu
日期：2022年 10月 22日
"""
import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        # 飞船的screen等于实例化后（self.ship = Ship(self)） self.screen = pygame.display.set_mode的
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 返回一个矩形区域 所以到底返回了什么呢？
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外界矩形
        # self.image是一个surface
        self.image = pygame.image.load('images/ship.bmp')
        # 得到Rect  Rect的边界的点在何处呢？
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中存储小数值。
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """更证据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据self.x更新rect对象  不是self.rect.x只能存储整数么？为啥又可以赋予小数呢？
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
