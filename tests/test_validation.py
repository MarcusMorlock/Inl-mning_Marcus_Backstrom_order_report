"""Testing for Validation Functions"""

import pandas as pd
import logging 
import pytest

from order_report.validation import validate_order_df, REQUIRED

def test_dataframe_validation_columns(caplog) -> None:

    invalid_data = {col: [1] for col in list(REQUIRED)[1:]}

    df= pd.DataFrame(invalid_data)
    with caplog.at_level(logging.ERROR):

        with pytest.raises(
            ValueError,
            match="Dataframe misses required columns:"
        ): validate_order_df(df)

    assert "Validation failed. Missing columns:" in caplog.text

def test_dataframe_validation_success() -> None:
    valid_data = {col: [1] for col in REQUIRED}
    df = pd.DataFrame(valid_data)
    
    result = validate_order_df(df)
    
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
