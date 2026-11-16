# LIBRARIES
import pygame as py 
import copy
import os
import pickle
import random

# FILES
import car as c

# Linear Interpolation function 
# Think of a slider where a is the left and b is the right,
# It returns the gap of size t between a and b
# For example a = 10, b = 20, t = 0.25 will give 12.5
def lerp(a, b, t):
    return a + (b - a) * t

# Rotates image by 'angle' degrees from centre and gives new hitbox
def blit_rotate_centre(image, top_left, angle):
    rotated_IMG = py.transform.rotate(image, angle)
    new_hitbox = rotated_IMG.get_rect(center=image.get_rect(topleft=top_left).center)
    return rotated_IMG, new_hitbox

def draw_scene(screen, map, cars):
    # Draw Map
    screen.blit(map, (0,0))

    # Draw every car
    for c in cars:
        # If its alive
        if c.alive:
            # Draw the car
            c.draw(screen)
        # If its dead
        else:
            # Indicate its dead so its transparency level is changed, and draw the car
            c.draw(screen, alive=False)

# Uses outputs to map it to movement.  
def move_ai(car, outputs, threshold=0.5):
    # Car cant move if its dead
    if not car.alive:
        return

    # Map each output to a direction to move/turn
    forward = outputs[0]
    backward = outputs[1]
    left = outputs[2]
    right = outputs[3]

    moved = False

    # For each direction if it meets threshold, consider it on and move/turn that way.
    if left > threshold:
        car.rotate(left=True)
    if right > threshold:
        car.rotate(right=True)
    if forward > threshold:
        car.move_forward()
        moved = True
    if backward > threshold:
        car.move_backward()
        moved = True

    # If it has not moved, reduce its speed
    if not moved:
        car.reduce_speed()

# This generates n cars at once
def generate_cars(n, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR):
    cars = []

    for i in range(n):
        cars.append(c.AbstractCar("car.png", MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR))

    return cars

# Gets the car with the highest score. If cars tie, the faster one is champion.
def get_champion(cars):
    highest_score = 0
    champion_car = cars[0]

    # Checks every car
    for c in cars:
        # If current car has a higher score than current best
        if c.score > highest_score:
            # Make it the new champion
            highest_score = c.score
            champion_car = c
        # If its a tie
        elif c.score == highest_score:
            # The best car is the one with the faster checkpoint time.
            if c.frame_of_last_cp < champion_car.frame_of_last_cp:
                # Make it the new champion
                highest_score = c.score
                champion_car = c

    return champion_car

# Decides when a generation of cars is over
# Returns Tuple (champion_car, is_generation_over)
def gen_over(cars, frame, max_frames, max_laps):
    # 1. Timeout
    if frame > max_frames:
        return True

    # 2. Someone finished a lap
    if any(c.lap_count >= max_laps for c in cars):
        return True

    # 3. Everyone got crashed or got stuck
    return all(not c.alive for c in cars)

# Returns a fresh list of n cars for the new generation.
def next_gen(champion, n, mutation, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR):
    #Generate fresh cars.
    cars = generate_cars(n, MAX_SPEED, MAX_ROT_SPEED, ACCELERATION, BASE_DIR)

    # Override car 0 - gets the previous generations champion's brain.
    cars[0].brain = copy.deepcopy(champion.brain)

    # Override every other car - a mutated version of the champion car.
    for i in range(1, n):
        cars[i].brain = copy.deepcopy(champion.brain)
        cars[i].brain.mutate(mutation * random.uniform(0.25, 2.5))

    return cars

# Returns (best score, best_lap_time). compares lap time if they have same score.
# lap time returns None is the champion didnt finish.
def save_champion(champion, best_score, best_lap_time, lap_time, generation, filepath):
    # If current generation goes further, True, Otherwise False
    further = champion.score > best_score
    faster = False

    # Handle tie breakers
    if champion.score == best_score and lap_time is not None:
        if best_lap_time is None or lap_time < best_lap_time:
            faster = True

    # If new generation went further or faster, new champion
    if further or faster:
        # Save car, generation and time in pickle file
        with open(filepath, "wb") as f:
            pickle.dump({
                "champion_brain": champion.brain,
                "generation": generation,
                "best_time": lap_time,
                "best_score": champion.score
            }, f)

        # And return the score and lap time of the champion.
        return champion.score, lap_time

    # Otherwise, return current champions score and time.
    return best_score, best_lap_time

# Loads champion in filepath into a fresh car and returns it, along with generation and best lap time
def load_champion(filepath, MAX_SPEED, MAX_ROT_SPEED, BASE_DIR):
    # If a load file doesn't exist
    if not os.path.exists(filepath):
        return None, None

    # Otherwise, unpack the data
    with open(filepath, "rb") as f:
        data = pickle.load(f)

    # Assign to variables
    champion_brain = data["champion_brain"]
    generation = data["generation"]
    best_time = data["best_time"]
    best_score = data["best_score"]

    return champion_brain, generation, best_time, best_score

# Draws HUD showing generation, best score and number of alive cars.
def draw_hud(screen, GENERATION, BEST_SCORE, BEST_LAP_TIME, ALIVE_COUNT, FINAL_TIME, FRAME, FPS, WIDTH):
    # Load font
    font = py.font.SysFont("Arial", 18)

    # Convert text to a surface
    # Generation Counter
    gen = font.render(f"Generation: {GENERATION}", True, (0,0,0))

    # Score counter
    score = font.render(f"Best Score: {BEST_SCORE}", True, (0,0,0))

    # Lap Time counter
    time = font.render(f"Lap Time: {FRAME/FPS:.2f}s", True, (0,0,0))

    # Best Lap Time counter
    if BEST_LAP_TIME is not None:
        best_time = font.render(f"Best Lap: {BEST_LAP_TIME:.2f}s", True, (0,0,0))
    else:
        best_time = font.render("Best Lap: --", True, (0,0,0))

    # Alive counter
    no_alive = font.render(f"No. Of Cars Alive: {ALIVE_COUNT}", True, (0,0,0))

    # Draw background
    rect_top_left_x = (WIDTH / 2) - 110

    # Draw on screen - uses width to dynamically draw on different tracks
    py.draw.rect(screen, (255,255,255), (rect_top_left_x,20,205,120))
    screen.blit(gen, (rect_top_left_x + 10, 25))
    screen.blit(score, (rect_top_left_x + 10, 45))
    screen.blit(time, (rect_top_left_x + 10, 65))
    screen.blit(best_time, (rect_top_left_x + 10, 85))
    screen.blit(no_alive, (rect_top_left_x + 10, 105))

# Figures out mutation - Use initial mutation, until generation 20, then use refining mutation
def get_mutation(GENERATION, INITIAL_MUTATION, REFINING_MUTATION):
    # Weak mutation used in generations 15-35 and 50 onwards.
    if (GENERATION >= 15 and GENERATION <= 35) or GENERATION >= 50:
        MUTATION = REFINING_MUTATION
    # Strong mutation used in generations 1-14 and 36-49.
    else:
        MUTATION = INITIAL_MUTATION
    return MUTATION