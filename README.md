# sisepuede_region_nbs
Repository storing notebooks with region-specific information

## Get Started

Create a conda env with python 3.11 (You can use any name)

```
conda create -n sisepuede python=3.11
```
Activate the env
```
conda activate sisepuede
```
Install the working version of the sisepuede package
```
pip install git+https://github.com/jcsyme/sisepuede.git@working_version
```
Install additional libraries
```
pip install -r requirements.txt
```

## TODO

### File Structure
- Create a folder for the excel files and a folder for the input data files under the data directory. Make sure to update the paths on the notebook and classes

### `ExcelYAMLHandler`

- The special cases (transformations without a single magnitude paramater) are not yet handled; we also need to multiply them by the scalar.
- We need to scale the default values to their maximum defaults.
- We also need to edit the YAML description.
- We need to come up with a better transformation name for the YAML parameter.
- If several strategies have the same magnitude in a transformation, we should create a single transformation file instead of one per each strategy.

### `StrategyCSVHandler`
- Come up with a better naming or a more standarize format for strategies.


