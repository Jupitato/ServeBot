import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from pydantic import SecretStr

# 加载 .env 文件中的环境变量
load_dotenv()


if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = '123'

if "OLLAMA_DEBUG" not in os.environ:
    os.environ["OLLAMA_DEBUG"] = "1"




def getLLM(model="deepseek-r1:8b"):
    llm = ChatOllama(
        model=model,
        temperature=0)


    # from langchain_community.llms import VLLM
    # llm = VLLM(
    #     model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    #     trust_remote_code=True,  # mandatory for hf models
    #     max_new_tokens=128,
    #     top_k=10,
    #     top_p=0.95,
    #     temperature=0.8,
    # )
    # llm = ChatDeepSeek(
    #     model="deepseek-chat",
    #     temperature=0,
    #     max_tokens=512,
    #     timeout=None,
    #     max_retries=2,
    #     api_key=SecretStr(os.getenv("DEEPSEEK_API_KEY", "")) if os.getenv("DEEPSEEK_API_KEY") else SecretStr(""),
    #     # other params...
    # )
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


if __name__ == "__main__":
    pass
