import asyncio
import os

from emp_agents.agents.persistentagent import PersistentAgent, PersistentAgentConfig
from emp_agents.models.protocol.registry import ToolRegistry
from emp_agents.providers import OpenAIModelType, OpenAIProvider, OllamaProvider, OllamaModelType

erc20_skill = ToolRegistry.get_skill("ERC20Skill")
wallet_skill = ToolRegistry.get_skill("SimpleWalletSkill")
dex_Skill  = ToolRegistry.get_skill("DexScreenerSkill")

agent = PersistentAgent.from_config(
    PersistentAgentConfig(
        agent_id="dynamic_agent",
        name="Tools",
        description="Tools for interacting with the blockchain",
        tools=[ *dex_Skill],
        default_model=OllamaModelType.mistral_small_3_1,
        extra={
            "ollama_api_key": os.environ.get("OPENAI_API_KEY"),
        },
    ),
    provider=OllamaProvider(),
)

if __name__ == "__main__":
    asyncio.run(agent.run())
    # info = agent.answer("Tell me about the token at 4hAAk3BtSvNUzsRde6Hnx5zYhBaqz641cFG9bbQWFc7M on sol.")
