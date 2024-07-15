import os
import sys
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
    screen = pg.display.set_mode((1200, 700))
    clock  = pg.time.Clock()
    beamallen = None
    #背景画像をロードして、ウインドウのサイズにリサイズ
    back_img = pg.image.load("fig/24535830.jpg") 
    back_img = pg.transform.scale(back_img, (1200, 700))
    allen = Allen((100, 600))
    show_allen = True
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                show_allen = not show_allen #アレンの表示非表示の切替(キャラの切り替えで使うかも)
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # スペースキー押下でBeamクラスのインスタンス生成
                beamallen = BeamAllen(allen)
        
        screen.blit(back_img, [0, 0]) #背景画像を表すsurfase
       
        key_lst = pg.key.get_pressed()
        if show_allen:
            allen.update(key_lst, screen)
        if beamallen is not None:
            beamallen.update(screen)

        pg.display.update()
        clock.tick(60)

 
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()