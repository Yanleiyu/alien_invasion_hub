import sys

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien


class AlienInvasion:
    """初始化游戏并创建游戏资源"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 实例化后得到所有的设置信息
        self.settings = Settings()
        # 返回的是什么  应该是一个surface
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # 设置背景色
        self.bg_color = (230, 230, 230)
        # 实例化自己 得到一个ship（用self.ship表示） 此处ai_game起了作用
        self.ship = Ship(self)
        # 编组self.bullets  是类pygame.sprite.Group()的一个实例，
        self.bullets = pygame.sprite.Group()
        # 如上 .......
        self.aliens = pygame.sprite.Group()
        #
        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        # 这是游戏的主体，将一些关联的代码重构为函数放在下面，一些方法在其他文件写好后直接调用
        while True:
            self._check_events()
            # 确定船的位置
            self.ship.update()
            # 确定子弹的位置
            self._update_bullets()
            # 检查并更新，更新外星人的坐标
            self._update_aliens()
            # 画各种图形
            self._update_screen()

    """这些函数有的是重构出来的，有的是为了完成项目内容而写出的函数"""
    # 下面的三个函数响应各种事件
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            # 鼠标事件
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""
        # 按q推出
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # KEYDOWN事件中使用的函数，将其重构了出来了。
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中。"""
        # 如果满足要求，就添加一个子弹
        if len(self.bullets) < self.settings.bullets_allowed:
            # 实例化一粒子弹，self是ai_game
            new_bullet = Bullet(self)
            # self.bullet是自己在初始化处定义的属性
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()

    # 得到一群外星人的坐标
    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少个外星人。
        # 外星人的间距为外星人宽度
        # 创建一个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # 创建第一行外星人 alien_number，row_number 辅助知道alien的位置
        # for循环使得每次循环将一个alien放入列表中
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # 得到的是外星人的二维坐标，
                self._create_alien(alien_number, row_number)

    # _create_fleet()中使用的函数。它可以确定一个外星人的坐标
    def _create_alien(self, alien_number, row_number):
        """创建一个外星人确定其当前坐标"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        # 确定外星人的位置
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        # 得到了一个外星人的坐标，就确定了外星人的位置，将其放入列表中
        self.aliens.add(alien)

    # 更新外星人的坐标  在主循环中使用
    def _update_aliens(self):
        """检擦外星人是否到达了边缘，更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # _check_fleet_edges中重构出来的函数
    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向"""
        # 向下移动一下
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # self.screen.fill 这一步不懂啊
        self.screen.fill(self.settings.bg_color)
        # 使用的是飞船的方法blitme来绘制图案，所以限制飞船的活动范围要在ship模块中更改他们
        self.ship.blitme()
        # 来画子弹  这里无法理解啊
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 画外星人， 这里
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
