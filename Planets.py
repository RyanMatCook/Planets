import math
from scipy import scipy.gravitational_constant

class Position():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Velocity():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Acceleration():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Force():
    def __init__(self, fX, fY, fZ):
        self.position = Position(fX, fY, fZ)

class Object():
    def __init__(self, id):
        self.id = 0
        self.charge = 0
        self.mass = 0
        self.position = Position(0, 0, 0)
        self.velocity = Velocity(0, 0, 0)
        self.acceleration = Acceleration(0, 0, 0)
        self.print_self()

    def on_step(self, time, universe):
        print("Calculating vectors for item {}".format(self.id))
        self.calculate_position(time, universe)

    def calculate_acceleration(self, time, universe):
        print("Calculating acceleration.")
        for item in universe:
            if item.id != self.id:
                return (self.mass * item.mass)/((math.abs(self.x - item.x)))
            else:
                return 0

    def get_impact_gravity(self, item):
        return (self.mass * item.mass)/((math.abs(self.x - item.x)))

    def calculate_velocity(self, time, universe):
        self.calculate_acceleration(time, universe)
        return 0
    
    def calculate_position(self, time, universe):
        self.calculate_velocity(time, universe)
        return 0
        

    def print_self(self):
        print("Object Defined:\n\tMass:{0}\n\tCharge:{1}\n\tPosition: ({2},{3})"
            .format(self.charge, self.mass, self.position.x, self.position.y))

print (gravitational_constant)
destination = Object("Destination")
source = Object("Source")
focus = Object("Focus")

universe = [
    source,
    destination,
    focus
]
running = True
time = 0
print("Program Started... Press any key to terminate.")
try:
    while True:
        time = time + 1
        for item in universe:
            item.on_step(time, universe)
        print(time)
except KeyboardInterrupt:
    pass

print("Program has ended")
