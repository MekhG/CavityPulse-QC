"""
visualization/quadrature_visualization.py

Plots <n>(t), <x>(t), <p>(t) across the full pulse evolution and saves the
figure to results/quadrature_dynamics.png.

This is the bosonic-mode analogue of the qubit project's Bloch-sphere
plot. Where a qubit's state is visualized on the Bloch sphere via
<X>, <Y>, <Z>, a driven oscillator's state is visualized in phase space
via its photon number <n> and its two quadratures <x> = <a + a^dag> and
<p> = i<a^dag - a>. Together these reveal *how* the mode built up (or
failed to build up) population in the target Fock state, not just the
final fidelity number.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_quadrature_dynamics(result, tlist, save_path):
    """
    Plot <n>(t), <x>(t), <p>(t) from a mesolve result with e_ops populated,
    and save the figure.

    Parameters
    ----------
    result : qutip.solver.Result
        Result of run_simulation(..., return_states=True). result.expect
        is expected to hold [n(t), x(t), p(t)] in that order, matching the
        e_ops ordering set in simulation/pulse_simulator.py.
    tlist : array-like
        Time points corresponding to result.expect.
    save_path : str
        File path to save the resulting PNG figure to.
    """
    n_t, x_t, p_t = result.expect

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(tlist, n_t, label=r"$\langle n \rangle$ (photon number)", color="tab:red")
    ax.plot(tlist, x_t, label=r"$\langle x \rangle$ (quadrature)", color="tab:blue")
    ax.plot(tlist, p_t, label=r"$\langle p \rangle$ (quadrature)", color="tab:green")

    ax.set_xlabel("Time")
    ax.set_ylabel("Expectation value")
    ax.set_title("Driven, Lossy Cavity Mode: Photon Number and Quadrature Dynamics")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
