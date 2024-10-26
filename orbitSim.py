import math

r = 0  # Radius
r2 = r * 1.1  # Radius 2
v = 0  # Velocity
a = 0  # Acceleration
axis = 0  # Axis
t = 0  # Period
fg = 0  # Gravitational force
m1 = 0  # Sun mass
m2 = 0  # Planet mass
G = 6.67e-11  # Gravitational constant


# Orbital velocity
def orbVel(m1, m2, r, axis):
    v = math.sqrt(G * (m1 + m2) * (2 / r - 1 / axis))
    return v


# Ellipse axis
def ellipse(r, r2):
    area = math.pi * r * r2
    axis = (area)/(math.pi * r)
    return axis


# Gravitational force
def grav_force(m1, m2, r):
    fg = (m1*m2)/(r**2)
    return fg


# Acceleration
def acceleration(m1, m2, r):
    a = grav_force(m1, m2, r) / m2
    return a


# Total energy
def energy(m1, m2, axis):
    return -G * (m1 * m2) / 2 * axis


# Kinetic energy
def kinetic(m1, m2, r):
    return G * (m1 * m2) / 2 * r


# Potential energy
def potential(m1, m2, r):
    return -G * (m1 * m2) / r


# Period
def period(m1, m2, axis):
    t = 2 * math.pi * math.sqrt(G *axis**3 / (m1 + m2))
    return t