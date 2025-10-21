#!/usr/bin/env python3
# from argparse import Action
import asyncio
from droidrun import AdbTools, DroidAgent
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

    # Load tools
    tools = AdbTools()
    # set up google gemini llm
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Create agent
    agent = DroidAgent(
        goal=prompts.SEND_CONNECTION_REQUESTS_GOAL(company_name=company_name),
        llm=llm,
        tools=tools,
        enable_tracing=True,
        save_trajectories="action",
        reasoning=True,
        vision=True,
        max_steps=25,
    )

    # Run agent
    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get("output"):
        print(f"Output: {result['output']}")

    # print(result)
    return result["success"]


if __name__ == "__main__":
    asyncio.run(send_connection_requests("jobs/demo_job.json"))
