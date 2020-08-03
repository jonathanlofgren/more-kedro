import pytest
from more_kedro.datasets import TryLoadDataSet
from unittest.mock import MagicMock


class TestTryLoadDataset:
    class TestWhenLoadThrowsException:
        @pytest.mark.filterwarnings("ignore")
        def test_it_returns_default_value(self):
            default_value = MagicMock()
            assert (
                TryLoadDataSet(
                    dataset={"type": "text.TextDataSet", "filepath": "missing.txt"},
                    default_value=default_value,
                ).load()
                == default_value
            )

    class TestWhenLoadIsSuccessful:
        def test_it_loads_underlying_data(self):
            data = 3.14159
            assert (
                TryLoadDataSet(dataset={"type": "MemoryDataSet", "data": data}).load()
                == data
            )
