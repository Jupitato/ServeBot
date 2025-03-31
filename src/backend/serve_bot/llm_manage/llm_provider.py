import os

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = '123'

if "OLLAMA_DEBUG" not in os.environ:
    os.environ["OLLAMA_DEBUG"] = "1"


def getLLM(model="deepseek-r1:8b"):
    from langchain_ollama import ChatOllama
    llm = ChatOllama(
        model=model,
        temperature=0,
    )
    return llm


def getEmbedding(provider="langchain"):
    if provider == "langchain":
        from langchain_ollama import OllamaEmbeddings
        # 向量的维数如何设置？
        embeddings_model = OllamaEmbeddings(model="quentinz/bge-large-zh-v1.5")
        return embeddings_model
    elif provider == "llamaindex":
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        embeddings = HuggingFaceEmbedding(
            model_name="BAAI/bge-m3"
        )
        return embeddings
    raise RuntimeError("不支持的provider")
