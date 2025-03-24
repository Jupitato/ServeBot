import logging
import traceback
from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, interrupt

from src.backend.serve_bot.chat_manage.chat_state import ChatState
from src.backend.serve_bot.common.utils.llm_response_parse import extract_answer
from src.backend.serve_bot.rag.context import MyStorageContext

logger = logging.getLogger(__name__)

storage_context = MyStorageContext.storageContext()


class IntentRecognitionAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, state: ChatState, config: RunnableConfig) -> Command[Literal["KeyInformationExtractionAgent"]]:
        logger.info("IntentRecognitionAgent run: %s ", config["configurable"]["user_id"])

        try:
            messages = [
                SystemMessage(content=IntentRecognitionSystemPrompt),
                HumanMessage(content=state["prompt"])
            ]
            response = await self.llm.ainvoke(messages)

            # 存储对话记录到state
            state.setdefault("messages", []).extend([
                *messages,
                AIMessage(content=response.content)  # 添加AI响应
            ])

            intent, confidence = extract_answer(response.content, ["intent", "confidence"])
            return Command(goto="KeyInformationExtractionAgent", update={"current_intent": intent, "messages": state["messages"]})
        except BaseException:
            traceback_info = traceback.format_exc()
            logger.error(traceback_info)


"""
{
    "model": "deepseek-r1:8b",
    "stream": true,
    "options": {
        "temperature": 0.0
    },
    "messages": [
        {
            "role": "system",
            "content": "You are an expert Q&A system that is trusted around the world.\nAlways answer the query using the provided context information, and not prior knowledge.\nSome rules to follow:\n1. Never directly reference the given context in your answer.\n2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines."
        },
        {
            "role": "user",
            "content": "Context information is below.\n---------------------\nfile_path: /Users/luxun/Desktop/car/全新第9代凯美瑞智能汽油版用户手册-2403版（01999-06272）.pdf\ntotal_pages: 416\nsource: 387\ndepartment: hr\n\n387\n8\n8-2. 定制\n车辆规格\n可通过仪表控制开关更改的设定\n需通过丰田汽车经销商更改的设定\n标记的定义:O = 可用，  = 不可用\n■警报 (P.65)\n■仪表和多信息显示屏 (P.68, 73, 76, 79, 84)\n功能\n定制设定\n使用机械钥匙解锁车门\n时解除警报\n启用、禁用\n\n\nO\n功能\n定制设定\n语言*1\n中文、英文\nO\nO\n\n单位*2\nL/100km、km/L\n\nO\n\n仪表显示类型*1,3\n类型1*4、类型2*4、类型3\n\nO\n\n仪表风格*1,3\n智能、休闲、硬朗、运动\n\nO\n\n仪表风格*1,5\n智能、休闲、运动\n\nO\n\n刻度盘类型*1,6\n转速表、车速表\n\nO\n\n刻度盘类型*1,5\n转速表、车速表、简洁（无刻度\n盘）\n\nO\n\n环保驾驶指示灯*1\n启用、禁用\n\nO\n\n燃油经济性\n平均燃油经济性（重置后）、平均\n燃油经济性（起动后）*3、平均燃\n油经济性（加注燃油后）*5\n\nO\n\n音响系统联动显示*1, 5\n启用、禁用\n\nO\n\n行驶信息项目（第一\n项）*1\n平均车速、距离、已行驶时间\n\nO\n\n行驶信息项目（第二\n项）*1\nB\n\nfile_path: /Users/luxun/Desktop/car/全新第9代凯美瑞智能汽油版用户手册-2403版（01999-06272）.pdf\ntotal_pages: 416\nsource: 80\ndepartment: hr\n\n80\n2-1. 仪表组\n即可显示菜单图标。\n■液晶显示屏\nP.74\n可使用仪表控制开关操作多信\n息显示屏。\n/\n: 选择菜单图标、平\n移画面和移动光标\n/\n: 更改显示内容、平\n移画面和移动光标\n按下: 确定/ 设定\n按住: 重置/ 显示定制项目\n返回上一画面\n去电/ 来电显示\n与免提系统联动，显示去电或来\n电。有关免提系统的详情，请参\n见《导航和多媒体系统用户手\n册》。\n■显示项目\n燃油经济性\n环保驾驶指示器\n■燃油经济性\n显示的值仅供参考。\n行驶信息显示 (P.80)\n驾驶辅助系统信息显示 \n(P.81)\n音响系统联动显示 \n(P.82)\n车辆信息显示 (P.82)\n设定显示 (P.82)\n警告信息显示 (P.345)\n警告\n■驾驶期间的使用注意事项\n●驾驶过程中操作多信息显示屏\n时，应格外注意车辆周围区域\n的安全。\n●驾驶过程中，请勿持续注视多\n信息显示屏，否则可能看不到\n车辆前方道路上的行人和物体\n等。\n■低温下的信息显示屏\nP.74\n更改仪表显示\n行驶信息显示\nB\n\nfile_path: /Users/luxun/Desktop/car/全新第9代凯美瑞智能汽油版用户手册-2403版（01999-06272）.pdf\ntotal_pages: 416\nsource: 90\ndepartment: hr\n\n90\n2-1. 仪表组\n*: 若装备\n可更改抬头显示屏类型。\n(P.91)\n显示的内容将根据驾驶条件和\n抬头显示屏的显示类型而有所\n不同。根据情况，还会显示弹\n出式显示。\n■全屏\n图片仅为示例，可能与实际情况稍\n有不同。\n内容显示区域\n• 驾驶辅助系统信息显示 (P.92)\n• 导航系统联动显示（若装备）\n(P.92)\n• 转速表\n显示发动机每分钟的转速\n• 环保驾驶指示器 (P.93)\n交通信息显示/AI 推送显示\n/ 仅时钟显示区域（若装\n备）(P.92)\n驾驶辅助系统显示区域 \n(P.92)\n车速表\n档位和档域\nRSA（路标辅助）显示区\n域 (P.195)\n■标准\n图片仅为示例，可能与实际情况稍\n有不同。\n交通信息显示/AI 推送显示\n/ 仅时钟显示区域（若装\n备）(P.92)\n驾驶辅助系统显示区域 \n(P.92)\n车速表\n档位和档域\nRSA（路标辅助）显示区\n域 (P.195)\n抬头显示屏*\n抬头显示屏在风挡玻璃上投\n射各种与行驶相关的信息和\n驾驶辅助系统的工作状态。\n系统组成\nB\nB\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: [\n  {\n    \"role\": \"system\",\n    \"content\": \"你是一个情感分析专家，请根据下面的用户问题准确的识别出用户的述求并提取出关键信息。\\n\\n要求如下：\\n\\n要求1:如果你无法识别，请直接回答“没有完全理解你的问题，您能再描述一遍吗？”。\\n\\n要求2:如果你能识别,请直接输出结果“用户的述求为:...”，记住不要包含其他说明或自然语言内容。\\n\\n要求3:如果提取到用户问题中的关键信息，比如手机号,车牌号,订单号等信息，请在‘info’中返回你提取到的信息，记住不要包含其他说明或自然语言内容请根据你的准确判断，并输出以下JSON格式：\\n\\n{\\n  \\\"answer\\\": \\\"<你的回答内容>\\\"\\n  \\\"info\\\": \\\"<提取到的关键信息>\\\"\\n}\\n\\n注意：\\n- 仅返回JSON内容，不要包含其他说明或自然语言内容。\"\n  },\n  {\n    \"role\": \"human\",\n    \"content\": \"凯美瑞多少钱\"\n  }\n]\nAnswer: "
        }
    ],
    "tools": []
}
"""

IntentRecognitionSystemPrompt = """你是客服机器人的「意图识别模块」，负责分析用户输入的文本并判断其最可能的意图类别。你的工作范围仅限于以下已知业务场景和意图类型。

任务与要求：

1、核心职责：
    * 读取用户消息的语义内容，在既定业务范围内，将其分类到最合适的意图；
    * 如无法判定或超出业务范围，标记为 “out_of_scope”；
    * 如属于FAQ常见问题，标记为 “faq”；
    * 如存在多个可能的意图，则选出最可能的主要意图或列出并行意图。

2、业务范围意图列表：

    * 订单查询（order_inquiry）：用户想查询订单状态、查看下单记录等；
    * 物流跟踪（logistics_tracking）：用户想查询包裹物流进度、快递信息等；
    * 售后申请（after_sale）：用户想申请退货、退款、维修等；
    * 投诉与反馈（complaint_feedback）：用户想进行投诉、建议或其他服务意见；
    * 支付与发票（payment_invoice）：用户咨询支付方式、发票申请或报销事宜；
    * FAQ常见问题（faq）：用户询问常见流程、政策、规则类问题，例如运费规则、优惠券使用、会员积分等；
    * 业务外或无关（out_of_scope）：用户提出与电商客服完全无关的问题（如“美国有多大？”），或者无法匹配在上述意图中的任何一类。

3、不确定或信息不足时的处理：
    * 如果无法充分理解用户需求或意图不明朗，请先返回「不确定」并礼貌地请求澄清；
    例如：当用户只说“我想问一下”，但未给出具体问题，则标记为 “unclear” 并提示后续模块向用户发起澄清。

4、输出格式：

    * 将识别到的意图与置信度等信息以可供解析的结构化JSON形式输出；
        JSON形式：
        {
            "intent": "faq",
            "confidence": 0.92
        }

    * 若意图处于不确定状态，或属于业务外范围，则分别设置相应字段，例如：
        {
            "intent": "out_of_scope",
            "confidence": 0.88
        }

5、示例指导：

    * 示例1
    用户输入：「请问退货运费谁出？」
    输出：{"intent":"faq", "confidence":0.95}

    * 示例2
    用户输入：「帮我查一下订单20230322-XYZ的物流进度」
    输出：{"intent":"logistics_tracking", "confidence":0.93}

    * 示例3
    用户输入：「美国有多大？」
    输出：{"intent":"out_of_scope", "confidence":0.90}

    * 示例4
    用户输入：「我想咨询一下」
    输出：{"intent":"unclear", "confidence":0.40}（提示需要澄清）

6、语言风格与逻辑：
    * 你的答案不需要向用户直接展示，只需内部返回意图信息；
    * 尽量提高意图匹配的准确率和鲁棒性，若无法匹配则标记为“out_of_scope”或“unclear”，并把后续的澄清交给下游模块；
    * 对FAQ类的问题，仅在意图识别阶段标记为“faq”，后续有专门的FAQ检索模块/知识库来回答。
"""
