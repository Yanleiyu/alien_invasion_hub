# coding=utf-8
"""
作者:yan lei yu
日期：2022年 10月 24日
"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        # 模块setting搭上了
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0，0）处创建一个子弹的矩形(self.rect)，在设置正确的位置。   自己创建的
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # 在初始的位置转移到了飞机的头部
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储用小数表示的子弹位置。  无法理解为啥self.rect.y无法存储整数，最终可以存储整数
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 只是更新位置罢了。后面的使用draw_bullet绘画
        # 更新表示子弹位置的小数值，改变了self.recet.y就表示子弹发射出去了，x轴向不变，因此子弹始终沿直线向上飞
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        # .draw与其他绘制的方法的区别？
        pygame.draw.rect(self.screen, self.color, self.rect)
