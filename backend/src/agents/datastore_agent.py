import logging
from src.utils import call_model
from src.utils.graph_db_utils import execute_query
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json
from .types import Parameter
from .agent import Agent, agent
from .tool import tool


logger = logging.getLogger(__name__)

current_user = "John Doe"
engine = PromptEngine()
narrative_options = "Bills, Groceries, Entertainment, Rent, Shopping"

graph_schema_prompt = engine.load_prompt("graph-schema", narrative_options=narrative_options)

generate_cypher_query_prompt = engine.load_prompt(
    "generate-cypher-query", graph_schema_prompt=graph_schema_prompt, current_date=datetime.now()
)



@tool(
    name="generate cypher query",
    description="Generate Cypher query if the category is data driven, based on the operation to be performed",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="The intent the question will be based on",
        ),
        "operation": Parameter(
            type="string",
            description="The operation the cypher query will have to perform",
        ),
        "question_params": Parameter(
            type="string",
            description="""
                The specific parameters required for the question to be answered with the question_intent
                or none if no params required
            """,
        ),
        "aggregation": Parameter(
            type="string",
            description="Any aggregation that is required to answer the question or none if no aggregation is needed",
        ),
        "sort_order": Parameter(
            type="string",
            description="The order a list should be sorted in or none if no sort_order is needed",
        ),
        "timeframe": Parameter(
            type="string",
            description="string of the timeframe to be considered or none if no timeframe is needed",
        ),
    },
)
def generate_query(question_intent, operation, question_params, aggregation, sort_order, timeframe) -> str:
    details_to_create_cypher_query = engine.load_prompt(
        "details-to-create-cypher-query",
        question_intent=question_intent,
        operation=operation,
        question_params=question_params,
        aggregation=aggregation,
        sort_order=sort_order,
        timeframe=timeframe,
    )
    llm_query = call_model(generate_cypher_query_prompt, details_to_create_cypher_query)
    json_query = to_json(llm_query)
    logger.info("Cypher generated by the LLM: ")
    logger.info(llm_query)
    if json_query["query"] == "None":
        return "No database query"
    db_response = execute_query(json_query["query"])
    logger.info(db_response)
    return str(db_response)


@agent(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries.",
    tools=[generate_query],
)
class DatastoreAgent(Agent):
    pass
