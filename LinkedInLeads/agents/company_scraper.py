#!/usr/bin/env python3
import asyncio
import os
import json
from datetime import datetime
from droidrun import AdbTools, DroidAgent
from llama_index.llms.google_genai import GoogleGenAI
from agents.prompts import prompts
from agents.utils import json_to_csv
from dotenv import load_dotenv

load_dotenv()


async def scrape_companies(
    user_config: dict, output_directory: str = "data/companies/"
):
    """
    Scrapes LinkedIn for companies matching the user's criteria
    """
    # Load tools
    tools = AdbTools()
    # set up google gemini llm
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Create agent
    agent = DroidAgent(
        goal=prompts.COMPANY_SCRAPER_GOAL(
            industry=user_config["industry"],
            region=user_config["region"],
            company_size=user_config["company_size"],
            target_audience=user_config["target_audience"],
        ),
        llm=llm,
        tools=tools,
        enable_tracing=True,
        save_trajectories="action",
        reasoning=True,
        reflection=True,
        vision=True,
        max_steps=75,
    )

    # Run agent
    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get("output"):
        print(f"Output: {result['output']}")

    if result["success"] and result.get("output"):
        # Parse the JSON output
        try:
            companies_data = json.loads(result["output"])

            # Create output directory
            os.makedirs(output_directory, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"companies_{user_config['industry'].replace(' ', '_')}_{timestamp}.json"
            json_file_path = os.path.join(output_directory, json_filename)
            csv_filename = (
                f"companies_{user_config['industry'].replace(' ', '_')}_{timestamp}.csv"
            )
            csv_file_path = os.path.join(output_directory, csv_filename)

            # Save companies data to JSON
            with open(json_file_path, "w") as f:
                json.dump(
                    {
                        "user_config": user_config,
                        "companies": companies_data,
                        "scraped_at": timestamp,
                    },
                    f,
                    indent=4,
                )

            # Save companies data to CSV
            try:
                # Create a temporary JSON file that we'll convert to CSV
                temp_json = os.path.join(output_directory, f"temp_{timestamp}.json")

                # Extract companies list from the response - handle both formats
                if isinstance(companies_data, dict):
                    companies_list = companies_data.get("companies", [])
                else:
                    companies_list = companies_data

                # Write companies list to temporary JSON
                with open(temp_json, "w") as f:
                    json.dump(companies_list, f)

                # Convert JSON to CSV
                field_mapping = {
                    "name": "name",
                    "industry": "industry",
                    "location": "location",
                    "follower_count": "follower_count",
                }

                json_to_csv(temp_json, csv_file_path, field_mapping)

                # Remove temporary JSON file
                if os.path.exists(temp_json):
                    os.remove(temp_json)

                print(f"Companies data saved to CSV: {csv_file_path}")
            except Exception as e:
                print(f"Error saving companies to CSV: {e}")

            return json_file_path

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output: {e}")
            return None

    return None


if __name__ == "__main__":
    # Test configuration
    test_config = {
        "target_audience": "Marketing directors of AI tech startups",
        "industry": "Software",
        "region": "Germany",
        "company_size": "Startup (1-200 employees)",
        "role_keywords": ["Marketing Director", "CMO"],
        "goal_intent": "Book demo calls",
        "about_yourself": "I'm a sales professional helping SaaS companies scale their revenue.",
    }

    asyncio.run(scrape_companies(test_config))
