from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel,Field
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

class AnswerGrade(BaseModel):
    """Binary score to assess if answer addresses question."""
    binary_score:bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

structer_llm = llm.with_structured_output(AnswerGrade)

system_prompt="""
ROLE
You are a 'Response Quality Auditor'. Your task is to evaluate if the generated answer fully addresses the user's specific question.
Sen bir 'Yanıt Kalitesi Denetçisi'sin. Görevin, üretilen yanıtın kullanıcının özel sorusunu tamamen yanıtlayıp yanıtlamadığını değerlendirmektir.

 EVALUATION CRITERIA / DEĞERLENDİRME KRİTERLERİ:
1. (EN) Does the answer directly address the user's intent?
   (TR) Yanıt doğrudan kullanıcının niyetini/sorusunu karşılıyor mu?
2. (EN) Is the answer useful and complete for the specific question asked?
   (TR) Yanıt, sorulan özel soru için yararlı ve eksiksiz mi?
3. (EN) If the answer avoids the question or says "I don't know" when information was available, the score is 'no'.
   (TR) Eğer yanıt sorudan kaçıyorsa veya bilgi mevcut olmasına rağmen "bilmiyorum" diyorsa, puan 'no' olmalıdır.

SCORING / PUANLAMA:
- 'yes': The answer is a helpful and direct response to the question. (Yanıt, soruya yardımcı ve doğrudan bir cevaptır.)
- 'no': The answer does not resolve the user's inquiry. (Yanıt, kullanıcının sorusunu çözmüyor/yanıtlamıyor.)
"""

answer_prompt = ChatPromptTemplate(
    [
        ("system",system_prompt),
        ("human","USER QUESTION: {question}  LLM GENERATION: {generation}")
    ]
)

answer_chain= answer_prompt | structer_llm