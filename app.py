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

# Load Existing Index

from langchain_pinecone import PineconeVectorStore
docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name
)

# question_answer_chain = RunnablePassthrough() | prompt | chatModel | StrOutputParser()
rag_chain = {
   "context": retriever,
   "input": RunnablePassthrough()
} | prompt | chatModel | StrOutputParser()


system_prompt = (
    "You are an Machine Learning assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])