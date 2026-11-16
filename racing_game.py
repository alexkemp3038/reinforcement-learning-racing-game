
# LIBRARIES
import pygame as py
from pathlib import Path
import copy
import os

# FILES
import utils as u
import checkpoint as cp
from sensor import Sensor
from car import AbstractCar
from network import NeuralNetwork, Level

#To change map:
# 1. Change width and height to match map size
# 2. Change player car start pos
# 3. Change map file names when loaded
# 4. Change finish line

# CONFIGURABLE PARAMETERS:
# DIRECTORIES
BASE_DIR = Path(__file__).resolve().parent
SAVE_FILE = BASE_DIR / "best_brain.pkl"

# GAME
FPS = 60
WIDTH = 1254
HEIGHT = 627
RUN = True

# CARS
CAR_WIDTH = 20
CAR_HEIGHT = 45
MAX_SPEED = 10
MAX_ROT_SPEED = 12
ACCELERATION = 0.25

# TRAINING
GENERATION = 1
NO_OF_CARS = 20
INITIAL_MUTATION = 0.25
REFINING_MUTATION = 0.05
NO_OF_CHECKPOINTS = 16
LOAD_PREV_CHAMPION = True
TRAIN = True
FRAME = 0
MAX_FRAMES = 3000
MAX_LAPS = 1
MAX_IDLE_FRAMES = 200
BEST_SCORE = 0
BEST_LAP_TIME = None
MODE = 'R'

# Makes sure it spans length of car to make sure it gets registered
TEST_MAP_CHECKPOINTS = [
    cp.Checkpoint(215, 30, CAR_WIDTH, 105, 1),
    cp.Checkpoint(375, 140, CAR_WIDTH, 115, 2),
    cp.Checkpoint(515, 150, CAR_WIDTH, 115, 3),
    cp.Checkpoint(645, 155, CAR_WIDTH, 115, 4),
    cp.Checkpoint(800, 225, CAR_WIDTH, 115, 5),
    cp.Checkpoint(950, 105, CAR_WIDTH, 140, 6),
    cp.Checkpoint(1080, 85, CAR_WIDTH, 140, 7),
    cp.Checkpoint(1090, 275, 110, CAR_WIDTH, 8),
    cp.Checkpoint(975, 410, 170, CAR_WIDTH, 9),
    cp.Checkpoint(855, 480, CAR_WIDTH, 110, 10),
    cp.Checkpoint(700, 480, CAR_WIDTH, 110, 11),
    cp.Checkpoint(550, 400, CAR_WIDTH, 130, 12),
    cp.Checkpoint(400, 380, CAR_WIDTH, 120, 13),
    cp.Checkpoint(250, 460, CAR_WIDTH, 110, 14),
    cp.Checkpoint(75, 450, 130, CAR_WIDTH, 15)
]

# ===================================================================================================================
# === PROMPT USER WHAT MODE TO GO IN ===
print("===== AUTOMATED DRIVING AGENT PROJECT ======\n")
if os.path.exists(SAVE_FILE):
    print("A champion car file has been found!")

    while True:
        print("Would you like to Reset Training (R), Watch Champion Car(W) or Keep training champion car(C)?")
        user_choice = input("Please type R/W/C: ").strip().lower()

        if user_choice == 'r':
            TRAIN = True
            LOAD_PREV_CHAMPION = False
            os.remove(SAVE_FILE)
            print("---> Starting a new training session (Resetting).")
            break
        elif user_choice == 'w':
            TRAIN = False
            LOAD_PREV_CHAMPION = True
            print("---> Loading watch champion car session.")
            break
        elif user_choice == 'c':
            TRAIN = True
            LOAD_PREV_CHAMPION = True
            print("---> Loading champion car for training session.")
            break
        else:
            print("Invalid input. Please type 'R' to reset, 'W' to watch or 'C' to train champion.")
else:
    print ("No champion file found. Starting fresh training automatically.")
    TRAIN = True
    LOAD_PREV_CHAMPION = False        

# ===================================================================================================================
# INITIALISE GAME AND CLOCK
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Autonomous Driving Project')
clock = py.time.Clock()

# Load map
map = py.image.load(BASE_DIR / "test_map.png")
map = py.transform.scale(map, (WIDTH, HEIGHT))

#Load Track border
track_border = py.image.load(BASE_DIR /"test_map_border.png")
track_border = py.transform.scale(track_border, (WIDTH, HEIGHT))
#Create border mask
track_border_mask = py.mask.from_surface(track_border)

#Create finish line mask 
# Easy map - finish_line = py.Rect(55, 455, 105, 50)
# Test map -
finish_line = py.Rect(79,317,96,30)
# ===================================================================================================================
# === GET CARS ===
CHAMPION = None

if LOAD_PREV_CHAMPION:
    CHAMPION_BRAIN, GENERATION, BEST_LAP_TIME, BEST_SCORE = u.load_champion(SAVE_FILE, MAX_SPEED, MAX_ROT_SPEED, BASE_DIR)
    CHAMPION = AbstractCar("car.png", MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)
    CHAMPION.brain = CHAMPION_BRAIN
# If no save file, random brains
if CHAMPION is None:
    cars = u.generate_cars(NO_OF_CARS, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)

# Resume training champion and mutated copies
elif TRAIN:
    # Get mutation
    MUTATION = u.get_mutation(GENERATION, INITIAL_MUTATION, REFINING_MUTATION)

    # Generate cars for next generation
    cars = u.next_gen(CHAMPION, NO_OF_CARS, MUTATION, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)
# Otherwise, just watch champion
else:
    cars = [CHAMPION]

# ===================================================================================================================
# === GAME LOOP === 
while RUN:
    # INPUT(EVENTS)
    for e in py.event.get():
        # Handle quit event
        if e.type == py.QUIT:
            RUN = False

        # Handle end training event
        elif e.type == py.KEYDOWN and e.key == py.K_SPACE and TRAIN:
            BEST_BRAIN, GENERATION, BEST_LAP_TIME, BEST_SCORE = u.load_champion(SAVE_FILE, MAX_SPEED, MAX_ROT_SPEED, BASE_DIR)
            BEST = AbstractCar("car.png", MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)
            BEST.brain = BEST_BRAIN

            if BEST is not None:
                TRAIN = False
                cars = [BEST]
                FRAME = 0

    # UPDATE (LOGIC)
    # For every car
    for c in cars:
        # If car is dead, ignore
        if not c.alive:
            continue

        # Update sensor values and score
        c.sensor.update(track_border_mask)

        # Get take those values as inputs and get the outputs
        outputs = c.brain.feedForward(c.sensor.rays)

        # Move the car using these output values
        u.move_ai(c, outputs, 0.5)
    
        #Check for collision
        if c.collide_mask(track_border_mask) is not None:
            c.alive = False

        # Check finish line
        c.check_finish_line(finish_line)

        # Check checkpoints
        c.check_checkpoints(TEST_MAP_CHECKPOINTS, FRAME)

        # Kill if its stuck
        c.check_stuck(FRAME, MAX_IDLE_FRAMES)

        # Update score
        c.update_score(NO_OF_CHECKPOINTS + 1)

    # Count frame and see if generation is over
    FRAME += 1

    # Check if any car has finished lap or if generation is ending
        
    # If the generation is over in training
    if TRAIN and u.gen_over(cars, FRAME, MAX_FRAMES, MAX_LAPS):
        # Set champion
        CHAMPION = u.get_champion(cars)

        # Get lap time
        if CHAMPION.lap_count >= MAX_LAPS:
            LAP_TIME = FRAME / FPS
        else:
            LAP_TIME = None

        # Save it if it got further, or finished the lap faster than the saved champion
        if CHAMPION.score > 0:
            BEST_SCORE, BEST_LAP_TIME = u.save_champion(CHAMPION, BEST_SCORE, BEST_LAP_TIME, LAP_TIME, GENERATION, SAVE_FILE)

        # If none reached first checkpoint, randomise until one does.
        if CHAMPION.score == 0:
            print("No cars reached the first checkpoint! Generating fresh random cars...")
            cars = u.generate_cars(NO_OF_CARS, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)
            GENERATION += 1

        # Otherwise, perform new generation with a champion to mutate
        else:
            # Get mutation
            MUTATION = u.get_mutation(GENERATION, INITIAL_MUTATION, REFINING_MUTATION)

            # Breed the next generation from the champion
            cars = u.next_gen(CHAMPION, NO_OF_CARS, MUTATION, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)
            GENERATION += 1

        # New generation means reset track, so frames resets
        FRAME = 0

    # If generation (lap) is over in watch mode
    elif not TRAIN and u.gen_over(cars, FRAME, MAX_FRAMES, MAX_LAPS):
        # Reset champion car to start
        CHAMPION.reset_attr()
        CHAMPION.alive = True
        FRAME = 0

    # Every frame, clear cars first, then draw new ones
    screen.fill((0,0,0))

    # Update map and cars
    u.draw_scene(screen, map, cars)

    # Draw HUD
    ALIVE_COUNT = sum(1 for c in cars if c.alive)
    u.draw_hud(screen, GENERATION, BEST_SCORE, BEST_LAP_TIME, ALIVE_COUNT, BEST_LAP_TIME, FRAME, FPS, WIDTH)

    # DRAW (RENDER)
    clock.tick(FPS)
    curr_time = py.time.get_ticks()
    py.display.flip()
    
# Save the best car when exiting training
if TRAIN and len(cars) > 0:
    current_best = u.get_champion(cars)

    if current_best.score > 0:
        lap_time = None

        if current_best.lap_count >= MAX_LAPS:
            lap_time = FRAME / FPS

        BEST_SCORE, BEST_LAP_TIME = u.save_champion(
            current_best,
            BEST_SCORE,
            BEST_LAP_TIME,
            lap_time,
            GENERATION,
            SAVE_FILE
        )

py.quit()