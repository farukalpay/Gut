import numpy as np
import hashlib
import time

def simulate_decision(initial_energy, cost_frac, benefit_frac, risk_frac, horizon, scenarios=1000):
    """
    Simulate the outcomes of taking action (YES) vs not taking action (NO) over a given time horizon.
    Returns a tuple of (survival_yes, survival_no, avg_yes, avg_no) which summarize the results.
    """
    cost = initial_energy * cost_frac                     # resource cost if action is taken
    base_decay = 0.05                                     # baseline fractional energy decay per time step (5%)
    effective_decay = max(0.0, base_decay * (1 - benefit_frac))  # reduced decay if action taken

    rand_std = 0.1 * initial_energy * risk_frac           # volatility of environment (10% of initial_energy if risk_frac=1)
    rand_mean = 0.0

    # Use a fixed seed derived from scenario parameters for reproducibility
    seed_key = f"{initial_energy}-{cost_frac}-{benefit_frac}-{risk_frac}-{horizon}"
    seed = int(hashlib.sha256(seed_key.encode()).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    random_matrix = np.random.normal(loc=rand_mean, scale=rand_std, size=(scenarios, horizon))

    def run_scenarios(decision):
        E = np.full(scenarios, initial_energy, dtype=float)
        alive = np.ones(scenarios, dtype=bool)

        # Apply initial decision effects
        decay_rate = base_decay
        if decision:  # action taken (YES)
            E -= cost
            dead_now = E <= 0
            if np.any(dead_now):
                alive[dead_now] = False
                E[dead_now] = 0.0
            decay_rate = effective_decay

        for t in range(horizon):
            if not np.any(alive):
                break  # all scenarios dead
            E[alive] *= (1 - decay_rate)
            if rand_std > 0:
                E[alive] += random_matrix[alive, t]
            newly_dead = (E <= 0) & alive
            if np.any(newly_dead):
                alive[newly_dead] = False
                E[newly_dead] = 0.0

        survival_rate = np.mean(E > 0)
        avg_final_energy = np.mean(E)
        return survival_rate, avg_final_energy

    # Run simulation for both taking the action (YES) and not taking the action (NO)
    surv_yes, avg_yes = run_scenarios(decision=True)
    surv_no, avg_no   = run_scenarios(decision=False)

    return surv_yes, surv_no, avg_yes, avg_no


def play_game():
    """
    A text-based “game” version of the computational gut decision system.
    """
    print("Welcome, traveler, to the Land of Algoria!")
    print("Here, every important choice could impact your survival and resources.\n")

    # Game-like intro story
    time.sleep(1)
    print("You stand at the gates of an ancient city. A mysterious Oracle stands before you,")
    print("offering guidance on a pressing yes/no question of your choice.\n")

    time.sleep(2)
    print("You begin the Oracle’s ritual...\n")

    while True:
        # Ask the user for their yes/no question or exit
        query = input("\nEnter your pressing question for the Oracle (or type 'quit' to exit): ")
        if query.strip().lower() in {"quit", "exit"}:
            print("\nThe Oracle nods silently. You step away, feeling the weight of unanswered riddles.")
            print("Farewell, brave traveler!\n")
            break

        # Story prompt
        print(f"\nThe Oracle tilts their head, intrigued by your question: \"{query}\"")
        print("To peer deeper into the possible futures, you must provide certain parameters...\n")
        
        try:
            cost_frac = float(input("1) The resource cost of your proposed action (0 to 1)? "))
            benefit_frac = float(input("2) The long-term benefit you believe it might bring (0 to 1)? "))
            risk_frac = float(input("3) The volatility or uncertainty of your world (0 to 1)? "))
            horizon = int(input("4) How many steps into the future shall the Oracle foresee (e.g. 50)? "))
        except ValueError:
            print("\nThe Oracle frowns. Your answers must be numeric. Please try again.")
            continue

        print("\nPeering through the swirling mists of time...")
        time.sleep(2)
        
        # Run the integrated simulation model
        initial_energy = 100.0
        surv_yes, surv_no, avg_yes, avg_no = simulate_decision(
            initial_energy, cost_frac, benefit_frac, risk_frac, horizon
        )

        # The Oracle's logic: 
        decision = None
        if surv_yes - surv_no > 0.01:
            decision = "YES"
        elif surv_no - surv_yes > 0.01:
            decision = "NO"
        else:
            decision = "YES" if avg_yes >= avg_no else "NO"

        # Build a little results summary
        print("The Oracle’s crystal reveals the following glimpses of the future:\n")
        print(f"  Survival rate if you proceed (YES): {surv_yes*100:.2f}%")
        print(f"  Average ending energy if you proceed (YES): {avg_yes:.2f}")
        print(f"  Survival rate if you decline (NO):  {surv_no*100:.2f}%")
        print(f"  Average ending energy if you decline (NO):  {avg_no:.2f}")

        time.sleep(2)
        # Output the Oracle's final recommendation
        print("\n*** The Oracle's Divine Pronouncement ***")
        print(f"The ritual indicates you should choose: {decision}\n")

        # Optional dramatic pause
        time.sleep(1)
        print("You feel the weight of possibility. The path is now clearer...\n")
        print("-" * 50)


if __name__ == "__main__":
    play_game()
