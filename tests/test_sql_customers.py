import pytest
from unittest.mock import MagicMock
import json
from arcade.core.schema import ToolSecretItem
from arcade.sdk import ToolContext
from arcade_sql_customers.tools.query import query_customer_data, direct_query


EXPECTED_EMPTY_RESULT = {"results": []}

@pytest.fixture
def mock_context():
    return ToolContext(secrets=[ToolSecretItem(key="customer_database_path", value="people.sqlite")])

def test_direct_query(mock_context) -> None:
    # get the first row
    query = "SELECT Occupation FROM people WHERE id = 1"
    expected_result = {"results": [
        {
            "Occupation": "Paediatric nurse",
        }
    ]}
    assert direct_query(mock_context, query=query) == expected_result


def test_query_customer_by_id(mock_context) -> None:
    # get the first row
    expected_result = {"results": [
        {
            "Age": 63,
            "Email": "grantanderson@simmons-jackson.com",
            "Location": "Los Angeles, CA",
            "Name": "Christopher Sharp",
            "Occupation": "Paediatric nurse",
            "id": 1
        }
    ]}
    assert query_customer_data(mock_context, filter_by_id=1) == expected_result
    assert query_customer_data(mock_context, filter_by_id=-1) == EXPECTED_EMPTY_RESULT


def test_query_customer_by_name(mock_context) -> None:
    # get the first row
    expected_result_len = 3
    retrieved_result = query_customer_data(mock_context, filter_by_name="David")
    retrieved_result_len = len(retrieved_result["results"])
    assert retrieved_result_len == expected_result_len
    assert query_customer_data(mock_context, filter_by_name="Dante") == EXPECTED_EMPTY_RESULT


def test_query_invalid_columns(mock_context) -> None:
    expected_result_len = 20  # we're expecting the default limit
    valid_columns = ["Name", "Location", "Email"]
    wrong_columns = ["Airport", "Coordinates", "Email"]
    retrieved_result = query_customer_data(mock_context, columns_to_select=valid_columns)
    retrieved_result_len = len(retrieved_result["results"])
    assert retrieved_result_len == expected_result_len
    assert query_customer_data(
        mock_context, columns_to_select=wrong_columns) == EXPECTED_EMPTY_RESULT
