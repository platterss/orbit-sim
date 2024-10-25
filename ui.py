import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulator")

def load_image(name, scale):
    image = pygame.image.load(f'images/{name}').convert_alpha()
    w, h = image.get_size()
    image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return image

class Planet:
    def __init__(self, name, image, orbit_radius, orbit_speed, size, angle=0):
        self.name = name
        self.image = load_image(image, size)
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = angle
        self.x = 0
        self.y = 0

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

    sun = Planet("Sun", "sun.jpg", 0, 0, 0.2)
    sun.x, sun.y = center_x, center_y
    planets.append(sun)

    # Parameters: name, image file, orbit radius, orbit speed, size scale
    planet_data = [
        ("Mercury", "mercury.jpg", 60, 0.04, 0.05),
        ("Venus", "venus.jpg", 100, 0.035, 0.07),
        ("Earth", "earth.jpg", 140, 0.03, 0.07),
        ("Mars", "mars.jpg", 180, 0.025, 0.06),
        ("Jupiter", "jupiter.jpg", 240, 0.02, 0.15),
        ("Saturn", "saturn.jpg", 300, 0.015, 0.13),
        ("Uranus", "uranus.jpg", 360, 0.01, 0.1),
        ("Neptune", "neptune.jpg", 420, 0.005, 0.1)
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
        clock.tick(60) # 60 FPS
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for planet in planets:
            if planet.name != "Sun":
                planet.update_position(center_x, center_y)
                pygame.draw.circle(SCREEN, (100, 100, 100), (center_x, center_y), int(planet.orbit_radius), 1)
            planet.draw(SCREEN)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
