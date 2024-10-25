import math
#vars
r = 0 #radius
r2 = r * 1.1 #radius 2
v = 0 #velocity
a = 0 #acceleration
axis = 0 #axis
t = 0 #period
fg = 0 #gravitational force
m1 = 0 #sun mass
m2 = 0 #planet mass
G = 6.67e-11 #gravitational constant


#functions
def orbVel(m1, m2, r, axis):
    #orbital velocity
    v = math.sqrt(G * (m1 + m2) * (2 / r - 1 / axis))
    return v

def ellipse(r, r2):
    #ellipse axis
    area = math.pi * r * r2
    axis = (area)/(math.pi * r)
    return axis

def grav_force(m1, m2, r):
    #gravitational force
    fg = (m1*m2)/(r**2)
    return fg

def acceleration(m1, m2, r):
    #acceleration
    a = grav_force(m1, m2, r) / m2
    return a

def energy(m1, m2, axis):
    #total energy
    return -G * (m1 * m2) / 2 * axis

def kinetic(m1, m2, r):
    #kinetic energy
    return G * (m1 * m2) / 2 * r

def potential(m1, m2, r):
    #potential energy
    return -G * (m1 * m2) / r

def period(m1, m2, axis):
    #period
    t = 2 * math.pi * math.sqrt(G *axis**3 / (m1 + m2))
    return t