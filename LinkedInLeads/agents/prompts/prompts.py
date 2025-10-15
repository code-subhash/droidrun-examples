def COMPANY_SCRAPER_GOAL(
    industry: str, region: str, company_size: str, target_audience: str
):
    """
    Prompt for scraping companies matching the specified criteria
    """
    return f"""
1. Open LinkedIn using package name com.linkedin.android
2. Navigate to the search section, click on search, leave the input empty and press enter to search.
3. Add "company" filter.
3. Add filters as below (First select all filters then click apply)
   - Industry: {industry}
   - Location: {region}
   - Company size: {company_size}
4. Browse through the search results and collect information about first 20 companies. 
5. For each relevant company, note down the following in an array:
   - Company name
   - Industry
   - Location
   - Follower count

   Output the current array after storing current screen's companies, then scroll.
   Stop when the array size becomes 20 or more.

6. Return the results in JSON format (as an array in companies) as output:
{{
  "companies": [
    {{
      "name": "string",
      "industry": "string", 
      "location": "string",
      "follower_count": "integer",
    }}
  ]
}}

Output only the JSON string, do not include any other text.
"""


def LEAD_CONNECTOR_GOAL(
    company_name: str,
    role_title: str,
    goal_intent: str,
    about_yourself: str,
    user_config: dict,
):
    """
    Prompt for connecting with specific roles at a company
    """
    return f"""
You are a LinkedIn networking agent focused on making authentic connections for business purposes.

Your Mission:
- Company: {company_name}
- Target Role: {role_title}
- Goal: {goal_intent}
- Your Background: {about_yourself}

Instructions:
0. Go back to home page of linkedin app and use the search bar at the top to search for people.
1. Search LinkedIn for: "{role_title} at {company_name}"
2. Look through the search results to find people who:
   - Actually work at {company_name} (verify the company name in their profile)
   - Have a role title matching or similar to "{role_title}"
    No need to scroll, if you can't find any relevant person on the top results just return  {{connections_sent:0}} 
3. For each relevant person found:
   - Send a connection request
   - Add a personalized message that:
     * Mentions their role at {company_name}
     * Briefly explains who you are: {about_yourself}
     * States your goal clearly: {goal_intent}
     * Keeps it professional and authentic (under 200 characters)

4. Example message template:
   "Hi [Name], I saw your {role_title} role at {company_name}. {about_yourself}. I'd love to connect and discuss {goal_intent}. Best, [Your Name]"

5. If you can't find people with the exact role, look for similar roles (managers, directors, etc.)
6. If you can't find any person in the company, just return {{connections_sent:0}} 

Important:
- Only connect with people who actually work at {company_name}
- Personalize each message - don't send generic requests
- Be respectful and professional

Return a brief summary of connections made in JSON format:
{{
  "connections_sent": number,
  "people_contacted": ["name and role"],
  "messages_sent": ["sample message used"]
}}
"""
