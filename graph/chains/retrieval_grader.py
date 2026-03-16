from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel,Field
from VectorDB import retriver

load_dotenv()

llm = ChatGoogleGenerativeAI(temperature=0,model="gemini-2.5-flash")

class Grade(BaseModel):
    """ Binary score for relevance check on  retrieved documents"""

    binary_score:str =Field(
        description="Documents are relevant to the question 'yes' or 'no'"
    )

structure_llm=llm.with_structured_output(Grade)

system_prompt="""
You are a grader assessing relevance of a retrieved document to a user question. 
If the document contains content related to the user question, grade it as relevant. 
It does not need to be a perfect answer. The goal is to filter out clearly irrelevant documents.
Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.

Critical Rule: If the document mentions the name of a person or a legal practice area requested in the question, ALWAYS say 'yes'
"""

grade_prompt = ChatPromptTemplate(
    [
        ("system",system_prompt),
        ("human","Retrieve Documents:{document} User question:{question}"),
    ]
)

grade_chain = grade_prompt | structure_llm


if __name__ == "__main__":
    pass
