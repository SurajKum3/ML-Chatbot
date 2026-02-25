from typing import List
from langchain_core.documents import Document

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        minimal_doc = Document(
            page_content=doc.page_content,
            metadata={"source": doc.metadata.get("source")}
        )
        minimal_docs.append(minimal_doc)
    return minimal_docs

# Chunking

def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk

# Database
from pinecone import ServerlessSpec

index_name = "machine-learning-chatbot"
if not pc.has_index(index_name):
    pc.create_index(name=index_name, dimension=384, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1"))

index = pc.Index(index_name)