# ─────────────────────────────────────────────
# Engine  (owned by RaceCar — Composition)
# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
# Vehicle Base Class
# ─────────────────────────────────────────────



# ─────────────────────────────────────────────
# RaceCar (inherits Vehicle, owns Engine — Composition)
# ─────────────────────────────────────────────



# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────




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


    # Demonstrate __gt__ and __lt__ before the race
 

    # Create a Race and add each car via add_car() (aggregation)

    #Take in number of laps from the user
    laps = int(input("Enter the number of laps: "))

    #Print the set of teams
    #Call the race() method
    #Print the final results of the race


