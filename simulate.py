# simulate.py: COBRApy simulation for gear-shifting metabolic enhancement
import cobra
from cobra.io import load_model
import pandas as pd
import numpy as np

# Load iML1515 model
print("Loading the E. coli iML1515 model...")
model = load_model("iML1515")
print("Model loaded successfully.")

# Stress function: Non-linear ATP cost
def calculate_stress_cost(glucose_uptake):
    base_stress = abs(glucose_uptake) * 0.02
    return min(base_stress ** 1.8, 200.0)

# Stress penalty for biomass: Piecewise function
def calculate_stress_penalty(glucose_uptake):
    glucose = abs(glucose_uptake)
    if glucose <= 30.0:  # Gears 1–2
        penalty = np.exp(glucose / 35) / 20  # Divisor for Gear 2
    elif glucose <= 80.0:  # Gear 3
        penalty = np.exp(glucose / 25) / 15  # Divisor for Gear 3
    else:  # Gears 4–5
        penalty = np.exp(glucose / 40) / 10
    return min(penalty, 0.95)

# Define parameters for each gear
gears = [
    {"name": "Gear 1", "glucose": -10.0, "oxygen": -18.0, "burden": 0.0},
    {"name": "Gear 2", "glucose": -30.0, "oxygen": -30.0, "burden": 0.05},
    {"name": "Gear 3", "glucose": -80.0, "oxygen": -60.0, "burden": 0.12},
    {"name": "Gear 4", "glucose": -150.0, "oxygen": -100.0, "burden": 0.18},
    {"name": "Gear 5", "glucose": -250.0, "oxygen": -150.0, "burden": 0.25}
]

# Store results
results = []

# Simulate each gear
for gear in gears:
    print(f"\n--- Simulating {gear['name']} ---")
    
    # Set glucose and oxygen uptake
    model.reactions.EX_glc__D_e.lower_bound = gear["glucose"]
    model.reactions.EX_o2_e.lower_bound = gear["oxygen"]
    
    # Apply plasmid burden and stress penalty
    base_biomass = model.reactions.BIOMASS_Ec_iML1515_core_75p37M.upper_bound
    stress_penalty = calculate_stress_penalty(gear["glucose"])
    biomass_bound = base_biomass * max(0.001, 1 - gear["burden"] - stress_penalty)
    model.reactions.BIOMASS_Ec_iML1515_core_75p37M.upper_bound = biomass_bound
    
    # Apply non-linear ATP maintenance cost
    model.reactions.ATPM.lower_bound = 35.0 + calculate_stress_cost(gear["glucose"])
    
    # Allow fermentation production
    model.reactions.EX_lac__D_e.lower_bound = 0.0
    model.reactions.EX_lac__D_e.upper_bound = 1000.0
    model.reactions.EX_etoh_e.lower_bound = 0.0
    model.reactions.EX_etoh_e.upper_bound = 1000.0
    
    # Optimize
    solution = model.optimize()
    
    # Store key metrics
    growth = solution.objective_value
    atp = solution.fluxes.get("ATPS4rpp", 0.0)
    glucose = solution.fluxes.get("EX_glc__D_e", 0.0)
    lactate = solution.fluxes.get("EX_lac__D_e", 0.0)
    ethanol = solution.fluxes.get("EX_etoh_e", 0.0)
    
    results.append({
        "Gear": gear["name"],
        "Growth Rate (h⁻¹)": round(growth, 2) if growth else 0.0,
        "ATP Production (mmol/gDW/h)": round(atp, 2) if atp else 0.0,
        "Glucose Uptake (mmol/gDW/h)": round(glucose, 2),
        "Lactate Production (mmol/gDW/h)": round(lactate, 2),
        "Ethanol Production (mmol/gDW/h)": round(ethanol, 2)
    })

# Print results table
print("\n--- Overall Performance Summary ---")
df = pd.DataFrame(results)
print(df.to_string(index=False))

# Calculate fold improvements
gear1 = results[0]
for gear in results[1:]:
    glucose_fold = abs(gear["Glucose Uptake (mmol/gDW/h)"]) / abs(gear1["Glucose Uptake (mmol/gDW/h)"])
    atp_fold = gear["ATP Production (mmol/gDW/h)"] / gear1["ATP Production (mmol/gDW/h)"]
    growth_fold = gear["Growth Rate (h⁻¹)"] / gear1["Growth Rate (h⁻¹)"]
    print(f"\n{gear['Gear']} Enhancements:")
    print(f"Glucose uptake: {glucose_fold:.1f}x")
    print(f"ATP production: {atp_fold:.1f}x")
    print(f"Growth rate: {growth_fold:.1f}x")
# Add this after the fold improvements calculation in your script
import matplotlib.pyplot as plt

# Extract data for plotting
gears = [result["Gear"] for result in results]
glucose_uptake = [-result["Glucose Uptake (mmol/gDW/h)"] for result in results]
growth_rates = [result["Growth Rate (h⁻¹)"] for result in results]
atp_production = [result["ATP Production (mmol/gDW/h)"] for result in results]
lactate_production = [result["Lactate Production (mmol/gDW/h)"] for result in results]
ethanol_production = [result["Ethanol Production (mmol/gDW/h)"] for result in results]

# Calculate fold changes relative to Gear 1
gear1 = results[0]
glucose_folds = [abs(result["Glucose Uptake (mmol/gDW/h)"]) / abs(gear1["Glucose Uptake (mmol/gDW/h)"]) for result in results]
atp_folds = [result["ATP Production (mmol/gDW/h)"] / gear1["ATP Production (mmol/gDW/h)"] for result in results]
growth_folds = [result["Growth Rate (h⁻¹)"] / gear1["Growth Rate (h⁻¹)"] if result["Growth Rate (h⁻¹)"] > 0 else 0.0 for result in results]

# Plot 1: Growth Rate vs. Glucose Uptake
plt.figure(figsize=(10, 6))
plt.plot(glucose_uptake, growth_rates, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
plt.xlabel("Glucose Uptake (mmol/gDW/h)", fontsize=12)
plt.ylabel("Growth Rate (h⁻¹)", fontsize=12)
plt.title("Growth Rate vs. Glucose Uptake in Gear-Shifting Model", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
for i, gear in enumerate(gears):
    plt.annotate(gear, (glucose_uptake[i], growth_rates[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig("growth_vs_glucose.png", dpi=300)
plt.close()

# Plot 2: ATP Production vs. Gear
plt.figure(figsize=(10, 6))
plt.bar(gears, atp_production, color='g', alpha=0.8)
plt.xlabel("Gear", fontsize=12)
plt.ylabel("ATP Production (mmol/gDW/h)", fontsize=12)
plt.title("ATP Production Across Metabolic Gears", fontsize=14)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
for i, atp in enumerate(atp_production):
    plt.text(i, atp + 5, f"{atp:.2f}", ha='center', fontsize=10)
plt.tight_layout()
plt.savefig("atp_vs_gear.png", dpi=300)
plt.close()

# Plot 3: Fold Changes vs. Gear
plt.figure(figsize=(10, 6))
bar_width = 0.25
x = np.arange(len(gears))
plt.bar(x - bar_width, glucose_folds, bar_width, label="Glucose Uptake", color='b', alpha=0.8)
plt.bar(x, atp_folds, bar_width, label="ATP Production", color='g', alpha=0.8)
plt.bar(x + bar_width, growth_folds, bar_width, label="Growth Rate", color='r', alpha=0.8)
plt.xlabel("Gear", fontsize=12)
plt.ylabel("Fold Change (Relative to Gear 1)", fontsize=12)
plt.title("Fold Changes in Glucose Uptake, ATP Production, and Growth Rate", fontsize=14)
plt.xticks(x, gears)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("fold_changes.png", dpi=300)
plt.close()
