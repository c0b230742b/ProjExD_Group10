import math
import os
import random
import sys
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
    

class Allen:
    """
    アレンに関するクラス
    """
    #キー移動に対する移動量
    delta = {
        pg.K_LEFT:(-10, 0),
        pg.K_RIGHT:(10, 0)
    }
    #画像のロード
    imgs = {
        (5, 0): pg.image.load("fig/allen_file.png"),      #初期状態(正面)
        (-10, 0): pg.image.load("fig/allen_file(0).png"), #左向き
        (10, 0): pg.image.load("fig/allen_file(1).png")   #右向き
    }
    
    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.imgs[(5, 0)] #初期画像の設定
        self.rct:pg.Rect = self.img.get_rect() 
        self.rct.center = xy
        self.gravity = 0.5      #重力の設定
        self.is_jumping = False #ジャンプ状態
        self.jump_speed = 20    #ジャンプ速度
    
    def change_img(self, num: int, screen: pg.Surface):
        #画像を変更、位置を調整して表示
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/allen_file({num}).png"), 0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rct.center
        screen.blit(self.image, self.rect)

    
    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        if key_lst[pg.K_UP] and not self.is_jumping:
                self.is_jumping = True
                self.jump_speed = 15

        if self.is_jumping: #ジャンプ中の処理
            self.rct.y -= self.jump_speed
            self.jump_speed -= self.gravity
            if self.rct.bottom >= 700: #地面についたら
                self.rct.bottom = 700
                self.is_jumping = False
                self.jump_speed = 15
        #移動処理
        self.rct.move_ip(sum_mv)
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)
        screen.blit(self.img, self.rct)
 


def main():
    pg.display.set_caption("Dreamer")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    back_img = pg.image.load("fig/allen_file.png") 
    back_img = pg.transform.scale(back_img, (WIDTH, HEIGHT))
    back_img = pg.image.load("fig/24535830.jpg") 
    back_img = pg.transform.scale(back_img, (WIDTH, HEIGHT))
    allen = Allen((100, 600))
    
    running = True
    clock  = pg.time.Clock()
    show_allen = True
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
            if event.type == pygame.KEYDOWN:
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
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                show_allen = not show_allen #アレンの表示非表示の切替(キャラの切り替えで使うかも)
        
        if in_start_screen: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
        elif in_start_screen1: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen1.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
        elif in_start_screen2: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen2.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
        elif in_start_screen3: #スタート画面が表示されているときに現在の画像の描写
            current_image = start_screen3.get_next_screen()
            screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
        else:
            screen.blit(back_img, (0, 0))  # Clear screen with white
            if show_allen:
                allen.update(pg.key.get_pressed(), screen)

        key_lst = pg.key.get_pressed()

        pg.display.update()
        clock.tick(60)

 


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()