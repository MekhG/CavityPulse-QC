"""
reference_layer/closed_system_reference.py

Provides a clean, loss-free reference against which the noisy,
pulse-driven cavity evolution can be compared -- the bosonic-mode
analogue of the qubit project's Qiskit ideal-X-gate layer.

Rather than calling out to a separate circuit-model library, the
reference here is obtained directly from this project's own Hamiltonian
with the collapse operators simply omitted (kappa = gamma_phi = 0). This
keeps the comparison exact: same Hamiltonian, same pulse, same solver --
the only difference is the presence or absence of the environment.
This isolates precisely how much of the fidelity gap is caused by
decoherence, as opposed to any mismatch in the Hamiltonian or pulse
shape itself.
"""

import numpy as np
import qutip as qt

from simulation.pulse_simulator import build_hamiltonian, _pulse_coefficient, _detuning_coefficient


def run_ideal_reference(amplitude, config):
    """
    Evolve the same driven bosonic mode with no decoherence at all
    (kappa = gamma_phi = 0), and report the ideal final-state fidelity
    with the target Fock state.

    Parameters
    ----------
    amplitude : float
        Same pulse amplitude used in the noisy simulation, so the
        comparison isolates the effect of decoherence alone.
    config : module
        The system_config module.

    Returns
    -------
    ideal_fidelity : float
    """
    a, n_op, x_like = build_hamiltonian(config.N_LEVELS, config.DETUNING)

    H = [
        [n_op, _detuning_coefficient],
        [x_like, _pulse_coefficient],
    ]

    rho0 = qt.fock_dm(config.N_LEVELS, 0)
    tlist = np.linspace(0, config.PULSE_DURATION, config.N_TIME_POINTS)

    args = {
        "amplitude": amplitude,
        "center": config.PULSE_CENTER,
        "sigma": config.PULSE_SIGMA,
        "detuning": config.DETUNING,
    }

    # No c_ops passed: this is the closed-system (lossless) reference.
    result = qt.mesolve(H, rho0, tlist, args=args, options={"store_states": True})
    rho_final = result.states[-1]

    ideal_fidelity = qt.expect(
        qt.fock_dm(config.N_LEVELS, config.TARGET_FOCK_STATE), rho_final
    )
    return ideal_fidelity
