"""
config/system_config.py

Central store of all physical and numerical parameters for CavityPulse-QC.

Physical picture
-----------------
Instead of a two-level qubit, the system here is a single bosonic mode
(a microwave cavity resonator, or an optical cavity mode) truncated to a
finite number of Fock states. The mode is driven by a shaped microwave/
optical pulse and loses photons to its environment.

Resonant-drive condition
-------------------------
As in the qubit project, the drive is set exactly on resonance with the
cavity (omega_cavity == omega_drive), so the detuning term vanishes in the
rotating frame. This isolates the effect of the control pulse and the loss
channels from any free-evolution phase accumulation, which keeps the
resulting <n>, <x>, <p> trajectories easy to interpret physically.
"""

# --- Hilbert space truncation ---
# Number of Fock levels kept: |0>, |1>, ..., |N_LEVELS - 1>.
# Must be large enough that population never significantly leaks into the
# highest kept level (checked automatically in the simulator).
N_LEVELS = 14

# --- Drive / cavity frequencies (rotating frame) ---
# Resonant drive: omega_cavity - omega_drive = 0, so no free-evolution term
# is needed in the rotating frame Hamiltonian.
DETUNING = 0.0

# --- Decoherence channels ---
KAPPA = 1.0 / 25.0      # photon loss rate (1/T_loss), analogous to 1/T1
GAMMA_PHI = 1.0 / 40.0  # photon dephasing rate (1/T_phi), analogous to 1/T2

# --- Pulse shape parameters ---
PULSE_DURATION = 20.0   # total simulated time window
PULSE_CENTER = 10.0     # t0: Gaussian pulse center
PULSE_SIGMA = 2.0       # Gaussian pulse width
INITIAL_AMPLITUDE = 1.0 # baseline (un-optimized) pulse amplitude

# --- Simulation resolution ---
N_TIME_POINTS = 400     # number of points in tlist

# --- Target state for fidelity ---
# Single-photon Fock state |1>, the bosonic analogue of the qubit's |1>.
TARGET_FOCK_STATE = 1

