# Tests

This folder is for future small automated checks after the notebook-based verification work is in a stable state.

What each folder is for:

- `unit/`: small checks for individual functions. These are the quickest checks and would cover things like analytical helper functions, settlement calculations, Boussinesq initial conditions, and simple input parsing.
- `integration/`: larger checks that run a small model workflow end to end and confirm the returned arrays, dimensions, and basic boundary behavior are sensible.
- `fixtures/`: stored reference inputs or small expected outputs used by those checks.

Practical examples for this project:

- Keep the full FEM-vs-analytical verification, convergence plots, and result discussion in the notebooks.
- Use `tests/` only for lightweight repeatable checks, such as confirming the analytical solution returns an array of shape `(time_steps, nodes)`.
- A small `integration` check could run the single-layer FEM solver on a very small mesh and confirm the top drained node stays at zero pore pressure.
- A `fixtures` file could store a tiny reference case so future code changes can be checked quickly without rerunning the full verification notebook.
