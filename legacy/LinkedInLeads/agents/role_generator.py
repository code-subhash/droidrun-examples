#!/usr/bin/env python3
import asyncio
import os
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
import json

load_dotenv()


async def generate_roles(role_keywords: list) -> list:
    """
    Generates expanded role variations and similar titles using LLM
    """
    # Set up google gemini llm
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Create prompt for role expansion
    role_expansion_prompt = f"""
You are a professional recruiter and LinkedIn expert. Given the following role keywords, generate a comprehensive list of similar and related job titles that a person might have.

Input roles: {', '.join(role_keywords)}

Instructions:
1. For each input role, think of:
   - Exact variations (e.g., "Marketing Director" -> "Director of Marketing")
   - Seniority levels (e.g., "Senior Marketing Director", "VP Marketing", "Chief Marketing Officer")
   - Similar roles in the same function (e.g., "Marketing Manager", "Brand Manager", "Growth Manager")
   - Abbreviated versions (e.g., "CMO" for "Chief Marketing Officer")
   - Regional variations (e.g., "Marketing Director EMEA", "Head of Marketing")

2. Include common alternative titles people might use
3. Consider both formal and informal titles
4. Include C-level, VP, Director, Manager, and Senior levels where appropriate
5. Remove duplicates and keep only realistic job titles

Return ONLY a JSON array of strings with the expanded role titles. No other text.

Example format:
["Marketing Director", "Director of Marketing", "VP Marketing", "Chief Marketing Officer", "CMO", "Senior Marketing Manager", "Head of Marketing", "Marketing Manager", "Brand Director", "Growth Director"]
"""

    try:
        # Get response from LLM
        response = await llm.acomplete(role_expansion_prompt)
        
        # Parse JSON response
        expanded_roles = json.loads(str(response))
        
        # Ensure we have a list and remove duplicates while preserving order
        if isinstance(expanded_roles, list):
            # Remove duplicates while preserving order
            seen = set()
            unique_roles = []
            for role in expanded_roles:
                if isinstance(role, str) and role.lower() not in seen:
                    seen.add(role.lower())
                    unique_roles.append(role)
            
            print(f"Generated {len(unique_roles)} role variations from {len(role_keywords)} input roles")
            return unique_roles
        else:
            print("Error: LLM did not return a list")
            return role_keywords
            
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response as JSON: {e}")
        return role_keywords
    except Exception as e:
        print(f"Error generating roles: {e}")
        return role_keywords


async def save_generated_roles(original_roles: list, expanded_roles: list, output_file: str = "data/generated_roles.json"):
    """
    Save the generated roles for reference
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    role_data = {
        "original_roles": original_roles,
        "expanded_roles": expanded_roles,
        "total_generated": len(expanded_roles),
        "expansion_ratio": len(expanded_roles) / len(original_roles) if original_roles else 0
    }
    
    with open(output_file, "w") as f:
        json.dump(role_data, f, indent=4)
    
    print(f"Role data saved to {output_file}")


if __name__ == "__main__":
    # Test the role generator
    test_roles = ["Marketing Director", "CEO", "Founder"]
    
    async def test_generate_roles():
        expanded = await generate_roles(test_roles)
        print(f"Original roles: {test_roles}")
        print(f"Expanded roles: {expanded}")
        await save_generated_roles(test_roles, expanded)
    
    asyncio.run(test_generate_roles())