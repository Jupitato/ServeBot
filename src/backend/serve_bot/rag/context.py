from llama_index.core import StorageContext, Settings
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.graph_stores.neo4j import Neo4jPGStore
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.vector_stores.milvus import MilvusVectorStore

from src.backend.serve_bot.llm_manage.llm_provider import getLLM, getEmbedding
from src.backend.serve_bot.rag.trace.llm_logger import LLMLogger


class _MyStorageContext:
    _storage_context = None

    def storageContext(self):
        if self._storage_context is None:
            # doc_store = get_doc_store()
            vector_store = get_vector_store()
            # graph_store = get_graph_store()
            self._storage_context = StorageContext.from_defaults(
                vector_store=vector_store
            )
        return self._storage_context


def get_doc_store():
    store = RedisDocumentStore.from_host_and_port(
        "localhost", 6379
    )
    return store


def get_graph_store():
    graph_store = Neo4jPGStore(
        username="neo4j",
        password="12345678",
        url="bolt://localhost:7689",
    )
    return graph_store


dim = 1024


def get_vector_store():
    vector_store = MilvusVectorStore(
        uri="/Users/luxun/workspace/ai/mine/project/ServeBot/.tmp/db/milvus.db", overwrite=False, dim=dim
    )
    return vector_store


def init_rag_settings():
    Settings.llm = getLLM()
    Settings.embed_model = getEmbedding(provider="llamaindex")
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    llm_logger = LLMLogger()
    Settings.callback_manager = CallbackManager([llama_debug, llm_logger])
    return Settings


# 单例
MyStorageContext = _MyStorageContext()
