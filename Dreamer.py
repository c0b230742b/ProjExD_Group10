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


image_paths3 = [
        'fig/gamen12.jpg',
        'fig/gamen13.jpg',
        'fig/gamen14.jpg',
        'fig/gamen15.jpg',
        'fig/gamen16.jpg',
        'fig/gamen17.jpg'
    ]

class StartScreen:
    def __init__(self, image_paths):
        self.images = [pygame.image.load(path) for path in image_paths3]
        self.current_index = 0
    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            return True
        return False 
    
    def get_next_screen(self):
        return self.images[self.current_index]
    
    


def main():
    pg.display.set_caption("Dreamer")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    start_screen=StartScreen(image_paths3)
    running = True
    clock  = pg.time.Clock()
    beamallen = None
    #背景画像をロードして、ウインドウのサイズにリサイズ
    #allen = Allen((100, 600))
    show_allen = True
    tmr = 0
    current_image = start_screen.get_next_screen()
    screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen.next_image()
                    if not start_screen.next_image():  # 次の画像に進めなかった場合
                        running = False 
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                show_allen = not show_allen #アレンの表示非表示の切替(キャラの切り替えで使うかも)
        
        
        current_image = start_screen.get_next_screen()
        screen.blit(current_image, (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
        key_lst = pg.key.get_pressed()

        pg.display.update()
        clock.tick(60)

 


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
