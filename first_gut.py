import numpy as np
import hashlib

# Computational Gut Decision System
# Models energy dynamics with entropy, uses optimal control simulation, and outputs Yes/No.

def simulate_decision(initial_energy, cost_frac, benefit_frac, risk_frac, horizon, scenarios=1000):
    """
    Simulate the outcomes of taking action (YES) vs not taking action (NO) over a given time horizon.
    Returns a tuple of (survival_yes, survival_no, avg_yes, avg_no) which summarize the results.
    """
    # Calculate immediate cost and adjusted decay rate based on benefit
    cost = initial_energy * cost_frac                     # resource cost if action is taken
    base_decay = 0.05                                     # baseline fractional energy decay per time step (5% of current energy)
    effective_decay = max(0.0, base_decay * (1 - benefit_frac))  # reduced decay if action taken (benefit_frac% reduction)

    # Set up random influences (entropy/noise) for the simulation
    # Random fluctuation per step ~ Normal(0, sigma), where sigma scales with risk and initial energy.
    rand_std = 0.1 * initial_energy * risk_frac           # volatility of environment (10% of initial_energy if risk_frac=1)
    rand_mean = 0.0                                       # zero mean for unbiased random fluctuations

    # Use a fixed seed derived from scenario parameters for reproducibility (same "quantum roll" for given inputs)
    seed_key = f"{initial_energy}-{cost_frac}-{benefit_frac}-{risk_frac}-{horizon}"
    seed = int(hashlib.sha256(seed_key.encode()).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    # Pre-generate random effects for all scenarios and time steps
    random_matrix = np.random.normal(loc=rand_mean, scale=rand_std, size=(scenarios, horizon))

    def run_scenarios(decision):
        """Run the simulation for either taking the action (decision=True) or not (False)."""
        E = np.full(scenarios, initial_energy, dtype=float)  # energy levels for each scenario
        alive = np.ones(scenarios, dtype=bool)               # track which scenarios are still "alive" (energy > 0)

        # Apply initial decision effects
        decay_rate = base_decay
        if decision:  # action taken (YES)
            E -= cost                            # immediate cost reduces energy
            # Any scenario that loses all energy or more is considered dead
            dead_now = E <= 0
            if np.any(dead_now):
                alive[dead_now] = False
                E[dead_now] = 0.0
            decay_rate = effective_decay         # use reduced decay rate due to long-term benefit of action

        # Simulate each time step
        for t in range(horizon):
            if not np.any(alive):
                break  # no scenarios left alive, end simulation early
            # Decay step: alive scenarios lose a fraction of their energy
            E[alive] *= (1 - decay_rate)
            # Random fluctuation step: add environmental random effect
            if rand_std > 0:
                E[alive] += random_matrix[alive, t]
            # Check for any scenarios that died (energy <= 0) this step
            newly_dead = (E <= 0) & alive
            if np.any(newly_dead):
                alive[newly_dead] = False
                E[newly_dead] = 0.0  # clamp energy at 0 for dead scenarios

        # Calculate outcome metrics
        survival_rate = np.mean(E > 0)            # fraction of scenarios that ended with energy > 0
        avg_final_energy = np.mean(E)             # average final energy across all scenarios
        return survival_rate, avg_final_energy

    # Run simulation for both decisions
    surv_yes, avg_yes = run_scenarios(decision=True)   # outcomes if action is taken
    surv_no, avg_no   = run_scenarios(decision=False)  # outcomes if action is not taken

    return surv_yes, surv_no, avg_yes, avg_no

# Main interactive loop to query the computational gut
print("Welcome to the Computational Gut Decision System. Ask a yes/no question and provide context.")
while True:
    # Get the user's yes/no question or exit command
    query = input("\nEnter your decision question (or type 'quit' to exit): ")
    if query.strip().lower() in {"quit", "exit"}:
        print("Goodbye!")
        break

    # Ask for scenario parameters (cost, benefit, risk, horizon)
    try:
        cost_frac = float(input("On a scale of 0 to 1, how costly is the action in terms of resources? "))
        benefit_frac = float(input("On a scale of 0 to 1, how much long-term benefit do you expect from the action? "))
        risk_frac = float(input("On a scale of 0 to 1, how volatile/uncertain is the environment? "))
        horizon = int(input("How far into the future (in time steps) should the model consider (e.g., 50)? "))
    except ValueError:
        print("Invalid input. Please enter numeric values for the parameters.")
        continue

    # Run the integrated simulation model
    initial_energy = 100.0  # assume an initial resource level of 100 units
    surv_yes, surv_no, avg_yes, avg_no = simulate_decision(initial_energy, cost_frac, benefit_frac, risk_frac, horizon)

    # Decide based on outcomes: prioritize survival (sustainability), then average energy
    decision = None
    # If one choice clearly yields higher survival, favor that
    if surv_yes - surv_no > 0.01:      # Yes yields higher survival rate by more than 1%
        decision = "YES"
    elif surv_no - surv_yes > 0.01:    # No yields higher survival significantly
        decision = "NO"
    else:
        # Survival rates are similar, use average energy as tiebreaker
        decision = "YES" if avg_yes >= avg_no else "NO"

    # Output the gut decision
    print(f"Gut Decision: {decision}")
