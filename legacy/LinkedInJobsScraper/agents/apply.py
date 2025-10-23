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


async def apply_to_job(
    job_data_file: str, candidate_data_file: str, phone_resume_location: str
):
    with open(job_data_file, "r") as f:
        company_data = json.load(f)
    with open(candidate_data_file, "r") as f:
        candidate_data = json.load(f)

    # Load tools
    tools = AdbTools()
    # set up google gemini llm
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Create agent
    agent = DroidAgent(
        goal=prompts.APPLY_GOAL(
            company_data=company_data,
            candidate_data=candidate_data,
            resume_path=phone_resume_location,
        ),
        llm=llm,
        tools=tools,
        enable_tracing=True,
        save_trajectories="action",
        reasoning=True,
        vision=True,
        max_steps=50,
    )

    # Run agent
    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get("output"):
        print(f"Output: {result['output']}")

    # print(result)
    return result["success"]


if __name__ == "__main__":
    asyncio.run(
        apply_to_job(
            "jobs/demo_job.json", "candidate_data.json", "Documents/resume.pdf"
        )
    )
