#!/usr/bin/env python3
import asyncio
import os
from colorama import init, Fore, Style
from agents.search_jobs import find_job
from agents.apply import apply_to_job
from agents.connection import send_connection_requests

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)


def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
     ██  ██████  ██████  ██████  ██████   ██████  ██ ██████  
     ██ ██    ██ ██   ██ ██   ██ ██   ██ ██    ██ ██ ██   ██ 
     ██ ██    ██ ██████  ██   ██ ██████  ██    ██ ██ ██   ██ 
██   ██ ██    ██ ██   ██ ██   ██ ██   ██ ██    ██ ██ ██   ██ 
 █████   ██████  ██████  ██████  ██   ██  ██████  ██ ██████  
{Style.RESET_ALL}
{Fore.YELLOW}{Style.BRIGHT}    🤖 Automated LinkedIn Job Application Assistant 🤖{Style.RESET_ALL}
{Fore.GREEN}           Press Enter to start the job hunting process...{Style.RESET_ALL}
"""
    print(banner)


def print_agent_status(agent_name: str, color: str = Fore.BLUE):
    print(f"\n{color}{Style.BRIGHT}🚀 Running Agent: {agent_name}{Style.RESET_ALL}")
    print(f"{color}{'='*50}{Style.RESET_ALL}")


async def run_job_application_cycle():
    cycle_count = 1
    max_retries = 3

    while True:
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}🔄 Starting Job Application Cycle #{cycle_count}{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")

        # Step 1: Search for jobs with retry logic
        job_file_path = None
        for attempt in range(max_retries):
            try:
                print_agent_status("SEARCH_JOBS", Fore.CYAN)
                if attempt > 0:
                    print(
                        f"{Fore.YELLOW}🔄 Retry attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

                job_file_path = await find_job()

                if job_file_path and os.path.exists(job_file_path):
                    print(
                        f"{Fore.GREEN}✅ Job found and saved to: {job_file_path}{Style.RESET_ALL}"
                    )
                    break
                else:
                    print(
                        f"{Fore.RED}❌ Failed to find job. Attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )
                    if attempt == max_retries - 1:
                        print(
                            f"{Fore.RED}❌ All search attempts failed. Moving to next cycle...{Style.RESET_ALL}"
                        )

            except Exception as e:
                print(
                    f"{Fore.RED}❌ Error in SEARCH_JOBS (attempt {attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
                )
                if attempt == max_retries - 1:
                    print(
                        f"{Fore.RED}❌ All search attempts failed. Moving to next cycle...{Style.RESET_ALL}"
                    )

        # If job search failed completely, skip to next cycle
        if not job_file_path or not os.path.exists(job_file_path):
            cycle_count += 1
            continue

        # Step 2: Send connection requests with retry logic
        connection_success = False
        for attempt in range(max_retries):
            try:
                print_agent_status("CONNECTION", Fore.GREEN)
                if attempt > 0:
                    print(
                        f"{Fore.YELLOW}🔄 Retry attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

                connection_success = await send_connection_requests(job_file_path)

                if connection_success:
                    print(
                        f"{Fore.GREEN}✅ Successfully sent connection requests!{Style.RESET_ALL}"
                    )
                    break
                else:
                    print(
                        f"{Fore.RED}❌ Failed to send connection requests. Attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

            except Exception as e:
                print(
                    f"{Fore.RED}❌ Error in CONNECTION (attempt {attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
                )

        # Step 3: Apply to the job with retry logic
        apply_success = False
        for attempt in range(max_retries):
            try:
                print_agent_status("APPLY", Fore.YELLOW)
                if attempt > 0:
                    print(
                        f"{Fore.YELLOW}🔄 Retry attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

                apply_success = await apply_to_job(
                    job_data_file=job_file_path,
                    candidate_data_file="candidate_data.json",
                    phone_resume_location="Documents/resume.pdf",
                )

                if apply_success:
                    print(
                        f"{Fore.GREEN}✅ Successfully applied to the job!{Style.RESET_ALL}"
                    )
                    break
                else:
                    print(
                        f"{Fore.RED}❌ Failed to apply to the job. Attempt {attempt + 1}/{max_retries}{Style.RESET_ALL}"
                    )

            except Exception as e:
                print(
                    f"{Fore.RED}❌ Error in APPLY (attempt {attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
                )

        # Cycle completion summary
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}📊 Cycle #{cycle_count} Summary:{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}   Job Search: {'✅ Success' if job_file_path else '❌ Failed'}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.GREEN}   Connections: {'✅ Success' if connection_success else '❌ Failed'}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}   Job Apply: {'✅ Success' if apply_success else '❌ Failed'}{Style.RESET_ALL}"
        )

        # Ask user if they want to continue
        print(
            f"\n{Fore.BLUE}🤔 Do you want to run another cycle? (y/n): {Style.RESET_ALL}",
            end="",
        )
        user_input = input().strip().lower()

        if user_input not in ["y", "yes", ""]:
            print(
                f"{Fore.CYAN}👋 JobDroid session ended. Happy job hunting!{Style.RESET_ALL}"
            )
            break

        cycle_count += 1


async def main():
    """Main function"""
    print_banner()
    input()  # Wait for user to press Enter

    print(f"{Fore.GREEN}{Style.BRIGHT}🚀 JobDroid is starting up...{Style.RESET_ALL}")

    # Check if required files exist
    required_files = ["candidate_data.json"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"{Fore.RED}❌ Required file missing: {file}{Style.RESET_ALL}")
            print(
                f"{Fore.YELLOW}Please ensure all required files are present before running JobDroid.{Style.RESET_ALL}"
            )
            return

    print(
        f"{Fore.GREEN}✅ All required files found. Starting job application process...{Style.RESET_ALL}"
    )

    await run_job_application_cycle()


if __name__ == "__main__":
    asyncio.run(main())
