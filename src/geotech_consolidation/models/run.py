"""
Utility wrappers that run the FEM-based Terzaghi models and expose
diagnostics such as pore-pressure history, settlement, and effective
stiffness/resilience inputs for downstream consumers and tests.
"""

from __future__ import annotations

import numpy as np

from src.geotech_consolidation.models.terazaghi_1d.fem import Get_Terazaghi1D_FEA
from src.geotech_consolidation.models.terazaghi_multilayer.fem import Get_Terazaghi1dMultilayer_FEA

SECONDS_PER_DAY = 60 * 60 * 24


def _build_layer_profile(z: np.ndarray, interfaces: np.ndarray, values: list[float]) -> np.ndarray:
    layer_ids = np.digitize(z, interfaces[1:], right=True)
    layer_ids = np.clip(layer_ids, 0, len(values) - 1)
    return np.asarray(values, dtype=np.float64)[layer_ids]


def run_terazaghi_1d(
    *,
    H: float,
    Cv: float,
    Mv: float,
    q: float,
    t_final: float,
    num: int,
    n_steps: int,
    base: float | None = None,
    use_uniform_initial: bool = True,
) -> dict[str, np.ndarray | float]:
    """
    Run the single-layer Terzaghi FE model and return the core outputs needed
    for plotting/validation.
    """
    if n_steps < 2:
        raise ValueError("n_steps must be >= 2 to form a valid time history.")

    base = float(base) if base is not None else max(abs(H), 1.0) / 2.0
    Tx = t_final * SECONDS_PER_DAY

    local_dcons, u_hist, settlement = Get_Terazaghi1D_FEA(
        H,
        num,
        q,
        Tx,
        n_steps,
        Cv,
        base,
        Mv,
        use_uniform_initial,
    )

    nodes = num + 1
    z = np.linspace(0.0, abs(H), nodes, dtype=np.float64)
    t = np.linspace(0.0, t_final, n_steps, dtype=np.float64)

    return {
        "u_hist": u_hist,
        "settlement": settlement,
        "local_dcons": local_dcons,
        "z": z,
        "t": t,
        "Cv": float(Cv),
        "Mv": float(Mv),
        "kappa": np.full(nodes, float(Cv), dtype=np.float64),
        "load": float(q),
        "base": float(base),
    }


def run_terazaghi_multilayer(
    *,
    H: float | None = None,
    depths: list[float],
    Cv: list[float],
    Mv: list[float],
    q: float,
    t_final: float,
    num: int,
    n_steps: int,
    base: float | None = None,
    use_uniform_initial: bool = True,
) -> dict[str, np.ndarray | float]:
    """
    Run the multi-layer Terzaghi model and expose the standard outputs.
    """
    if n_steps < 2:
        raise ValueError("n_steps must be >= 2 to form a valid time history.")

    depth_max = float(max(depths))
    H = float(H) if H is not None else depth_max
    if H < depth_max:
        raise ValueError("H must be greater than or equal to the maximum depth.")
    base = float(base) if base is not None else H / 2.0
    Tx = t_final * SECONDS_PER_DAY
    depth_array = np.asarray(depths, dtype=np.float64)
    if np.isclose(depth_array[0], 0.0):
        interfaces = depth_array
    else:
        interfaces = np.concatenate(([0.0], depth_array))

    local_dcons, u_hist, settlement = Get_Terazaghi1dMultilayer_FEA(
        depths,
        num,
        q,
        Tx,
        n_steps,
        Cv,
        Mv,
        base,
        use_uniform_initial,
    )

    nodes = num + 1
    z = np.linspace(0.0, H, nodes, dtype=np.float64)
    t = np.linspace(0.0, t_final, n_steps, dtype=np.float64)
    kappa_profile = _build_layer_profile(z, interfaces, Cv)
    Mv_profile = _build_layer_profile(z, interfaces, Mv)

    return {
        "u_hist": u_hist,
        "settlement": settlement,
        "local_dcons": local_dcons,
        "z": z,
        "t": t,
        "Cv": np.asarray(Cv, dtype=np.float64),
        "Mv": np.asarray(Mv, dtype=np.float64),
        "kappa_profile": kappa_profile,
        "Mv_profile": Mv_profile,
        "load": float(q),
        "base": float(base),
    }
