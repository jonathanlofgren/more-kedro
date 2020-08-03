# more-kedro :hammer_and_wrench:

A collection of utilities and extensions for [Kedro](https://github.com/quantumblacklabs/kedro)

## Installation

    $ pip install more-kedro

## [hooks.TypedParameters](more_kedro/hooks.py)
Enables on the fly typing and validation of your parameter dictionaries.

#### Usage
Activate by adding the `TypedParameters` hook to your `KedroContext`:
```python
from more_kedro.hooks import TypedParameters

class ProjectContext(KedroContext):
    hooks = (
        TypedParameters(),
    )

    ...
```
Now you can specify types in your `parameters.yml`:
```yaml
training__type: my_project.nodes.model.TrainingParams
training:
  num_iter: 100
  learning_rate: 0.001
```
or if you pass `TypedParameters(inline=True)`:
```yaml
training:
  type: my_project.nodes.model.TrainingParams
  num_iter: 100
  learning_rate: 0.001
```
The benefit of the first approach is that you can overwrite your parameter values in `conf/local/`
without having to respecify the types.

Any node which has an input `params:training` will now be injected with the
equivalent of `TrainingParams(num_iter=100, learning_rate=0.001)` instead of a raw
dictionary. You can use any custom class, dataclass,
[pydantic](https://github.com/samuelcolvin/pydantic) model or any other
callable to get validation and typing of your parameters. The type must contain
the full location and name of your type object, so that it can be imported
from the root of your project.

The parameters are typed right after your `DataCatalog` is created, so any failures
will surface before your kedro run starts.

## [datasets.TryLoadDataSet](more_kedro/datasets.py)

A dataset which uses an underlying dataset definition to load and save, but if the load method
throws an exception it returns a default value instead. Can be used if the existence of some
data is optional to the pipeline.

### Usage
`TryLoadDataSet` takes two arguments, `dataset` which is a normal dataset definition,
and an optional `default_value` which is the value to return if the load fails
(defaults to `None`). Example of an entry in `catalog.yml`:

```yaml
companies:
  dataset:
    type: pandas.CSVDataSet
    filepath: "path/to/companies.csv"
  default_value: null
```

## Contributions
If you have any useful Kedro utilities such as runners, hooks, datasets or whatever it may be - PR's are very welcome!
