from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace


def prepare_embedding_model():
    model_name = "./bge-m3"
    model_kwargs = {'device': 'cuda:0'}
    encode_kwargs = {'normalize_embeddings': True}
    hf_embedding = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf_embedding


def prepare_llm_model():
    llm = HuggingFacePipeline.from_model_id(
        model_id="./Qwen2-0.5B-Instruct/",
        task="text-generation",
        pipeline_kwargs=dict(
            max_new_tokens=512,
            do_sample=False,
            token=False
        ),
        device=0,
    )
    chat_model = ChatHuggingFace(llm=llm, token=False)
    return chat_model


chat_model = prepare_llm_model()
hf_embedding = prepare_embedding_model()

path = "./heishenhua_sub.txt"

def encode_data(path, chunk_size=1000, chunk_overlap=200):
    loader = TextLoader(path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    texts = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(texts, hf_embedding)
    return vectorstore


chunks_vector_store = encode_data(path, chunk_size=1000, chunk_overlap=200)
chunks_query_retriever = chunks_vector_store.as_retriever(search_kwargs={"k": 2})

test_query = "白衣秀士攻略"
docs = chunks_query_retriever.get_relevant_documents(test_query)
context = [doc.page_content for doc in docs]


qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", """使用以下上下文来回答最后的问题。
如果您不知道答案，就说您不知道，不要试图编造答案。

{context}

Question: {question}

答案:"""),
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": chunks_query_retriever | format_docs, "question": RunnablePassthrough()}
    | qa_prompt
    | chat_model
    | StrOutputParser()
)

for chunk in rag_chain.stream(test_query):
    print(chunk, end="", flush=True)