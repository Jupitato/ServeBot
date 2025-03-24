import logging
from typing import Optional, Dict, Any, List

from llama_index.core import BaseCallbackHandler
from llama_index.core.callbacks import CBEventType

logger = logging.getLogger(__name__)


class LLMLogger(BaseCallbackHandler):
    def __init__(
            self,
            event_starts_to_ignore: Optional[List[CBEventType]] = None,
            event_ends_to_ignore: Optional[List[CBEventType]] = None,
    ):
        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore or [],
            event_ends_to_ignore=event_ends_to_ignore or [],
        )

    def on_event_start(
            self,
            event_type: CBEventType,
            payload: Optional[Dict[str, Any]] = None,
            **kwargs: Any
    ) -> None:
        if event_type == CBEventType.LLM:
            request = payload.get("messages", "")
            logger.info(f"\n=== LLM 输入 ===\n{request.text if hasattr(request, 'text') else request}")

    def on_event_end(
            self,
            event_type: CBEventType,
            payload: Optional[Dict[str, Any]] = None,
            **kwargs: Any
    ) -> None:
        if event_type == CBEventType.LLM:
            response = payload.get("response", "")
            logger.info(f"\n=== LLM 输出 ===\n{response.text if hasattr(response, 'text') else response}")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """Run when an overall trace is launched."""

    pass

    def end_trace(
            self,
            trace_id: Optional[str] = None,
            trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Run when an overall trace is exited."""

    pass
