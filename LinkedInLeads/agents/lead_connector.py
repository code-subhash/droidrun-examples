#!/usr/bin/env python3
import asyncio
import os
import json
from datetime import datetime
from droidrun import AdbTools, DroidAgent
from llama_index.llms.google_genai import GoogleGenAI
from prompts import prompts
from utils import append_to_csv
from dotenv import load_dotenv

load_dotenv()


async def connect_with_leads(companies_file: str, user_config: dict):
    """
    Connects with prospects at the scraped companies
    """
    # Load companies data
    with open(companies_file, "r") as f:
        companies_data = json.load(f)

    companies = companies_data.get("companies", [])
    if not companies:
        print("No companies found in the data file")
        return False

    # Load tools
    tools = AdbTools()
    # set up google gemini llm
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    success_count = 0
    total_companies = len(companies)

    # Process each company
    for i, company in enumerate(companies, 1):
        print(
            f"\n🏢 Processing company {i}/{total_companies}: {company.get('name', 'Unknown')}"
        )

        # Get expanded roles from user config
        roles_to_search = user_config.get(
            "expanded_roles", user_config.get("role_keywords", [])
        )

        for role in roles_to_search:
            try:
                # Create agent for this specific company and role
                agent = DroidAgent(
                    goal=prompts.LEAD_CONNECTOR_GOAL(
                        company_name=company.get("name", ""),
                        role_title=role,
                        goal_intent=user_config["goal_intent"],
                        about_yourself=user_config["about_yourself"],
                        user_config=user_config,
                    ),
                    llm=llm,
                    tools=tools,
                    enable_tracing=True,
                    save_trajectories="action",
                    reasoning=True,
                    vision=True,
                    max_steps=30,
                )

                # Run agent
                result = await agent.run()
                print(
                    f"🔍 Searching for {role} at {company.get('name', 'Unknown')}: {'✅' if result['success'] else '❌'}"
                )

                if result["success"]:
                    success_count += 1

                    # Log successful connection
                    await log_connection(
                        company, role, user_config, result.get("output", "")
                    )

                # Brief pause between searches to avoid overwhelming LinkedIn
                await asyncio.sleep(2)

            except Exception as e:
                print(
                    f"❌ Error processing {role} at {company.get('name', 'Unknown')}: {str(e)}"
                )
                continue

    print(f"\n📊 Connection Summary: {success_count} successful connections made")
    return success_count > 0


async def log_connection(company: dict, role: str, user_config: dict, output: str):
    """
    Log successful connections for tracking
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "company": company,
        "role_searched": role,
        "goal_intent": user_config["goal_intent"],
        "output": output,
        "success": True,
    }

    # Create logs directory
    os.makedirs("data/logs", exist_ok=True)

    # Append to connections log
    log_file = "data/logs/connections.json"
    csv_file = "data/logs/connections.csv"

    # Load existing logs or create new list
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append(log_entry)

    # Save updated logs to JSON
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

    # Parse the output to extract contacted people information
    try:
        output_data = json.loads(output)
        contacts = output_data.get("people_contacted", [])
        messages = output_data.get("messages_sent", [])
        connections_sent = output_data.get("connections_sent", 0)

        # Define fieldnames for CSV
        fieldnames = [
            "timestamp",
            "company_name",
            "company_industry",
            "company_location",
            "role_searched",
            "person_contacted",
            "message_sent",
            "goal_intent",
        ]

        # Write a row for each contacted person
        if contacts:
            for i in range(len(contacts)):
                message = messages[i] if i < len(messages) else ""
                append_to_csv(
                    csv_file,
                    {
                        "timestamp": timestamp,
                        "company_name": company.get("name", "Unknown"),
                        "company_industry": company.get("industry", "Unknown"),
                        "company_location": company.get("location", "Unknown"),
                        "role_searched": role,
                        "person_contacted": contacts[i],
                        "message_sent": message,
                        "goal_intent": user_config["goal_intent"],
                    },
                    fieldnames,
                )
        elif connections_sent == 0:
            # Log that no connections were made for this company/role
            append_to_csv(
                csv_file,
                {
                    "timestamp": timestamp,
                    "company_name": company.get("name", "Unknown"),
                    "company_industry": company.get("industry", "Unknown"),
                    "company_location": company.get("location", "Unknown"),
                    "role_searched": role,
                    "person_contacted": "None",
                    "message_sent": "None",
                    "goal_intent": user_config["goal_intent"],
                },
                fieldnames,
            )
    except (json.JSONDecodeError, AttributeError, TypeError) as e:
        print(f"Error processing connection output for CSV: {e}")

    print(f"📝 Connection logged for {role} at {company.get('name', 'Unknown')}")


if __name__ == "__main__":
    # Test configuration
    test_config = {
        "target_audience": "Software Startup marketing directors",
        "industry": "Tech, Software",
        "region": "Germany",
        "company_size": "Startup (1-11employees)",
        "role_keywords": ["Marketing Director", "CMO"],
        "expanded_roles": [
            "Marketing Director",
            "Director of Marketing",
            "CMO",
            "Chief Marketing Officer",
        ],
        "goal_intent": "Book demo calls",
        "about_yourself": "With Droidrun you can automate any mobile app. Grant AI native control of virtual & physical phones - Automate mobile workflows, unlock data, and more. Everything is possible through natural language.",
    }

    # This would need a real companies file in practice
    asyncio.run(connect_with_leads("data/companies/test_companies.json", test_config))
