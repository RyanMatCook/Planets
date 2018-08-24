#import math
from scipy import constants

class Position():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_string(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

class Velocity():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_string(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

class Acceleration():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_string(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

class ObjectLog():
    def __init__(self):
        self.log_size = 200
        self.position_log = []
        self.velocity_log = []
        self.acceleration_log = []

    def clean_log(self, time):
        self.position_log.remove(filter(lambda x: (time - self.log_size) >= x.time , self.position_log))
        self.velocity_log.remove(filter(lambda x: (time - self.log_size) >= x.time , self.velocity_log))
        self.acceleration_log.remove(filter(lambda x: (time - self.log_size) >= x.time , self.acceleration_log))
        

class Object():
    def __init__(self, id):
        self.id = id
        self.charge = 0
        self.mass = 0
        self.position = Position(0, 0, 0)
        self.velocity = Velocity(0, 0, 0)
        self.acceleration = Acceleration(0, 0, 0)
        self.log = ObjectLog()
        #self.print_self()

    def on_step(self, time, universe):
        self.calculate_position(time, universe)
        self.log.position_log.append(self.position)
        self.log.velocity_log.append(self.velocity)
        self.log.acceleration_log.append(self.acceleration)
        self.log.clean_log(time)

    def calculate_acceleration(self, time, universe):
        forces_x = []
        forces_y = []
        forces_z = []

        for item in universe:
            if item.id != self.id:
                abs_distance_vector = Position((self.position.x - item.position.x)**2, (self.position.y - item.position.y)**2, (self.position.z - item.position.z)**2)
                mass_multiplier = self.mass * item.mass
                # When distance between two objects is zero, gravitation force is infinite.
                if abs_distance_vector.x != 0:
                    forces_x.append((constants.gravitational_constant * mass_multiplier)/abs_distance_vector.x)
                if abs_distance_vector.y != 0:
                    forces_y.append((constants.gravitational_constant * mass_multiplier)/abs_distance_vector.y)
                if abs_distance_vector.z != 0:
                    forces_z.append((constants.gravitational_constant * mass_multiplier)/abs_distance_vector.z)

        self.acceleration.x = sum(forces_x)
        self.acceleration.y = sum(forces_y)
        self.acceleration.z = sum(forces_z)

    def calculate_velocity(self, time, universe):
        self.calculate_acceleration(time, universe)
        self.velocity.x = self.velocity.x + self.acceleration.x * time
        self.velocity.y = self.velocity.y + self.acceleration.y * time
        self.velocity.z = self.velocity.z + self.acceleration.z * time
    
    def calculate_position(self, time, universe):
        v0_x = self.velocity.x
        v0_y = self.velocity.y
        v0_z = self.velocity.z
        self.calculate_velocity(time, universe)
        self.position.x = self.position.x + ((v0_x + self.velocity.x)/2)*time
        self.position.y = self.position.y + ((v0_y + self.velocity.y)/2)*time
        self.position.z = self.position.z + ((v0_z + self.velocity.z)/2)*time
        
    def print_self(self):
        print("Object {0}:\n\tMass:\t\t{1}\n\tCharge:\t\t{2}\n\tPosition:\t{3}\n\tVelocity:\t{4}\n\tAcceleration:\t{5}"
                .format(self.id, self.mass, self.charge, self.position.to_string(), self.velocity.to_string(),self.acceleration.to_string())
            )

    def print_log(self):
        print("Dumping log for item {0}".format(self.id))
        print("Position, Velocity, Acceleration")
        log_size = min(len(self.log.position_log), self.log.log_size)
        for i in range(log_size):
            #print(i)
            print("{0}, {1}, {2}".format(self.log.position_log[i].to_string(), self.log.velocity_log[i].to_string(), self.log.acceleration_log[i].to_string()))

def test_two_objects():
    # Initialised @ 0, 0, 0
    destination = Object("Destination")
    destination.mass = 200
    destination.print_self()

    # Initialised @ 20, 0, 0
    focus = Object("Focus")
    focus.mass = 100
    focus.position.x = 20
    focus.print_self()

    return [destination, focus]

def dump_logs(universe):
    for item in universe:
        item.print_log()

universe = test_two_objects()

running = True
time = 0

for time in range(1, 300):
    print(time)
    for item in universe:
        item.on_step(time, universe)
        #item.print_self()

dump_logs(universe)

# print("Program Started... Press any key to terminate.")
# try:
#     while True:
#         time = time + 1
#         for item in universe:
#             item.on_step(time, universe)
#             item.print_self()
#         print(time)
# except KeyboardInterrupt:
#     pass
# print("Program has ended")
