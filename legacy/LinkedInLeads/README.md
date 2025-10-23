# LeadSpot

**LinkedIn Lead Generation & Connection System with Real-time Dashboard**

LeadSpot is an automated LinkedIn lead generation system that finds companies, generates role variations, and connects with prospects. Features a real-time Streamlit dashboard for monitoring progress and results.

## Features

### **Automated Lead Generation**
- **Company Discovery**: Automatically finds companies matching your criteria
- **Role Expansion**: AI-powered generation of job title variations
- **Prospect Connection**: Automated LinkedIn outreach and connection requests
- **Multi-cycle Processing**: Continuous lead generation with retry logic

## Demo
[![Leadspot](images/Leadspot.png)](https://youtu.be/KO6uydpv0kM)

## Quick Start

```bash
cd LeadSpot/
```
If you don't have ADB, setup and configure it through [Android SDK platform tools](https://developer.android.com/tools/releases/platform-tools).

Install dependencies
```sh
pip install -r requirements.txt
```

Connect your device (or turn on your emulator), then run 
```sh
droidrun setup
```
Once droidrun-portal is installed, give it accessibility access.

Then run
```bash
python main.py
```
