#!/usr/bin/env python3
# from argparse import Action
import asyncio
from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    TracingConfig,
    LoggingConfig,
    AgentConfig,
)
from llama_index.llms.google_genai import GoogleGenAI
from agents.prompts import prompts
from dotenv import load_dotenv
import os
import json

load_dotenv()


async def send_connection_requests(job_data_file: str):
    with open(job_data_file, "r") as f:
        company_data = json.load(f)

    company_name = company_data["company_name"]

    # Use default configuration with built-in LLM profiles
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )
    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True, max_steps=25),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    # Create agent
    # LLMs can also be automatically loaded from config.llm_profiles
    agent = DroidAgent(
        goal=prompts.SEND_CONNECTION_REQUESTS_GOAL(company_name=company_name),
        config=config,
        llms=llm,
    )

    # Run agent
    result = await agent.run()

    # Check results (result is a ResultEvent object)
    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")
    if result.output:
        print(f"Output: {result.output}")

    return result.success


if __name__ == "__main__":
    asyncio.run(send_connection_requests("jobs/demo_job.json"))
