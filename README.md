# The Computational Gut: [First Version](https://blog.wasda.ai/post.html?id=wasd-ai-pursuit-algorithm-2025)

We present our initial experiment in creating a **Computational Gut**—a decision-making program that simulates human-like “gut feelings” by blending:
- **Biological & Entropy Modeling**  
- **Stochastic & Emergent Complexity**  
- **Optimal Control (HJB/Pontryagin)**  
- **Quantum-Like Uncertainty**  

The result is a simple, easy-to-run Python script that provides a \`YES\` or \`NO\` recommendation based on user input about costs, benefits, risk, and time horizon.

---

## 1. Why a Computational Gut?

In many decisions, humans rely on an intuitive sense—often called a “gut feeling.” We aim to replicate that using mathematical tools:

- **Biological/Energy Dynamics:** We treat “resources” as a numeric quantity that ages and decays over time, subject to random shocks (like entropic forces).
- **Optimal Control:** We simulate how an action (say, investing in a project) vs. inaction plays out over a time horizon, balancing present costs against future benefits.
- **Emergent Complexity:** We run many micro-simulations, letting patterns emerge from random fluctuations—akin to quantum superpositions collapsing into a final yes/no choice.
- **Yes/No Output:** We keep it simple: the code prints a single answer—like a gut instinct—built on complex internal reasoning.

---

## 2. What's in This Repository?

1. **\`first_gut.py\`**: The primary Python script.  
2. **Example Scenarios**: Use cases showing how to query the gut with cost, benefit, risk, and horizon.  

---

## 3. How It Works (Short Explanation)

1. **Resource & Decay**: We assume you start with 100 units of resources. Each time step, a baseline decay (e.g. 5%) reduces available resources, modeling how things naturally degrade or become more chaotic over time (aging, energy usage, etc.).  
2. **Volatility/Uncertainty**: Random fluctuations add unpredictability. A higher “risk” parameter means bigger positive or negative hits each step.  
3. **Decision Impact**: If we say “YES” to a decision:
    - We pay an immediate “cost” fraction of our resources.
    - We reduce our future decay by a “benefit” fraction, hopefully saving us resources in the long run.
4. **Monte Carlo Simulation**: The script simulates many random futures under two paths: “YES” vs. “NO,” compares survival rates and average final resources, then picks whichever path typically leads to better outcomes.  
5. **Result**: It prints “YES” if the action is beneficial in most random scenarios and yields better final states, or “NO” if it performs worse.

---

## 4. Usage

1. **Install Python** (3.7+ recommended).
2. **Clone or Download** this repository.
3. **Open a Terminal** in the project directory.
4. **Run**:
   ```bash
   python first_gut.py
