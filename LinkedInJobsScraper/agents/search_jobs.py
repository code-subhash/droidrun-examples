import asyncio
from pydantic import BaseModel, Field

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


class JobData(BaseModel):
    company_name: str = Field(description="Name of the company offering the job")
    job_title: str = Field(description="Title of the job position")
    location: str = Field(description="Location of the job")
    job_description: str = Field(description="Detailed description of the job")
    date_posted: str = Field(description="Date when the job was posted")


async def find_job():
    # Use default configuration with built-in LLM profiles
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )
    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )
    # Create agent
    # LLMs can also be automatically loaded from config.llm_profiles
    agent = DroidAgent(
        goal=prompts.SEARCH_JOBS_GOAL(),
        config=config,
        llms=llm,
        output_model=JobData,
    )

    # Run agent
    result = await agent.run()

    # Check results (result is a ResultEvent object)
    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")

    if result.success:
        job_data: JobData = result.output
        print(f"Job Data: {job_data.json(indent=4)}")

        output_directory = "jobs/"
        os.makedirs(output_directory, exist_ok=True)
        job_title = (
            job_data.company_name.replace(" ", "_")
            + "_"
            + job_data.job_title.replace(" ", "_")
        )
        file_path = os.path.join(output_directory, f"{job_title}.json")
        with open(file_path, "w") as f:
            f.write(job_data.json(indent=4))
        print(f"Job data saved to {file_path}")

        return file_path
    else:
        return None


if __name__ == "__main__":
    asyncio.run(find_job())
