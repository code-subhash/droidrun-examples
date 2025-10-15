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


async def find_job(output_directory: str = "jobs/"):
    # Load tools
    tools = AdbTools()
    # set up google gemini llm
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Create agent
    agent = DroidAgent(
        goal=prompts.SEARCH_JOBS_GOAL(),
        llm=llm,
        tools=tools,
        enable_tracing=True,
        save_trajectories="action",
        reasoning=True,
        vision=True,
    )

    # Run agent
    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get("output"):
        print(f"Output: {result['output']}")

    job_data = json.loads(result["output"])
    os.makedirs(output_directory, exist_ok=True)
    job_title = (
        job_data.get("company_name", "unknown_job").replace(" ", "_")
        + "_"
        + job_data.get("job_title", "unknown_title").replace(" ", "_")
    )
    file_path = os.path.join(output_directory, f"{job_title}.json")
    with open(file_path, "w") as f:
        json.dump(job_data, f, indent=4)
    # print(result)
    return file_path


if __name__ == "__main__":
    asyncio.run(find_job())
