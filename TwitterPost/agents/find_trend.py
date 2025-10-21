#!/usr/bin/env python3
import asyncio
import json
from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    TracingConfig,
    LoggingConfig,
    AgentConfig,
)
from llama_index.llms.google_genai import GoogleGenAI
from agents.prompts.prompts import OPEN_CHROME_GOOGLE_TRENDS_GOAL
from dotenv import load_dotenv
import os

load_dotenv()


async def find_trend():
    """Find trending topics using Chrome and Google Trends"""
    # Use default configuration with built-in LLM profiles
    llm = GoogleGenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-2.5-pro",
    )
    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    # Create the DroidAgent
    # LLMs can also be automatically loaded from config.llm_profiles
    agent = DroidAgent(
        goal=OPEN_CHROME_GOOGLE_TRENDS_GOAL(),
        config=config,
        llms=llm,
    )

    # Run the agent
    result = await agent.run()

    # Check results (result is a ResultEvent object)
    print(f"Trend finder - Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")

    if result.output:
        try:
            # Parse the JSON output
            trend_data = json.loads(result.output)
            print(
                f"Found trending topic: {trend_data.get('trending_topic', 'Unknown')}"
            )
            return trend_data
        except json.JSONDecodeError:
            print(f"Could not parse trend data: {result.output}")
            # Return a fallback trend
            return {
                "trending_topic": "Latest Technology Trends",
                "description": "Current technology trends and innovations",
                "category": "Technology",
            }
    else:
        print("No trend data found, using fallback")
        return {
            "trending_topic": "Daily Tech News",
            "description": "Latest technology news and updates",
            "category": "Technology",
        }


if __name__ == "__main__":
    asyncio.run(find_trend())
