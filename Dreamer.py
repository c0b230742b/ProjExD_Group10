import os
import sys 
import random
import pygame as pg
import time
import pygame as pg
import pygame
import math


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

class MusicPlayer:
    """
    音楽再生を管理するクラス
    """
    def __init__(self, file_path, volume=0.5):
        """
        初期化メソッド
        :param file_path: 再生する音楽ファイルのパス
        :param volume: 音量（デフォルトは0.5）
        """
        self.sound = pg.mixer.Sound(file_path)
        self.sound.set_volume(volume)
        self.playing = False

    def play(self):
        """
        音楽を再生するメソッド
        """
        if not self.playing:
            self.sound.play(-1)  # -1 はループ再生を意味するフラグ
            self.playing = True

    def stop(self):
        """
        音楽を停止するメソッド
        """
        if self.playing:
            self.sound.stop()
            self.playing = False

    def update(self):
        """
        音楽の更新（ここでは特に何もしない）
        """
        pass

class BossBeam(pg.sprite.Sprite):
    """
    ビームに関するクラス
    """
    def __init__(self, enemy, image, mag=2.0, speed = 10):
        """
        ビーム画像Surfaceを生成する
        引数 enemy：ビームを放つ敵
        """
        super().__init__()
        angle = 0
        if isinstance(enemy, Midboss):  # Midboss クラスの場合は左側にビームを発射する
            self.vx, self.vy = -math.cos(enemy.direction), -math.sin(enemy.direction)
            angle = math.degrees(math.atan2(0, 0))
        elif isinstance(enemy, Smallenemy):  # Smallenemy クラスの場合の条件分岐
            if enemy.current_mode == 'rotate':
                angle = random.uniform(225, 125)  # 扇状に放つ
                self.vx, self.vy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
                angle = math.degrees(math.atan2(-self.vy, self.vx))
            elif enemy.current_mode == 'vertical':
                self.vx, self.vy = -1, 0  # 左に向けて放つ
                angle = math.degrees(math.atan2(-self.vy, self.vx))
        else:
            self.vx, self.vy = math.cos(enemy.direction), math.sin(enemy.direction)
    
        self.image = pg.transform.rotozoom(pg.image.load(image), angle, mag)
        self.rect = self.image.get_rect()
        self.rect.centery = enemy.rect.centery
        self.rect.centerx = enemy.rect.centerx+(enemy.rect.width/2)*self.vx
        self.speed = speed

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        """
        self.rect.move_ip(self.speed * self.vx, self.speed * self.vy)
        
        # 画面外に出たらビームを消去する
        if not self.rect.colliderect(pg.Rect(0, 0, WIDTH, HEIGHT)):
            self.kill()

class Bigenemy(pg.sprite.Sprite):
    """
    大ボスに関するクラス
    """
    def __init__(self, x, y):
        """
        大ボスSurfaceを作成する
        引数1 x：大ボスのx座標
        引数2 y：大ボスのy座標
        """
        super().__init__()
        #self.bg_img = pg.image.load("fig/23300955.jpg")
        #self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/boss_koukaton.png"), 0, 0.2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 5
        self.direction = random.uniform(0, 2 * math.pi)
        self.target_direction = self.direction
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.curve_factor = 0.1  # カーブの強さを調整する係数
        self.beam_timer = 0
        self.beam_interval = 500  # ビーム発射のためのタイマーを設定

        # 音楽プレイヤーを初期化
        self.music_player = MusicPlayer("fig/Will_you_still_cry.mp3", volume=0.5)

        # 初期状態では音楽は停止しておく
        self.stop_music()

    def update(self):
        if random.random() < 0.04:  # ランダムに方向を変える確率
            self.target_direction = random.uniform(0, 2 * math.pi)
            # self.speed = random.randint(5, 15)  # ランダムな速さに変更

        # 方向を徐々にターゲット方向に向けて変更
        self.direction += (self.target_direction - self.direction) * 0.05

        # 移動量を計算
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)

        # 新しい位置を計算
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # 画面端に近づいたら滑らかに曲がる
        buffer = 100  # 画面端からの距離
        if self.rect.left < buffer:
            self.direction += self.curve_factor * (1 - self.rect.centery / HEIGHT)
        elif self.rect.right > WIDTH - buffer:
            self.direction -= self.curve_factor * (1 - self.rect.centery / HEIGHT)
        if self.rect.top < buffer:
            self.direction += self.curve_factor * (self.rect.centerx / WIDTH)
        elif self.rect.bottom > HEIGHT - buffer:
            self.direction -= self.curve_factor * (self.rect.centerx / WIDTH)

        # 新しい位置を設定
        self.rect.x = new_x
        self.rect.y = new_y

        # 画面の端に近づいたら反転
        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.direction = math.pi - self.direction
            self.target_direction = self.direction
        if not tate:
            self.direction = -self.direction
            self.target_direction = self.direction
        
        self.beam_timer += 1
        if self.beam_timer >= self.beam_interval:
            self.beam_timer = 0
            self.beam_interval = random.randint(1, 3)
            return BossBeam(self, "fig/p2.png", 0.1)  # ビームを発射
        return None

    def stop_music(self):
        """
        音楽を停止するメソッド
        """
        self.music_player.stop()

    def start_music(self):
        """
        音楽を再生するメソッド
        """
        self.music_player.play()

    def switch_to_bigboss(self):
        """
        大ボスに切り替わった際の処理
        ここで音楽を再生するなどの追加の処理を行う
        """
        self.start_music()


class Smallenemy(pg.sprite.Sprite):
    """
    小ボスに関するクラス
    """
    def __init__(self, x, y):
        """
        小ボスSurfaceを作成する
        引数1 x：小ボスのx座標
        引数2 y：小ボスのy座標
        """
        super().__init__()
        #self.bg_img = pg.image.load("fig/24535830.jpg")
        #self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/alien1.png"), 0, 2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.center = x, y
        self.speed = 5
        self.angle = 0
        self.mode = 'circle'
        self.timer = 0
        self.warp_count = 0
        self.warp_duration = 60  # 1秒（60fps * 1）
        self.warp_mode = False
        self.mode_duration = 300  # 各モードの持続時間（60fps * 5）
        self.current_mode_timer = 0
        self.current_mode = 'rotate'  # 初期モードは回転

        # 音楽プレイヤーを初期化
        self.music_player = MusicPlayer("fig/Vital_Waves.mp3", volume=0.5)

        # 初期状態では音楽を再生する
        self.start_music()

        # ビームのためのタイマー
        self.beam_timer = 0
        self.beam_interval = 500  # ビーム発射のためのタイマーを設定

    def update(self):
        self.current_mode_timer += 1

        if self.current_mode == 'rotate':
            self.angle += 0.05
            radius = 100  # 回転の半径を調整
            cx = WIDTH - radius - 100  # 右中央に収まるように中心を調整
            cy = HEIGHT // 2

            self.rect.centerx = cx + radius * math.cos(self.angle)
            self.rect.centery = cy + radius * math.sin(self.angle)

            # ビームの種類,大きさ
            self.fig = "fig/cc.png"
            self.mag = 0.1

            if self.current_mode_timer > self.mode_duration:  # 持続時間が終わったら次のモードへ
                self.current_mode = 'vertical'
                self.current_mode_timer = 0
                self.rect.x = 1000
                self.speed = 5
                self.warp_mode = True

        elif self.current_mode == 'vertical':
            self.rect.y += self.speed
            _, tate = check_bound(self.rect)

            # ビームの種類,大きさ
            self.fig = "fig/bb.png"
            self.mag = 0.1

            if not tate:
                self.speed = -self.speed  # 方向を反転
            if self.current_mode_timer > self.mode_duration:  # 持続時間が終わったら次のモードへ
                self.current_mode = 'warp'
                self.current_mode_timer = 0

        elif self.current_mode == 'warp':
            if self.warp_mode:
                # 画面外にはみ出さないようにする
                self.rect.centerx = random.randint(self.rect.width // 2, WIDTH - self.rect.width // 2)
                self.rect.centery = random.randint(self.rect.height // 2, HEIGHT - self.rect.height // 2)
                self.current_mode_timer = 0
                self.warp_mode = False
                self.warp_count += 1
            else:
                if self.current_mode_timer >= self.warp_duration:
                    self.current_mode_timer = 0
                    self.warp_mode = True

        # すべてのワープが終了したら最初のモードに戻す
        if self.warp_count >= 10:
            self.current_mode = 'rotate'
            self.angle = 0
            self.rect.center = self.center
            self.warp_count = 0
        
        # ビームの発射
        self.beam_timer += 1
        if self.beam_timer >= self.beam_interval:
            self.beam_timer = 0
            self.beam_interval = random.randint(3, 5)
            if self.current_mode != 'warp':  # ワープ中でなければビームを発射
                return BossBeam(self, self.fig, self.mag)
        return None

    def stop_music(self):
        """
        音楽を停止するメソッド
        """
        self.music_player.stop()

    def start_music(self):
        """
        音楽を再生するメソッド
        """
        self.music_player.play()

    def switch_to_smallboss(self):
        """
        小ボスに切り替わった際の処理
        ここで音楽を再生するなどの追加の処理を行う
        """
        self.start_music()



class Midboss(pg.sprite.Sprite):
    """
    中ボスのクラス
    """
    def __init__(self, x, y):
        """
        中ボスのSurfaceを作成します。
        引数1 x：中ボスのx座標
        引数2 y：中ボスのy座標
        """
        super().__init__()
        # 中ボスの画像を読み込み、サイズを調整して反転させます
        #self.bg_img = pg.image.load("fig/24535848.jpg")
        #self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        self.image = pg.transform.rotozoom(pg.image.load("fig/mika.png"), 0, 0.5)
        self.image = pg.transform.flip(self.image, False, False)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 5  # 移動速度を小さくする
        self.target_y = self.rect.y  # 垂直移動の目標Y座標
        self.set_new_target()  # 初期目標位置を設定
        

        # 音楽プレイヤーを初期化
        self.music_player = MusicPlayer("fig/crux.mp3", volume=0.5)

        # 初期状態では音楽を再生する
        self.stop_music()

        self.beam_timer = 0
        self.beam_interval = 500  # ビーム発射のためのタイマーを設定

    def set_new_target(self):
        """
        新しい目標位置を設定する関数
        """
        move_distance = random.randint(-300, 300)  # 小さなランダムな移動距離を設定
        new_target_y = self.rect.y + move_distance
        # 画面内に収まるように調整
        self.target_y = max(self.rect.height // 2, min(new_target_y, HEIGHT - self.rect.height // 2))

    def update(self):
        # 縦移動を実行
        if abs(self.rect.y - self.target_y) < self.speed:
            self.rect.y = self.target_y
            self.set_new_target()  # 目標位置に達したら新しい目標位置を設定
        else:
            direction = 1 if self.target_y > self.rect.y else -1
            self.rect.y += direction * self.speed

        # 画面外に出ないように調整
        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.speed *= -1  # 横方向の速度を反転

        _, tate = check_bound(self.rect)
        if not tate:
            self.set_new_target()  # 垂直移動を元に戻すために新しい目標位置を設定

        self.direction = 0

        # ビーム速度
        self.b_speed = 0

        self.beam_timer += 1
        if self.beam_timer >= self.beam_interval:
            self.beam_timer = 0
            randomcounter = random.randint(1, 30)
            if randomcounter == 1:
                self.beam_interval = random.randint(10, 30)
                return BossBeam(self, "fig/b.png", 0.3)  # 大ビームを発射
            elif 1 < randomcounter < 30:
                self.beam_interval = random.randint(20, 30)
                self.b_speed = 10
                return BossBeam(self, "fig/mika_ac.png", 0.12, self.b_speed)
    

        return None

    def stop_music(self):
        """
        音楽を停止するメソッド
        """
        self.music_player.stop()

    def start_music(self):
        """
        音楽を再生するメソッド
        """
        self.music_player.play()

    def switch_to_midboss(self):
        """
        小ボスに切り替わった際の処理
        ここで音楽を再生するなどの追加の処理を行う
        """
        self.start_music()

class Mika:
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (+10, 0),
        pg.K_UP: (0, -10),   # 上方向への移動を追加
        pg.K_DOWN: (0, 10),  # 下方向への移動を追加
    }

    imgs = {
        (+5, 0): pg.transform.rotozoom(pg.image.load("fig/mika.png"), 0, 0.4),   # 初期画像を指定してください
        (-10, 0): pg.transform.rotozoom(pg.image.load("fig/mika(0).png"), 0, 0.4),
        (+10, 0): pg.transform.rotozoom(pg.image.load("fig/mika(1).png"), 0, 0.4),
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/mika(2).png"), 0, 0.4),   #上向き
        (0, 10): pg.transform.rotozoom(pg.image.load("fig/mika.png"), 0, 0.4), #下向き
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.max_hp = 100         # 最大HP
        self.current_hp = 100     # 現在のHP

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/file({num}).png"), 0, 4.0)
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
        elif self.rct.right > screen.get_width():
            self.rct.right = screen.get_width()

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)
        
        if self.rct.top < 0:
            self.rct.top = 0
        elif self.rct.bottom > screen.get_height():
            self.rct.bottom = screen.get_height()

        # 移動が成功した場合、前回の位置を更新
        if self.rct.topleft == prev_rect.topleft:
            self.rct.topleft = prev_rect.topleft

        screen.blit(self.img, self.rct)

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0
            

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
    show_allen = False

    player_hp = HP(50, 50, 100)
    beam_list = []  # ビームのリストを初期化

    start_screen=StartScreen(image_paths)
    in_start_screen = True
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

    b_enemy = Bigenemy(800, 300)
    s_enemy = Smallenemy(1100, 650)
    m_enemy = Midboss(1000, 400)

    enemies = [s_enemy, m_enemy, b_enemy]
    current_enemy = 0  # 現在表示中の敵のインデックス
    enemy_group = pg.sprite.Group(enemies[current_enemy])
    beams = pg.sprite.Group()  # ビームグループの追加

    # 初期状態で音楽を再生
    enemies[current_enemy].start_music()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enterキーでクラスを切り替え
                    # 前の敵の音楽を停止
                    enemies[current_enemy].stop_music()
                    current_enemy = (current_enemy + 1) % len(enemies)
                    enemy_group = pg.sprite.Group(enemies[current_enemy])

                    # 新しい敵が大ボスならば、switch_to_bigbossを呼ぶ
                    if isinstance(enemies[current_enemy], Bigenemy):
                        enemies[current_enemy].switch_to_bigboss()
                    # 新しい敵が小ボスならば、switch_to_smallbossを呼ぶ
                    elif isinstance(enemies[current_enemy], Smallenemy):
                        enemies[current_enemy].switch_to_smallboss()
                    elif isinstance(enemies[current_enemy], Midboss):
                        enemies[current_enemy].switch_to_midboss()
                    enemies[current_enemy].start_music()

                    # ビームグループを空にする
                    beams.empty()
                    #current_bg_img = enemies[current_enemy].bg_img
                    #screen.blit(current_bg_img, (0, 0))
                if event.key == pg.K_2 and show_hiroin:
                    show_hiroin = False
                    show_allen = True
                    allen.rct.center = hiroin.rct.center
                elif event.key == pg.K_3 and show_allen:
                    show_allen = False
                    show_hiroin = True
                    hiroin.rct.center = allen.rct.center
                elif event.key == pg.K_h and show_hiroin:
                    #player_hp.heal(30)
                    #hiroin.heal(30)
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
                    back_img = pg.image.load("fig/24535848.jpg")
                    back_img = pg.transform.scale(back_img, (1600, 900))
                if event.key == pg.K_b: #bキーを押すことでミカ撃退画面に移行
                    in_start_screen2 = True
                    back_img = pg.image.load("fig/23300955.jpg")
                    back_img = pg.transform.scale(back_img, (1600, 900))
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

        #current_bg_img = enemies[current_enemy].bg_img
        #screen.blit(current_bg_img, (0, 0))
        
        # 更新
        enemy_group.update()
        enemy_group.draw(screen)
        
        # ビームの発射と更新
        beam = enemies[current_enemy].update()
        if beam:
            beams.add(beam)
        beams.update()
        beams.draw(screen)

        
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
