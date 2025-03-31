import logging

from llama_index.core import Settings, PropertyGraphIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import PyMuPDFReader

from src.backend.serve_bot.rag.context import MyStorageContext, init_rag_settings
from src.backend.serve_bot.rag.document.clean.doc_clean import DocumentsCleaner

logger = logging.getLogger(__name__)

required_exts = [".html", ".pdf"]
# 需要和使用的嵌入模型的维度一致
dim = 1024

file_extractor = {
    # UnstructuredReader()
    ".pdf": PyMuPDFReader(),
}


def documents_load(directory: str, department: str):
    documents = SimpleDirectoryReader(
        input_dir=directory,
        required_exts=required_exts,
        recursive=True,
        filename_as_id=True,
        file_extractor=file_extractor,  # 不同文件类型使用不同的解析器
    ).load_data()
    for doc in documents:
        doc.metadata["department"] = department
    return documents


def add_documents_to_vector_store(documents, storage_context, embed_model):
    # 整个pipeline包括读取文档、分块、元数据提取、嵌入生成和存储到向量数据库
    pipeline = IngestionPipeline(
        transformations=[
            DocumentsCleaner(),
            # SentenceWindowNodeParser.from_defaults(window_size=3),
            SentenceSplitter(chunk_size=1024, chunk_overlap=100),
            # TitleExtractor(),  # 通过llm提出标题添加到metadata中
            embed_model
        ],
        vector_store=storage_context.vector_store,
        docstore=storage_context.docstore,
        docstore_strategy="upserts_and_delete"  # 感知删除更新和删除文档
    )
    nodes = pipeline.run(documents=documents, show_progress=True, num_workers=1)

    logger.info(f"Ingested {len(nodes)} Nodes")


def add_documents_to_graph_store(documents, graph_store, llm):
    kg_extractor = SimpleLLMPathExtractor(llm=llm)

    # 对文档进行清洗
    cleaner = DocumentsCleaner()
    cleaned_documents = cleaner(documents)

    index = PropertyGraphIndex.from_documents(
        cleaned_documents,
        embed_model=Settings.embed_model,
        kg_extractors=[
            kg_extractor
        ],
        property_graph_store=graph_store,
        show_progress=True,
    )


if __name__ == "__main__":
    storage_context = MyStorageContext.storageContext()
    init_rag_settings()
    # 保存文档增加部门信息
    docs = documents_load("/Users/luxun/Desktop/car/", "hr")
    add_documents_to_vector_store(documents=docs, storage_context=storage_context, embed_model=Settings.embed_model)
