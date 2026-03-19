import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.terzaghi_1d_multi.fem import Get_terzaghi1dMultilayer_FEA
from src.geotech_consolidation.models.terzaghi_2d.fem import Get_terzaghi2D_FEA


seconds_to_days = 60 * 60 * 24


def test_2d_model_runs_and_peak_settlement_matches_multilayer_peak():
    H = 10.0
    W = 50.0
    nx = 20
    load = 100.0
    final_time_days = 10.0
    num_time_steps = 11
    base = 100.0

    depths = [10.0]
    cv_values = [1e-3]
    mv_values = [1e-4]

    settlement_surface, u_hist_2d, unique_x, node_x, node_y = Get_terzaghi2D_FEA(
        H,
        W,
        nx,
        load,
        final_time_days * seconds_to_days,
        num_time_steps,
        cv_values,
        mv_values,
        base,
        depths=depths,
    )

    settlement_history_1d, u_hist_1d, settlement_1d = Get_terzaghi1dMultilayer_FEA(
        depths,
        nx,
        load,
        final_time_days * seconds_to_days,
        num_time_steps,
        cv_values,
        mv_values,
        base,
        False,
    )

    peak_settlement_2d = np.max(settlement_surface)
    peak_settlement_1d = np.max(settlement_history_1d)

    assert settlement_surface.shape[0] == num_time_steps
    assert u_hist_2d.shape[0] == num_time_steps
    assert np.all(np.isfinite(settlement_surface))
    assert np.all(np.isfinite(u_hist_2d))
    assert np.isclose(peak_settlement_2d, peak_settlement_1d, rtol=0.2), (
        f"2D peak settlement = {peak_settlement_2d:.6f}, "
        f"1D multilayer peak settlement = {peak_settlement_1d:.6f}"
    )
