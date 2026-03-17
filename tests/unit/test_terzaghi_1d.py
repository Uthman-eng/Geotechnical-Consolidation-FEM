import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.terzaghi_1d.fem import Get_terzaghi1D_FEA
from src.geotech_consolidation.models.terzaghi_1d.fem import boussinesq_condition
from src.geotech_consolidation.models.terzaghi_1d.u0_analytical import Get_terzaghi1d_Analytical_u0

SECONDS_PER_DAY = 60 * 60 * 24

def test_single_layer_model_runs():
    H = 10.0
    Cv = 1e-3
    Mv = 1e-4
    load = 100.0
    final_time_days = 10.0
    num_elements = 21
    num_time_steps = 11

    settlement_history, u_hist, settlement = Get_terzaghi1D_FEA(
        H,
        num_elements,
        load,
        final_time_days * SECONDS_PER_DAY,
        num_time_steps,
        Cv,
        H / 2.0,
        Mv,
        False,
    )

    z = np.linspace(0.0, H, num_elements + 1)
    t = np.linspace(0.0, final_time_days, num_time_steps)

    assert u_hist.shape[0] == t.shape[0]
    assert u_hist.shape[1] == z.shape[0]
    assert settlement_history.shape == t.shape
    assert settlement.shape == z.shape
    assert np.all(np.isfinite(settlement_history))
    assert np.all(np.isfinite(settlement))

    settlement_history, u_hist, settlement = Get_terzaghi1D_FEA(
        H,
        num_elements,
        load,
        final_time_days * SECONDS_PER_DAY,
        num_time_steps,
        Cv,
        H / 2.0,
        Mv,
        True,
    )
    
    assert u_hist.shape[0] == t.shape[0]
    assert u_hist.shape[1] == z.shape[0]
    assert settlement_history.shape == t.shape
    assert settlement.shape == z.shape
    assert np.all(np.isfinite(settlement_history))
    assert np.all(np.isfinite(settlement))

def test_boussinesq_initial_condition_matches_u0_analytical_solution():
    H = 10.0
    Cv = 1e-3
    Mv = 1e-4
    load = 100.0
    base = H / 2.0
    final_time_days = 10.0
    num_elements = 21
    num_time_steps = 11
    n_terms = int(np.round(0.8 * num_elements))

    settlement_history, u_hist, settlement = Get_terzaghi1D_FEA(
        H,
        num_elements,
        load,
        final_time_days * SECONDS_PER_DAY,
        num_time_steps,
        Cv,
        base,
        Mv,
        False,
    )

    depth_grid = np.linspace(0.0, H, num_elements + 1, dtype=float)[None, :]
    u0 = boussinesq_condition(depth_grid, load, base)

    p_data, _, _ = Get_terzaghi1d_Analytical_u0(
        u0,
        H,
        num_elements,
        final_time_days * SECONDS_PER_DAY,
        num_time_steps,
        Cv,
        n_terms,
    )

    final_error = u_hist[-1] - p_data[-1]
    final_l2_error = np.sqrt(np.sum(final_error**2))

    assert final_l2_error < 0.01, (
        f"Final-time L2 error = {final_l2_error:.6f}",
    )
