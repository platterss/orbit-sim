import pygame
import math
import sys
import orbitSim
import self

m1 = 1.989e30  # Sun mass (kg)
time_scale = 2000000  # Speed up time by this factor

pygame.init()

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulator")


def text_objects(text, font, a, b):
    white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', font)
    text = font.render(text, True, white)
    textRect = text.get_rect()
    textRect.center = (WIDTH // a, HEIGHT // b)
    SCREEN.blit(text, textRect)


def load_image(name, size):
    image = pygame.image.load(f'images/{name}').convert_alpha()
    image = pygame.transform.scale(image, (int(size), int(size)))
    return image

class Slider:
    def __init__(self, pos:tuple, size,tuple, initial_val: float, min: int) -> None:
        self.pos = (20, pos[1]) #pos
        self.size = size

        self.slider_left_pos = self.pos[0]
        self.slider_right_pos = self.pos[0] + self.size[0]
        self.slider_top_pos = self.pos[1] - self.size[1]

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val #percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.container_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.button_rect)

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

class Planet:
    def __init__(self, name, image, mass, orbit_radius_m, orbit_radius_pixels, size):
        self.name = name
        self.image = load_image(image, size)
        self.mass = mass  # kg
        self.orbit_radius_m = orbit_radius_m
        self.orbit_radius = orbit_radius_pixels
        self.size = size
        self.angle = 0
        self.x = 0
        self.y = 0

        if self.name != "Sun":
            axis = self.orbit_radius_m
            v = orbitSim.orbVel(m1, self.mass, self.orbit_radius_m, axis)
            omega = v / self.orbit_radius_m
            self.orbit_speed = omega * (1 / 60.0) * time_scale
        else:
            self.orbit_speed = 0

    def update_position(self, center_x, center_y):
        self.angle += self.orbit_speed
        self.x = center_x + self.orbit_radius * math.cos(self.angle)
        self.y = center_y + self.orbit_radius * math.sin(self.angle)

    def draw(self, surface):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, rect)


def create_planets():
    planets = []
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    sun_size = 75  # pixels
    sun = Planet("Sun", "sun.jpg", m1, 0, 0, sun_size)
    sun.x, sun.y = center_x, center_y
    planets.append(sun)

    planetary_radii = {  # km
        "Sun": 696340,
        "Mercury": 2440,
        "Venus": 6052,
        "Earth": 6371,
        "Mars": 3390,
        "Jupiter": 69911,
        "Saturn": 58232,
        "Uranus": 25362,
        "Neptune": 24622
    }

    sun_radius = planetary_radii["Sun"]

    # Parameters: name, image file, mass (kg), orbit radius (m), orbit radius (pixels)
    planet_data = [
        ("Mercury", "mercury.jpg", 3.285e23, 5.791e10, 60),
        ("Venus", "venus.jpg", 4.867e24, 1.082e11, 100),
        ("Earth", "earth.jpg", 5.972e24, 1.496e11, 140),
        ("Mars", "mars.jpg", 6.39e23, 2.279e11, 180),
        ("Jupiter", "jupiter.jpg", 1.898e27, 7.785e11, 240),
        ("Saturn", "saturn.jpg", 5.683e26, 1.433e12, 300),
        ("Uranus", "uranus.jpg", 8.681e25, 2.872e12, 360),
        ("Neptune", "neptune.jpg", 1.024e26, 4.495e12, 420)
    ]

    for data in planet_data:
        name, image_file, mass, orbit_radius_m, orbit_radius_pixels = data
        planet_radius = planetary_radii[name]
        size = sun_size * ((planet_radius / sun_radius) ** (1 / 6))  # 6th root for visibility
        planet = Planet(name, image_file, mass, orbit_radius_m, orbit_radius_pixels, size)
        planets.append(planet)

    return planets

self.sliders = [Slider((WIDTH // 2, HEIGHT - 50), (WIDTH // 4, 10), (0, 1), 0.5, 0)]

def main():
    clock = pygame.time.Clock()
    planets = create_planets()
    running = True

    BLACK = (0, 0, 0)

    center_x, center_y = WIDTH // 2, HEIGHT // 2

    while running:
        clock.tick(60)  # 60 FPS
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for planet in planets:
            if planet.name != "Sun":
                planet.update_position(center_x, center_y)
                pygame.draw.circle(SCREEN, (100, 100, 100), (center_x, center_y), int(planet.orbit_radius), 1)
            else:
                planet.x, planet.y = center_x, center_y
            planet.draw(SCREEN)

        for slider in self.sliders:
            if slider.container_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
               slider.move_slider(pygame.mouse.get_pos())
            slider.draw(SCREEN)

        text_objects("Planet: " + planets[0].name, 24, 8, 7)
        text_objects("Mass: " + str(planets[0].mass) + " kg", 24, 8, 5)
        text_objects("Radius: " + str(planets[0].orbit_radius_m) + "km", 24, 8, 4)
        text_objects("Adjust mass by dragging slider", 24, 8, 1.1)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
