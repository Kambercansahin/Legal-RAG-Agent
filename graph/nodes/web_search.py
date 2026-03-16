from typing import Any,Dict


from graph.state import  GraphState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document
from dotenv import load_dotenv
load_dotenv()
web_search_tool = TavilySearchResults(k=5)

def web_search(state:GraphState) ->Dict[str,Any]:
    question = state["question"]
    documents = state["documents"] if state["documents"] is not None else []

    legal_query = f"{question} (site:gov.tr OR site:org.tr OR site:lexpera.com.tr)"
    docs = web_search_tool.invoke({"query":legal_query})

    allowed_domains = [
        "mevzuat.gov.tr",
        "resmigazete.gov.tr",
        "barobirlik.org.tr",
        "adalet.gov.tr",
        "yargitay.gov.tr",
        "danistay.gov.tr",
        "anayasa.gov.tr",
        "sozluk.adalet.gov.tr",
        "https://www.tbb.gov.tr/tr/tc-cumhurbaskanligi-mevzuat-bilgi-sistemi",
        "https://bertahukuk.com/tr/",
        "https://bertahukuk.com/en/"
    ]

    web_results = []
    for d in docs:
        source_url = d["url"].lower()
        if any(domain in source_url for domain in allowed_domains):
            new_doc = Document(
                page_content=d["content"],
                metadata={"source": d["url"]}
            )
            web_results.append(new_doc)
            print(f"--- Allowed: {source_url}")
        else:

            print(f"--- REFUSE----): {source_url}")
    documents.extend(web_results)

    return {"documents": documents, "question": question}




