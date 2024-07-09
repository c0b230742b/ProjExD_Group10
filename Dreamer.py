import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


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

class BeamAllen:
    """
    アレンが放つビームに関するクラス
    """
    def __init__(self, bird:"Bird"):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つこうかとん（Birdインスタンス）
        """
        self.img = pg.image.load(f"fig/beam.png")
        self.rct = self.img.get_rect()
        self.rct.centery = bird.rct.centery  # こうかとんの中心縦座標をビームの中心縦座標に設定
        self.rct.left = bird.rct.right  # こうかとん右座標をビーム左座標に設定
        self.vx, self.vy = +5, 0

    def update(self, screen: pg.Surface):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        if check_bound(self.rct) == (True, True):
            self.rct.move_ip(self.vx, self.vy)
            screen.blit(self.img, self.rct)    




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()