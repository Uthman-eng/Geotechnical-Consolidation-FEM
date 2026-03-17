import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.terzaghi_1d_multi.fem import (
    Get_terzaghi1dMultilayer_FEA,
    _layer_values_at_depths,
    _normalise_layer_depths,
)


SECONDS_PER_DAY = 60 * 60 * 24


def test_depths_start_from_surface_if_surface_not_given():
    depths = [5.0, 10.0]
    final_depth = 10.0

    layer_depths = _normalise_layer_depths(depths, final_depth)
    expected_layer_depths = np.array([0.0, 5.0, 10.0])

    assert np.allclose(layer_depths, expected_layer_depths)


def test_repeated_depths_are_rejected():
    with pytest.raises(ValueError, match="strictly increasing"):
        _normalise_layer_depths([0.0, 5.0, 5.0, 10.0], 10.0)


def test_mv_values_go_to_the_expected_layers():
    # Two layers:
    # 0 to 5 m  -> Mv = 1e-4
    # 5 to 10 m -> Mv = 2e-4
    layer_depths = _normalise_layer_depths([0.0, 5.0, 10.0], 10.0)
    mv_values = [1e-4, 2e-4]
    depths_to_check = np.array([0.0, 2.5, 5.0, 7.5, 10.0])

    mv_profile = _layer_values_at_depths(depths_to_check, layer_depths, mv_values)
    expected_mv_profile = np.array([1e-4, 1e-4, 1e-4, 2e-4, 2e-4])

    assert np.allclose(mv_profile, expected_mv_profile)


def test_cv_values_go_to_the_expected_layers():
    # Four layers:
    # 0 to 1 m -> 2e-7
    # 1 to 2 m -> 4e-7
    # 2 to 4 m -> 6e-7
    # 4 to 5 m -> 8e-7
    layer_depths = _normalise_layer_depths([1.0, 2.0, 4.0, 5.0], 5.0)
    cv_values = [2e-7, 4e-7, 6e-7, 8e-7]
    depths_to_check = np.array([0.25, 1.0, 1.5, 2.0, 3.0, 4.0, 4.75])

    cv_profile = _layer_values_at_depths(depths_to_check, layer_depths, cv_values)
    expected_cv_profile = np.array([2e-7, 2e-7, 4e-7, 4e-7, 6e-7, 6e-7, 8e-7])

    assert np.allclose(cv_profile, expected_cv_profile)


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
            final_time_days * SECONDS_PER_DAY,
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
