import asyncio

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph

from src.backend.serve_bot.chat_manage.chat_state import ChatState
from src.backend.serve_bot.common.logging import init_logging
from src.backend.serve_bot.llm_manage.llm_provider import getLLM
from src.backend.serve_bot.workflow.agents.business_logic_process import BusinessLogicProcessAgent
from src.backend.serve_bot.workflow.agents.human_interrupt import HumanInterruptAgent
from src.backend.serve_bot.workflow.agents.intent_recognition import IntentRecognitionAgent
from src.backend.serve_bot.workflow.agents.key_information_extraction import KeyInformationExtractionAgent
from src.backend.serve_bot.workflow.agents.knowledge_faq import KnowledgeFaqAgent
from src.backend.serve_bot.workflow.agents.prompt_security import PromptSecurityAgent


class ServeBot:
    def __init__(self, user_id: str):
        self.llm = getLLM(model="deepseek-r1:14b")
        self.user_id = user_id
        memory = MemorySaver()
        agents = self._init_all_agents()
        self.graph = agents.compile(checkpointer=memory)

        # display_graph(self.graph)

    def _init_all_agents(self):
        agents = self._initialize_agents()
        return self._create_workflow(agents)

    async def run_chat(self, task_id: str, prompt: str):
        self.task_id = task_id
        config = {
            "configurable": {
                "thread_id": self.task_id,
                "user_id": self.user_id
            }
        }
        self.graph.config = config

        result = await self.graph.ainvoke({"prompt": prompt}, config=config)
        return result

    def _initialize_agents(self):
        return {
            "PromptSecurityAgent": PromptSecurityAgent(llm=self.llm),
            "IntentRecognitionAgent": IntentRecognitionAgent(llm=self.llm),
            "KeyInformationExtractionAgent": KeyInformationExtractionAgent(llm=self.llm),
            "BusinessLogicProcessAgent": BusinessLogicProcessAgent(llm=self.llm),
            "HumanInterruptAgent": HumanInterruptAgent(llm=self.llm),
            "KnowledgeFaqAgent": KnowledgeFaqAgent(llm=self.llm)
        }

    def _create_workflow(self, agents):
        workflow = StateGraph(ChatState)

        workflow.add_node("PromptSecurityAgent", agents["PromptSecurityAgent"].run)
        workflow.add_node("IntentRecognitionAgent", agents["IntentRecognitionAgent"].run)
        workflow.add_node("KeyInformationExtractionAgent", agents["KeyInformationExtractionAgent"].run)
        workflow.add_node("BusinessLogicProcessAgent", agents["BusinessLogicProcessAgent"].run)
        workflow.add_node("HumanInterruptAgent", agents["HumanInterruptAgent"].run)
        workflow.add_node("KnowledgeFaqAgent", agents["KnowledgeFaqAgent"].run)
        workflow.add_edge(START, "PromptSecurityAgent")


        return workflow


init_logging()


async def main():
    bot = ServeBot(user_id="luxun")
    result = await bot.run_chat(task_id="111", prompt="凯美瑞汽车支持L3驾驶吗")
    state = bot.graph.get_state(config={"configurable": {"thread_id": "111"}})
    print("回答用户:" + result["response_content"])


if __name__ == "__main__":
    asyncio.run(main())
