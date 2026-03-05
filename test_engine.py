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
# Engine Tests (Composition — owned by RaceCar)
# ══════════════════════════════════════════════════════════════════════════════

class TestEngine:

    def test_horsepower(self, basic_engine):
        assert basic_engine.horsepower == 800

    def test_engine_type(self, basic_engine):
        assert basic_engine.engine_type == "V6 Hybrid"

    def test_initial_not_running(self, basic_engine):
        assert basic_engine.is_running == 'Off'

    def test_start_sets_running_true(self, basic_engine):
        basic_engine.start()
        assert basic_engine.is_running == 'On'

    def test_stop_sets_running_false(self, basic_engine):
        basic_engine.start()
        basic_engine.stop()
        assert basic_engine.is_running == 'Off'

    def test_get_data_when_off(self, basic_engine):
        result = basic_engine.get_data()
        assert "V6 Hybrid" in result
        assert "800" in result
        assert "Off" in result

    def test_get_data_when_running(self, basic_engine):
        basic_engine.start()
        result = basic_engine.get_data()
        assert "On" in result

    def test_get_data_returns_string(self, basic_engine):
        assert isinstance(basic_engine.get_data(), str)
