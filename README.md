# MetabolicGearShift_inSilico

## Overview

This repository contains the computational model and *in silico* simulation code developed for the paper entitled "Cascading Metabolic Enhancement via Gear-Shifting Biological Systems: A Novel Approach to Sustainable Bacterial Hypermetabolism."

The work introduces a novel theoretical framework for achieving sustainable bacterial hypermetabolism through a dynamic, multi-gear metabolic control system. This repository houses the COBRApy code used to validate this framework, specifically utilizing the *E. coli* iML1515 genome-scale metabolic model. The simulations validate how the proposed 'gear-shifting' mechanism adaptively regulates metabolic flux, balancing high production demands with cellular sustainability by explicitly accounting for internal stress levels and nutrient availability.

## Key Features of This Simulation

* **Multi-Gear Metabolic States:** Simulates five distinct metabolic "gears" or operational modes, each characterized by specific glucose and oxygen uptake rates.
* **Stress-Responsive Adaptation:** Integrates a non-linear ATP maintenance cost and a piecewise, stress-dependent biomass growth penalty. These mechanisms mathematically represent the increasing physiological burden on the cell as metabolic intensity escalates.
* **Plasmid Burden Integration:** Accounts for the additional metabolic load imposed by synthetic genetic constructs, a critical consideration in engineered biological systems.
* **Validation of Sustainability:** *In silico* results demonstrate significant metabolic enhancement (e.g., up to 6.7x ATP production in Gear 5) while showing controlled growth decline or cessation at high stress levels, preventing catastrophic collapse and promoting long-term viability.

## Contents

* **`simulate.py`**: The main Python script that implements the metabolic gear-shifting model using COBRApy. It defines the gears, applies the stress functions, runs Flux Balance Analysis (FBA), and outputs the key metabolic metrics.
* **`requirements.txt`**: A list of all necessary Python dependencies required to run the simulation successfully.
* **`plots/`**: (Optional) This directory is intended for generated figures (`growth_vs_glucose.png`, `atp_vs_gear.png`, `fold_changes.png`) that visualize the simulation results. *Note: The current `simulate.py` version may require additional code to automatically generate and save plots to this directory.*
* **`data/`**: (Optional) This directory is intended for raw simulation output data (e.g., results tables saved as CSV files). *Note: The current `simulate.py` version may require additional code to save data to this directory.*
* **`LICENSE`**: The license file specifying the terms under which this project's code is distributed.
* **`.gitignore`**: Configures which files and directories Git should ignore (e.g., temporary files, environment folders).

## Installation

To set up the necessary environment and run the simulations locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Blaise-Maxwell/MetabolicGearShift_inSilico.git](https://github.com/Blaise-Maxwell/MetabolicGearShift_inSilico.git)
    cd MetabolicGearShift_inSilico
    ```
2.  **Create and activate a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows: .\venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```
3.  **Install dependencies:**
    Ensure you have Python (3.7+) installed. Then, install the required libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    *(If you haven't created a `requirements.txt` file yet, you can create one in the repository root with contents like:
    ```
    cobrapy
    pandas
    numpy
    # Add if you plan to generate plots:
    # matplotlib
    # seaborn
    ```
    )*
4.  **Download the `iML1515` model:**
    The simulation relies on the *E. coli* iML1515 genome-scale metabolic model. Please download the `.xml` or `.json` file for this model (e.g., from the [BiGG Models Database](http://bigg.ucsd.edu/models/iML1515)) and place it in the same working directory as `simulate.py`.

## Usage

Once the installation steps are complete, you can run the simulation from your terminal:

```bash
python simulate.py

Upon execution, the script will print an overall performance summary table to the console. If further functionality for saving plots or data files is implemented in simulate.py, they will be generated in the respective plots/ and data/ directories.

Citation

If you use this code or data in your academic or professional work, please cite the associated paper:

Britton, B.-M. F.-D. (2025). Cascading Metabolic Enhancement via Gear-Shifting Biological Systems: A Novel Approach to Sustainable Bacterial Hypermetabolism. bioRxiv. [DOI to be added upon publication]

License

This project is licensed under the MIT License. Please see the LICENSE file in the repository root for full details.

Contact

For any questions, feedback, or collaborations, please feel free to reach out:

Blaise-Maxwell F.-D. Britton
blamaxbritton@gmail.com
