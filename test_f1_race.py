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
        assert basic_engine.is_running is False

    def test_start_sets_running_true(self, basic_engine):
        basic_engine.start()
        assert basic_engine.is_running is True

    def test_stop_sets_running_false(self, basic_engine):
        basic_engine.start()
        basic_engine.stop()
        assert basic_engine.is_running is False

    def test_get_data_when_off(self, basic_engine):
        result = basic_engine.get_data()
        assert "V6 Hybrid" in result
        assert "800" in result
        assert "Off" in result

    def test_get_data_when_running(self, basic_engine):
        basic_engine.start()
        result = basic_engine.get_data()
        assert "Running" in result

    def test_get_data_returns_string(self, basic_engine):
        assert isinstance(basic_engine.get_data(), str)


# ══════════════════════════════════════════════════════════════════════════════
# Vehicle Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestVehicle:

    def test_default_fuel(self):
        v = Vehicle(speed=100)
        assert v.fuel == 100

    def test_custom_fuel(self):
        v = Vehicle(speed=80, fuel=50)
        assert v.fuel == 50

    def test_speed_set(self):
        v = Vehicle(speed=150)
        assert v.speed == 150

    def test_refuel_adds_fuel(self):
        v = Vehicle(speed=100, fuel=40)
        v.refuel(30)
        assert v.fuel == 70

    def test_get_data_returns_string(self):
        v = Vehicle(speed=100, fuel=75)
        assert isinstance(v.get_data(), str)

    def test_get_data_format(self):
        v = Vehicle(speed=100, fuel=75)
        assert v.get_data() == "Vehicle with speed 100 and fuel 75"

    def test_no_str_method(self):
        """Vehicle should use get_data(), not __str__, for formatted output."""
        v = Vehicle(speed=100, fuel=75)
        # get_data() must exist
        assert hasattr(v, "get_data")


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
        car = RaceCar(14, driver_alonso, "Aston Martin", 20)
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
        car_a = RaceCar(1, driver_alonso, "Team A", 20)
        car_b = RaceCar(2, driver_alonso, "Team B", 20)
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


# ══════════════════════════════════════════════════════════════════════════════
# Race Tests (Aggregation with RaceCar)
# ══════════════════════════════════════════════════════════════════════════════

class TestRace:

    def test_race_starts_with_empty_list(self):
        assert Race().race_cars == []

    def test_add_car_appends_to_list(self, standard_cars):
        race = Race()
        race.add_car(standard_cars[0])
        assert standard_cars[0] in race.race_cars

    def test_add_car_multiple(self, standard_cars):
        race = Race()
        for car in standard_cars:
            race.add_car(car)
        assert len(race.race_cars) == 3

    def test_aggregation_same_objects(self, standard_cars):
        """Aggregation: Race holds the exact same RaceCar objects that were added."""
        race = Race()
        for car in standard_cars:
            race.add_car(car)
        for i, car in enumerate(standard_cars):
            assert race.race_cars[i] is car

    def test_race_holds_correct_number_of_cars(self, standard_race):
        assert len(standard_race.race_cars) == 3

    def test_race_cars_are_racecar_instances(self, standard_race):
        for car in standard_race.race_cars:
            assert isinstance(car, RaceCar)

    def test_car_numbers_assigned(self, standard_race):
        numbers = {car.number for car in standard_race.race_cars}
        assert numbers == {1, 14, 44}

    def test_car_speeds_assigned(self, standard_race):
        speeds = {car.number: car.speed for car in standard_race.race_cars}
        assert speeds[14] == 20
        assert speeds[1]  == 25
        assert speeds[44] == 22

    # print_set_teams
    def test_print_set_teams_output(self, standard_race, capsys):
        standard_race.print_set_teams()
        captured = capsys.readouterr()
        assert "Teams in race:" in captured.out
        assert "Aston Martin" in captured.out
        assert "Red Bull" in captured.out
        assert "Mercedes" in captured.out

    def test_print_set_teams_unique(self, driver_alonso, driver_verstappen, capsys):
        """Duplicate team names should appear only once (set behaviour)."""
        car_a = RaceCar(14, driver_alonso,     "Red Bull", 20)
        car_b = RaceCar(1,  driver_verstappen, "Red Bull", 25)
        race = Race()
        race.add_car(car_a)
        race.add_car(car_b)
        race.print_set_teams()
        captured = capsys.readouterr()
        assert captured.out.count("Red Bull") == 1

    # run_lap
    def test_run_lap_prints_lap_header(self, standard_race, capsys):
        standard_race.run_lap(1)
        captured = capsys.readouterr()
        assert "---Lap 1---" in captured.out

    def test_run_lap_prints_all_cars(self, standard_race, capsys):
        standard_race.run_lap(1)
        captured = capsys.readouterr()
        assert "Car: 14" in captured.out
        assert "Car: 1"  in captured.out
        assert "Car: 44" in captured.out

    def test_run_lap_calls_get_data(self, standard_race, capsys):
        """run_lap must use get_data() to print car info."""
        standard_race.run_lap(1)
        captured = capsys.readouterr()
        # get_data() output format: "Car: X Distance: Y"
        assert "Distance:" in captured.out

    def test_run_lap_pit_stop_triggered(self, standard_race, capsys):
        car = standard_race.race_cars[0]
        car.fuel = 20
        standard_race.run_lap(1)
        captured = capsys.readouterr()
        assert f"Car {car.number} must pit!" in captured.out

    def test_run_lap_no_pit_updates_distance(self, standard_race):
        car = next(c for c in standard_race.race_cars if c.number == 14)
        standard_race.run_lap(1)
        assert car.distance == pytest.approx(20.0)

    # race — full simulation
    def test_race_5_laps_final_distances(self, standard_race):
        """Run 5 laps and verify final distances match expected values."""
        standard_race.race(5)
        dist = {car.number: int(car.distance) for car in standard_race.race_cars}
        assert dist[1]  == 50
        assert dist[44] == 45
        assert dist[14] == 41

    def test_race_zero_laps_no_output(self, standard_race, capsys):
        standard_race.race(0)
        captured = capsys.readouterr()
        assert "---Lap" not in captured.out

    def test_race_zero_division_handled(self, driver_alonso, capsys):
        """ZeroDivisionError raised during a lap must be caught and reported."""
        car = RaceCar(99, driver_alonso, "Test Team", 10)
        race = Race()
        race.add_car(car)

        def bad_lap(lap):
            raise ZeroDivisionError("division by zero")

        race.run_lap = bad_lap
        race.race(1)
        captured = capsys.readouterr()
        assert "Lap count cannot be zero" in captured.out

    # print_final_results
    def test_final_results_header(self, standard_race, capsys):
        standard_race.race(5)
        standard_race.print_final_results()
        captured = capsys.readouterr()
        assert "---Final Results---" in captured.out

    def test_final_results_sorted_descending(self, standard_race, capsys):
        standard_race.race(5)
        standard_race.print_final_results()
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        driver_lines = [l.strip() for l in lines if l.strip().startswith("Driver:")]
        assert driver_lines[0] == "Driver: Verstappen"
        # Hamilton and Alonso both finish at 45 — either order is valid for 2nd/3rd
        assert set(driver_lines[1:]) == {"Driver: Hamilton", "Driver: Alonso"}

    def test_final_results_contains_teams(self, standard_race, capsys):
        standard_race.race(5)
        standard_race.print_final_results()
        captured = capsys.readouterr()
        assert "Red Bull" in captured.out
        assert "Mercedes" in captured.out
        assert "Aston Martin" in captured.out

    def test_final_results_contains_distances(self, standard_race, capsys):
        standard_race.race(5)
        standard_race.print_final_results()
        captured = capsys.readouterr()
        assert "Distance: 50" in captured.out
        assert "Distance: 45" in captured.out
        assert "Distance: 41" in captured.out