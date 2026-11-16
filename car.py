# LIBRARIES
import pygame as py
from pathlib import Path
import math as m
import pickle as p

# FILES
import sensor as s
import utils as u
import network as n

# Car Class
class AbstractCar:
    def __init__(self, image_filename, max_speed, rot_speed, acceleration, BASE_DIR):
        # Load and scale image
        self.image = py.image.load(BASE_DIR / image_filename)
        self.image = py.transform.scale(self.image,(25,50))

        # INIT START POSITION
        self.START_POS = (112, 250)
        self.x, self.y = self.START_POS

        # INIT DEFAULT VARIABLES
        self.max_speed = max_speed
        self.rot_speed = rot_speed
        self.speed = 0
        self.angle = 0
        self.acceleration = acceleration

        # INIT HITBOX AND ROTATION HANDLING
        self.rotated_image, self.hitbox = u.blit_rotate_centre(self.image, (self.x, self.y), self.angle)

        # INIT TRAINING VARIABLES
        self.lap_count = 0
        self.cp_crossed_this_lap = 0
        self.score = 0
        self.frame_of_last_cp = 0
        self.sensor = s.Sensor(self)
        self.brain = n.NeuralNetwork([self.sensor.ray_count, 20, 4])
        self.alive = True
    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_speed
        if right:
            self.angle -= self.rot_speed

    def draw(self, screen, alive=True):
        self.update_image()

        if alive:
            screen.blit(self.rotated_image, self.hitbox.topleft)
        else: 
            # If dead, set 50% transparency
            self.rotated_image.set_alpha(128)
            screen.blit(self.rotated_image, self.hitbox.topleft)

    def update_image(self):
        self.rotated_image, self.hitbox = u.blit_rotate_centre(self.image, (self.x, self.y), self.angle)

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
        radians = m.radians(self.angle)
        vertical = m.cos(radians) * self.speed
        horizontal = m.sin(radians) * self.speed

        self.y -= vertical
        self.x -= horizontal

    # Used to reset car to starting position
    def reset_pos(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.speed = 0

    # Used to reduce speed of car
    def reduce_speed(self):
        # Ensures it doesnt go backwards, just slows down by half
        self.speed = max(self.speed - self.acceleration / 2, 0)
        self.move()

    # Used to compare collision of two surfaces - The car and another surface, 'mask'
    def collide_mask(self, mask, x=0, y=0):
        # Builds mask of cars current rotated image
        car_mask = py.mask.from_surface(self.rotated_image)
        # Lines up two masks - specifically the top left of both masks
        offset = (int(self.hitbox.x - x), int(self.hitbox.y - y))
        # Returns (x,y) point where they both overlap, None if not
        point_of_intersection = mask.overlap(car_mask, offset)
        return point_of_intersection

    # Used to compare collision of a surface and a rect - The car and a rect.
    def collide_rect(self, rect):
        # Uses clip function which returns rectangle where the boxes overlap
        point_of_intersection = self.hitbox.clip(rect)

        # If overlap has real area
        if point_of_intersection.width > 0 and point_of_intersection.height > 0:
            return point_of_intersection.top

        return None

    def check_finish_line(self, finish_line):
        #If a collision with the finish line has not occured, ignore.
        if self.collide_rect(finish_line) is None:
            return

        #If one has and its interacting with the finish line, pronounce dead.
        if self.y > self.prev_y and self.y < finish_line.top:
            self.alive = False

        #If the player has crossed the finish line, operate finish sequence.
        elif self.prev_y > finish_line.top >= self.y:
            self.cp_crossed_this_lap = 0
            self.lap_count += 1
            self.reset_pos()

    # Updates score that determines champion car
    def update_score(self, no_of_gates):
        # Determines score based on how many checkpoints its crossed in total.
        self.score = (self.lap_count * no_of_gates) + self.cp_crossed_this_lap

    # Used in load function - Resets attributes so it starts at beginning of track.
    def reset_attr(self):
            self.reset_pos()
            self.alive = True
            self.cp_crossed_this_lap = 0
            self.update_image()
            self.lap_count = 0
            self.score = 0
            self.frame_of_last_cp = 0

    # Saves car's neural network into a .pickle file.
    def save(self, filepath):
        state = {
            "brain": self.brain 
        }

        with open(filepath, "wb") as f:
            p.dump(state, f)

    # Takes .pickle file and unpacks it into car object.
    def load(self, filepath):
        # Load file into 'state' variable.
        with open(filepath, "rb") as f:
            state = p.load(f)

        # Unpack state into the neural network variable.
        self.brain = state["brain"]

        # Reset attributes so it starts at beginning of track.
        self.reset_attr()

    # Checks if car has hit next checkpoint, if so increments cp variable.
    def check_checkpoints(self, checkpoints, frame):
        # If the car has already passed all checkpoints, ignore
        if self.cp_crossed_this_lap >= len(checkpoints):
            return
        
        # Get checkpoints rect to check for collision
        next_cp = checkpoints[self.cp_crossed_this_lap].rect

        # See if the car is interacting with checkpoint
        poi = self.collide_rect(next_cp)

        # If car is touching next checkpoint
        if poi is not None:
            self.cp_crossed_this_lap += 1
            self.frame_of_last_cp = frame

    # Used to handle spinning or idle cars
    def check_stuck(self, frame, max_idle_frame = 300):
        # If the car hasnt hit the next checkpoint in max idle frames
        if frame - self.frame_of_last_cp > max_idle_frame:
            # Consider it dead
            self.alive = False