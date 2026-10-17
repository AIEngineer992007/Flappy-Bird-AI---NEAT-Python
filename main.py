import pygame
import neat
import os
import time
import random
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMG = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs_b286d95d6d', 'imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs_b286d95d6d' ,'imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs_b286d95d6d' ,'imgs', 'bird3.png')))
]

PIPE_PNG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs_b286d95d6d', 'imgs', 'pipe.png')))
BASE_PNG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs_b286d95d6d', 'imgs', 'base.png')))
BG_PNG = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs_b286d95d6d", "imgs", "bg.png")),
    (WIN_WIDTH, WIN_HEIGHT),
)
STAT_FONT = pygame.font.SysFont('JetBrains', 50)
gen = 0
class Bird:
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.titl = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[1]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        
        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2

        self.y = self.y + d
        
        if d < 0 or self.y < self.height + 50:
            if self.titl < self.MAX_ROTATION:
                self.titl = self.MAX_ROTATION
        else:
            if self.titl > -90:
                self.titl -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.titl <= -80:
            self.imgs = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        
        rotate_image = pygame.transform.rotate(self.img, self.titl)
        new_rect = rotate_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotate_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self, x):
        self.x = x 
        self.height = 0
        self.gap = 100
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_PNG, False, True)
        self.PIPE_BOTTOM = PIPE_PNG
        
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
     
    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) #Not collision -> None
        t_point = bird_mask.overlap(top_mask, top_offset)  #Else -> return position
        
        if b_point or t_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_PNG.get_width()
    HEIGHT = BASE_PNG.get_height()
    IMG = BASE_PNG
    
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
    

def draw_win(win, birds, pipes, base, score, gen):
    win.blit(BG_PNG, (0, 0))
    text_score = STAT_FONT.render(f'Score: {str(score)}', 1, (255, 255, 255))
    text_total_gen = STAT_FONT.render(f'Gen: {str(gen)}', 1, (255, 255, 255))
    win.blit(text_score, (WIN_WIDTH - 10 - text_score.get_width(), 10))
    win.blit(text_total_gen, (WIN_WIDTH - 200 - text_score.get_width(), 10))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    
    for bird in birds:
        bird.draw(win)
    
    pygame.display.update()

def main(genomes, config):
    global gen
    nets = []
    ge = []
    birds = []
    gen += 1
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird AI")
    score = 0 
    clock = pygame.time.Clock()
    
    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            
            output = nets[x].activate((
                bird.y, 
                abs(bird.y - pipes[pipe_ind].height), 
                abs(bird.y - pipes[pipe_ind].bottom)
            ))
            
            if output[0] > 0.5:
                bird.jump()
            
        #Pipe collision      
        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            pipe.move()
            
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            for g in ge:
                g.fitness += 5
            score += 1
            pipes.append(Pipe(WIN_WIDTH))

        #Base collision
        for bird in birds:
            if bird.y + bird.img.get_height() > 730 or bird.y < 0:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
            
        for r in remove_pipes:
            pipes.remove(r)
            
        base.move()
        draw_win(win, birds, pipes, base, score, gen)

def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    winner = population.run(main, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    