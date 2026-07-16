# CavityPulse-QC

### Pulse-Level Quantum Control and Optimization of a Noisy, Driven Cavity Mode

CavityPulse-QC is a compact simulation framework for modeling, optimizing, and visualizing microwave/optical-driven **bosonic mode** dynamics under photon loss and dephasing. 

---

## Table of Contents

- [Motivation](#motivation)
- [Physics Background](#physics-background)
  - [Driven Bosonic Mode Dynamics](#driven-bosonic-mode-dynamics)
  - [Gaussian Pulse Engineering](#gaussian-pulse-engineering)
  - [Open Quantum Systems](#open-quantum-systems)
  - [Photon Loss and Dephasing](#photon-loss-and-dephasing)
  - [Fidelity](#fidelity)
  - [Phase-Space Observables](#phase-space-observables)
- [Features](#features)
- [Software Stack](#software-stack)
- [Project Structure](#project-structure)
- [Module Breakdown](#module-breakdown)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Results and Physical Interpretation](#results-and-physical-interpretation)
- [Critical Assessment](#critical-assessment)
- [Future Extensions](#future-extensions)
- [Requirements](#requirements)
- [Relationship to PulseForge-QC](#relationship-to-pulseforge-qc)

---

## Motivation

A microwave cavity or optical resonator mode is not controlled by an abstract "photon number gate." Physically, population is built up (or removed) by sending a shaped drive tone into the mode, where the drive's **amplitude**, **duration**, and **shape** jointly determine the resulting quantum state.

This turns "prepare a single photon" into a genuine control-engineering problem:

- The drive must build up population in the target Fock state,
- Photon loss and dephasing act continuously throughout the drive, not just afterward,
- This project's results reveal: the *type* of drive itself imposes a hard structural limit on what's reachable, independent of how well any single parameter is tuned.

CavityPulse-QC simulates exactly that workflow computationally, using the same five-stage pipeline as the qubit-based PulseForge-QC project, applied to a different Hilbert space.

---

## Physics Background

### Driven Bosonic Mode Dynamics

A driven single bosonic mode evolves under the Schrödinger equation:

$$i\frac{d}{dt}|\psi(t)\rangle = H(t)|\psi(t)\rangle$$

In the frame rotating at the drive frequency, the Hamiltonian used in this project is:

$$H(t) = \Delta\, a^\dagger a + \frac{\Omega(t)}{2}(a + a^\dagger)$$

where $\Delta = \omega_{\text{cavity}} - \omega_{\text{drive}}$ is the detuning, $a, a^\dagger$ are bosonic ladder operators on a Fock space truncated to `N_LEVELS` levels, and $\Omega(t)$ is the drive envelope.

The current configuration sets $\omega_{\text{cavity}} = \omega_{\text{drive}}$, so $\Delta = 0$. As in PulseForge-QC, this removes free-evolution drift entirely and isolates the effect of the drive and the decoherence channels.

### Gaussian Pulse Engineering

The control field is shaped as a Gaussian envelope:

$$\Omega(t) = A\exp\left(-\frac{(t-t_0)^2}{2\sigma^2}\right)$$

exactly as in PulseForge-QC. A smooth envelope avoids sharp spectral content that could drive unwanted transitions into higher, non-target Fock levels — the bosonic-mode analogue of qubit leakage.

### Open Quantum Systems

The project models environmental interaction with the Lindblad master equation:

$$\dot{\rho} = -i[H,\rho] + \sum_k\left(L_k\rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\}\right)$$

### Photon Loss and Dephasing

Two decoherence channels are included, directly analogous to T1/T2 in the qubit project:

**Photon loss** (rate $\kappa$, collapse operator $\sqrt{\kappa}\,a$) — the bosonic analogue of T1 relaxation. It continuously pulls population from $|n\rangle$ toward $|n-1\rangle$, competing with the drive throughout the evolution rather than only after it ends.

**Photon dephasing** (rate $\gamma_\phi$, collapse operator $\sqrt{\gamma_\phi}\, a^\dagger a$) — the bosonic analogue of T2 dephasing. It destroys coherences between different Fock components without directly changing populations, weakening the interference the drive relies on.

### Fidelity

The target state is the single-photon Fock state $|1\rangle$. The simulator evaluates:

$$F = \langle 1|\rho_f|1\rangle$$

The optimizer searches for the pulse amplitude that maximizes this quantity.

### Phase-Space Observables

Instead of Bloch-sphere coordinates, a driven oscillator is visualized through its **photon number** $\langle n\rangle = \langle a^\dagger a\rangle$ and its two **quadratures**:

$$\langle x\rangle = \langle a + a^\dagger\rangle, \qquad \langle p\rangle = i\langle a^\dagger - a\rangle$$

$\langle n\rangle$ tracks population buildup (the oscillator analogue of population inversion), while $\langle x\rangle, \langle p\rangle$ track the mode's position in phase space — together they show *how* the state got to its final fidelity, not just the final number.

---

## Features

- Gaussian pulse engineering
- Time-dependent Hamiltonian simulation on a truncated Fock space
- Lindblad master equation evolution (QuTiP `mesolve`)
- Photon-loss modeling
- Photon-dephasing modeling
- Pulse amplitude optimization (SciPy L-BFGS-B)
- Photon-number and quadrature trajectory visualization
- Ideal closed-system (decoherence-free) reference, built from the same Hamiltonian
- Automatic Fock-space truncation sanity check (leakage warning)
- Modular scientific software architecture, mirroring PulseForge-QC

---

## Software Stack

| Library | Purpose |
|---|---|
| QuTiP | Open quantum system simulation |
| NumPy | Numerical computation |
| SciPy | Numerical optimization |
| Matplotlib | Visualization |

---

## Project Structure

```text
CavityPulse-QC/
│
├── README.md
├── requirements.txt
├── main.py
│
├── config/
│   └── system_config.py
│
├── pulses/
│   └── pulse_shapes.py
│
├── noise/
│   └── noise_model.py
│
├── simulation/
│   └── pulse_simulator.py
│
├── optimization/
│   └── optimize_pulse.py
│
├── visualization/
│   └── quadrature_visualization.py
│
├── reference_layer/
│   └── closed_system_reference.py
│
└── results/
    └── quadrature_dynamics.png
```

---

## Module Breakdown

### `config/system_config.py`

Holds all physical and numerical parameters: Fock-space truncation size, drive detuning, photon-loss rate $\kappa$, dephasing rate $\gamma_\phi$, pulse duration, Gaussian width, and simulation resolution. The resonant-drive condition is set here, exactly as in PulseForge-QC.

### `pulses/pulse_shapes.py`

Defines the Gaussian pulse envelope as a standalone function of time — unchanged in spirit from PulseForge-QC, since waveform generation doesn't depend on which quantum system the pulse ultimately drives.

### `noise/noise_model.py`

Constructs the Lindblad collapse operators for photon loss and dephasing from $\kappa$ and $\gamma_\phi$. These operators encode irreversible mode-environment interaction; without them the cavity would be a lossless idealization.

### `simulation/pulse_simulator.py`

The core simulation engine. Builds the time-dependent Hamiltonian on the truncated Fock space, calls QuTiP's `mesolve` to evolve the Lindblad dynamics, and evaluates the final-state fidelity. Also performs an automatic **leakage check**: if population in the highest truncated Fock level exceeds $10^{-3}$, it raises a warning that `N_LEVELS` should be increased, since a too-small truncation would silently produce inaccurate dynamics.

### `optimization/optimize_pulse.py`

Uses SciPy's L-BFGS-B to tune the pulse amplitude, searching for the drive strength that best balances coherent Fock-state buildup against continuous photon loss and dephasing.

### `visualization/quadrature_visualization.py`

Plots $\langle n\rangle, \langle x\rangle, \langle p\rangle$ across the full pulse evolution and saves the figure to `results/quadrature_dynamics.png` — the phase-space analogue of PulseForge-QC's Bloch-sphere plot.

### `reference_layer/closed_system_reference.py`

Re-evolves the *same* Hamiltonian and *same* pulse with the collapse operators removed ($\kappa = \gamma_\phi = 0$), providing a clean, decoherence-free reference. Unlike PulseForge-QC's separate Qiskit ideal-gate layer, this reference is built from the project's own Hamiltonian, which isolates the effect of decoherence *exactly* — nothing about the Hamiltonian or pulse shape differs between the two runs.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/<your-username>/CavityPulse-QC.git
cd CavityPulse-QC
```

### Create a Virtual Environment (Recommended)

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python main.py
```

The execution pipeline performs, in order:

1. baseline pulse simulation (noisy),
2. pulse amplitude optimization,
3. optimized pulse re-simulation (noisy, with full state tracking),
4. photon-number/quadrature visualization (saved to `results/quadrature_dynamics.png`),
5. ideal closed-system (decoherence-free) reference comparison.

Actual console output from this repository:

```text
==================================
 CAVITY-MODE QUANTUM CONTROL SIMULATION
==================================

Baseline fidelity: 0.067988

Optimization Results
------------------------
Optimal amplitude: 0.493737
Optimal fidelity: 0.367789

Quadrature dynamics plot saved to: results/quadrature_dynamics.png

Ideal Closed-System Reference
------------------------
Ideal fidelity (no decoherence, same pulse): 0.331106
Fidelity gap attributable to decoherence: -0.036683
```

> **QuTiP version note:** `simulation/pulse_simulator.py` uses the QuTiP ≥5.0 pythonic time-dependent coefficient signature `f(t, **kwargs)` and passes `c_ops`/`e_ops` as keyword arguments to `mesolve`. If running an older QuTiP 4.x environment, both the coefficient functions and the `mesolve` call will need to be adapted to the legacy `f(t, args)` / positional-argument signature.

---

## Results and Physical Interpretation

The project was executed end-to-end with the current system parameters: $\kappa = 1/25$, $\gamma_\phi = 1/40$, Gaussian width $\sigma = 2$, pulse duration $= 20$, resonant drive ($\Delta = 0$), Fock-space truncation `N_LEVELS = 14`.

```text
Baseline fidelity: 0.067988

Optimization Results
------------------------
Optimal amplitude: 0.493737
Optimal fidelity: 0.367789
```

### Baseline Fidelity Analysis

At the un-optimized amplitude $A = 1.0$, fidelity is very low ($F \approx 0.07$): the drive overshoots well past a single photon of population before loss and dephasing pull it back down, so very little final population sits specifically in $|1\rangle$. As in PulseForge-QC, this is expected behavior for an uncalibrated pulse, not a sign of a broken simulator.

### Optimization Behavior

After optimization, $F \approx 0.368$ at $A \approx 0.494$ — more than five times the baseline. The optimizer clearly finds real, recoverable structure in the amplitude landscape.

### The Central Physical Insight: A Hard Coherent-State Ceiling

This is where the bosonic-mode system reveals something the qubit system cannot. The drive term $(\Omega(t)/2)(a + a^\dagger)$ is **linear** in the ladder operators. A linear drive on a harmonic oscillator generates a *displacement* of the vacuum state — it can only ever produce a **coherent state** $|\alpha\rangle$ (up to the small distortions introduced by loss and dephasing), never an exact Fock state.

A coherent state's overlap with the Fock state $|1\rangle$ is:

$$P(1) = |\langle 1|\alpha\rangle|^2 = |\alpha|^2 e^{-|\alpha|^2}$$

which is maximized at $|\alpha|^2 = 1$, giving a hard theoretical ceiling of

$$P(1)_{\max} = \frac{1}{e} \approx 0.367879$$

**The optimizer converged to $F = 0.367789$ — within $10^{-4}$ of this exact theoretical bound.** This is not a coincidence: no matter how the single amplitude parameter is tuned, a Gaussian-shaped *linear* drive cannot exceed this ceiling, because the family of states it can reach is restricted to (quasi-)coherent states, and $1/e$ is the maximum any coherent state can achieve against $|1\rangle$. This is the direct bosonic-mode analogue of PulseForge-QC's qubit fidelity ceiling — except here the ceiling has an exact, closed-form value, which makes the limitation of the control model unusually easy to verify quantitatively.

### Phase-Space (Quadrature) Analysis

<p align="center">
  <img src="results/quadrature_dynamics.png" width="850" alt="Photon number and quadrature expectation values during the optimized pulse">
</p>

<p align="center"><sub>⟨n⟩, ⟨x⟩, ⟨p⟩ expectation values across the pulse duration, evaluated at the optimized amplitude (A ≈ 0.494).</sub></p>

**Why $\langle x\rangle$ stays at ≈ 0 throughout.** The drive Hamiltonian is proportional to $(a+a^\dagger)$, i.e. the $x$ quadrature operator itself. A linear drive along $x$ displaces the state purely along $p$ (the canonically conjugate direction), leaving $\langle x\rangle$ essentially unchanged. This is the direct analogue of PulseForge-QC's flat $\langle X\rangle$ trace, and serves the same purpose: a sanity check that the Hamiltonian's coupling direction and the resulting phase-space geometry are internally consistent.

**Why $\langle p\rangle$ develops a large, smooth excursion.** As the Gaussian pulse turns on around its center ($t=10$), the mode is coherently displaced along $p$, reaching roughly $-2.1$ near the pulse peak before decay pulls it partway back toward zero. This displacement is what builds up photon-number population.

**Why $\langle n\rangle$ rises to about 1.2 and settles near 1.0.** $\langle n\rangle = |\alpha(t)|^2$ for a coherent state tracks the squared magnitude of the phase-space displacement. It overshoots slightly above 1 near the pulse's trailing edge, then photon loss brings it back down to settle near $\langle n\rangle \approx 1.0$ by the end of the evolution — consistent with a final state close to a coherent state with $|\alpha|^2 \approx 1$, exactly the point at which $P(1)$ is maximized.

**The synthesis.** The quadrature plot and the $1/e$ fidelity ceiling are two views of the same fact: the optimizer isn't failing to find a better pulse — it is correctly finding the best point *within the reachable family of coherent-like states*, and that family has a hard, closed-form limit against any single target Fock state.

---

## Critical Assessment

**What it already demonstrates well:**
- pulse-driven bosonic-mode control,
- open-system dynamics in a truncated Fock space,
- decoherence-aware simulation (loss + dephasing),
- fidelity optimization,
- phase-space diagnostics,
- an exact, verifiable theoretical fidelity ceiling for the chosen control model,
- ideal-versus-noisy evolution comparison from a shared Hamiltonian.

**What still limits current performance:**
- the drive is strictly linear in $a, a^\dagger$, which restricts reachable states to (quasi-)coherent states,
- only one control degree of freedom is optimized (amplitude),
- the pulse family is fixed to a single Gaussian,
- no nonlinear (e.g. two-photon, Kerr-mediated) drive terms are included,
- the mode is single-cavity only,
- $\kappa$ and $\gamma_\phi$ are generic rather than hardware-calibrated values.

As in PulseForge-QC, these limitations are informative rather than embarrassing: they expose, in closed form, exactly why a linear one-parameter drive cannot exceed $1/e$ fidelity against a Fock state — a genuine and quantifiable structural fact about the control problem, not an artifact of insufficient tuning.

---

## Future Extensions

- nonlinear (two-photon / parametric) drive terms to break the coherent-state restriction
- joint optimization over amplitude, width, and detuning
- GRAPE or CRAB optimal control for richer pulse shapes
- conditional/measurement-based Fock-state preparation
- multi-mode (two-cavity, beamsplitter-coupled) dynamics
- Kerr-nonlinear oscillator modeling instead of a strict harmonic mode
- stochastic noise channels
- Wigner-function visualization alongside quadrature traces
- closed-loop calibration simulation
- Qiskit Dynamics / bosonic-backend integration

---

## Requirements

```text
numpy>=1.24
scipy>=1.10
matplotlib>=3.7
qutip>=5.0
```

---

## Relationship to PulseForge-QC

This project intentionally reuses PulseForge-QC's five-stage architecture — config → pulse shaping → noise model → simulator → optimizer → visualization → reference layer — applied to a different Hilbert space and a different control problem. The qubit project asks "how well can a one-parameter pulse invert a two-level system under T1/T2 noise?"; this project asks the analogous question for a bosonic mode, and additionally uncovers an exact, closed-form answer to *why* the achievable fidelity is capped where it is — a level of quantitative insight that emerges naturally from choosing a different, but architecturally parallel, physical system to model.

Project focus: pulse-level quantum control, open quantum systems, bosonic-mode dynamics, coherent-state control limits, numerical optimization.
