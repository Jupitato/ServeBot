# 原始文档清洗
from llama_index.core.schema import TransformComponent

from src.backend.serve_bot.rag.document.clean.doc_html_clean import clean_html


class DocumentsCleaner(TransformComponent):
    """
        文档清洗和处理，提升文档质量（语义相关，去重复等）
    """

    def __call__(self, nodes, **kwargs):
        for doc in nodes:
            if doc.metadata["file_type"] == "text/html":
                doc.set_content(clean_html(doc.text))
            elif doc.metadata["file_type"] == "'application/pdf'":
                continue
        return nodes
