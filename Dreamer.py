import os
import sys
import random
import pygame as pg
import time
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 1600
HEIGHT = 900

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
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
    def __init__(self, image_paths):
        self.images = [pg.image.load(path) for path in image_paths]
        self.current_index = 0

    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            return True
        return False

    def get_next_screen(self):
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
        self.heal_text = None
        self.heal_text_time = 0

    def draw(self, screen, character_rect):
        fill = (self.current_hp / self.max_hp) * self.width
        fill_rect = pg.Rect(self.x, self.y, fill, self.height)
        border_rect = pg.Rect(self.x, self.y, self.width, self.height)

        if self.current_hp <= 20:
            pg.draw.rect(screen, (255, 0, 0), fill_rect)
        else:
            pg.draw.rect(screen, (0, 255, 0), fill_rect)

        pg.draw.rect(screen, (0, 0, 0), border_rect, 2)
        if self.heal_text and pg.time.get_ticks() - self.heal_text_time < 2000:
            screen.blit(self.heal_text, (character_rect.right + 10, character_rect.y))

    def take_damage(self, amount: int):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        # self.heal_sound.play()
        self.heal_text = self.font.render(f"{amount} HP UP!", True, (0, 255, 0))
        self.heal_text_time = pg.time.get_ticks()

class Allen(pg.sprite.Sprite):
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
        super().__init__()
        self.image = __class__.imgs[(+5, 0)]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.max_hp = 100
        self.current_hp = 100

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/allen_file({num}).png"), 0, 4.0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        self.rect.move_ip(sum_mv)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.image = __class__.imgs.get(tuple(sum_mv), self.image)

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0

class BeamAllen(pg.sprite.Sprite):
    def __init__(self, allen: Allen):
        super().__init__()
        self.image = pg.image.load("fig/beam.png")
        self.rect = self.image.get_rect()
        self.rect.centery = allen.rect.centery
        self.rect.left = allen.rect.right
        self.vx, self.vy = +5, 0

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        if not pg.Rect(0, 0, WIDTH, HEIGHT).contains(self.rect):
            self.kill()

class Hiroin(pg.sprite.Sprite):
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
        super().__init__()
        self.image = __class__.imgs[(5, 0)]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.gravity = 0.5
        self.can_heal = True

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/file({num}).png"), 0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        prev_rect = self.rect.copy()

        self.rect.move_ip(sum_mv)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

        if self.rect.topleft == prev_rect.topleft:
            self.rect.topleft = prev_rect.topleft

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.image = __class__.imgs.get(tuple(sum_mv), self.image)

        screen.blit(self.image, self.rect)

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
    def __init__(self, file_path, volume=0.5):
        self.sound = pg.mixer.Sound(file_path)
        self.sound.set_volume(volume)
        self.playing = False

    def play(self):
        if not self.playing:
            self.sound.play(-1)
            self.playing = True

    def stop(self):
        if self.playing:
            self.sound.stop()
            self.playing = False

    def update(self):
        pass

class BossBeam(pg.sprite.Sprite):
    def __init__(self, enemy, image, mag=2.0, speed=10):
        super().__init__()
        angle = 0
        if isinstance(enemy, Midboss):
            if enemy.current_mode == "hissatu":
                angle = random.uniform(225, 125)
                self.vx, self.vy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
                angle = math.degrees(math.atan2(-self.vy, self.vx))
            else:
                self.vx, self.vy = -math.cos(enemy.direction), -math.sin(enemy.direction)
                angle = math.degrees(math.atan2(0, 0))
        elif isinstance(enemy, Smallenemy):
            if enemy.current_mode == 'rotate':
                angle = random.uniform(225, 125)
                self.vx, self.vy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
                angle = math.degrees(math.atan2(-self.vy, self.vx))
            elif enemy.current_mode == 'vertical':
                self.vx, self.vy = -1, 0
                angle = math.degrees(math.atan2(-self.vy, self.vx))
        else:
            self.vx, self.vy = math.cos(enemy.direction), math.sin(enemy.direction)

        self.image = pg.transform.rotozoom(pg.image.load(image), angle, mag)
        self.rect = self.image.get_rect()
        self.rect.centery = enemy.rect.centery
        self.rect.centerx = enemy.rect.centerx + (enemy.rect.width / 2) * self.vx
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed * self.vx, self.speed * self.vy)
        if not self.rect.colliderect(pg.Rect(0, 0, WIDTH, HEIGHT)):
            self.kill()

    def set_speed(self, new_speed):
        self.speed = new_speed

class Bigenemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/boss_koukaton.png"), 0, 0.2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 5
        self.direction = random.uniform(0, 2 * math.pi)
        self.target_direction = self.direction
        self.curve_factor = 0.1
        self.beam_timer = 0
        self.beam_interval = 0
        self.music_player = MusicPlayer("fig/Will_you_still_cry.mp3", volume=0.5)
        self.stop_music()
        self.hp = HP(self.rect.x, self.rect.y - 40, max_hp=100)

    def update(self):
        if random.random() < 0.04:
            self.target_direction = random.uniform(0, 2 * math.pi)

        self.direction += (self.target_direction - self.direction) * 0.05

        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        buffer = 100
        if self.rect.left < buffer:
            self.direction += self.curve_factor * (1 - self.rect.centery / HEIGHT)
        elif self.rect.right > WIDTH - buffer:
            self.direction -= self.curve_factor * (1 - self.rect.centery / HEIGHT)
        if self.rect.top < buffer:
            self.direction += self.curve_factor * (self.rect.centerx / WIDTH)
        elif self.rect.bottom > HEIGHT - buffer:
            self.direction -= self.curve_factor * (self.rect.centerx / WIDTH)

        self.rect.x = new_x
        self.rect.y = new_y

        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.direction = math.pi - self.direction
            self.target_direction = self.direction
        if not tate:
            self.direction = -self.direction
            self.target_direction = self.direction

        if self.hp.current_hp <= 0:
            self.kill()
            return None

        self.beam_timer += 1
        if self.beam_timer >= self.beam_interval:
            self.beam_timer = 0
            self.beam_interval = random.randint(1, 3)
            return BossBeam(self, "fig/p2.png", 0.1)
        return None

    def stop_music(self):
        self.music_player.stop()

    def start_music(self):
        self.music_player.play()

    def switch_to_bigboss(self):
        self.start_music()

    def draw_hp(self, screen):
        self.hp.x = WIDTH - 450
        self.hp.y = 50
        self.hp.draw(screen, self.rect)

class Smallenemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/alien1.png"), 0, 2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 5
        self.angle = 0
        self.mode = 'circle'
        self.timer = 0
        self.warp_count = 0
        self.warp_duration = 60
        self.warp_mode = False
        self.mode_duration = 300
        self.current_mode_timer = 0
        self.current_mode = 'rotate'
        self.music_player = MusicPlayer("fig/Vital_Waves.mp3", volume=0.5)
        self.start_music()
        self.beam_timer = 0
        self.beam_interval = 0
        self.hp = HP(self.rect.x, self.rect.y - 40, max_hp=100)

    def update(self):
        self.current_mode_timer += 1

        if self.current_mode == 'rotate':
            self.angle += 0.05
            radius = 100
            cx = WIDTH - radius - 100
            cy = HEIGHT // 2

            self.rect.centerx = cx + radius * math.cos(self.angle)
            self.rect.centery = cy + radius * math.sin(self.angle)

            self.fig = "fig/cc.png"
            self.mag = 0.1

            if self.current_mode_timer > self.mode_duration:
                self.current_mode = 'vertical'
                self.current_mode_timer = 0
                self.rect.x = 1000
                self.speed = 5
                self.warp_mode = True

        elif self.current_mode == 'vertical':
            self.rect.y += self.speed
            _, tate = check_bound(self.rect)

            self.fig = "fig/bb.png"
            self.mag = 0.1

            if not tate:
                self.speed = -self.speed
            if self.current_mode_timer > self.mode_duration:
                self.current_mode = 'warp'
                self.current_mode_timer = 0

        elif self.current_mode == 'warp':
            if self.warp_mode:
                self.rect.centerx = random.randint(self.rect.width // 2, WIDTH - self.rect.width // 2)
                self.rect.centery = random.randint(self.rect.height // 2, HEIGHT - self.rect.height // 2)
                self.current_mode_timer = 0
                self.warp_mode = False
                self.warp_count += 1
            else:
                if self.current_mode_timer >= self.warp_duration:
                    self.current_mode_timer = 0
                    self.warp_mode = True

        if self.warp_count >= 10:
            self.current_mode = 'rotate'
            self.angle = 0
            #self.rect.center = self.center
            self.warp_count = 0

        if self.hp.current_hp <= 0:
            self.kill()
            return None

        self.beam_timer += 1
        if self.beam_timer >= self.beam_interval:
            self.beam_timer = 0
            self.beam_interval = random.randint(3, 5)
            if self.current_mode != 'warp':
                return BossBeam(self, self.fig, self.mag)
        return None

    def stop_music(self):
        self.music_player.stop()

    def start_music(self):
        self.music_player.play()

    def switch_to_smallboss(self):
        self.start_music()

    def draw_hp(self, screen):
        self.hp.x = WIDTH - 450
        self.hp.y = 50
        self.hp.draw(screen, self.rect)

class Midboss(pg.sprite.Sprite):
    """
    中ボスのクラス
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/mika.png"), 0, 0.5)
        self.image = pg.transform.flip(self.image, False, False)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 6
        self.target_y = self.rect.y
        self.set_new_target()
        self.current_mode = "normal"
        self.music_player = MusicPlayer("fig/crux.mp3", volume=0.5)
        self.stop_music()
        self.beam_timer = 0
        self.beam_interval = 0
        self.beam_count = 0
        self.beams = []
        self.hissatu_mode_counter = 0
        self.hp = HP(self.rect.x, self.rect.y - 40, max_hp=100)

    def set_new_target(self):
        move_distance = random.randint(-400, 400)
        new_target_y = self.rect.y + move_distance
        self.target_y = max(self.rect.height // 2, min(new_target_y, HEIGHT - self.rect.height // 2))

    def update(self):
        if abs(self.rect.y - self.target_y) < self.speed:
            self.rect.y = self.target_y
            self.set_new_target()
        else:
            direction = 1 if self.target_y > self.rect.y else -1
            self.rect.y += direction * self.speed

        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.speed *= -1
        _, tate = check_bound(self.rect)
        if not tate:
            self.set_new_target()

        self.direction = 0
        self.b_speed = 0

        if self.hp.current_hp <= 0:
            self.kill()
            return None

        self.beam_timer += 1
        if self.beam_timer >= self.beam_interval:
            self.beam_timer = 0
            randomcounter = random.randint(1, 30)
            if self.current_mode == "normal":
                self.speed = 6
                if randomcounter < 5:
                    self.beam_interval = random.randint(10, 20)
                    self.b_speed = 50
                    return BossBeam(self, "fig/b.png", 0.3, self.b_speed)
                elif randomcounter == 20:
                    self.current_mode = "hissatu"
                elif randomcounter > 25:
                    self.beam_interval = random.randint(10, 20)
                    self.b_speed = 30
                    return BossBeam(self, "fig/25162925.png", 0.3, self.b_speed)
                elif randomcounter < 30:
                    self.beam_interval = random.randint(5, 10)
                    self.b_speed = random.randint(5, 15)
                    return BossBeam(self, "fig/mika_ac.png", 0.12, self.b_speed)
            elif self.current_mode == "hissatu":
                if self.hissatu_mode_counter < 20:
                    self.hissatu_mode_counter += 1
                    self.beam_interval = random.randint(1, 5)
                    self.b_speed = 0
                    beam = BossBeam(self, "fig/cyber_ball.png", 0.2, self.b_speed)
                    self.beams.append(beam)
                    return beam
                elif self.hissatu_mode_counter == 20:
                    for beam in self.beams:
                        beam.set_speed(30)
                    self.hissatu_mode_counter += 1
                elif self.hissatu_mode_counter > 20:
                    self.beam_interval = random.randint(1, 5)
                    return BossBeam(self, "fig/mika_ac.png", 0.12, self.b_speed)
                self.current_mode = "normal"
                self.hissatu_mode_counter = 0
        return None
    
    def stop_music(self):
        self.music_player.stop()

    def start_music(self):
        self.music_player.play()

    def switch_to_midboss(self):
        self.start_music()

    def draw_hp(self, screen):
        self.hp.x = WIDTH - 450
        self.hp.y = 50
        self.hp.draw(screen, self.rect)

def main():
    pg.display.set_caption("Dremer")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    back_img = pg.image.load("fig/24535830.jpg")
    back_img = pg.transform.scale(back_img, (1600, 900))

    hiroin = Hiroin((100, 500))
    allen = Allen((100, 500))
    frame = Frame()
    show_hiroin = False
    show_allen = True

    player_hp = HP(50, 50, 1000)
    beam_group = pg.sprite.Group()

    start_screen = StartScreen(image_paths)
    in_start_screen = True
    current_image = start_screen.get_next_screen()

    start_screen1 = StartScreen(image_paths1)
    in_start_screen1 = False
    current_image1 = start_screen1.get_next_screen()

    start_screen2 = StartScreen(image_paths2)
    in_start_screen2 = False
    current_image2 = start_screen2.get_next_screen()

    start_screen3 = StartScreen(image_paths3)
    in_start_screen3 = False
    current_image3 = start_screen3.get_next_screen()

    b_enemy = Bigenemy(800, 300)
    s_enemy = Smallenemy(1100, 650)
    m_enemy = Midboss(WIDTH - 100, 400)

    enemies = [s_enemy, m_enemy, b_enemy]
    current_enemy = 0
    enemy_group = pg.sprite.Group(enemies[current_enemy])
    enemy_beams = pg.sprite.Group()

    enemies[current_enemy].start_music()

    game_over_screen = False
    game_over_image = pg.image.load("fig/gameover.png")  # ゲームオーバー画像の読み込み
    game_over_image = pg.transform.scale(game_over_image, (1600, 900))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                
                if event.key == pg.K_LSHIFT:
                    if show_allen:
                        show_hiroin = True
                        show_allen = False
                        allen.rect.center = hiroin.rect.center
                if event.key == pg.K_RSHIFT:
                    if show_hiroin:
                        show_hiroin = False
                        show_allen = True
                        hiroin.rect.center = allen.rect.center
                elif event.key == pg.K_h and show_hiroin:
                    player_hp.heal(100)
                    hiroin.heal(100)
                    allen.rect.center = hiroin.rect.center
                    show_hiroin = False
                    show_allen = True
                elif event.key == pg.K_SPACE and show_allen:
                    beamallen = BeamAllen(allen)
                    beam_group.add(beamallen)
                if event.key == pg.K_RETURN:
                    if in_start_screen and not start_screen.next_image():
                        in_start_screen = False
                    if in_start_screen1 and not start_screen1.next_image():
                        in_start_screen1 = False
                        back_img = pg.image.load("fig/24535848.jpg")
                        back_img = pg.transform.scale(back_img, (1600, 900))
                    if in_start_screen2 and not start_screen2.next_image():
                        in_start_screen2 = False
                        back_img = pg.image.load("fig/23300955.jpg")
                        back_img = pg.transform.scale(back_img, (1600, 900))
                    if in_start_screen3 and not start_screen3.next_image():
                        in_start_screen3 = False
                        time.sleep(5)
                        return
        
        screen.blit(back_img, [0, 0])

        if in_start_screen:
            current_image = start_screen.get_next_screen()
            screen.blit(current_image,
                        (WIDTH // 2 - current_image.get_width() // 2, HEIGHT // 2 - current_image.get_height() // 2))
            show_hiroin = False
            show_allen = False
        elif in_start_screen1:
            current_image1 = start_screen1.get_next_screen()
            screen.blit(current_image1, (
                WIDTH // 2 - current_image1.get_width() // 2, HEIGHT // 2 - current_image1.get_height() // 2))
            show_hiroin = False
            show_allen = False
        elif in_start_screen2:
            current_image2 = start_screen2.get_next_screen()
            screen.blit(current_image2, (
                WIDTH // 2 - current_image2.get_width() // 2, HEIGHT // 2 - current_image2.get_height() // 2))
            show_hiroin = False
            show_allen = False
        elif in_start_screen3:
            current_image3 = start_screen3.get_next_screen()
            screen.blit(current_image3, (
                WIDTH // 2 - current_image3.get_width() // 2, HEIGHT // 2 - current_image3.get_height() // 2))
            show_hiroin = False
            show_allen = False
        else:
            screen.blit(back_img, (0, 0))
            show_allen = True
            #show_hiroin = False
            player_hp.draw(screen, hiroin.rect if show_hiroin else allen.rect)
            frame.draw(screen, show_hiroin, show_allen)

        key_lst = pg.key.get_pressed()
        if show_hiroin:
            hiroin.update(key_lst, screen)
        elif show_allen:
            allen.update(key_lst, screen)

        # Skip all game logic if in any start screen
        if not (in_start_screen or in_start_screen1 or in_start_screen2 or in_start_screen3):
            # ビーム同士の当たり判定
            collisions = pg.sprite.groupcollide(beam_group, enemy_beams, True, True)

            # プレイヤーと敵のビームの当たり判定
            if pg.sprite.spritecollideany(allen, enemy_beams):
                player_hp.take_damage(10)

            # プレイヤーのビームと敵の当たり判定
            for enemy in enemies:
                if pg.sprite.spritecollideany(enemy, beam_group):
                    enemy.hp.take_damage(10)

            # すべてのビームを更新して描画
            beam_group.update()
            beam_group.draw(screen)

            # ボスのHPを描画
            if isinstance(enemies[current_enemy], (Bigenemy, Midboss, Smallenemy)):
                enemies[current_enemy].draw_hp(screen)

            if player_hp.current_hp <= 0:
                game_over_screen = True

            # 敵の更新と描画
            enemy_group.update()
            enemy_group.draw(screen)

            # ビームの発射と更新
            beam = enemies[current_enemy].update()
            if beam:
                enemy_beams.add(beam)
            enemy_beams.update()
            enemy_beams.draw(screen)

            if enemies[current_enemy].hp.current_hp <= 0:
                enemies[current_enemy].stop_music()
                current_enemy = (current_enemy + 1) % len(enemies)
                enemy_group = pg.sprite.Group(enemies[current_enemy])

                # Clear the ally beam group when switching to a new enemy
                beam_group.empty()

                if isinstance(enemies[current_enemy], Bigenemy):
                    enemies[current_enemy].switch_to_bigboss()
                    player_hp.current_hp = player_hp.max_hp  # Restore player HP
                elif isinstance(enemies[current_enemy], Smallenemy):
                    enemies[current_enemy].switch_to_smallboss()
                elif isinstance(enemies[current_enemy], Midboss):
                    enemies[current_enemy].switch_to_midboss()
                    player_hp.current_hp = player_hp.max_hp  # Restore player HP
                enemies[current_enemy].start_music()

                enemy_beams.empty()
                if current_enemy == 1:
                    in_start_screen1 = True
                elif current_enemy == 2:
                    in_start_screen2 = True
                elif current_enemy == 0:
                    in_start_screen3 = True
            elif game_over_screen:  # ゲームオーバー画面を描画
                screen.blit(game_over_image, (
                    WIDTH // 2 - game_over_image.get_width() // 2, HEIGHT // 2 - game_over_image.get_height() // 2))
                pg.display.flip()
                time.sleep(5)
                return

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()


