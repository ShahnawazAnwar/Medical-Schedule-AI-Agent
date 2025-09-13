# Medical AI Scheduling Agent

**Author:** [Shahnawaz Anwar](https://www.linkedin.com/in/shaikh-shahnawaz-anwar-137683150)  
**Phone:** +91 8750191902  
**Email:** shaikhmdanwar80@gmail.com  
**GitHub:** [github.com/shahnawazanwar](https://github.com/shahnawazanwar)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Directory Structure](#directory-structure)
- [Dependencies](#dependencies)
- [Code Files Overview](#code-files-overview)
- [Data Files](#data-files)
- [Setup & Run Instructions](#setup--run-instructions)
- [Example Usage](#example-usage)
- [Limitations & Future Work](#limitations--future-work)

## Introduction

The Medical AI Scheduling Agent is an intelligent system for automating medical appointment management. It handles scheduling, rescheduling, and confirming patient–doctor appointments using a combination of LangGraph and Google Gemini, integrating with patient and doctor data and providing simulated email/SMS confirmations.

Goals:
- Reduce manual appointment booking effort.
- Provide a user-friendly Streamlit UI for patients and staff.
- Demonstrate LLM-driven workflow orchestration in healthcare.

## Features

- Patient Lookup: Identify new or returning patients.
- Doctor Listing: Fetch available doctors dynamically.
- Smart Scheduling: Real-time slot booking (30 min for returning, 60 min for new patients).
- Communication Tools: Simulated Email & SMS confirmations.
- Streamlit UI: Simple interface for patients and admins.
- Data Generator: Create mock patients & doctor schedules for testing.
- Logging: Automatically store confirmed appointments in Excel logs.

## System Architecture

Modular, tool-driven architecture:

- User: Interacts via natural language.
- Streamlit UI: Simple, user-friendly booking interface.
- LangGraph Agent (Gemini-powered):  
  - Understands user requests
  - Decides when/how to use tools
  - Manages conversation flow
- Tools:  
  - Patient DB: Identifies new/returning patients.
  - Calendar: Checks doctor availability, books slots.
  - Communication: Sends simulated Email/SMS confirmations.

Diagram:  
*(Add your system architecture diagram here)*

Workflow ensures:  
Accurate scheduling, clear communication, scalable integration with real healthcare systems.

## Directory Structure

```
ai_scheduling_agent/
├── app/
│   └── main.py                 # Streamlit UI application
├── agent/
│   ├── __init__.py
│   ├── graph.py                # LangGraph agent logic
│   ├── nodes.py                # Agent workflow nodes
│   ├── schemas.py              # Data schema definitions
│   └── state.py                # Agent state (memory/variables)
├── tools/
│   ├── __init__.py
│   ├── calendar_tools.py       # Calendar availability & booking
│   ├── communication_tools.py  # Simulated Email/SMS
│   ├── db_tools.py             # Patient lookup tool
│   ├── file_tools.py           # Appointment logging
│   └── general_tools.py        # Doctor listing
├── utils/
│   └── data_generator.py       # Generates mock patients & schedules
├── data/
│   ├── intake_forms/           # Intake form templates
│   ├── appointment_log.xlsx    # Auto-generated appointment log
│   ├── doctor_schedules.xlsx   # Auto-generated doctor schedules
│   └── patients.csv            # Auto-generated patient records
├── venv/                      # Virtual environment (not included)
├── .env                       # API key configuration (user-provided)
├── .gitignore                 # Git ignore rules
├── config.py                  # Project configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── setup_project.py           # Setup helper script
```

## Dependencies

- langchain, langgraph, langchain-google-genai – Core agent framework & Gemini integration
- streamlit – Interactive UI
- pandas, openpyxl – Data handling/schedule storage
- Faker – Mock data generation
- python-dotenv – Environment variable management

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Code Files Overview

- app/main.py – Streamlit app for user interaction
- agent/state.py – Agent state (patient info, doctor, date, etc.)
- agent/graph.py – LangGraph workflow logic
- agent/nodes.py – Custom workflow steps
- agent/schemas.py – Data schemas for validation
- tools/db_tools.py – Patient lookup
- tools/calendar_tools.py – Check & book slots
- tools/general_tools.py – List available doctors
- tools/communication_tools.py – Simulated Email/SMS
- tools/file_tools.py – Export appointments to Excel
- utils/data_generator.py – Generates mock patients and schedules
- config.py – Project configuration
- setup_project.py – Environment/data setup script

## Data Files

- patients.csv – Mock patient records (ID, name, DOB, phone)
- doctor_schedules.xlsx – Doctor schedules and availability
- appointment_log.xlsx – Booked appointments log
- intake_forms/ – (Placeholder) Patient intake forms

## Setup & Run Instructions

1. Create Virtual Environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Linux/Mac
    venv\Scripts\activate      # On Windows
    ```

2. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set Up API Key:
    - Create a .env file in the project root.
    - Add your Google API key:
      ```
      GOOGLE_API_KEY="your_api_key_here"
      ```

4. Generate Mock Data:
    ```bash
    python utils/data_generator.py
    ```

5. Run Application:
    ```bash
    streamlit run app/main.py
    ```

## Example Usage

Conversation Flow:
```
Agent: Hello Shahnawaz! I’m your AI medical scheduling assistant. How may I help you today?
User: I want to book a doctor appointment.
Agent: Sure! Please provide your full name and date of birth (YYYY-MM-DD).
User: My name is Shahnawaz Anwar, DOB 1995-03-15.
Agent: Thanks, Shahnawaz. I found your record as a returning patient.
  Here are the available doctors:
  - Dr. Smith
  - Dr. Jones
  - Dr. Williams
User: I want to book with Dr. Smith on 2025-09-15.
Agent: Dr. Smith is available on 2025-09-15.
  The available slots are:
  - 10:00
  - 10:30
  - 11:00
  Which time would you prefer?
User: Book 10:30. My mobile number is 8750191902.
Agent: Appointment confirmed for Shahnawaz Anwar with Dr. Smith on 2025-09-15 at 10:30.
  A confirmation Email + SMS have been sent to 8750191902.
```

## Limitations & Future Work

Current Limitations:
- Works with mock data only (generated with Faker).
- Email & SMS are simulated (not real).
- No real-time calendar sync.
- Basic error handling; may fail with unexpected inputs.

Planned Enhancements:
- Integrate with real EHR systems/hospital databases.
- Sync with Google/Outlook Calendar APIs.
- Use real communication APIs (Twilio, SendGrid).
- Add authentication & secure data storage.
- Admin dashboard for bookings & reports.
