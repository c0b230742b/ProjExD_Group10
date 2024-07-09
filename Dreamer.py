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

class Allen(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/スクリーンショット 2024-07-09 145858.png"), 0, 0.9)
        self.rect = self.image.get_rect()
        self.rect.center = 300, 200
        self.gravity = 1
        self.velocity = 0
        self.on_ground = True
    
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.on_ground:
            self.velocity = self.jump_speed
            self.on_ground = False

        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0
            self.on_ground = True
"""
class Beam3(pg.sprite.Sprite):
    
  爆弾に関するクラス
    
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    def __init__(self, emy: "Enemy", bird: Bird):
        
        爆弾円Surfaceを生成する
        引数1 emy：爆弾を投下する敵機
        引数2 bird：攻撃対象のこうかとん
        
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
        
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()
"""
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

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    back_img = pg.image.load("fig/24535830.jpg") #背景画像
    
    allen = Allen()
    all_sprites = pg.sprite.Group()
    all_sprites.add(allen)

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beam = BeamAllen(Allen) 

        x = tmr%3200
        screen.blit(back_img, [0, 0]) #背景画像を表すsurfase
       
        
        key_lst = pg.key.get_pressed()
        x, y = 0, 0
        if key_lst[pg.K_UP]:
            x , y =0 ,-20
        if key_lst[pg.K_DOWN]:
            x, y= 0, 20
        if key_lst[pg.K_RIGHT]:
            x, y=20, 0
        if key_lst[pg.K_LEFT]:
            x, y=-20  , 0
        
        allen.rect.move_ip(x, y)
        all_sprites.update()

        screen.blit(back_img, (0, 0))
        all_sprites.draw(screen) 
        pg.display.update()
        tmr += 1        
        clock.tick(60)

 




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()