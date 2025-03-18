from arcade.sdk import ToolCatalog
from arcade.sdk.eval import (
    EvalRubric,
    EvalSuite,
    ExpectedToolCall,
    SimilarityCritic,
    BinaryCritic,
    tool_eval,
)

import arcade_sql_customers
from arcade_sql_customers.tools.query import query_customer_data

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)


catalog = ToolCatalog()
catalog.add_module(arcade_sql_customers)


@tool_eval()
def sql_toolkit_query_customer_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="sql_toolkit Tools Evaluation",
        system_message=(
            "You are an AI assistant with access to sql_toolkit tools. "
            "Use them to help the user with their tasks."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    suite.add_case(
        name="Getting names and emails from a given Name",
        user_message="Get the names and emails of all customers named David",
        expected_tool_calls=[ExpectedToolCall(
            func=query_customer_data, args={
                "filter_by_name": "David",
                "columns_to_select": ["name", "email"],
            })],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="filter_by_name", weight=0.5),
            BinaryCritic(critic_field="columns_to_select", weight=0.5),
        ]
    )

    suite.add_case(
        name="Getting emails from customers of a given age",
        user_message="Get the emails of all customers aged 44",
        expected_tool_calls=[ExpectedToolCall(
            func=query_customer_data, args={
                "filter_by_age": 44,
                "columns_to_select": ["email"],
            })],
        rubric=rubric,
        critics=[
            BinaryCritic(critic_field="filter_by_age", weight=0.5),
            BinaryCritic(critic_field="columns_to_select", weight=0.5),
        ]
    )

    suite.add_case(
        name="Getting Names and Occupations of all customers in California",
        user_message="Get the names and occupation of customers in California",
        expected_tool_calls=[ExpectedToolCall(
            func=query_customer_data, args={
                "filter_by_location": "CA",
                "columns_to_select": ["name", "occupation"],
            })],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="filter_by_location", weight=0.5),
            BinaryCritic(critic_field="columns_to_select", weight=0.5),
        ]
    )

    suite.add_case(
        name="Get a sorted list of up to 100 users from Los Angeles",
        user_message="List up to 100 customers in los angeles, sort by age",
        expected_tool_calls=[ExpectedToolCall(
            func=query_customer_data, args={
                "filter_by_location": "Los Angeles, CA",
                "order_by": "age",
                "limit": 100,
            })],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="filter_by_location", weight=0.2),
            BinaryCritic(critic_field="order_by", weight=0.4),
            BinaryCritic(critic_field="limit", weight=0.4),
        ]
    )

    return suite
