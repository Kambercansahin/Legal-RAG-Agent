from VectorDB import retriver
from graph.state import GraphState
from typing import Dict,Any


def retrieve(state:GraphState) -> Dict[str,Any]:
    question = state["question"]
    documents = retriver.invoke(question)
    return {"question":question,"documents":documents}