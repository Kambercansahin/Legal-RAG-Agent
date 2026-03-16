from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel,Field

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature=0
)

class GradeHallucination(BaseModel):
    """ Binary score for Hallucination present in generated answer."""

    binary_score : bool = Field(
        description="Answer is grounded in the facts 'yes' or 'no'"
    )

structured_llm= llm.with_structured_output(GradeHallucination)

system_prompt = """
You are a professional legal auditor specializing in 'Groundedness'. 
Your job is to verify if an LLM-generated answer is logically based on the provided facts.

### RULES:
1. (EN) Meaning over Words: If the generation says the same thing as the documents using different professional words, it is GROUNDED (yes).
   (TR) Kelimeler değil anlam önemli: Eğer yanıt dökümandaki bilgiyi farklı hukuki terimlerle anlatıyorsa bu bir halüsinasyon DEĞİLDİR (yes).
2. (EN) Fact Check: Only score 'no' if the answer includes names, dates, law numbers, or specific legal rules NOT present in the documents.
   (TR) Sadece dökümanda hiç geçmeyen isim, tarih, kanun maddesi veya kural eklendiyse 'no' puanı ver.
3. (EN) Intro Sentences: Phrases like "According to Berta Law..." or "Based on the documents..." are acceptable and should not be penalized.
   (TR) "Berta Hukuk'a göre..." gibi giriş cümleleri halüsinasyon sayılmaz.

SCORING:
- 'yes': The logic and facts are in the documents.
- 'no': The answer adds NEW legal facts or contradicts the documents.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","DOCUMENTS:{documents}  LLM Generation: {generation}")
    ]
)

hallucination_chain = prompt |structured_llm


