import math
import pygame

def lerp(a, b, t):
    return a + (b - a) * t

class Sensor:
    def __init__(self, car):
        self.car = car

        # Number of rays
        self.ray_count = 9

        # Maximum length of each ray
        self.ray_length = 100

        # Same as 120 degrees - I want the ray to cast 120 degrees out the front
        self.ray_spread = math.pi * 0.66666666666666666

        # Will store distance values for each ray
        self.rays = []

        # Stores start and end co-ords for drawing
        self.draw_points = []

    # Calculates angle-dependant bounding box to update rays.
    def update(self, mask):
        # Resets lists from previous update
        self.rays = []
        self.draw_points = []

        # Find centre point of car (Want rays to come out the center)
        half_width = self.car.IMG.get_width() / 2
        half_height = self.car.IMG.get_height() / 2
        cx, cy = self.car.x + half_width, self.car.y + half_height

        # Converts angle to radians
        car_angle = math.radians(self.car.angle)
        # Gets size of map
        map_width, map_height = mask.get_size()

        # Loops through every ray
        for i in range(self.ray_count):
            # Figures out angle of this ray relative to car
            rel = lerp(self.ray_spread / 2, -self.ray_spread / 2, i / (self.ray_count - 1))
            # Adds angle with angle so its facing correct direction
            angle = rel + car_angle
            # How much the code should move by x and y when going pixel-by-pixel each ray.
            delta_x, delta_y = -math.sin(angle), -math.cos(angle)

            # Finds positive sin and cosine values of relative angle
            s, c = abs(math.sin(rel)), abs(math.cos(rel))

            # Calculates distance from cars center to its outer edge along ray.
            # Prevents div by zero by checking if s and c are close to zero
            if s > 0.0001:
                horizontal_edge = half_width / s
            else:
                horizontal_edge = math.inf
            
            if c > 0.00001:
                vertical_edge = half_height / c
            else:
                vertical_edge = math.inf

            # Find closest edge 
            edge = min(horizontal_edge, vertical_edge)

            # March along the ray until it hits the wall, leaves the map, or maxes out
            hit = self.ray_length
            for d in range(self.ray_length):
                px, py = int(cx + delta_x * d), int(cy + delta_y * d)
                if not (0 <= px < map_width and 0 <= py < map_height) or mask.get_at((px, py)):
                    hit = d
                    break

            self.rays.append(max(hit - edge, 0) / (self.ray_length - edge))
            self.draw_points.append(((cx, cy), (cx + delta_x * hit, cy + delta_y * hit)))

    def draw(self, screen):
        for start, end in self.draw_points:
            pygame.draw.line(screen, (255, 255, 0), start, end, 2)

    # Debugging
    def print_val(self):
        # Turn into list for readability
        rl = []
        for r in self.rays:
            rl.append(r)

        print(rl)

        
