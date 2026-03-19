import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.terzaghi_1d_multi.fem import Get_terzaghi1dMultilayer_FEA


seconds_to_days = 60 * 60 * 24

def test_multilayer_solver_runs_for_both_initial_conditions():
    depths = [0.0, 5.0, 10.0]
    cv_values = [1e-3, 5e-4]
    mv_values = [1e-4, 2e-4]
    load = 100.0
    final_time_days = 10.0
    num_elements = 21
    num_time_steps = 11

    for use_uniform_initial_condition in [False, True]:
        settlement_history, u_hist, settlement = Get_terzaghi1dMultilayer_FEA(
            depths,
            num_elements,
            load,
            final_time_days * seconds_to_days,
            num_time_steps,
            cv_values,
            mv_values,
            max(depths) / 2.0,
            use_uniform_initial_condition,
        )

        expected_depth_grid = np.linspace(0.0, max(depths), num_elements + 1)
        expected_time_grid = np.linspace(0.0, final_time_days, num_time_steps)

        assert u_hist.shape[0] == expected_time_grid.shape[0]
        assert u_hist.shape[1] == expected_depth_grid.shape[0]
        assert settlement_history.shape == expected_time_grid.shape
        assert settlement.shape == expected_depth_grid.shape
        assert np.all(np.isfinite(settlement_history))
        assert np.all(np.isfinite(settlement))
