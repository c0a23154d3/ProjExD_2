import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  #練習1
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]: # 練習3
    """
    こうかとんRect、または爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect、または爆弾Rect
    戻り値：横方向判定結果、　縦方向判定結果
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate


def show_explosion(screen):
    # ブラックアウト
    bo_surface = pg.Surface((WIDTH, HEIGHT))
    bo_surface.fill((0, 0, 0))
    bo_surface.set_alpha(128)  # 半透明にする
    screen.blit(bo_surface, (0, 0))

    # 泣いているこうかとんの画像
    sad_kk_img = pg.image.load("fig/8.png")
    sad_kk_rect = sad_kk_img.get_rect()
    sad_kk_rect.center = (WIDTH // 2, HEIGHT // 2)

    # "Game Over" の表示
    font = pg.font.SysFont(None, 48)
    go_text = font.render("Game Over", True, (255, 255, 255))
    go_rect = go_text.get_rect()
    go_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    # 画面に表示
    screen.blit(sad_kk_img, sad_kk_rect)
    screen.blit(go_text, go_rect)
    pg.display.flip()

    # 5秒間待つ
    pg.time.wait(5000)


def create_bd_surfaces() -> list: #拡大爆弾Surfaceの関数
    bd_imgs = []
    for r in range(1, 11):
        bd_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bd_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bd_imgs.append(bd_img)
    return bd_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_imgs = create_bd_surfaces()  # 拡大爆弾Surfaceのリストを作成
    bd_img = pg.Surface((20,20))  #練習2
    pg.draw.circle(bd_img, (255,0,0), (10,10), 10)
    bd_img.set_colorkey((0,0,0))
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    bd_accs = [a for a in range(1, 11)]  # 加速度のリスト

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct): #練習3
            print("GameOver")
            show_explosion(screen)
            return

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)


        avx = vx * bd_accs[min(tmr//500, 9)]  # 加速度の適用
        bd_img = bd_imgs[min(tmr//500, 9)]  # 適切なサイズの爆弾Surfaceを選択
        bd_rct.move_ip(avx, vy)
        screen.blit(bd_img, bd_rct)

        bd_rct.move_ip(vx, vy) 
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct) #練習4
        if not yoko: #横にはみ出たら
            vx *= -1
        if not tate: #縦にはみ出たら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()