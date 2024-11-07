# sisepuede_region_nbs
Repository storing notebooks with region-specific information

## Tutorials

1. To learn how to use the `TransformationUtils` classes to generate YAML files and strategies based on an Excel file, please refer to the [class_tutorial.ipynb](class_tutorial.ipynb) notebook.
2. For a walkthrough on running a simulation and generating new YAML files and strategies, please refer to the [croatia_manager_wb.ipynb](croatia/croatia_manager_wb.ipynb) notebook.

## TODO

### `manager_wb`
- Add a variable called region to the top cell so everytime you want to run a different country you just change this variable.
- Standarize file names so the change suggested above makes sense.

### `ExcelYAMLHandler`

- The special cases (transformations without a single magnitude paramater) are not yet handled; we also need to multiply them by the scalar.
- We need to scale the default values to their maximum defaults.
- We also need to edit the YAML description.
- We need to come up with a better transformation name for the YAML parameter.
- If several strategies have the same magnitude in a transformation, we should create a single transformation file instead of one per each strategy.

### `StrategyCSVHandler`
- Come up with a better naming or a more standarize format for strategies.
