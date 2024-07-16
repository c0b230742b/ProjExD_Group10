import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class HP:
    def __init__(self, x, y, max_hp, width=400, height=30) -> None:
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.width = width
        self.height = height
        self.font = pg.font.Font(None, 36)
        self.heal_sound = pg.mixer.Sound("fig/heal_sound.mp3")
        self.heal_text = None
        self.heal_text_time = 0

    def draw(self, screen, character_rect):
        fill = (self.current_hp / self.max_hp) * self.width #1ダメージ当たりの減少量
        fill_rect = pg.Rect(self.x, self.y, fill, self.height)
        border_rect = pg.Rect(self.x, self.y, self.width, self.height)

        if self.current_hp <= 20:
            pg.draw.rect(screen, (255, 0, 0), fill_rect)
        else:
            pg.draw.rect(screen, (0, 255, 0), fill_rect)

        pg.draw.rect(screen, (0, 0, 0), border_rect, 2)
        #self.heal_text textが存在するかどうか pg.time.get_ticks() 現在の時刻を取得 
        if self.heal_text and pg.time.get_ticks() - self.heal_text_time < 2000: #テキストが設定されてから2秒以内かどうか
            screen.blit(self.heal_text, (character_rect.right + 10, character_rect.y))

    def take_damage(self, amount: int): #amount hpの変化量
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        self.heal_sound.play()
        self.heal_text = self.font.render(f"{amount} HP UP!", True, (0, 255, 0))
        self.heal_text_time = pg.time.get_ticks()


class Allen:
    delta = {
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (+10, 0),
        pg.K_UP: (0, -10),
        pg.K_DOWN: (0, 10),
    }

    imgs = {
        (+5, 0): pg.transform.rotozoom(pg.image.load("fig/allen_file.png"), 0, 0.4),
        (-10, 0): pg.transform.rotozoom(pg.image.load("fig/allen_file(0).png"), 0, 0.4),
        (+10, 0): pg.transform.rotozoom(pg.image.load("fig/allen_file(1).png"), 0, 0.4),
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/allen_file(2).png"), 0, 0.4),
        (0, 10): pg.transform.rotozoom(pg.image.load("fig/allen_file.png"), 0, 0.4),
    }

    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.max_hp = 100
        self.current_hp = 100

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/allen_file({num}).png"), 0, 4.0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rct.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        self.rct.move_ip(sum_mv)

        if self.rct.left < 0:
            self.rct.left = 0
        elif self.rct.right > screen.get_width():
            self.rct.right = screen.get_width()

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)

        if self.rct.top < 0:
            self.rct.top = 0
        elif self.rct.bottom > screen.get_height():
            self.rct.bottom = screen.get_height()

        screen.blit(self.img, self.rct)

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0


class Alice:
    delta = {
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (10, 0),
        pg.K_UP: (0, -10),
        pg.K_DOWN: (0, 10),
    }

    imgs = {
        (5, 0): pg.transform.rotozoom(pg.image.load("fig/alice_file.png"), 0, 0.6),
        (-10, 0): pg.transform.rotozoom(pg.image.load("fig/alice_file(0).png"), 0, 0.6),
        (10, 0): pg.transform.rotozoom(pg.image.load("fig/alice_file(1).png"), 0, 0.6),
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/alice_file(2).png"), 0, 1.4),
        (0, 10): pg.transform.rotozoom(pg.image.load("fig/alice_file.png"), 0, 0.6),
    }

    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.imgs[(5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.gravity = 0.5
        self.can_heal = True

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/file({num}).png"), 0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rct.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        prev_rect = self.rct.copy()

        self.rct.move_ip(sum_mv)

        if self.rct.left < 0:
            self.rct.left = 0
        elif self.rct.right > screen.get_width(): #画面横にいったら
            self.rct.right = screen.get_width()

        if self.rct.top < 0:
            self.rct.top = 0
        elif self.rct.bottom > screen.get_height(): #画面縦にいったら
            self.rct.bottom = screen.get_height()

        #移動が成功した場合、前回の位置を更新
        if self.rct.topleft == prev_rect.topleft:
            self.rct.topleft = prev_rect.topleft

        #移動方向に応じた画像の更新
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)

        screen.blit(self.img, self.rct)

    def heal(self, amount):
        pass

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0


class Frame:
    def __init__(self, frame_x=20, frame_y=570, frame_width=120, frame_height=120):
        self.frame_x = frame_x
        self.frame_y = frame_y
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.alice_img = pg.transform.rotozoom(pg.image.load("fig/alice.png"), 0, 1.0)
        self.allen_img = pg.transform.rotozoom(pg.image.load("fig/allen.png"), 0, 0.6)

    def draw(self, screen, show_alice: bool, show_allen: bool):
        chara_rect = pg.Surface((self.frame_width, self.frame_height))
        pg.draw.rect(chara_rect, (0, 0, 0), pg.Rect(self.frame_x, self.frame_y, self.frame_width, self.frame_height))

        if show_alice:
            alice_img_rect = self.allen_img.get_rect(center=(self.frame_width // 2, self.frame_height // 2))
            chara_rect.blit(self.allen_img, alice_img_rect)
        elif show_allen:
            allen_img_rect = self.alice_img.get_rect(center=(self.frame_width // 2, self.frame_height // 2))
            chara_rect.blit(self.alice_img, allen_img_rect)

        screen.blit(chara_rect, (self.frame_x, self.frame_y))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((1200, 700))
    clock = pg.time.Clock()
    #背景画像をロードしてウインドウのサイズにリサイズ
    back_img = pg.image.load("fig/24535830.jpg")
    back_img = pg.transform.scale(back_img, (1200, 700))
    alice = Alice((100, 500))
    allen = Allen((100, 500))
    frame = Frame()
    show_alice = False
    show_allen = True

    player_hp = HP(50, 50, 100)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_2 and show_alice:
                    show_alice = False
                    show_allen = True
                    allen.rct.center = alice.rct.center #現在の位置を保存
                elif event.key == pg.K_3 and show_allen:
                    show_allen = False
                    show_alice = True
                    alice.rct.center = allen.rct.center #現在の位置を保存
                elif event.key == pg.K_h and show_alice:
                    player_hp.heal(30)
                    alice.heal(30)
                    show_alice = False
                    show_allen = True

        screen.blit(back_img, [0, 0])

        key_lst = pg.key.get_pressed()
        if show_alice:
            alice.update(key_lst, screen)
        elif show_allen:
            allen.update(key_lst, screen)

        player_hp.draw(screen, alice.rct if show_alice else allen.rct)
        frame.draw(screen, show_alice, show_allen)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
