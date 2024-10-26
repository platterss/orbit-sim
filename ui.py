import pygame
import math
import sys
import orbitSim

m1 = 1.989e30  # Sun mass (kg)
time_scale = 2000000  # Speed up time by this factor

pygame.init()

WIDTH, HEIGHT = 1300, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulator")

#Display text
def text_objects(text, font):
    white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', font)
    text = font.render(text, True, white)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 8, HEIGHT // 4)
    SCREEN.blit(text, textRect)

def load_image(name, scale):
    image = pygame.image.load(f'images/{name}').convert_alpha()
    w, h = image.get_size()
    image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return image


class Planet:
    def __init__(self, name, image, mass, orbit_radius_m, orbit_radius_pixels, size):
        self.name = name
        self.image = load_image(image, size)
        self.mass = mass # kg
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

    sun = Planet("Sun", "sun.jpg", m1, 0, 0, 0.1)
    sun.x, sun.y = center_x, center_y
    planets.append(sun)

    # Parameters: name, image file, mass (kg), orbit radius (m), orbit radius (pixels), size scale
    planet_data = [
        ("Mercury", "mercury.jpg", 3.285e23, 5.791e10, 60, 0.05),
        ("Venus", "venus.jpg", 4.867e24, 1.082e11, 100, 0.07),
        ("Earth", "earth.jpg", 5.972e24, 1.496e11, 140, 0.07),
        ("Mars", "mars.jpg", 6.39e23, 2.279e11, 180, 0.06),
        ("Jupiter", "jupiter.jpg", 1.898e27, 7.785e11, 240, 0.15),
        ("Saturn", "saturn.jpg", 5.683e26, 1.433e12, 300, 0.13),
        ("Uranus", "uranus.jpg", 8.681e25, 2.872e12, 360, 0.1),
        ("Neptune", "neptune.jpg", 1.024e26, 4.495e12, 420, 0.1)
    ]

    for data in planet_data:
        planet = Planet(*data)
        planets.append(planet)

    return planets

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

        text_objects("Orbit Simulator", 16)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
