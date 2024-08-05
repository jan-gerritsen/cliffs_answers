from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
import logging


def process_llm_response(llm_response) -> str:
    logging.debug(llm_response['result'])
    logging.debug('\n\nSources:')
    for source in llm_response["source_documents"]:
        logging.debug(source.metadata['source'])
    return llm_response['result']


def retrieve_and_respond(query: str) -> str:
    qa_chain = RetrievalQA.from_chain_type(llm=llm_open,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True,
                                           verbose=True)  # set to True for more debug info
    llm_response = qa_chain(query)
    return process_llm_response(llm_response)


# initialize connection to Chroma
# Ollama embeddings
embeddings_open = OllamaEmbeddings(model="Llama2")
llm_open = Ollama(model='Llama2',
                  callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

persist_directory = 'chroma_data'

vectordb = Chroma(
    collection_name='my_collection',
    persist_directory=persist_directory,
    embedding_function=embeddings_open
)
retriever = vectordb.as_retriever()

if __name__ == "__main__":
    while True:
        text = input("Ask me anything: ")
        answer = retrieve_and_respond(text)
        print(answer)
