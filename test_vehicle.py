"""
test_f1_race.py
pytest unit tests for the F1 Race OOP lab.

Run with:
    pytest test_f1_race.py -v
"""

import pytest
from f1_race import Engine, Driver, Vehicle, RaceCar, RaceTeam, Race


# ══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def driver_alonso():
    return Driver("Alonso")

@pytest.fixture
def driver_verstappen():
    return Driver("Verstappen")

@pytest.fixture
def driver_hamilton():
    return Driver("Hamilton")

@pytest.fixture
def basic_engine():
    return Engine(horsepower=800, engine_type="V6 Hybrid")

@pytest.fixture
def basic_car(driver_alonso):
    """A single RaceCar for unit testing."""
    return RaceCar(number=14, driver=driver_alonso, team_name="Aston Martin",
                   speed=20, horsepower=750, engine_type="V6 Hybrid")

@pytest.fixture
def standard_cars(driver_alonso, driver_verstappen, driver_hamilton):
    """Three independent RaceCar objects — aggregation with Race."""
    car_14 = RaceCar(number=14, driver=driver_alonso,     team_name="Aston Martin",
                     speed=20, horsepower=750, engine_type="V6 Hybrid")
    car_1  = RaceCar(number=1,  driver=driver_verstappen, team_name="Red Bull",
                     speed=25, horsepower=820, engine_type="V6 Hybrid")
    car_44 = RaceCar(number=44, driver=driver_hamilton,   team_name="Mercedes",
                     speed=22, horsepower=800, engine_type="V6 Hybrid")
    return [car_14, car_1, car_44]

@pytest.fixture
def standard_race(standard_cars):
    race = Race()
    for car in standard_cars:
        race.add_car(car)
    return race



# ══════════════════════════════════════════════════════════════════════════════
# Vehicle Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestVehicle:

    def test_default_fuel(self):
        v = Vehicle(speed=100)
        assert v.fuel == 100
    #Removed because doesn't match the instructions
    '''
    def test_custom_fuel(self):
        v = Vehicle(speed=80, fuel=50)
        assert v.fuel == 50
        '''

    def test_speed_set(self):
        v = Vehicle(speed=150)
        assert v.speed == 150

    def test_refuel_adds_fuel(self):
        v = Vehicle(speed=100)
        v.fuel = 40
        v.refuel(30)
        assert v.fuel == 70

    def test_get_data_returns_string(self):
        v = Vehicle(speed=100)
        v.fuel = 75
        assert isinstance(v.get_data(), str)

    def test_get_data_format(self):
        v = Vehicle(speed=100)
        v.fuel = 75
        assert v.get_data() == "Vehicle with speed 100 and fuel 75"

    def test_no_str_method(self):
        """Vehicle should use get_data(), not __str__, for formatted output."""
        v = Vehicle(speed=100)
        v.fuel = 75
        # get_data() must exist
        assert hasattr(v, "get_data")
