# ─────────────────────────────────────────────
# Engine  (owned by RaceCar — Composition)
# ─────────────────────────────────────────────
class Engine():
    def __init__(self, horsepower, engine_type):
        self.horsepower = horsepower
        self.engine_type = engine_type
        self.is_running = False
    
    def start(self):
        self.is_running = True
    
    def stop(self):
        self.is_running = False
    
    def get_data(self):
        return f'Enging : {self.engine_type} | HP: {self.horsepower} | Status: {self.is_running}'


# ─────────────────────────────────────────────
# Vehicle Base Class
# ─────────────────────────────────────────────
class Vehicle():
    def __init__(self, speed):
        self.speed = speed
        self.fuel = 100
    
    def refuel(self, amount):
        self.fuels += amount
    
    def get_data(self):
        return f'Vehicle with speed {self.speed} and fuel {self.fuel}'

# ─────────────────────────────────────────────
# RaceCar (inherits Vehicle, owns Engine — Composition)
# ─────────────────────────────────────────────
class RaceCar(Vehicle):
    def __init__(self, number, driver, team_name, speed, horsepower, engine_type):
        super().__init__(speed)
        self.number = number
        self.driver = driver
        self.team_name = team_name
        self.distance = 0
        self.engine = Engine(horsepower, engine_type)
    
    def needs_pit_stop(self):
        if self.fuel <= 25:
            return True
        else:
            return False
    
    def pit_stop(self):
        print(f'Car {self.number} must pit!')
        self.fuel = 100
    
    def drive(self, lap):
        self.distance += (self.speed / lap)
        self.fuel -= (self.speed + lap)
    
    def get_data(self):
        return f'Car: {self.number} Distance: {int(self.distance)}'


# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
class Driver:
    def __init__(self, name):
        self.name = name
    
    def get_driver_data(self):
        return f'Driver: {self.name}'



# ─────────────────────────────────────────────
# RaceTeam (Aggregation with Driver)
# ─────────────────────────────────────────────



# ─────────────────────────────────────────────
# Race (Aggregation with RaceCar)
# ─────────────────────────────────────────────



# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    #Remove pass
    pass
    # Create Driver objects independently (aggregation)
    

    # Create RaceCar objects independently (aggregation with Race).
    # Each RaceCar creates its own Engine internally (composition).
   

    # Create a Race and add each car via add_car() (aggregation)
   