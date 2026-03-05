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
# RaceCar Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestRaceCar:

    # Inheritance
    def test_inherits_vehicle(self, basic_car):
        assert isinstance(basic_car, Vehicle)

    def test_speed_inherited(self, basic_car):
        assert basic_car.speed == 20

    def test_initial_fuel_100(self, basic_car):
        assert basic_car.fuel == 100

    # Basic attributes
    def test_initial_distance_zero(self, basic_car):
        assert basic_car.distance == 0

    def test_number(self, basic_car):
        assert basic_car.number == 14

    def test_team_name(self, basic_car):
        assert basic_car.team_name == "Aston Martin"

    # Aggregation — Driver passed in from outside
    def test_driver_assigned(self, basic_car, driver_alonso):
        assert basic_car.driver is driver_alonso

    def test_driver_exists_independently(self, driver_alonso):
        """Aggregation: the same Driver object can be referenced without the car."""
        car = RaceCar(14, driver_alonso, "Aston Martin", 20, 750, 'V6 Hybrid')
        assert car.driver is driver_alonso   # same object, not a copy

    # Composition — Engine created inside RaceCar
    def test_engine_created_on_init(self, basic_car):
        assert hasattr(basic_car, "engine")
        assert isinstance(basic_car.engine, Engine)

    def test_engine_horsepower(self, basic_car):
        assert basic_car.engine.horsepower == 750

    def test_engine_type(self, basic_car):
        assert basic_car.engine.engine_type == "V6 Hybrid"

    def test_engine_is_composition(self, driver_alonso):
        """Composition: two different cars must have two different Engine objects."""
        car_a = RaceCar(1, driver_alonso, "Team A", 20, 750, 'V6 Hybrid')
        car_b = RaceCar(2, driver_alonso, "Team B", 20, 750, 'V6 Hybrid')
        assert car_a.engine is not car_b.engine

    # needs_pit_stop
    def test_needs_pit_stop_true_at_25(self, basic_car):
        basic_car.fuel = 25
        assert basic_car.needs_pit_stop() is True

    def test_needs_pit_stop_true_below_25(self, basic_car):
        basic_car.fuel = 10
        assert basic_car.needs_pit_stop() is True

    def test_needs_pit_stop_false_above_25(self, basic_car):
        basic_car.fuel = 26
        assert basic_car.needs_pit_stop() is False

    # pit_stop
    def test_pit_stop_resets_fuel(self, basic_car, capsys):
        basic_car.fuel = 20
        basic_car.pit_stop()
        assert basic_car.fuel == 100

    def test_pit_stop_prints_message(self, basic_car, capsys):
        basic_car.fuel = 20
        basic_car.pit_stop()
        captured = capsys.readouterr()
        assert "Car 14 must pit!" in captured.out

    # drive
    def test_drive_updates_distance_lap1(self, basic_car):
        basic_car.drive(1)
        assert basic_car.distance == pytest.approx(20.0)

    def test_drive_decreases_fuel(self, basic_car):
        initial_fuel = basic_car.fuel
        basic_car.drive(1)
        assert basic_car.fuel == initial_fuel - 21   # speed(20) + lap(1)

    def test_drive_multiple_laps(self, basic_car):
        basic_car.drive(1)   # +20
        basic_car.drive(2)   # +10
        assert basic_car.distance == pytest.approx(30.0)

    # get_data
    def test_get_data_returns_string(self, basic_car):
        assert isinstance(basic_car.get_data(), str)

    def test_get_data_format(self, basic_car):
        basic_car.drive(1)   # distance = 20
        assert basic_car.get_data() == "Car: 14 Distance: 20"

    def test_get_data_distance_as_int(self, basic_car):
        basic_car.drive(2)   # distance = 10.0 → displays as 10
        assert "Distance: 10" in basic_car.get_data()

    def test_get_data_exists(self, basic_car):
        assert hasattr(basic_car, "get_data")

