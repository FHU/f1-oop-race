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
# Driver Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestDriver:

    def test_name(self, driver_alonso):
        assert driver_alonso.name == "Alonso"

    def test_get_driver_data_returns_string(self, driver_alonso):
        assert isinstance(driver_alonso.get_driver_data(), str)

    def test_get_driver_data_format(self, driver_alonso):
        assert driver_alonso.get_driver_data() == "Driver: Alonso"

    def test_get_driver_data_exists(self, driver_alonso):
        assert hasattr(driver_alonso, "get_driver_data")
