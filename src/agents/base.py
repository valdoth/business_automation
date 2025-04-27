from typing import Dict, List, Any, Optional
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from ..core.config import settings

class AITool:
    def __init__(self, name: str, description: str, func: callable):
        self.name = name
        self.description = description
        self.func = func

    def to_langchain_tool(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            func=self.func
        )

class AIAgent:
    def __init__(self, model: str = settings.AI_MODEL):
        self.llm = ChatOpenAI(
            model_name=model,
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.tools: List[AITool] = []

    def add_tool(self, tool: AITool):
        self.tools.append(tool)

    def create_agent(self) -> AgentExecutor:
        tool_names = [tool.name for tool in self.tools]
        tool_descriptions = [tool.description for tool in self.tools]

        template = """You are an AI agent that helps automate business processes.
        You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        {agent_scratchpad}"""

        prompt = StringPromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join(tool_descriptions),
                "tool_names": ", ".join(tool_names)
            }
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            stop=["\nObservation:"]
        )

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=[tool.to_langchain_tool() for tool in self.tools],
            verbose=True
        )

    async def execute_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        agent = self.create_agent()
        result = await agent.arun(scenario["description"])
        return {"result": result} 