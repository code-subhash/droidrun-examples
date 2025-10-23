def SEARCH_JOBS_GOAL():
    prompt = """
1. Open Linkedin using package name com.linkedin.android 
2. Go to jobs section.
3. Click "Show all" in the "Top Job picks for you" section (this section is present on top of the page, do not scroll).
4. Goto IT tab.
5. Open first job which is not promoted (does not contain "Promoted" below it).
6. Click on "show more" in About the job section to expand the full job description.
7. return the following details in json format as output:
{
  "job_title": "string",
  "company_name": "string",
  "location": "string",
  "date_posted": "string",
  "job_description": "string",
}

Output only the JSON string, do not include any other text.
"""
    # print(prompt)
    return prompt


def APPLY(
    company_name: str,
    job_title: str,
    job_description: str,
    resume_path: str,
    candidate_data: str,
):
    prompt = """
1. Click on {company_name} company name on top of the screen on the job page.
2. Click on "People" tab to see all employees.
3. Scroll to the bottom of the to see associated members.
4. Click on connection request button twice to send connection requests to everyone whose connection request button is visible. 
Note clicking on connection request highlights it (focused state), then you have to click on it again to actually send a connection request. 
"""
    # print(prompt)
    return prompt


def SEND_CONNECTION_REQUESTS_GOAL(company_name: str):
    return """
1. Click on {company_name} company name on top of the screen on the job page.
2. Click on "People" tab to see all employees.
3. Scroll to the bottom of the to see associated members.
4. Click on connection request button twice to send connection requests to everyone whose connection request button is visible. 
Note clicking on connection request highlights it (focused state), then you have to click on it again to actually send a connection request.
If there is a follow button (plus sign) instead of connection request button, click on person's profile and click connect button from there, then go back.
After all connection requests are sent, return back to the {company_name}'s job page on linkedin by pressing back multiple times.
"""


def APPLY_GOAL(company_data: dict, candidate_data: dict, resume_path: str):
    prompt = f"""
You are a job applying agent. You have all information about the company and the candidate who is applying. You have to fill the job application form for the candidate.
1. Click on Apply from screen to open application website.
2. Find the apply button and navigate to job application form. (If the form asks to login, stop there)
3. Fill the form according to company and candidate information given below. Fill the information not given yourself to something common and generic (like no disability, allowed to work at the location, no military experience). Fill best responses to subjective questions withing 200 words if needed. The resume is stored in the device at {resume_path}, select it from there for uploading. No need to apply, just fill all the fields and upload resume through upload button. Make sure to fill all fields even after scrolling

candidate information:
{candidate_data}


company information:
{company_data}

(In case the input field is dropdown and you can't find relevant option, select "other")
"""
    # print(prompt)
    return prompt
