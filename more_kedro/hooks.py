from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.utils import load_obj
from typing import Dict
import logging


logger = logging.getLogger(__name__)


class TypedParameters:
    def __init__(self, type_indicator: str = "type", inline: bool = False):
        self._type_indicator = type_indicator
        self._type_suffix = f"__{type_indicator}"
        self._inline = inline

    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog) -> None:
        if self._inline:
            param_types = self._get_param_types_inline(catalog)
        else:
            param_types = self._get_param_types(catalog)

        for param, type_string in param_types.items():
            type_obj = load_obj(type_string)
            catalog._data_sets[param]._data = type_obj(
                **catalog._data_sets[param]._data
            )

    def _get_param_types(self, catalog: DataCatalog) -> Dict[str, str]:
        param_types = {}

        for name, dataset in catalog._data_sets.items():
            if name.startswith("params:") and name.endswith(self._type_suffix):
                param_name = name[: -len(self._type_suffix)]
                if param_name in catalog._data_sets:
                    param_types[param_name] = dataset._data
        return param_types

    def _get_param_types_inline(self, catalog: DataCatalog) -> Dict[str, str]:
        param_types = {}

        for name, dataset in catalog._data_sets.items():
            if name.startswith("params:") and self._type_indicator in dataset._data:
                param_types[name] = dataset._data.pop(self._type_indicator)
        return param_types
