import pytest
from arcade.core.schema import ToolSecretItem
from arcade.sdk import ToolContext
from arcade_sql_customers.tools.query import query_customer_data, direct_query
import os
import dotenv

dotenv.load_dotenv()


EXPECTED_EMPTY_RESULT = {"results": []}
DATABASE_URL = os.environ["DATABASE_URL"]


@pytest.fixture
def mock_context():
    return ToolContext(
        secrets=[ToolSecretItem(
            key="database_url",
            value=DATABASE_URL)]
    )


def test_direct_query(mock_context) -> None:
    # get the first row
    query = "SELECT Occupation FROM people WHERE id = 1"
    expected_result = {"results": [
        {
            "occupation": "Paediatric nurse",
        }
    ]}
    assert direct_query(mock_context, query=query) == expected_result


def test_query_customer_by_id(mock_context) -> None:
    # get the first row
    expected_result = {"results": [
        {
            "age": 63,
            "email": "grantanderson@simmons-jackson.com",
            "location": "Los Angeles, CA",
            "name": "Christopher Sharp",
            "occupation": "Paediatric nurse",
            "id": 1
        }
    ]}
    assert query_customer_data(mock_context, filter_by_id=1) == expected_result
    assert query_customer_data(
        mock_context, filter_by_id=-1) == EXPECTED_EMPTY_RESULT


def test_query_customer_by_name(mock_context) -> None:
    # get the first row
    expected_result_len = 3
    retrieved_result = query_customer_data(
        mock_context, filter_by_name="David")
    retrieved_result_len = len(retrieved_result["results"])
    assert retrieved_result_len == expected_result_len
    assert query_customer_data(
        mock_context, filter_by_name="Dante") == EXPECTED_EMPTY_RESULT


def test_query_invalid_columns(mock_context) -> None:
    expected_result_len = 20  # we're expecting the default limit
    valid_columns = ["name", "location", "email"]
    wrong_columns = ["airport", "coordinates", "email"]
    retrieved_result = query_customer_data(
        mock_context, columns_to_select=valid_columns)
    retrieved_result_len = len(retrieved_result["results"])
    assert retrieved_result_len == expected_result_len
    assert query_customer_data(
        mock_context, columns_to_select=wrong_columns) == EXPECTED_EMPTY_RESULT
