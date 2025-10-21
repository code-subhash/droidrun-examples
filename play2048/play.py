import asyncio
from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    AgentConfig,
    LoggingConfig,
)
from llama_index.llms.google_genai import GoogleGenAI


async def main():
    # Use default configuration with built-in LLM profiles
    config = DroidrunConfig(
        agent=AgentConfig(
            max_steps=100,
            reasoning=True,
        ),
        logging=LoggingConfig(debug=False, save_trajectory="action", rich_text=True),
    )

    llm = GoogleGenAI(model="gemini-2.5-pro", temperature=0)

    # Create agent
    # LLMs are automatically loaded from config.llm_profiles
    agent = DroidAgent(
        goal="Play 2048 by going to play2048.co till you win. Your objective is to reach 2048 tile.",
        config=config,
        llms=llm,
    )

    # Run agent
    result = await agent.run()

    # Check results (result is a ResultEvent object)
    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")


if __name__ == "__main__":
    asyncio.run(main())
