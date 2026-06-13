from crewai.tools import tool

from my_project.rag import retrieve_context


@tool("Case Retrieval Tool")
def case_retrieval_tool(query: str) -> str:
    """
    Retrieve relevant evidence from uploaded documents.
    """

    return retrieve_context(query)