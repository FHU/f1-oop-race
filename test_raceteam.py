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
# RaceTeam Tests (Aggregation with Driver)
# ══════════════════════════════════════════════════════════════════════════════

class TestRaceTeam:

    def test_team_name(self):
        team = RaceTeam("Red Bull")
        assert team.name == "Red Bull"

    def test_empty_drivers_list(self):
        team = RaceTeam("Red Bull")
        assert team.drivers == []

    def test_add_driver(self, driver_verstappen):
        team = RaceTeam("Red Bull")
        team.add_driver(driver_verstappen)
        assert driver_verstappen in team.drivers

    def test_add_multiple_drivers(self, driver_alonso, driver_hamilton):
        team = RaceTeam("Multi")
        team.add_driver(driver_alonso)
        team.add_driver(driver_hamilton)
        assert len(team.drivers) == 2

    def test_aggregation_same_object(self, driver_alonso):
        """Aggregation: Driver passed in is the exact same object (not a copy)."""
        team = RaceTeam("Aston Martin")
        team.add_driver(driver_alonso)
        assert team.drivers[0] is driver_alonso

    def test_get_team_data_returns_string(self, driver_verstappen):
        team = RaceTeam("Red Bull")
        team.add_driver(driver_verstappen)
        assert isinstance(team.get_team_data(), str)

    def test_get_team_data_contains_name(self, driver_verstappen):
        team = RaceTeam("Red Bull")
        team.add_driver(driver_verstappen)
        assert "Red Bull" in team.get_team_data()

    def test_get_team_data_contains_driver(self, driver_verstappen):
        team = RaceTeam("Red Bull")
        team.add_driver(driver_verstappen)
        assert "Verstappen" in team.get_team_data()

    def test_get_team_data_multiple_drivers(self, driver_alonso, driver_hamilton):
        team = RaceTeam("Multi")
        team.add_driver(driver_alonso)
        team.add_driver(driver_hamilton)
        result = team.get_team_data()
        assert "Alonso" in result
        assert "Hamilton" in result

    def test_get_team_data_exists(self):
        assert hasattr(RaceTeam("X"), "get_team_data")