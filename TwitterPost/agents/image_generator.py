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
from agents.prompts.prompts import OPEN_GEMINI_CREATE_IMAGE_GOAL
from dotenv import load_dotenv
import os

load_dotenv()


async def generate_image(image_prompt: str):
    """Generate image using Gemini with the provided prompt"""
    # Use default configuration with built-in LLM profiles
    llm = GoogleGenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-2.5-flash",
    )
    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    # Create the DroidAgent
    # LLMs can also be automatically loaded from config.llm_profiles
    agent = DroidAgent(
        goal=OPEN_GEMINI_CREATE_IMAGE_GOAL(image_prompt),
        config=config,
        llms=llm,
    )

    # Run the agent
    result = await agent.run()

    # Check results (result is a ResultEvent object)
    print(f"Image generator - Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")

    if result.output:
        try:
            # Parse the JSON output
            image_result = json.loads(result.output)
            print(f"Image generation status: {image_result.get('message', 'Unknown')}")
            return image_result
        except json.JSONDecodeError:
            print(f"Could not parse image generation result: {result.output}")
            return {
                "success": False,
                "message": "Failed to parse image generation result",
            }
    else:
        print("No image generation result")
        return {"success": False, "message": "No result from image generation"}


if __name__ == "__main__":
    # Test with a sample prompt
    test_prompt = (
        "A futuristic cityscape with flying cars and neon lights, digital art style"
    )
    asyncio.run(generate_image(test_prompt))
