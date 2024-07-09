import math
import os
import random
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1100
HEIGHT = 650

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

class Beam3(pg.sprite.Sprite):
    """
    爆弾に関するクラス
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    def __init__(self, emy: "Enemy", bird: Bird):
        """
        爆弾円Surfaceを生成する
        引数1 emy：爆弾を投下する敵機
        引数2 bird：攻撃対象のこうかとん
        """
        super().__init__()
        rad = random.randint(10, 50)  # 爆弾円の半径：10以上50以下の乱数
        self.image = pg.Surface((2*rad, 2*rad))
        color = random.choice(__class__.colors)  # 爆弾円の色：クラス変数からランダム選択
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        # 爆弾を投下するemyから見た攻撃対象のbirdの方向を計算
        self.vx, self.vy = calc_orientation(emy.rect, bird.rect)  
        self.rect.centerx = emy.rect.centerx
        self.rect.centery = emy.rect.centery+emy.rect.height//2
        self.speed = 6

    def update(self):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg") #背景画像
    bg_img2 = pg.transform.flip(bg_img, True, False) #背景画像
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_rect = kk_img.get_rect() #こうかとんrectの抽出
    kk_rect.center = 300, 200
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        x = tmr%3200
        screen.blit(bg_img, [-x, 0]) #背景画像を表すsurfase
        screen.blit(bg_img2, [-x+1600, 0])
        screen.blit(bg_img, [-x+3200, 0]) #背景画像を表すsurfase
        screen.blit(bg_img2, [-x+4800, 0])
        
        kye_lst = pg.key.get_pressed()
        if kye_lst[pg.K_UP]: #上矢印を押したとき
            a = -1
            b = -1
        elif kye_lst[pg.K_DOWN]:
            a = -1
            b = +1
        elif kye_lst[pg.K_LEFT]:
            a = -1
            b = 0
        elif kye_lst[pg.K_RIGHT]:
            a = +2
            b = 0
        else:
            a = -1
            b = 0
        kk_rect.move_ip(a, b)
        screen.blit(kk_img, kk_rect) #kk_imageをkk_rectの設定に従って貼り付け
        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()