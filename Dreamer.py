import os
import sys
import pygame as pg
import time
import pygame as pg
import pygame


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 1600
HEIGHT = 900
def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

image_paths = [
        'fig/gamen1.png',
        'fig/gamen2.png',
        'fig/gamen3.png',
        'fig/gamen4.png',
        'fig/gamen5.png',
        'fig/gamen6.jpg'
    ]
image_paths1 = [
        'fig/gamen7.jpg',
        'fig/gamen8.jpg',
        'fig/gamen9.jpg',
        'fig/gamen10.jpg',
        'fig/gamen11.jpg'
    ]
image_paths2 = [
        'fig/gamen12.jpg',
        'fig/gamen13.jpg',
        'fig/gamen14.jpg',
        'fig/gamen15.jpg',
        'fig/gamen16.jpg',
        'fig/gamen17.jpg'
    ]
image_paths3 = [
        'fig/gamen18.jpg',
        'fig/gamen19.jpg',
        'fig/gamen20.jpg',
        'fig/gamen21.jpg',
        'fig/gamen22.jpg',
        'fig/gamen23.jpg',
        'fig/gamen1.png'
    ]
class StartScreen:
    """
    スタート画面を表すクラス
    """
    def __init__(self, image_paths):
        """画像をリスト化して保存する
        """
        self.images = [pygame.image.load(path) for path in image_paths]
        self.current_index = 0
    def next_image(self):
        """
        次の画像に進むメソッド
        最後の画像出ない場合Trueを返し最後の場合Falseを返す
        """
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            return True
        return False 
    
    def get_next_screen(self):
        """
        現在の画像を表すメソッド
        """
        return self.images[self.current_index]
 

class HP:
    def __init__(self, x, y, max_hp, width=400, height=30) -> None:
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.width = width
        self.height = height
        self.font = pg.font.Font(None, 36)
        #self.heal_sound = pg.mixer.Sound("fig/heal_sound.mp3")
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
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/allen_file(2).png"), 0, 0.2),
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

class BeamAllen:
    """
    アレンが放つビームに関するクラス
    """
    def __init__(self, Allen:"Allen"):
        """
        ビーム画像Surfaceを生成する
        引数 Allen：ビームを放つアレン（Allenインスタンス）
        """
        self.img = pg.image.load(f"fig/beam.png")
        self.rct = self.img.get_rect()
        self.rct.centery = Allen.rct.centery  # アレンの中心縦座標をビームの中心縦座標に設定
        self.rct.left = Allen.rct.right  # アレン右座標をビーム左座標に設定
        self.vx, self.vy = +5, 0

    def update(self, screen: pg.Surface):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        if check_bound(self.rct) == (True, True):
            self.rct.move_ip(self.vx, self.vy)
            screen.blit(self.img, self.rct)

class Hiroin:
    delta = {
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (10, 0),
        pg.K_UP: (0, -10),
        pg.K_DOWN: (0, 10),
    }

    imgs = {
        (5, 0): pg.transform.rotozoom(pg.image.load("fig/hiroin_file.png"), 0, 0.6),
        (-10, 0): pg.transform.rotozoom(pg.image.load("fig/hiroin_file(0).png"), 0, 0.6),
        (10, 0): pg.transform.rotozoom(pg.image.load("fig/hiroin_file(1).png"), 0, 0.6),
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/hiroin_file(2).png"), 0, 0.16),
        (0, 10): pg.transform.rotozoom(pg.image.load("fig/hiroin_file.png"), 0, 0.6),
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
        self.hiroin_img = pg.transform.rotozoom(pg.image.load("fig/hiroin_file.png"), 0, 1.0)
        self.allen_img = pg.transform.rotozoom(pg.image.load("fig/allen_file.png"), 0, 0.6)

    def draw(self, screen, show_hiroin: bool, show_allen: bool):
        chara_rect = pg.Surface((self.frame_width, self.frame_height))
        pg.draw.rect(chara_rect, (0, 0, 0), pg.Rect(self.frame_x, self.frame_y, self.frame_width, self.frame_height))

        if show_hiroin:
            hiroin_img_rect = self.allen_img.get_rect(center=(self.frame_width // 2, self.frame_height // 2))
            chara_rect.blit(self.allen_img, hiroin_img_rect)
        elif show_allen:
            allen_img_rect = self.hiroin_img.get_rect(center=(self.frame_width // 2, self.frame_height // 2))
            chara_rect.blit(self.hiroin_img, allen_img_rect)

        screen.blit(chara_rect, (self.frame_x, self.frame_y))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    back_img = pg.image.load("fig/24535830.jpg")
    back_img = pg.transform.scale(back_img, (1600, 900))
    
    hiroin = Hiroin((100, 500))
    allen = Allen((100, 500))
    frame = Frame()
    show_hiroin = False
    show_allen = True

    player_hp = HP(50, 50, 100)
    beam_list = []  # ビームのリストを初期化

    start_screen=StartScreen(image_paths)
    in_start_screen = False
    current_image = start_screen.get_next_screen()
    
    start_screen1=StartScreen(image_paths1)
    in_start_screen1 = False
    current_image = start_screen.get_next_screen()

    start_screen2=StartScreen(image_paths2)
    in_start_screen2 = False
    current_image = start_screen.get_next_screen()

    start_screen3=StartScreen(image_paths3)
    in_start_screen3 = False
    current_image = start_screen.get_next_screen()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_2 and show_hiroin:
                    show_hiroin = False
                    show_allen = True
                    allen.rct.center = hiroin.rct.center
                elif event.key == pg.K_3 and show_allen:
                    show_allen = False
                    show_hiroin = True
                    hiroin.rct.center = allen.rct.center
                elif event.key == pg.K_h and show_hiroin:
                    player_hp.heal(30)
                    hiroin.heal(30)
                    show_hiroin = False
                    show_allen = True
                elif event.key == pg.K_SPACE and show_allen:
                    # SPACEキーが押されたときに新しいBeamAllenインスタンスを作成してリストに追加
                    beamallen = BeamAllen(allen)
                    beam_list.append(beamallen)
                if event.key == pg.K_s: #sキーを押すことでスタート画面に移行
                    in_start_screen = True
                if event.key == pg.K_a: #aキーを押すことでミカ登場画面に移行
                    in_start_screen1 = True
                if event.key == pg.K_b: #bキーを押すことでミカ撃退画面に移行
                    in_start_screen2 = True
                if event.key == pg.K_c: #cキーを押すことでこうかとん撃退後画面に移行
                    in_start_screen3 = True   
                if event.key == pg.K_RETURN and in_start_screen:#エンターキーを押すことで次の画面に映る
                    if not start_screen.next_image():
                        in_start_screen = False
                if event.key == pg.K_RETURN and in_start_screen1:#エンターキーを押すことで次の画面に映る
                    if not start_screen1.next_image():
                        in_start_screen1 = False
                if event.key == pg.K_RETURN and in_start_screen2:#エンターキーを押すことで次の画面に映る
                    if not start_screen2.next_image():
                        in_start_screen2 = False
                if event.key == pg.K_RETURN and in_start_screen3:#エンターキーを押すことで次の画面に映る
                    if not start_screen3.next_image():
                        in_start_screen3 = False
                        time.sleep(5)
                        return   

                if event.key == pg.K_s and in_start_screen:
                    start_screen = StartScreen(image_paths)
                if event.key == pg.K_a and in_start_screen1:
                    start_screen1 = StartScreen(image_paths1)
                if event.key == pg.K_b and in_start_screen2:
                    start_screen2 = StartScreen(image_paths2)
                if event.key == pg.K_c and in_start_screen3:
                    start_screen3 = StartScreen(image_paths3)  

        screen.blit(back_img, [0, 0])

        if in_start_screen: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
            show_hiroin = False
            show_allen = False
        elif in_start_screen1: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen1.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
            show_hiroin = False
            show_allen = False
        elif in_start_screen2: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen2.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
            show_hiroin = False
            show_allen = False
        elif in_start_screen3: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen3.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
            show_hiroin = False
            show_allen = False
        else:
            screen.blit(back_img, (0, 0))  
            show_allen = True
            show_hiroin = False
            player_hp.draw(screen, hiroin.rct if show_hiroin else allen.rct)
            frame.draw(screen, show_hiroin, show_allen)
        
        key_lst = pg.key.get_pressed()
        if show_hiroin:
            hiroin.update(key_lst, screen)
        elif show_allen:
            allen.update(key_lst, screen)

        # すべてのビームを更新して描画
        for beam in beam_list:
            beam.update(screen)

        
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
