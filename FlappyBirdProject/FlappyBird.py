
import pygame
import os
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

FONT_PATH = "Handjet-ExtraBold.ttf"
STAT_FONT = pygame.font.Font("Handjet-ExtraBold.ttf", 50)
pygame.display.set_caption("Flappy Bird")


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self ,x ,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False,  True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()


    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMGS.get_width()
    IMG = BASE_IMGS

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



def draw_windows(win, bird, pipes, base, score):
    win.blit(BG_IMGS, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Your Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 -text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

    
def draw_game_over(win, score):
    win.blit(BG_IMGS, (0, 0)) 
    game_over_font = pygame.font.Font("Handjet-ExtraBold.ttf", 36)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    score_text = game_over_font.render("Score: " + str(score), True, (255, 255, 255))
    retry_text = game_over_font.render("Press SPACE to Retry", True, (255, 255, 255))

    win.blit(game_over_text, ((WIN_WIDTH - game_over_text.get_width()) // 2, WIN_HEIGHT // 2 - 100))
    win.blit(score_text, ((WIN_WIDTH - score_text.get_width()) // 2, WIN_HEIGHT // 2 - 50))
    win.blit(retry_text, ((WIN_WIDTH - score_text.get_width()) // 2 -80 , WIN_HEIGHT // 2 ))
    pygame.display.update()

def start_menu(win):
    title_font = pygame.font.Font("Handjet-ExtraBold.ttf", 60)
    start_font = pygame.font.Font("Handjet-ExtraBold.ttf", 36)

    title_text = title_font.render("Flappy Bird", True, (255, 255, 255))
    start_text = start_font.render("Press SPACE to Start", True, (255, 255, 255))
    

    win.blit(BG_IMGS, (0, 0))
    win.blit(title_text, ((WIN_WIDTH - title_text.get_width()) // 2, WIN_HEIGHT // 4))
    win.blit(start_text, ((WIN_WIDTH - start_text.get_width()) // 2, WIN_HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False



def main():
    game_over = False 
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock() 
    run = True
    start = True

    if start:
        start_menu(win)
        start = False

    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        game_over = False 
                        bird = Bird(230, 350)
                        base = Base(730)
                        pipes = [Pipe(600)]
                        score = 0
                    else:
                        bird.jump()
        
        if not game_over:
            bird.move()
            add_pipe = False
            rem = []
            
            for pipe in pipes:
                if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                    game_over = True
                if pipe.collide(bird):
                    game_over = True
                
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                
                pipe.move()
            
            if add_pipe:
                score += 1
                pipes.append(Pipe(random.randrange(500, 800)))
            
            for r in rem:
                pipes.remove(r)
            
            if bird.y + bird.img.get_height() >= 730:
                game_over = True
            
            
        
        win.fill((0, 0, 0))
        
        if game_over:
            draw_game_over(win, score)
        else:
            draw_windows(win, bird, pipes, base, score)
        
        pygame.display.update()

    pygame.quit()
    quit()

main()