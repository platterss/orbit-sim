import pygame
import math
import sys
import orbitSim
from orbitSim import grav_force

pygame.init()

WIDTH, HEIGHT = 1500, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulator")


def text_objects(text, font_size, a, b):
    white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', int(font_size))
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // a, HEIGHT // b)
    SCREEN.blit(text_surface, text_rect)


def load_image(name, size):
    image = pygame.image.load(f'images/{name}').convert_alpha()
    image = pygame.transform.scale(image, (int(size), int(size)))
    return image


class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = (20, pos[1])  # pos
        self.size = size

        self.slider_left_pos = self.pos[0]
        self.slider_right_pos = self.pos[0] + self.size[0]
        self.slider_top_pos = self.pos[1] - self.size[1]

        self.min = min
        self.max = max
        self.initial_val = initial_val  # between min and max

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])

        initial_fraction = (initial_val - self.min) / (self.max - self.min)
        initial_button_x = self.slider_left_pos + initial_fraction * (self.slider_right_pos - self.slider_left_pos)
        self.button_rect = pygame.Rect(initial_button_x - 5, self.slider_top_pos, 10, self.size[1])

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.container_rect)
        pygame.draw.rect(surface, (128, 128, 128), self.button_rect)

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]
        self.button_rect.centerx = max(self.slider_left_pos, min(self.button_rect.centerx, self.slider_right_pos))

    def get_val(self):
        value_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val / value_range) * (self.max - self.min) + self.min

    def set_val(self, value):
        # Ensure value is within [self.min, self.max]
        value = max(self.min, min(value, self.max))
        fraction = (value - self.min) / (self.max - self.min)
        self.button_rect.centerx = self.slider_left_pos + fraction * (self.slider_right_pos - self.slider_left_pos)




class RadioButton:
    def __init__(self, x, y, radius, text, value, group):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.value = value
        self.group = group
        self.selected = False
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.label = self.font.render(text, True, (255, 255, 255))
        self.label_rect = self.label.get_rect()
        self.label_rect.left = x + radius + 10
        self.label_rect.centery = y

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 2)
        if self.selected:
            pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius - 4)
        surface.blit(self.label, self.label_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            distance = math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
            if distance <= self.radius:
                for rb in self.group:
                    rb.selected = False
                self.selected = True
                return self.value
        return None


class Planet:
    def __init__(self, name, image, mass, orbit_radius_m, orbit_radius_pixels, size, time_scale):
        self.name = name
        self.image = load_image(image, size)
        self.mass = mass  # kg
        self.orbit_radius_m = orbit_radius_m
        self.orbit_radius = orbit_radius_pixels
        self.size = size
        self.angle = 0
        self.x = 0
        self.y = 0
        self.visible = True

        if self.name != "Sun":
            axis = self.orbit_radius_m
            v = orbitSim.orbVel(m1, self.mass, self.orbit_radius_m, axis)
            omega = v / self.orbit_radius_m
            self.orbital_velocity = v
            self.orbit_speed = omega * (1 / 60.0) * time_scale
        else:
            self.orbital_velocity = 0
            self.orbit_speed = 0

    def update_position(self, center_x, center_y):
        self.angle += self.orbit_speed
        self.x = center_x + self.orbit_radius * math.cos(self.angle)
        self.y = center_y + self.orbit_radius * math.sin(self.angle)

    def draw(self, surface):
        if self.visible:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, rect)

    def is_clicked(self, mouse_pos):
        if not self.visible:
            return False
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        return rect.collidepoint(mouse_pos)


def create_planets():
    planets = []
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    sun_size = 75  # pixels
    sun = Planet("Sun", "sun.jpg", m1, 0, 0, sun_size, time_scale)
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
        planet = Planet(name, image_file, mass, orbit_radius_m, orbit_radius_pixels, size, time_scale)
        planets.append(planet)

    return planets


def update_mass_slider(selected_planet, slider, original_masses):
    original_mass = original_masses[selected_planet.name]
    min_mass = original_mass * 0.5
    max_mass = original_mass * 1.5
    slider_value = (selected_planet.mass - min_mass) / (max_mass - min_mass)
    slider.set_val(slider_value)


# def update_velocity(selected_planet, sliders, original_masses):
#     new_mass = update_selected_planet_mass(selected_planet, sliders[0], original_masses)
#     v = orbitSim.orbVel(m1, new_mass, selected_planet.orbit_radius_m, selected_planet.orbitSim.ellipse(selected_planet.orbit_radius_m, Place radius 2))
#     return v


def update_selected_planet_mass(selected_planet, slider, original_masses):
    slider_value = slider.get_val()
    original_mass = original_masses[selected_planet.name]
    min_mass = original_mass * 0.5
    max_mass = original_mass * 1.5
    new_mass = min_mass + (max_mass - min_mass) * slider_value
    selected_planet.mass = new_mass
    return new_mass


def main():
    global m1
    clock = pygame.time.Clock()
    running = True

    BLACK = (0, 0, 0)

    center_x, center_y = WIDTH // 2, HEIGHT // 2

    reset_button_rect = pygame.Rect(WIDTH - 150, 20, 130, 40)
    reset_button_color = (100, 100, 100)

    hide_button_rect = pygame.Rect(WIDTH - 150, 80, 130, 40)
    hide_button_color = (100, 100, 100)

    sliders = [Slider((WIDTH // 2, HEIGHT - 30), (WIDTH // 4, 20), 0.5, 0, 1)]

    radio_buttons = []
    radio_button_x = 170
    radio_button_y = HEIGHT - 250
    radio_button_radius = 10
    radio_button_spacing = 30

    time_scales = [(1, "1x"), (2, "2x"), (5, "5x")]
    radio_button_group = []

    for i, (value, label) in enumerate(time_scales):
        rb = RadioButton(
            radio_button_x,
            radio_button_y + i * radio_button_spacing,
            radio_button_radius,
            label,
            value,
            radio_button_group
        )
        radio_button_group.append(rb)
        radio_buttons.append(rb)

    radio_buttons[0].selected = True
    global time_scale
    time_scale = radio_buttons[0].value * 2000000

    planets = create_planets()
    selected_planet = planets[0]

    original_masses = {planet.name: planet.mass for planet in planets}

    update_mass_slider(selected_planet, sliders[0], original_masses)

    while running:
        clock.tick(60)  # 60 FPS
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if reset_button_rect.collidepoint(mouse_pos):
                    for planet in planets:
                        planet.visible = True
                        planet.mass = original_masses[planet.name]
                    m1 = original_masses["Sun"]
                    for planet in planets:
                        if planet.name != "Sun":
                            axis = planet.orbit_radius_m
                            v = orbitSim.orbVel(m1, planet.mass, planet.orbit_radius_m, axis)
                            omega = v / planet.orbit_radius_m
                            planet.orbital_velocity = v
                            planet.orbit_speed = omega * (1 / 60.0) * time_scale
                        else:
                            planet.orbital_velocity = 0
                            planet.orbit_speed = 0
                    update_mass_slider(selected_planet, sliders[0], original_masses)
                elif hide_button_rect.collidepoint(mouse_pos):
                    selected_planet.visible = not selected_planet.visible
                else:
                    for planet in planets:
                        if planet.is_clicked(mouse_pos):
                            selected_planet = planet
                            update_mass_slider(selected_planet, sliders[0], original_masses)
                            break
                for btn in radio_buttons:
                    selected_value = btn.handle_event(event)
                    if selected_value is not None:
                        time_scale = selected_value * 2000000
                        for planet in planets:
                            if planet.name != "Sun":
                                axis = planet.orbit_radius_m
                                v = orbitSim.orbVel(m1, planet.mass, planet.orbit_radius_m, axis)
                                omega = v / planet.orbit_radius_m
                                planet.orbital_velocity = v
                                planet.orbit_speed = omega * (1 / 60.0) * time_scale

        for slider in sliders:
            if slider.container_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                slider.move_slider(pygame.mouse.get_pos())
            slider.draw(SCREEN)

        new_mass = update_selected_planet_mass(selected_planet, sliders[0], original_masses)

        if selected_planet.name == "Sun":
            m1 = new_mass
            for planet in planets:
                if planet.name != "Sun":
                    axis = planet.orbit_radius_m
                    v = orbitSim.orbVel(m1, planet.mass, planet.orbit_radius_m, axis)
                    omega = v / planet.orbit_radius_m
                    planet.orbital_velocity = v
                    planet.orbit_speed = omega * (1 / 60.0) * time_scale
                else:
                    planet.orbital_velocity = 0
        else:
            axis = selected_planet.orbit_radius_m
            v = orbitSim.orbVel(m1, selected_planet.mass, selected_planet.orbit_radius_m, axis)
            omega = v / selected_planet.orbit_radius_m
            selected_planet.orbital_velocity = v
            selected_planet.orbit_speed = omega * (1 / 60.0) * time_scale

        for planet in planets:
            if planet.name != "Sun":
                planet.update_position(center_x, center_y)
                if planet.visible:
                    pygame.draw.circle(
                        SCREEN,
                        (100, 100, 100),
                        (center_x, center_y),
                        int(planet.orbit_radius),
                        1
                    )
            else:
                planet.x, planet.y = center_x, center_y
            planet.draw(SCREEN)

        for rb in radio_buttons:
            rb.draw(SCREEN)

        pygame.draw.rect(SCREEN, reset_button_color, reset_button_rect)
        reset_text = pygame.font.Font('freesansbold.ttf', 20).render(
            "Reset Planets", True, (255, 255, 255)
        )
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        SCREEN.blit(reset_text, reset_text_rect)

        pygame.draw.rect(SCREEN, hide_button_color, hide_button_rect)
        hide_text = pygame.font.Font('freesansbold.ttf', 20).render(
            "Hide Planet", True, (255, 255, 255)
        )
        hide_text_rect = hide_text.get_rect(center=hide_button_rect.center)
        SCREEN.blit(hide_text, hide_text_rect)

        text_objects("Planet: " + selected_planet.name, 24, 8, 7)
        text_objects("Mass: " + "{:.2e}".format(selected_planet.mass) + " kg", 24, 8, 5)

        if selected_planet.name != "Sun":
            text_objects("Orbit Radius: " + "{:.2e}".format(selected_planet.orbit_radius_m) + " m", 24, 8, 3.7)
            orbital_speed_kms = selected_planet.orbital_velocity / 1000  # Convert m/s to km/s
            text_objects("Orbital Speed: " + "{:.2f}".format(orbital_speed_kms) + " km/s", 24, 8, 4.2)
            force = orbitSim.grav_force(m1, selected_planet.mass, selected_planet.orbit_radius_m)
            text_objects("Gravitational Force: " + "{:.2e}".format(force) + " N", 24, 8, 3.3)
            acceleration = orbitSim.acceleration(m1, selected_planet.mass, selected_planet.orbit_radius_m) / 1000
            text_objects("Acceleration: " + "{:.2f}".format(acceleration) + " km/s^2", 24, 8, 3)
            total_energy = orbitSim.energy(m1, selected_planet.mass, selected_planet.orbit_radius_m)
            text_objects("Total Energy: " + "{:.2e}".format(total_energy) + " J", 24, 8, 2.7)
            kinetic_energy = orbitSim.kinetic(m1, selected_planet.mass, selected_planet.orbit_radius_m)
            text_objects("Kinetic Energy: " + "{:.2e}".format(kinetic_energy) + " J", 24, 8, 2.5)
            potential_energy = orbitSim.potential(m1, selected_planet.mass, selected_planet.orbit_radius_m)
            text_objects("Potential Energy: " + "{:.2e}".format(potential_energy) + " J", 24, 8, 2.3)
        else:
            text_objects("Orbit Radius: N/A", 24, 8, 3.7)
            text_objects("Orbital Speed: N/A", 24, 8, 4.2)
            text_objects("Gravitational Force: N/A", 24, 8, 3.3)
            text_objects("Acceleration: N/A", 24, 8, 3)
            text_objects("Total Energy: N/A", 24, 8, 2.7)
            text_objects("Kinetic Energy: N/A", 24, 8, 2.5)
            text_objects("Potential Energy: N/A", 24, 8, 2.3)


        text_objects("Adjust mass of selected planet", 24, 7.5, 1.1)
        text_objects("Click on a planet to select it", 18, 8, 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    m1 = 1.989e30  # Sun mass (kg)
    time_scale = 2000000  # Speed up time by this factor
    main()