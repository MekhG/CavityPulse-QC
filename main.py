"""
main.py

Execution pipeline for CavityPulse-QC, mirroring the qubit-based
PulseForge-QC pipeline step for step:

  1. baseline pulse simulation (noisy),
  2. pulse amplitude optimization,
  3. optimized pulse re-simulation (noisy, with full state tracking),
  4. quadrature-dynamics visualization (saved to results/),
  5. ideal closed-system reference (ideal, decoherence-free comparison).
"""

import os
import numpy as np

from config import system_config as config
from simulation.pulse_simulator import run_simulation
from optimization.optimize_pulse import optimize_pulse_amplitude
from visualization.quadrature_visualization import plot_quadrature_dynamics
from reference_layer.closed_system_reference import run_ideal_reference


def main():
    print("=" * 34)
    print(" CAVITY-MODE QUANTUM CONTROL SIMULATION")
    print("=" * 34)
    print()

    # --- 1. Baseline (un-optimized) noisy simulation ---
    baseline_fidelity, _ = run_simulation(
        config.INITIAL_AMPLITUDE, config, return_states=False
    )
    print(f"Baseline fidelity: {baseline_fidelity:.6f}")
    print()

    # --- 2. Optimize pulse amplitude ---
    optimal_amplitude, optimal_fidelity = optimize_pulse_amplitude(config)
    print("Optimization Results")
    print("-" * 24)
    print(f"Optimal amplitude: {optimal_amplitude:.6f}")
    print(f"Optimal fidelity: {optimal_fidelity:.6f}")
    print()

    # --- 3. Optimized pulse re-simulation with full state tracking ---
    _, optimized_result = run_simulation(
        optimal_amplitude, config, return_states=True
    )
    tlist = np.linspace(0, config.PULSE_DURATION, config.N_TIME_POINTS)

    # --- 4. Quadrature-dynamics visualization ---
    os.makedirs("results", exist_ok=True)
    save_path = os.path.join("results", "quadrature_dynamics.png")
    plot_quadrature_dynamics(optimized_result, tlist, save_path)
    print(f"Quadrature dynamics plot saved to: {save_path}")
    print()

    # --- 5. Ideal closed-system (decoherence-free) reference ---
    ideal_fidelity = run_ideal_reference(optimal_amplitude, config)
    print("Ideal Closed-System Reference")
    print("-" * 24)
    print(f"Ideal fidelity (no decoherence, same pulse): {ideal_fidelity:.6f}")
    print(
        f"Fidelity gap attributable to decoherence: "
        f"{ideal_fidelity - optimal_fidelity:.6f}"
    )


if __name__ == "__main__":
    main()
