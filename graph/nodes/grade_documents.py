from typing import Dict,Any


from graph.chains.retrieval_grader import grade_chain
from graph.state import GraphState

def grade_documents(state:GraphState) -> Dict[str,Any]:
    """
    Determine whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search
    Args:
         state(dict):The current state of graph
    Returns:
        state(dict):Filtered out irrelevant documents and updated web_search state
    """
    question = state["question"]
    documents=state["documents"]

    web_search=False

    filtered_doc = []
    for d in documents:
        score = grade_chain.invoke(
            {"question":question,"document":d.page_content}

        )
        grade=score.binary_score

        if grade.lower() == "yes":
            print("---Grade: document Relevant")
            filtered_doc.append(d)
        else:
            print("--Grade: Document not relevant")

            continue
    web_search = True if not filtered_doc else False
    return {"question": question, "documents":filtered_doc, "web_search":web_search }
