import asyncio

from backend.serve_bot.chat_manage.chat_state import ChatState
from backend.serve_bot.common.utils.display_graph import display_graph
from backend.serve_bot.llm_manage.llm_provider import getLLM
from backend.serve_bot.workflow.agents.action_runner import ActionRunnerAgent
from backend.serve_bot.workflow.agents.dialogue_policy import DialoguePolicyAgent
from backend.serve_bot.workflow.agents.intent_recognition import IntentRecogintionAgent
from backend.serve_bot.workflow.agents.prompt_security import PromptSecurityAgent
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver

class ServeBot:
    def __init__(self, task: dict, user_id: str):
        self.task = task
        self.llm = getLLM()
        self.user_id = user_id
        memory = MemorySaver() 
        agents = self._init_all_agents()
        self.graph = agents.compile(checkpointer=memory)
        display_graph(self.graph)

    def _init_all_agents(self):
        agents = self._initialize_agents()
        return self._create_workflow(agents)

    async def run_chat(self, task_id: str):
        self.task_id = task_id
        config = {
            "configurable": {
                "thread_id": self.task_id,
                "user_id": self.user_id
            }
        }
        self.graph.config = config

        result = await self.graph.ainvoke({"task": self.task}, config=config)
        return result

    def _initialize_agents(self):
        return {
            "PromptSecurityAgent": PromptSecurityAgent(llm=self.llm),
            "DialoguePolicyAgent": DialoguePolicyAgent(llm=self.llm),
            "ActionRunnerAgent": ActionRunnerAgent(llm=self.llm),
            "IntentRecogintionAgent": IntentRecogintionAgent(llm=self.llm)
        }

    def _create_workflow(self, agents):
        workflow = StateGraph(ChatState)

        workflow.add_node("PromptSecurityAgent", agents["PromptSecurityAgent"].run)
        workflow.add_node("DialoguePolicyAgent", agents["DialoguePolicyAgent"].run)
        workflow.add_node("ActionRunnerAgent", agents["ActionRunnerAgent"].run)
        workflow.add_node("IntentRecogintionAgent", agents["IntentRecogintionAgent"].run)
        workflow.add_edge(START, "PromptSecurityAgent")
        return workflow


async def main():
    bot = ServeBot({"prompt": "如何使用华为M50手机"}, user_id="luxun")
    result = await bot.run_chat()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())