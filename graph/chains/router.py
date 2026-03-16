from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel,Field
from typing import Literal
import time

load_dotenv()
class Router(BaseModel):
    """Route a user query to the most relevant datasource"""

    datasource:Literal["vectorstore","websearch","out_of_scope"]=Field(
        ...,
        description="Choose 'vectorstore' for Berta Law info, 'websearch' for general law, and 'out_of_scope' for non-legal/general topics. "
    )


llm = ChatGoogleGenerativeAI(temperature=0,model="gemini-2.5-flash")

structure_LLM = llm.with_structured_output(Router)


system_prompt = """
You are the strategic router for Berta Law Firm. Your job is to classify the user's question.

ROUTE TO VECTORSTORE IF:
- About Berta Law Firm (contact, location, services).
- Questions about hiring the firm or specific practice areas.
- The question is about Berta Law Firm (contact, location, services).
- The question is about specific legal definitions or practice areas (e.g., "Ceza Hukuku nedir?", "İcra hukuku nedir?", "Ticaret hukuku"). 
- We now have a 'Legal Knowledge Base' inside our vectorstore for these definitions.
- The question is about Talip Şahin or Berna Şahin.

ROUTE TO 'websearch' ONLY IF:
- The question is about a specific court case from TODAY or very recent changes in the Official Gazette (Resmi Gazete).
- The question is a complex legal scenario that is definitely NOT in our internal handbook.

ROUTE TO 'out_of_scope' IF:
- The question mentions any person OTHER than Talip Şahin or Berna Şahin.
- The question is NOT related to law (e.g., weather, sports, cooking).

KEY GUIDELINE:
If the question is about a general law field definition (Ceza, Aile, İş Hukuku vb.), ALWAYS check 'vectorstore' first.
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{question}")
]
)

question_chain = route_prompt | structure_LLM

