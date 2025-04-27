import asyncio
import os

from eth_rpc import set_alchemy_key

from emp_agents.providers import OpenAIProvider, OpenAIModelType, OllamaProvider, OllamaModelType
from emp_agents.agents.skills import SkillsAgent
from emp_agents.tools.dexscreener import DexScreenerSkill
from emp_agents.tools.protocol.erc20 import ERC20Skill
from emp_agents.tools.protocol.wallets import SimpleWalletSkill

# if alchemy_key := os.environ.get("ALCHEMY_KEY"):
#     set_alchemy_key(alchemy_key)


agent = SkillsAgent(
    skills=[
        # ERC20Skill,
        # SimpleWalletSkill,
        DexScreenerSkill,
    ],
    # default_model=OpenAIModelType.gpt3_5_turbo,
    openai_api_key=os.environ.get("OLLAMA_API_KEY"),
    # provider=OpenAIProvider(),
    default_model= OllamaModelType.llama3_2,
    # openai_api_key=os.environ.get("ANTHROPIC_API_KEY"),
    provider=OllamaProvider(),

)


if __name__ == "__main__":
    asyncio.run(agent.run())
