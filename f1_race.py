# ─────────────────────────────────────────────
# Engine  (owned by RaceCar — Composition)
# ─────────────────────────────────────────────
class Engine():
    def __init__(self, horsepower, engine_type):
        self.horsepower = horsepower
        self.engine_type = engine_type
        self.is_running = 'Off'

    def start(self):
        self.is_running = 'On'
    
    def stop(self):
        self.is_running = 'Off'
    
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
        self.fuel += amount
    
    def get_data(self):
        return f'Vehicle with speed {self.speed} and fuel {self.fuel}'

# ─────────────────────────────────────────────
# RaceCar (inherits Vehicle, owns Engine — Composition)
# ─────────────────────────────────────────────
#TODO: CHECK FUNCTIONALITY
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
class RaceTeam:
    def __init__(self, name):
        self.name = name
        self.drivers = []
    
    def add_driver(self, driver):
        self.drivers.append(driver)

    #TODO: Double check that instructions are clear
    def get_team_data(self):
        driver_names = ", ".join(d.name for d in self.drivers)
        return f'Team: {self.name} Drivers: {driver_names}'


# ─────────────────────────────────────────────
# Race (Aggregation with RaceCar)
# ─────────────────────────────────────────────
class Race:
    def __init__(self):
        self.race_cars = []
    
    def add_car(self, race_car):
        self.race_cars.append(race_car)

    #TODO: FIX INSTRUCTION AND TESTS FOR THIS FUNCTION
    #Should match original instructions
    def print_set_teams(self):
        teams = {car.team_name for car in self.race_cars}
        print(f"Teams in race: {teams}")
    
    def run_lap(self, lap):
        print(f'---Lap {lap}---')
        for car in self.race_cars:
            if car.needs_pit_stop() == True:
                car.pit_stop()
            else:
                car.drive(lap)
            print(car.get_data())
    
    def race(self, laps):
        try:
            for lap in range(1,laps + 1):
                self.run_lap(lap)
        except ZeroDivisionError as e:
            print(f'{e} - Lap count cannot be zero')
    
    def print_final_results(self):
        print("---Final Results---")
        sorted_cars = sorted(self.race_cars, key=lambda c: c.distance, reverse=True)
        for car in sorted_cars:
            print(f"Driver: {car.driver.name}")
            print(f"\t Team: {car.team_name} ")
            print(f"\t Distance: {int(car.distance)}")





# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    #Remove pass
    pass
    # Create Driver objects independently (aggregation)
    alonso = Driver('Alonso')
    verstappen = Driver('Verstappen')
    hamilton = Driver('Hamilton')


    # Create RaceCar objects independently (aggregation with Race).
     #number, driver, team_name, speed, horsepower, engine_type
    car_14 = RaceCar(14, alonso, 'Aston Martin', 20, 750, 'V6 Hybrid')
    car_1 = RaceCar(1, verstappen, 'Red Bull', 25, 820, 'V6 Hybrid')
    car_44 = RaceCar(55, hamilton, 'Mercedes', 22, 800, 'V6 Hybrid')
    # Each RaceCar creates its own Engine internally (composition).
   

    # Create a Race and add each car via add_car() (aggregation)
    #TODO: change instructions to call add_car
    f1_race = Race()
    f1_race.add_car(car_14)
    f1_race.add_car(car_1)
    f1_race.add_car(car_44)

    #TODO: Add instructions to take in the number of laps for a race
    laps = int(input("Enter the number of laps for the race: "))
    f1_race.print_set_teams()
    f1_race.race(laps)
    f1_race.print_final_results()
   
    #TODO: Add teams to instructions
    red_bull = RaceTeam('Red Bull')
    red_bull.add_driver(alonso)
    red_bull.add_driver(verstappen)
    print(red_bull.get_team_data())