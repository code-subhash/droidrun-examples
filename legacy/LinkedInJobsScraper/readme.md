

![JobDroid Banner](images/banner_logo.png)
# JobDroid
> Note: This project is for educational and personal use. Please respect LinkedIn's terms of service and use responsibly.

**Automated LinkedIn Job Application Assistant**


JobDroid is an intelligent automation system that streamlines your LinkedIn job search, connection and application process using AI-powered Android automation. It combines the power of [DroidRun](https://droidrun.ai/)'s Android automation capabilities to 
- search for jobs
- send connection requests
- Fill the application form and apply to positions automatically
- Repeat

## 🌟 Features

- **🔍 Intelligent Job Search**: Automatically searches for relevant jobs in the IT sector on LinkedIn
- **🤝 Smart Networking**: Sends targeted connection requests to professionals at target companies
- **📝 Automated Applications**: Applies to jobs with customized responses based on your profile
- **🔄 Continuous Operation**: Runs in cycles with retry mechanisms for robustness
- **📊 Progress Tracking**: Real-time status updates with colored terminal output
- **💾 Data Persistence**: Saves job data and maintains application history


## Demo
[![Demo Video](images/youtube_link.png)](https://youtu.be/hVAhdVm86i0)

## Setup
1. clone the repository and install dependencies
  ```bash
  python3 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
  ```
2. create `.env` file in root directory
  ```env
  GEMINI_API_KEY=YOUR_GEMINI_API_KEY
  ```
3. Add your resume information and anything that might be relevant in `candidate_data.json`. See the current file for reference. Note there is no fixed format, this file will be read by an LLM so you can add things in natural language also.
4. Keep your resume in your phone at `Documents/` directory. Or, you can change the resume location in `main.py` at `apply_to_job()` function.
5. Connect your physical device or emulator and run
  ```bash
  droidrun setup
  ```
  Then give accessibility permissions to the app (droidrun portal). Know more [here](https://github.com/droidrun/droidrun/)
6. run `main.py`
  ```bash
  python3 main.py
  ```



## 🏗️ Architecture

JobDroid consists of three main intelligent agents:

## 🔧 About DroidRun

[DroidRun](https://github.com/droidrun-ai/droidrun) is the core automation framework powering JobDroid's Android interactions. It provides:

- **ADB Tools**: Direct Android device communication and control
- **AI Agent Framework**: LLM-powered decision making for UI interactions
- **Vision Capabilities**: Screenshot analysis and UI element recognition
- **Action Execution**: Automated tapping, scrolling, and text input
- **Trajectory Saving**: Records and saves automation sequences for debugging

DroidRun enables JobDroid to interact with the LinkedIn mobile app intelligently, making decisions based on visual context and executing complex workflows autonomously.


## 📁 Project Structure

```
LinkedInJobsScraper/
├── main.py                 # Main application entry point
├── candidate_data.json     # Your profile information
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── agents/                # AI agent modules
│   ├── __init__.py
│   ├── search_jobs.py     # Job search agent
│   ├── apply.py           # Job application agent
│   ├── connection.py      # Networking agent
│   └── prompts/           # Agent prompts and instructions
│       ├── __init__.py
│       └── prompts.py
├── jobs/                  # Saved job data (auto-created)
│   └── *.json            # Individual job files
└── trajectories/          # Automation logs (auto-created)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and personal use. Please respect LinkedIn's terms of service and use responsibly.

---

**Happy Job Hunting! 🎯**

