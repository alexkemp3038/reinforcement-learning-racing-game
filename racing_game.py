from unittest import case
import pygame
from pathlib import Path
import time
import math
from sensor import Sensor
from network import NeuralNetwork, Level

#To change map:
# 1. Change width and height to match map size
# 2. Change player car start pos
# 3. Change map file names when loaded
# 4. Change finish line

# CONFIGURABLE PARAMETERS:
BASE_DIR = Path(__file__).resolve().parent
FPS = 60
WIDTH = 1254
HEIGHT = 627
CAR_WIDTH = 20
CAR_HEIGHT = 45
car_speed = 5
car_direction = 'up'

# ===================================================================================================================
# === Helper Functions ===
def blit_rotate_center(image, top_left, angle):
    rotated_IMG = pygame.transform.rotate(image, angle)
    new_hitbox = rotated_IMG.get_rect(center=image.get_rect(topleft=top_left).center)
    return rotated_IMG, new_hitbox

# ====================================================================================================================
# === SPRITE CLASSES ===
class AbstractCar:
    def __init__(self, image, max_speed, rot_speed):
        self.image = image
        self.max_speed = max_speed
        self.rot_speed = rot_speed
        self.speed = 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05
        self.lap_count = 0
        self.sensor = Sensor(self)
        self.brain = NeuralNetwork([self.sensor.ray_count, 6, 4])

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_speed
        if right:
            self.angle -= self.rot_speed

    def draw(self, screen):
        self.rotated_IMG, self.hitbox = blit_rotate_center(self.IMG, (self.x, self.y), self.angle)
        screen.blit(self.rotated_IMG, self.hitbox.topleft)

    def move_forward(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
        self.move()

    def move_backward(self):
        # Updates speed so its slows by acceleration, 
        # and can never go as fast as half of max speed when reversing.
        self.speed = max(self.speed - self.acceleration, -self.max_speed/2)
        self.move()

    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed

        self.y -= vertical
        self.x -= horizontal

    def reset_pos(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.speed = 0

    def reduce_speed(self):
        # Ensures it doesnt go backwards, just slows down by half
        self.speed = max(self.speed - self.acceleration / 2, 0)
        self.move()

    def collide_mask(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.rotated_IMG)
        offset = (int(self.hitbox.x - x), int(self.hitbox.y - y))
        point_of_intersection = mask.overlap(car_mask, offset)
        return point_of_intersection

    def collide_rect(self, rect, x=0, y=0):
        point_of_intersection = self.hitbox.clip(rect)

        if point_of_intersection.width > 0 and point_of_intersection.height > 0:
            return point_of_intersection.top

        return None

    def check_finish_line(self, finish_line):
        #If a collision with the finish line has not occured, ignore.
        if self.collide_rect(finish_line) is None:
            return

        #If one has and its interacting with the finish line, bounce.
        if self.y > self.prev_y and self.y < finish_line.top:
            self.bounce()

        #If the player has crossed the finish line, operate finish sequence.
        elif self.prev_y > finish_line.top >= self.y:
            self.lap_count += 1
            self.reset_pos()
            print("Lap", self.lap_count)

class PlayerCar(AbstractCar):
    IMG = pygame.image.load(BASE_DIR / "player_car.png")
    IMG = pygame.transform.scale(IMG,(25,50))
    # Easy map - START_POS = (100, 380)
    # Test map - 
    START_POS = (112, 250)

    def bounce(self):
        self.speed = -self.speed * 0.8
        self.move()
# ===================================================================================================================
# ===================================================================================================================
# === Functions ===
def draw(screen, images, player_car, sensor):
    for img, pos in images:
        screen.blit(img, pos)
    player_car.draw(screen)
    player_car.sensor.draw(screen)
    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        player_car.move_forward()
        moved = True
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

# ==================================================================================================================
# ===================================================================================================================
#Initialise game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load map
map = pygame.image.load(BASE_DIR / "test_map.png")
map = pygame.transform.scale(map, (WIDTH, HEIGHT))

#Load Track border
track_border = pygame.image.load(BASE_DIR /"test_map_border.png")
track_border = pygame.transform.scale(track_border, (WIDTH, HEIGHT))
#Create border mask
track_border_mask = pygame.mask.from_surface(track_border)

#Create finish line mask 
# Easy map - finish_line = pygame.Rect(55, 455, 105, 50)
# Test map -
finish_line = pygame.Rect(79,317,96,30)
clock = pygame.time.Clock()
run = True

#Initialise Player car - CHANGE MAX SPEED AND MAX ROT SPEED HERE
player_car = PlayerCar(PlayerCar.IMG, 2.5, 3)

full_map = [(map, (0, 0))]

# ===================================================================================================================
# === GAME LOOP === 
while run:
    # INPUT(EVENTS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    # UPDATE (LOGIC)
    #update map and car
    draw(screen, full_map, player_car, player_car.sensor)
    move_player(player_car)
    player_car.sensor.update(track_border_mask)
    player_car.sensor.print_val()

    #Check for collision
    if player_car.collide_mask(track_border_mask) is not None:
        player_car.bounce()

    # Check finish line
    finish_check = player_car.check_finish_line(finish_line)

    # DRAW (RENDER)
    clock.tick(FPS)
    curr_time = pygame.time.get_ticks()
    pygame.display.flip()

    
pygame.quit()