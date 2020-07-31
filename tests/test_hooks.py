import pytest
from kedro.io import DataCatalog
from more_kedro import TypedParameters
from collections import namedtuple


FirstType = namedtuple("FirstType", "a,b")
SecondType = namedtuple("SecondType", "d,f")


@pytest.fixture()
def mock_catalog() -> DataCatalog:
    return DataCatalog(feed_dict={
        "params:one": {
            "a": 100,
            "b": "test",
        },
        "params:one__type": "test_hooks.FirstType",
        "params:one__spec": "test_hooks.SecondType",
        "params:two": {
            "type": "test_hooks.SecondType",
            "d": 1,
            "f": 2,
        },
    })


class TestTypedParameters:
    class TestWithDefaultConfiguration:
        def test_it_converts_to_valid_type(self, mock_catalog):
            TypedParameters().after_catalog_created(mock_catalog)

            assert mock_catalog.load("params:one") == FirstType(
                a=100,
                b="test",
            )
            # Unchanged:
            assert mock_catalog.load("params:two") == {
                "type": "test_hooks.SecondType",
                "d": 1,
                "f": 2,
            }

    class TestWithModifiedTypeIndicator:
        def test_it_raises_exception_when_invalid_type(self, mock_catalog):
            with pytest.raises(TypeError):
                TypedParameters(type_indicator="spec").after_catalog_created(mock_catalog)

    class TestWithInlineMode:
        def test_it_uses_argument_inside_the_params_dict(self, mock_catalog):
            TypedParameters(inline=True).after_catalog_created(mock_catalog)

            assert mock_catalog.load("params:two") == SecondType(d=1, f=2)
