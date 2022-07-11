import time
import pygame
import random

pipe_images = [
    pygame.transform.scale(pygame.image.load("real.PNG"),(60,300)),
    pygame.transform.scale(pygame.image.load("valencia.PNG"), (60,300)),
    pygame.transform.scale(pygame.image.load("geatfe.PNG"), (60,300)),
    pygame.transform.scale(pygame.image.load("atletico.PNG"),(60,300)),
    pygame.transform.scale(pygame.image.load("villareal.PNG"),(60,300)),
]


class Pipe:
    def __init__(self, x, y, sizeofX, sizeofY,i):
        self.x = x  # this is position x
        self.y = y  # this is position y
        self.width = sizeofX
        self.height = sizeofY
        self.img = pygame.transform.scale(pipe_images[i], (sizeofX, sizeofY))


class Pipes:
    def __init__(self, pipes):
        self.pipeList = pipes

    def render(self, screen):
        for pipe in self.pipeList:
            screen.blit(pipe.img, (pipe.x, pipe.y))


def create_random_pipes():
    isupper = random.choice([True, False])
    pipe_list = []
    for i in range(1, 6):
        # random for pipe x coordinate
        random_x = random.randint(i * 200, i * 200 + 100)
        # random for height, random_y is calculated from that
        random_height = random.randint(250,300)

        random_width = 50

        if isupper:
            created_pipe = Pipe(random_x, 0, random_width, random_height,i-1)
        else:
            created_pipe = Pipe(random_x, 700 - random_height, random_width, random_height,i-1)
        pipe_list.append(created_pipe)

        isupper = not isupper  # just changing position of pipe, from up to down or vice versa
    return pipe_list


def isCollisionBetweenRectangles(a, b):
    if a[0] >= b[2] or a[2] <= b[0] or a[3] <= b[1] or a[1] >= b[3]:
        return False
    else:
        return True


def isCollision(pipe, bird):
    pipe_rectangle = [pipe.x, pipe.y, pipe.x + pipe.width,
                      pipe.y + pipe.height]  # left top and right bottom coordinates
    bird_rectangle = [bird.x, bird.y, bird.x + 50, bird.y + 50]
    return isCollisionBetweenRectangles(pipe_rectangle, bird_rectangle)


def collisonMusic():
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("siu.wav")
        pygame.mixer.music.play()

def playMusic():
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("ankaramessi.wav")
        pygame.mixer.music.play()


class Bird:
    def __init__(self):
        self.x = 50
        self.y = 350
        self.radius = 50
        self.speedright = 3
        self.gravity = 13

    def update(self):
        self.y -= self.gravity
        self.gravity -= 1

    def render(self, screen):
        bird_img = pygame.transform.scale(pygame.image.load('goldenball.png'), (50, 50))
        screen.blit(bird_img, (self.x, self.y))


class App:

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.bird = None
        self.pipes = None
        self.pause_count = 0

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        time.sleep(1.5)
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1400, 700))
        pygame.display.set_caption("flappy messi")

        self.pipes = Pipes(create_random_pipes())
        self.clock = pygame.time.Clock()
        self.running = True
        self.bird = Bird()

    def update(self):
        self.events()
        self.bird.x += self.bird.speedright
        self.bird.update()

        for pipe in self.pipes.pipeList:
            if isCollision(pipe, self.bird):
                pygame.mixer.music.pause()
                collisonMusic()
                self.running = False

        if self.bird.y < 0 or self.bird.y + 50 > 700: #colliding to borders
            pygame.mixer.music.pause()
            collisonMusic()
            self.running = False

        if self.bird.x > 1400: #it's over then
            self.running = False



    def events(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.bird.gravity = 15
            if keys[pygame.K_t]:
                if self.pause_count % 2 == 0: #to make sure its mute or unmute
                    pygame.mixer.music.pause()
                else:
                    playMusic()
                self.pause_count += 1
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        background = pygame.transform.scale(pygame.image.load("messivsgetafe.jpg"),(1400,700))
        self.screen.blit(background, (0, 0))
        self.bird.render(self.screen)
        self.pipes.render(self.screen)
        playMusic()
        pygame.display.flip()
        self.clock.tick(120)

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()

