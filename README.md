# 🏎️ F1 Race Simulation — Object-Oriented Programming Lab

## Introduction

In this lab, you will re-implement the F1 Race Simulation you completed earlier this semester — but this time using **Object-Oriented Programming (OOP)** principles. By rebuilding the same simulation with classes and objects, you will be able to directly compare the procedural and OOP approaches and appreciate the benefits of encapsulation, inheritance, composition, and aggregation.

In this lab you will practice:

- Defining and instantiating **classes and objects**
- Using **encapsulation** to bundle data and behavior
- Applying **inheritance** to share behavior across related classes
- Using **composition** to model "owns-a" relationships (RaceCar owns an Engine)
- Using **aggregation** to model "uses-a" relationships (Race uses RaceCars; RaceTeam uses Drivers)
- Writing custom data-display methods on your classes

> The winner of the race is still the car that travels the farthest distance over the course of the race!

---
## Setup

1. Create a conda environment by running these two commands:
   ```
   conda create --name oop_f1 python=3.13.1
   conda activate oop_f1
   ```
2. Download this project and open it in VS Code.
3. Switch to the `oop_f1` environment in VS Code.
4. Complete the lab in the file `f1_race.py`.
5. Push your code to your repo to submit.
---

## Class Design

You will implement **five classes**. Study the relationship diagram below before you begin coding.

```
Vehicle  (Base Class)
└── RaceCar  (Inherits from Vehicle)
      │
      ├── Engine      [COMPOSITION]  — RaceCar creates and owns its Engine
      └── Driver      [AGGREGATION]  — Driver is passed in from outside

RaceTeam              [AGGREGATION]  — RaceTeam holds references to Driver objects
Race                  [AGGREGATION]  — Race holds references to RaceCar objects
```
### Composition vs. Aggregation — Key Distinction

| Relationship | Meaning | Example in this lab |
|---|---|---|
| **Composition** | The child object is *created inside* the parent and cannot exist independently. If the parent is destroyed, so is the child. | `Engine` is created inside `RaceCar.__init__()` — no car, no engine. |
| **Aggregation** | The child object is *created outside* the parent and passed in. It can exist independently and could be shared or reassigned. | `Driver` objects are created in `main` and passed into `RaceCar`. A driver could exist without being in a car. `RaceCar` objects are created in `main` and passed into `Race`. |

---
## Note
-If an attribute does not have a defined default value, you must take that value in as a parameter in init. 

## Part 1 — `Engine`

Create a class called `Engine`. `RaceCar` will create an `Engine` internally — this is **composition**.

### Attributes (set in `__init__`)
| Attribute | Type | Description |
|---|---|---|
| `horsepower` | `int` | The engine's power output |
| `engine_type` | `str` | The type of engine (e.g., `"V6 Hybrid"`) |
| `is_running` | `bool` | Whether the engine is currently on (default: `False`) |

### Methods
| Method | Returns | Description |
|---|---|---|
| `start()` | `None` | Sets `is_running` to `True` |
| `stop()` | `None` | Sets `is_running` to `False` |
| `get_data()` | `str` | Returns a string in this format: `"Engine: {engine_type} \| HP: {horsepower} \| Status: {Running or Off}"` |

> **Example:** `Engine("V6 Hybrid", 800).get_data()` → `"Engine: V6 Hybrid | HP: 800 | Status: Off"`

---

## Part 2 — `Vehicle` (Base Class)

Create a base class called `Vehicle` with the following:

### Attributes (set in `__init__`)
| Attribute | Type | Description |
|---|---|---|
| `speed` | `int` | The vehicle's speed |
| `fuel` | `int` | The current fuel level (default: `100`) |

### Methods
| Method | Returns | Description |
|---|---|---|
| `refuel(amount)` | `None` | Adds `amount` to `self.fuel` |
| `get_data()` | `str` | Returns `"Vehicle with speed {speed} and fuel {fuel}"` |

---

## Part 3 — `Driver`

Create a class `Driver` with the following:

### Attributes (set in `__init__`)
| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | The driver's name |

### Methods
| Method | Returns | Description |
|---|---|---|
| `get_driver_data()` | `str` | Returns `"Driver: {name}"` |

---

## Part 4 — `RaceCar` (Inherits from `Vehicle`)

Create a class `RaceCar` that **inherits** from `Vehicle`.

`RaceCar` demonstrates **both** relationships:
- **Composition** with `Engine` — the car creates its own engine inside `__init__`
- **Aggregation** with `Driver` — the driver is created outside and passed in

### Additional Attributes
| Attribute | Type | Description |
|---|---|---|
| `number` | `int` | The car's race number |
| `driver` | `Driver` | The `Driver` object assigned to this car (passed in — aggregation) |
| `team_name` | `str` | The name of the team |
| `distance` | `float` | Total distance traveled (starts at `0`) |
| `engine` | `Engine` | An `Engine` object created inside `__init__` (composition) |

> Consider first creating the RaceCar class first. Then think about how to model inheritance, then how to model the engine with comoposition. 

### Methods
| Method | Returns | Description |
|---|---|---|
| `needs_pit_stop()` | `bool` | Returns `True` if `self.fuel <= 25`, otherwise `False` |
| `pit_stop()` | `None` | Prints `Car {number} must pit!` and resets `self.fuel` to `100` |
| `drive(lap)` | `None` | Adds `self.speed / lap` to `self.distance`; subtracts `self.speed + lap` from `self.fuel` |
| `get_data()` | `str` | Returns `"Car: {number} Distance: {distance}"` where distance is shown as an **integer** (use `int()`) |

---

## Part 5 — `RaceTeam`

Create a class `RaceTeam` that uses **aggregation** — it holds references to `Driver` objects that are created outside the team and passed in.

### Attributes (set in `__init__`)
| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | The team name |
| `drivers` | `list` | A list of `Driver` objects (starts empty) |

### Methods
| Method | Returns | Description |
|---|---|---|
| `add_driver(driver)` | `None` | Appends a `Driver` object to `self.drivers` |
| `get_team_data()` | `str` | Returns `"Team: {name} Drivers: {comma-separated driver names}"` |

> **Aggregation note:** `Driver` objects must be created *outside* of `RaceTeam` and passed into `add_driver()`. The same `Driver` object could be referenced elsewhere (e.g., also assigned to a `RaceCar`).

---

## Part 6 — `Race`

Create a class `Race` that uses **aggregation** — it receives already-created `RaceCar` objects and stores references to them.

> **Aggregation note:** `RaceCar` objects must be created *outside* of `Race` and added via `add_car()`. A `RaceCar` can exist independently of any `Race`.

### Attributes (set in `__init__`)
| Attribute | Type | Description |
|---|---|---|
| `race_cars` | `list` | A list of `RaceCar` objects (starts empty) |

### Methods
| Method | Returns | Description |
|---|---|---|
| `add_car(race_car)` | `None` | Appends an existing `RaceCar` object to `self.race_cars` |
| `print_set_teams()` | `None` | Prints a set of all unique team names in the race in this format: `Teams in race: {'Aston Martin', 'Mercedes', 'Red Bull'}` |
| `run_lap(lap)` | `None` | Prints `---Lap {lap}---`, then for each car: calls `pit_stop()` if `needs_pit_stop()` is `True`, otherwise calls `drive(lap)`, then prints the car's info using `get_data()` |
| `race(laps)` | `None` | Loops from lap `1` through `laps` (inclusive) calling `run_lap(lap)` each iteration. Wraps the loop in a `try/except` catching `ZeroDivisionError` as `e` and prints: `{e} - Lap count cannot be zero` |
| `print_final_results()` | `None` | Sorts cars by distance (greatest first) and prints each car's driver, team, and distance (see format below) |

**`print_final_results()` output format:**
```
---Final Results---
Driver: Verstappen
	 Team: Red Bull 
	 Distance: 50
Driver: Hamilton
	 Team: Mercedes 
	 Distance: 45
Driver: Alonso
	 Team: Aston Martin 
	 Distance: 41
```
> **Format note:** Each line after `Driver:` is indented with a **tab** (`\t`) followed by a space.

---

## Part 7 — `if __name__ == "__main__":`

Complete the main block at the bottom of your file:

1. Create the following `Driver` objects independently:

| Variable | Name |
|---|---|
| `alonso` | `"Alonso"` |
| `verstappen` | `"Verstappen"` |
| `hamilton` | `"Hamilton"` |

2. Create the following `RaceCar` objects independently, passing in the driver objects (aggregation). Each car creates its own `Engine` internally (composition):

| Variable | Number | Driver | Team | Speed | HP | Engine Type |
|---|---|---|---|---|---|---|
| `car_14` | 14 | alonso | Aston Martin | 20 | 750 | V6 Hybrid |
| `car_1` | 1 | verstappen | Red Bull | 25 | 820 | V6 Hybrid |
| `car_44` | 44 | hamilton | Mercedes | 22 | 800 | V6 Hybrid |

3. Create a `Race` object by passing in the list of cars (aggregation):
   ```python
   f1_race = Race([car_14, car_1, car_44])
   ```

4. Ask the user to input the number of laps.

5. Call `print_set_teams()`, `race(laps)`, and `print_final_results()`.

> ⚠️ **Do not remove** `if __name__ == "__main__":` from your submission.

---

## Expected Output (5 Laps)

```
Teams in race: {'Aston Martin', 'Mercedes', 'Red Bull'}
---Lap 1---
Car: 14 Distance: 20
Car: 1 Distance: 25
Car: 44 Distance: 22
---Lap 2---
Car: 14 Distance: 30
Car: 1 Distance: 37
Car: 44 Distance: 33
---Lap 3---
Car: 14 Distance: 36
Car: 1 Distance: 45
Car: 44 Distance: 40
---Lap 4---
Car: 14 Distance: 41
Car 1 must pit!
Car: 1 Distance: 45
Car: 44 Distance: 45
---Lap 5---
Car 14 must pit!
Car: 14 Distance: 41
Car: 1 Distance: 50
Car 44 must pit!
Car: 44 Distance: 45
---Final Results---
Driver: Verstappen
	 Team: Red Bull 
	 Distance: 50
Driver: Hamilton
	 Team: Mercedes 
	 Distance: 45
Driver: Alonso
	 Team: Aston Martin 
	 Distance: 41
```

> **Note:** The order of team names in the set may differ — sets are unordered.

---
## Testing Your Code
1. To run the unit tests, in the terminal run the following: ```pytest```
2. If pytest is not found, run this first: ```conda install pytest```
   

## Other
1. This is a collaborative lab.
2. The AI Usage Policy as outlined in the syllabus applies to this lab.
