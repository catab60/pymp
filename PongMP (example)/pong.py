import pygame
from pymp import Client
import time


pygame.init()
client = Client()
client.connect("localhost", 5555)
time.sleep(1)

IsFirstPlayer = False
if not client.data:
    IsFirstPlayer = True
else:
    for key, value in client.data.items():
        if key != "Server":
            if value:
                if value[0].get('IsFirstPlayer'):
                    IsFirstPlayer = False
                else:
                    IsFirstPlayer = True
            
class Ball:
    def __init__(self, x, y):
        self.width = 10
        self.height = 10
        self.body = pygame.Rect(x, y, self.width, self.height)
        self.color = (255,255,255)

    def draw(self, screen, x, y):
        self.body.x = x
        self.body.y = y
        pygame.draw.rect(screen, self.color, self.body)

class Player_local:
    def __init__(self, x, y):
        self.width = 25
        self.height = 100
        self.body = pygame.Rect(x, y, self.width, self.height)
        self.color = (255,255,255)
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_UP]:
            if self.body.y > 10:
                self.body.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.body.y < height - self.height - 10:
                self.body.y += self.speed

    
        
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.body)

class Player_remote:
    def __init__(self, x, y):
        self.width = 25
        self.height = 100
        self.body = pygame.Rect(x, y, self.width, self.height)
        self.color = (255,255,255)
        self.speed = 10

    def draw(self, screen, y):
        self.body.y = y
        pygame.draw.rect(screen, self.color, self.body)

width, height = 800, 600
FPS = 60
player_y = 10
ball_x = 0
ball_y = 0
score_left = 0
score_right = 0
font = pygame.font.Font(None, 36)
ball = Ball(width//2,height//2)

if IsFirstPlayer:
    player = Player_local(10,10)
    player2 = Player_remote(width-10-25,10)
else:
    player = Player_local(width-10-25,10)
    player2 = Player_remote(10,10)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("pygmp example")
clock = pygame.time.Clock()

running = True

if client.client_id == None:
    print("Failed to connect to server.")
    running = False
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    screen.fill((0,0,0))


    player.move(keys)
    client.send_variables({"player_y": player.body.y, "IsFirstPlayer": IsFirstPlayer})
    player.draw(screen)
    

    for key, value in client.data.items():
        if key != "Server":
            if value:
                player_y = value[0].get('player_y')
            
        if key == "Server":
            ball_x = value[0]
            ball_y = value[1]
            score_left = value[2]
            score_right = value[3]

    ball.draw(screen, ball_x, ball_y)
    player2.draw(screen, player_y)
    score_text = font.render(f"{score_left} - {score_right}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(width // 2, 50))
    screen.blit(score_text, text_rect)
    
    pygame.display.flip()
pygame.quit()