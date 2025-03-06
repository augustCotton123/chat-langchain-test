from langchain_community.vectorstores import Chroma
from ingest import get_embeddings_model
import os

from langchain_community.llms import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate


llm = Ollama(model="llama3.2")

COLLECTION_NAME = os.environ["COLLECTION_NAME"]

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=get_embeddings_model(),
    persist_directory="./chroma_chat_langchain_test_db",
)

retriever = vectorstore.as_retriever(search_kwargs=dict(k=1))
# print(len(retriever.invoke("did marcos graduate from oxford")))

promptTemplate = PromptTemplate.from_template(
    """
    You are an assistant who is very good at searching documents. If you do not have an answer from the provided information, say sorry.
    {input}
            Context: {context}
            Answer:
"""
)
document_prompt = PromptTemplate(
    input_variables=["page_content", "claim_author"],
    template="{page_content}\n\n\nClaim Author: {claim_author}"
)
documentChain = create_stuff_documents_chain(llm, promptTemplate, document_prompt=document_prompt)
retrieverChain = create_retrieval_chain(retriever, documentChain)

print(retrieverChain.invoke({"input":"who made the claim that the bataan power plant will be reopened?"}))
