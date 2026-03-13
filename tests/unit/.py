import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.terzaghi_1d.fem import Get_terzaghi1D_FEA


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
        True,
    )

    z = np.linspace(0.0, H, num_elements + 1)
    t = np.linspace(0.0, final_time_days, num_time_steps)

    assert u_hist.shape[0] == t.shape[0]
    assert u_hist.shape[1] == z.shape[0]
    assert settlement_history.shape == t.shape
    assert settlement.shape == z.shape
    assert np.all(np.isfinite(settlement_history))
    assert np.all(np.isfinite(settlement))