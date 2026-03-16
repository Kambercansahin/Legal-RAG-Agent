from graph.node_constants import RETRIEVE,GENERATE,WEBSEARCH,GRADE_DOCUMENTS,REFUSE
from graph.nodes import generation,grade_documents,web_search,retrieve
from graph.chains.router import Router,question_chain
from graph.state import  GraphState
from graph.chains.hallucination_for_generation import hallucination_chain
from graph.chains.answer_grade import answer_chain
from langgraph.graph import END,StateGraph
from graph.nodes.out_of_scope import refuse_general_question
from dotenv import load_dotenv

load_dotenv()


def decided_to_generate(state:GraphState):
    if state["web_search"]:
        print("Websearch")
        return  WEBSEARCH
    else:
        return GENERATE

def grade_generation_documents_and_question(state:GraphState) -> str:
    print("Check Hallucination")
    question = state["question"]
    documents = state["documents"]
    generate = state["generation"]

    score = hallucination_chain.invoke(
        {"documents":documents ,"generation":generate}
    )

    if is_hallucination_free := score.binary_score:

        print("Generation is grounded in Documents")
        ans_score = answer_chain.invoke({"question":question,"generation":generate})
        if is_answer_useful:=ans_score.binary_score:
            print("Generation Address Question")
            return "useful"
        else:
            print("Generation does not address the question")
            return "not useful"
    else:
        print("Generation is not Grounded in Documents")
        return  "not supported"


def route_question(state:GraphState) -> str:
    print("Route Question")
    question = state["question"]
    source = question_chain.invoke({"question":question})
    if source.datasource == "out_of_scope":
        print("Out Of scope")
        return "out_of_scope"
    elif source.datasource == "websearch":
        print("Web Search")
        return WEBSEARCH
    else:
        return RETRIEVE



workflow=StateGraph(GraphState)

workflow.add_node(RETRIEVE,retrieve)
workflow.add_node(GRADE_DOCUMENTS,grade_documents)
workflow.add_node(GENERATE,generation)
workflow.add_node(WEBSEARCH,web_search)
workflow.add_node(REFUSE, refuse_general_question)

workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH:WEBSEARCH,
        RETRIEVE:RETRIEVE,
        "out_of_scope": REFUSE,
    }
)
workflow.add_edge(RETRIEVE,GRADE_DOCUMENTS)
workflow.add_edge(REFUSE, END)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decided_to_generate,
    {
        WEBSEARCH:WEBSEARCH,
        GENERATE:GENERATE
     }
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_documents_and_question,
    {
        "not supported":GENERATE,
        "useful": END,
        "not useful" : WEBSEARCH
    }

)

workflow.add_edge(WEBSEARCH,GENERATE)
workflow.add_edge(GENERATE,END)

app =workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")
