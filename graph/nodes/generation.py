from graph.chains.generation import generation_chain
from graph.state import GraphState
from typing import Any,Dict

def generation(state:GraphState) -> Dict[str,Any]:
    question=state["question"]
    documents=state["documents"]
    generation = generation_chain.invoke(
        {"context":documents,"question":question}
    )
    return {"question":question,"documents":documents,"generation":generation}


