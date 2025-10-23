#!/usr/bin/env python3
import asyncio
import os
import json
from colorama import init, Fore, Style
from agents.company_scraper import scrape_companies
from agents.role_generator import generate_roles
from agents.lead_connector import connect_with_leads

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)


def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
██      ███████  █████  ██████  ███████ ██████   ██████  ████████ 
██      ██      ██   ██ ██   ██ ██      ██   ██ ██    ██    ██    
██      █████   ███████ ██   ██ ███████ ██████  ██    ██    ██    
██      ██      ██   ██ ██   ██      ██ ██      ██    ██    ██    
███████ ███████ ██   ██ ██████  ███████ ██       ██████     ██    
{Style.RESET_ALL}
{Fore.YELLOW}{Style.BRIGHT}    🎯 LinkedIn Lead Generation & Connection System 🎯{Style.RESET_ALL}
{Fore.GREEN}           Press Enter to start finding prospects...{Style.RESET_ALL}
"""
    print(banner)


def print_agent_status(agent_name: str, color: str = Fore.BLUE):
    print(f"\n{color}{Style.BRIGHT}🚀 Running Agent: {agent_name}{Style.RESET_ALL}")
    print(f"{color}{'='*50}{Style.RESET_ALL}")


def get_user_input():
    print(
        f"\n{Fore.CYAN}{Style.BRIGHT}📋 Please provide your lead generation details:{Style.RESET_ALL}"
    )

    # Example templates in dimmed text
    example_target = "Marketing directors at SaaS startups in the US"
    example_industry = "Tech, Software and IT"
    example_region = "Germany, Europe, France, UK"
    example_size = "Startup (1-200 employees)"
    example_roles = "Founder, CEO, CTO, CMO"
    example_goal = "Book Demo Call"
    example_about = "With Droidrun you can automate any mobile app..."

    # Collect input with colored prompts
    print(
        f"{Fore.YELLOW}👥 Target Audience {Fore.BLUE}(e.g. {example_target}):{Style.RESET_ALL}"
    )
    target_audience = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    print(
        f"{Fore.YELLOW}🏢 Industry {Fore.BLUE}(e.g. {example_industry}):{Style.RESET_ALL}"
    )
    industry = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    print(
        f"{Fore.YELLOW}🌍 Region {Fore.BLUE}(e.g. {example_region}):{Style.RESET_ALL}"
    )
    region = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    print(
        f"{Fore.YELLOW}📏 Company Size {Fore.BLUE}(e.g. {example_size}):{Style.RESET_ALL}"
    )
    company_size = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    print(
        f"{Fore.YELLOW}🎯 Role Keywords {Fore.BLUE}(comma separated, e.g. {example_roles}):{Style.RESET_ALL}"
    )
    role_keywords = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    print(
        f"{Fore.YELLOW}🎯 Goal/Intent {Fore.BLUE}(e.g. {example_goal}):{Style.RESET_ALL}"
    )
    goal_intent = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    print(
        f"{Fore.YELLOW}📝 About Yourself {Fore.BLUE}(for connection messages):{Style.RESET_ALL}"
    )
    about_yourself = input(f"{Fore.GREEN}> {Style.RESET_ALL}")

    # Use default values if empty inputs
    target_audience = target_audience if target_audience else example_target
    industry = industry if industry else example_industry
    region = region if region else example_region
    company_size = company_size if company_size else example_size
    role_keywords = role_keywords if role_keywords else example_roles
    goal_intent = goal_intent if goal_intent else example_goal
    about_yourself = about_yourself if about_yourself else example_about

    print(
        f"\n{Fore.CYAN}{Style.BRIGHT}✅ Input collected successfully!{Style.RESET_ALL}"
    )

    return {
        "target_audience": target_audience.strip(),
        "industry": industry.strip(),
        "region": region.strip(),
        "company_size": company_size.strip(),
        "role_keywords": [keyword.strip() for keyword in role_keywords.split(",")],
        "goal_intent": goal_intent.strip(),
        "about_yourself": about_yourself.strip(),
    }


async def run_lead_generation_cycle(user_config: dict):
    cycle_count = 1
    max_retries = 3

    while True:
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}🔄 Starting Lead Generation Cycle #{cycle_count}{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")

        # Step 1: Scrape companies matching criteria
        companies_file = None
        for attempt in range(max_retries):
            try:
                print_agent_status("COMPANY_SCRAPER", Fore.CYAN)
                if attempt > 0:
                    print(
                        f"{Fore.YELLOW}🔄 Retry attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

                companies_file = await scrape_companies(user_config)

                if companies_file and os.path.exists(companies_file):
                    print(
                        f"{Fore.GREEN}✅ Companies found and saved to: {companies_file}{Style.RESET_ALL}"
                    )
                    break
                else:
                    print(
                        f"{Fore.RED}❌ Failed to find companies. Attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

            except Exception as e:
                print(
                    f"{Fore.RED}❌ Error in COMPANY_SCRAPER (attempt {attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
                )

        if not companies_file or not os.path.exists(companies_file):
            print(
                f"{Fore.RED}❌ Failed to find companies. Skipping to next cycle...{Style.RESET_ALL}"
            )
            cycle_count += 1
            continue

        # Step 2: Generate role variations
        roles_generated = False
        for attempt in range(max_retries):
            try:
                print_agent_status("ROLE_GENERATOR", Fore.BLUE)
                if attempt > 0:
                    print(
                        f"{Fore.YELLOW}🔄 Retry attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

                expanded_roles = await generate_roles(user_config["role_keywords"])
                user_config["expanded_roles"] = expanded_roles
                roles_generated = True

                print(
                    f"{Fore.GREEN}✅ Role variations generated: {', '.join(expanded_roles)}{Style.RESET_ALL}"
                )
                break

            except Exception as e:
                print(
                    f"{Fore.RED}❌ Error in ROLE_GENERATOR (attempt {attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
                )

        # Step 3: Connect with leads
        connection_success = False
        for attempt in range(max_retries):
            try:
                print_agent_status("LEAD_CONNECTOR", Fore.GREEN)
                if attempt > 0:
                    print(
                        f"{Fore.YELLOW}🔄 Retry attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

                connection_success = await connect_with_leads(
                    companies_file, user_config
                )

                if connection_success:
                    print(
                        f"{Fore.GREEN}✅ Successfully connected with leads!{Style.RESET_ALL}"
                    )
                    break
                else:
                    print(
                        f"{Fore.RED}❌ Failed to connect with leads. Attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

            except Exception as e:
                print(
                    f"{Fore.RED}❌ Error in LEAD_CONNECTOR (attempt {attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
                )

        # Cycle completion summary
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}📊 Cycle #{cycle_count} Summary:{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}   Company Scraping: {'✅ Success' if companies_file else '❌ Failed'}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.BLUE}   Role Generation: {'✅ Success' if roles_generated else '❌ Failed'}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.GREEN}   Lead Connections: {'✅ Success' if connection_success else '❌ Failed'}{Style.RESET_ALL}"
        )

        # Ask user if they want to continue
        print(
            f"\n{Fore.BLUE}🤔 Do you want to run another cycle? (y/n): {Style.RESET_ALL}",
            end="",
        )
        user_input = input().strip().lower()

        if user_input not in ["y", "yes", ""]:
            print(
                f"{Fore.CYAN}👋 LeadSpot session ended. Happy networking!{Style.RESET_ALL}"
            )
            break

        cycle_count += 1


async def main():
    """Main function"""
    print_banner()
    input()  # Wait for user to press Enter

    print(f"{Fore.GREEN}{Style.BRIGHT}🚀 LeadSpot is starting up...{Style.RESET_ALL}")

    # Get user configuration
    user_config = get_user_input()

    # Display confirmation of settings
    print(
        f"\n{Fore.CYAN}{Style.BRIGHT}📝 Your Lead Generation Settings:{Style.RESET_ALL}"
    )
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(
        f"{Fore.CYAN}👥 Target Audience: {Fore.WHITE}{user_config['target_audience']}{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}🏢 Industry: {Fore.WHITE}{user_config['industry']}{Style.RESET_ALL}"
    )
    print(f"{Fore.CYAN}🌍 Region: {Fore.WHITE}{user_config['region']}{Style.RESET_ALL}")
    print(
        f"{Fore.CYAN}📏 Company Size: {Fore.WHITE}{user_config['company_size']}{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}🎯 Role Keywords: {Fore.WHITE}{', '.join(user_config['role_keywords'])}{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}🎯 Goal/Intent: {Fore.WHITE}{user_config['goal_intent']}{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}📝 About You: {Fore.WHITE}{user_config['about_yourself']}{Style.RESET_ALL}"
    )
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")

    # Confirm settings
    print(f"\n{Fore.BLUE}Are these settings correct? (y/n): {Style.RESET_ALL}", end="")
    confirm = input().strip().lower()

    if confirm not in ["y", "yes", ""]:
        print(f"{Fore.YELLOW}Let's try again with new settings.{Style.RESET_ALL}")
        return await main()  # Restart the process

    # Save user config for reference
    os.makedirs("data", exist_ok=True)
    with open("data/user_config.json", "w") as f:
        json.dump(user_config, f, indent=4)

    print(
        f"{Fore.GREEN}✅ Configuration saved. Starting lead generation process...{Style.RESET_ALL}"
    )

    await run_lead_generation_cycle(user_config)


if __name__ == "__main__":
    asyncio.run(main())
