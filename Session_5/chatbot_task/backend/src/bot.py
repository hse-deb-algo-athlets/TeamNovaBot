import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.memory import ConversationBufferMemory
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.load.serializable import Serializable
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chromadb.api import ClientAPI
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from uuid import uuid4
from typing import List
import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# TODO: Implement the functions of the CustomChatBot Class. Use the knowledge and code from Session_4
# (Implementieren Sie die Funktionen der CustomChatBot-Klasse. Nutzen Sie das Wissen und dem Code von Session_4)

class CustomChatBot:
    """
    A class representing a chatbot that uses a ChromaDB client for document retrieval
    and the ChatOllama model for generating answers.

    This chatbot uses a retrieval-augmented generation (RAG) pipeline where it retrieves
    relevant information from a custom document database (ChromaDB) and then generates
    concise answers using a language model (ChatOllama).
    """

    def __init__(self, index_data: bool) -> None:
        """
        Initialize the CustomChatBot class by setting up the ChromaDB client for document retrieval
        and the ChatOllama language model for answer generation.
        """
        # Initialize the embedding function for document retrieval
        self.embedding_function = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2", cache_folder = "/embedding_model")
        
        # Initialize the ChromaDB client
        self.client = self._initialize_chroma_client()
        
        # Get or create the document collection in ChromaDB
        self.vector_db = self._initialize_vector_db()

        # Process pdf, embedd data and index to ChromaDB
        if index_data:
            self._index_data_to_vector_db()

        # Initialize the document retriever
        self.retriever = self.vector_db.as_retriever(k = 3)

        # Initialize the large language model (LLM) from Ollama
        # TODO: ADD HERE YOUR CODE ================================================================================
        model = "llama3.2:1"
        self.llm = ChatOllama(model = model) #!?

        # Set up the retrieval-augmented generation (RAG) pipeline
        self.qa_rag_chain = self._initialize_qa_rag_chain()

    def _initialize_chroma_client(self) -> ClientAPI:
        """
        Initialize and return a ChromaDB HTTP client for document retrieval.

        Returns:
            chromadb.HttpClient: A client used to communicate with ChromaDB.
        """
        logger.info("Initialize chroma db client.")

        # TODO: ADD HERE YOUR CODE =================================================================================
        client   = chromadb.HttpClient(
            host     = "localhost",
            port     = 8000,
            ssl      = False,
            headers  = None,
            settings = Settings(allow_reset=True, anonymized_telemetry = False),
            tenant   = DEFAULT_TENANT,
            database = DEFAULT_DATABASE,
        )
        return client

    def _initialize_vector_db(self) -> Chroma:
        """
        Initialize and return a Chroma vector database using the HTTP client.

        Returns:
            Chroma: A vector database instance connected to the document collection in ChromaDB.
        """
        logger.info("Initialize chroma vector db.")

        # TODO: ADD HERE YOUR CODE =================================================================================
        collection = self.client.get_or_create_collection("ChatBot_Collection")
        vector_db = Chroma(
            client             = self.client,
            collection_name    = collection.name,
            embedding_function = self.embedding_function)

        return vector_db

    def _index_data_to_vector_db(self):

        # TODO: ADD HERE YOUR CODE =================================================================================
        text = "This is a test document."
        query_vector = text

        pdf_doc = "./AI_Book.pdf"

        loader = PyPDFLoader(
        file_path = pdf_doc,
        # passwort = "my-passwort"
        extract_images = False,)

        pages_chunked = RecursiveCharacterTextSplitter().split_documents(documents = loader.load())

        def clean_text(text):
            # Remove surrogate pairs
            text = re.sub(r'[\ud800-\udfff]', '', text)
            # Optionally remove non-ASCII characters (depends on your use case)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            return text

        def clean_and_create_document(chunk):
            cleaned_text = clean_text(chunk.page_content)
            return Document(page_content = cleaned_text, metadata = chunk.metadata)

        pages_chunked_cleaned1 = [clean_and_create_document(chunk) for chunk in pages_chunked]
        pages_chunked_cleaned = [clean_text(chunk.page_content) for chunk in pages_chunked]

    def _initialize_qa_rag_chain(self) -> RunnableSerializable[Serializable, str]:
        """
        Set up the retrieval-augmented generation (RAG) pipeline for answering questions.
        
        The pipeline consists of:
        - Retrieving relevant documents from ChromaDB.
        - Formatting the retrieved documents for input into the language model (LLM).
        - Using the LLM to generate concise answers.
        
        Returns:
            dict: The RAG pipeline configuration.
        """

        # TODO: ADD HERE YOUR CODE =================================================================================
        prompt_template = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        <context>
        {context}
        </context>
        Answer the following question: {question}"""

        rag_prompt = ChatPromptTemplate.from_template(prompt_template)

        retriever = self.vector_db.as_retriever()

        qa_rag_chain = ({"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )
        return qa_rag_chain # ??????????????????????

    def _format_docs(self, docs: List[Document]) -> str:
        """
        Helper function to format the retrieved documents into a single string.
        
        Args:
            docs (List[Document]): A list of documents retrieved by ChromaDB.

        Returns:
            str: A string containing the concatenated content of all retrieved documents.
        """

        # TODO: ADD HERE YOUR CODE =================================================================================
        return "\n\n".join(doc.page_content for doc in docs)

    async def astream(self, question: str):
        """
        Handle a user query asynchronously by running the question through the RAG pipeline and stream the answer.

        Args:
            question (str): The user's question as a string.

        Yields:
            str: The generated answer from the model, streamed chunk by chunk.
        """
        logger.info("Streaming RAG chain response.")
        try:
            async for chunk in self.qa_rag_chain.astream(question):
                logger.debug(f"Yielding chunk: {chunk}")
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream_answer: {e}", exc_info=True)
            raise