from graph.state import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import  load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature=0
)


def refuse_general_question(state: GraphState):
    print("---REFUSE---")

    system_prompt = """
    You are a legal assistant. Whatever language the user's question is in (Turkish or English),

    provide the appropriate rejection message ONLY in that language. Do not provide any additional explanations.

    TR Mesajı: Ben Berta Hukuk Bürosu için özelleşmiş bir hukuk asistanıyım. Sadece hukuki konularda yardımcı olabilirim.
    EN Mesajı: I am a specialized legal assistant for Berta Law Firm. I can only assist with legal matters.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    chain = prompt | llm


    response = chain.invoke({"question": state["question"]})

    return {"generation": response.content}
