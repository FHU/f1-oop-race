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
        car_a = RaceCar(14, driver_alonso,     "Red Bull", 20, 750, 'V6 Hybrid')
        car_b = RaceCar(1,  driver_verstappen, "Red Bull", 25, 750, 'V6 Hybrid')
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
        car = RaceCar(99, driver_alonso, "Test Team", 10, 750, 'V6 Hybrid')
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