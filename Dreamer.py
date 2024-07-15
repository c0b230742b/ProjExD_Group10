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
        self.image = pg.transform.rotozoom(pg.image.load("fig/allen_file"), 0, 0.9)
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

        x = tmr%3200
        screen.blit(back_img, [0, 0]) #背景画像を表すsurfase
       
        
        key_lst = pg.key.get_pressed()
        x, y = 0, 0
        if key_lst[pg.K_UP]:
            x , y =0 ,-2
        if key_lst[pg.K_DOWN]:
            x, y= 0, 2
        if key_lst[pg.K_RIGHT]:
            x, y=2, 0
        if key_lst[pg.K_LEFT]:
            x, y=-2, 0
        
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