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
    # Each RaceCar creates its own Engine internally (composition).
   

    # Create a Race and add each car via add_car() (aggregation)
   