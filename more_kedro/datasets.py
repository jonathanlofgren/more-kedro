from typing import Any, Dict, Union, Type
from kedro.io import AbstractDataSet
from kedro.io.core import parse_dataset_definition


class TryLoadDataSet(AbstractDataSet):
    def __init__(
        self,
        dataset: Union[Type[AbstractDataSet], Dict[str, Any]],
        default_value: Any = None,
    ):
        self._dataset_type, self._dataset_config = parse_dataset_definition(dataset)
        self._default_value = default_value
        self._dataset = self._dataset_type(**self._dataset_config)

    def _load(self) -> Any:
        try:
            return self._dataset._load()
        except Exception as err:
            self._logger.info(
                f"TryLoadDataSet got exception '{err}' when trying to load - "
                f"returning {self._default_value} instead."
            )
            return self._default_value

    def _save(self, data: Any) -> None:
        return self._dataset._save(data)

    def _describe(self) -> Dict[str, Any]:
        return dict(
            dataset_type=self._dataset_type.__name__,
            dataset_config=self._dataset_config,
            default_value=self._default_value,
        )
