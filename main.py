
import arcade
from math import pi, cos, sin
import random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def get_distance(hero1, hero2):
    return ((hero1.x - hero2.x) ** 2 + (hero1.y - hero2.y) ** 2) ** 0.5


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = [10, 10, 10]
        self.speed = 5
        self.bullet_score = 1000


    def draw(self):
        arcade.draw_line(self.x, self.y, self.x + self.dx * 5, self.y + self.dy * 5, self.color, 4)


    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def is_removeable(self):
        out_x = not 0 < self.x < SCREEN_WIDTH
        out_y = not 0 < self.y < SCREEN_HEIGHT
        return out_x or out_y

    def is_hit(self, hero):
        dist = get_distance(self, hero) <= hero.r
        self.bullet_score += 2
        return dist

class Hero:
    def __init__(self, color = arcade.color.RED_DEVIL, size=30):
        self.x = random.randint(100, 600)
        self.y = random.randint(100, 500)
        self.dir = random.randint(0, 360)
        self.r = size
        self.speed = 1
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)
        self.color = color
        self.dyy = 1.2
        self.dxx = 1.2
        self.a = 0
        self.bullet_score = 1


    def it_crash(self, hero):
        return get_distance(self, hero) <= self.r + hero.r

    def to_growth(self):
        if self.r < SCREEN_HEIGHT // 3:
            self.r += 2

    def turn_left(self):
        self.dir -= 15
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)

    def turn_right(self):
        self.dir += 15
        self.dx = sin(self.dir * pi / 180)
        self.dy = cos(self.dir * pi / 180)

    def speed_up(self):
        self.dyy += self.speed
        self.dxx += self.speed
        self.a += 1

    def speed_down(self):
        self.dyy -= self.speed
        self.dxx -= self.speed
        self.a -= 1

    def bullet_reload(self):
        self.bullet_score = 1

    def shoot(self, bullet_list):
        if self.bullet_score > 0:
            self.bullet_score -= 1
            bullet_list.append(Bullet(self.x + self.dx * self.r,
                                      self.y + self.dy * self.r,
                                      self.dx, self.dy))

    # def dx(self):
    #     return sin(self.dir * pi / 180)
    #
    # def dy(self):
    #     return cos(self.dir * pi / 180)

    def move(self):
        if self.x > SCREEN_WIDTH - self.r or self.x < self.r:
            self.dir *= -1
            self.dx = sin(self.dir * pi / 180)
            self.dy = cos(self.dir * pi / 180)

        if self.y > SCREEN_HEIGHT - self.r or self.y < self.r:
            self.dir = 180 - self.dir
            self.dx = sin(self.dir * pi / 180)
            self.dy = cos(self.dir * pi / 180)



        # print(self.dir, self.y)

        if self.x > SCREEN_WIDTH - self.r:
            self.x = SCREEN_WIDTH - self.r
        if self.x < self.r:
            self.x = self.r


        self.y += self.dy * self.dyy
        self.x += self.dx * self.dxx


    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)
        x1, y1, = self.x, self.y
        x2 = x1 + self.r * 1.3 * self.dx
        y2 = y1 + self.r * 1.3 * self.dy
        arcade.draw_line(x1, y1, x2, y2, arcade.color.BLACK, 4)




class MyGame(arcade.Window):
    """ Главный класс приложения. """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color([240, 240, 240, 150])

    def setup(self):
        # Настроить игру здесь
        self.hero = Hero()
        self.enemy_list = []
        self.game_over = False
        self.bullet_list = []
        for i in range(10):
            self.enemy_list.append(Hero(color=arcade.color.BLUE, size=20))

    def get_telemetry(self):
        st = 'bullet: {}\n'.format(self.hero.bullet_score) + \
             'count enemy: {}'.format(len(self.enemy_list))
        return st

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        arcade.draw_text(self.get_telemetry(), 10, 60, arcade.color.BLACK, 24)
        if self.game_over:
            arcade.draw_text('YOU WIN', 300, 400, [200, 0, 0], 30)
        else:
            for enemy in self.enemy_list:
                arcade.draw_line(self.hero.x, self.hero.y, enemy.x, enemy.y, (50, 50, 50))
                enemy.draw()
            self.hero.draw()

            for bullet in self.bullet_list:
                bullet.draw()


    def on_key_press(self, key, modifiers):
        """Вызывается при нажатии пользователем клавиши"""

        if key == arcade.key.LEFT:
            self.hero.turn_left()
        elif key == arcade.key.RIGHT:
            self.hero.turn_right()
        elif key == arcade.key.UP:
            self.hero.speed_up()
        elif key == arcade.key.DOWN:
            self.hero.speed_down()
        elif key == arcade.key.R:
            self.hero.bullet_reload()


    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        if not self.game_over:
            self.hero.move()
            for enemy in self.enemy_list:
                enemy.move()
            for bullet in self.bullet_list:
                bullet.move()


                # обрабатываем попадание пулек в вражин
                if bullet.is_removeable():
                    self.bullet_list.remove(bullet)

                for enemy in self.enemy_list:
                    if bullet.is_hit(enemy):
                        self.enemy_list.remove(enemy)
                        self.bullet_list.remove(bullet)


            #for enemy in self.enemy_list:
                #if self.hero.it_crash(enemy):
                #   self.hero.to_growth()
                #  self.enemy_list.remove(enemy)
            if len(self.enemy_list) == 0:
                self.game_over = True

            if random.randint(1, 400) < 5:
                self.enemy_list.append(Hero(color=arcade.color.BLUE, size=20))

            self.hero.shoot(self.bullet_list)
            self.hero.bullet_reload()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
