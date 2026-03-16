from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader,PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import bs4
import os

load_dotenv()

urls = [
    "https://bertahukuk.com/en/about/",
    "https://bertahukuk.com/en/services/",
    "https://bertahukuk.com/en/#home",
    "https://bertahukuk.com/tr/",
    "https://bertahukuk.com/tr/hakkimizda/",
    "https://bertahukuk.com/tr/hizmetler/",
    "https://bertahukuk.com/tr/hizmet/ticaret-hukuku/",
    "https://bertahukuk.com/tr/hizmet/sozlesmeler/",
    "https://bertahukuk.com/tr/hizmet/icra-alacak/",
    "https://bertahukuk.com/tr/hizmet/gayrimenkul/",
    "https://bertahukuk.com/tr/hizmet/is-hukuku/",
    "https://bertahukuk.com/tr/hizmet/hukuki-danismanlik/",
    "https://bertahukuk.com/tr/hizmet/sigorta-hukuku/",
    "https://bertahukuk.com/tr/hizmet/yabancilar-hukuku/",
    "https://bertahukuk.com/tr/hizmet/idare-hukuku/",
    "https://bertahukuk.com/tr/hizmet/aile-hukuku/",
    "https://bertahukuk.com/tr/hizmet/ceza-hukuku/",
    "https://bertahukuk.com/en/service/commercial-law/",
    "https://bertahukuk.com/en/service/contracts/",
    "https://bertahukuk.com/en/service/debt-collection/",
    "https://bertahukuk.com/en/service/real-estate/",
    "https://bertahukuk.com/en/service/labor-law/",
    "https://bertahukuk.com/en/service/legal-consultancy/",
    "https://bertahukuk.com/en/service/insurance-law/",
    "https://bertahukuk.com/en/service/immigration-law/",
    "https://bertahukuk.com/en/service/administrative-law/",
    "https://bertahukuk.com/en/service/family-law/",
    "https://bertahukuk.com/en/service/criminal-law/",
    "https://bertahukuk.com/en/team/",
    "https://bertahukuk.com/en/team/talip-sahin/",
    "https://bertahukuk.com/en/team/berna-sahin/",
    "https://bertahukuk.com/en/contact/",
    "https://bertahukuk.com/tr/ekip/",
    "https://bertahukuk.com/tr/ekip/talip-sahin/",
    "https://bertahukuk.com/tr/ekip/berna-sahin/",
    "https://bertahukuk.com/tr/iletisim/",
]

docs = [WebBaseLoader(url).load() for url in urls]

docs_list = []
for sublist in docs:
    for item in sublist:
        docs_list.append(item)

pdf_loader = PyPDFLoader("data/Berta_Rehber.pdf")
pdf_docs = pdf_loader.load()
docs_list.extend(pdf_docs)


text_spliter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)

spliter=text_spliter.split_documents(docs_list)

vectore_store=Chroma.from_documents(
    documents=spliter,
    embedding=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"),
    persist_directory="./.chroma",
)

retriver = Chroma(
    embedding_function= GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"),
    persist_directory="./.chroma",
).as_retriever()

if __name__ == "__main__":
    pass


