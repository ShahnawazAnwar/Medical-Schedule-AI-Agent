
# # # app/main.py

# # import streamlit as st
# # from langchain_core.messages import HumanMessage, AIMessage

# # # Import your compiled LangGraph application
# # from agent.graph import app

# # st.title("🩺 AI Medical Appointment Scheduler")
# # st.write("Hello! I'm here to help you book, reschedule, or check your medical appointments.")

# # # Initialize conversation history in Streamlit's session state
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # # Display past messages
# # for message in st.session_state.messages:
# #     # Use the 'role' to determine the chat bubble type
# #     with st.chat_message(message.role):
# #         st.markdown(message.content)

# # # Handle user input
# # if prompt := st.chat_input("What would you like to do?"):
# #     # Add user message to session state and display it
# #     st.session_state.messages.append(HumanMessage(content=prompt, role="user"))
# #     with st.chat_message("user"):
# #         st.markdown(prompt)

# #     # Show a thinking spinner while the agent is processing
# #     with st.spinner("Thinking..."):
# #         # The input to the agent is the entire conversation history
# #         agent_input = {"messages": st.session_state.messages}
        
# #         # Invoke the agent
# #         response = app.invoke(agent_input)
        
# #         # The agent's response is the last message in the output
# #         agent_response = response['messages'][-1]
        
# #         # Add the agent's response to the session state and display it
# #         st.session_state.messages.append(AIMessage(content=agent_response.content, role="assistant"))
# #         with st.chat_message("assistant"):
# #             st.markdown(agent_response.content)
            
            
            
            
            
            
            
# # app/main.py

# import nest_asyncio
# nest_asyncio.apply()


# import streamlit as st
# # ADD SystemMessage to the imports
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from ai_scheduling_agent.agent.graph1 import app

# # --- DEFINE YOUR SYSTEM PROMPT ---
# # SYSTEM_PROMPT = """You are a friendly and efficient medical scheduling assistant. Your goal is to help users book, reschedule, or check medical appointments.

# # When a user wants to book an appointment, you must collect the following information step-by-step:
# # 1.  Full name and date of birth (in YYYY-MM-DD format).
# # 2.  Use the `patient_lookup` tool to check if they are a new or returning patient.
# # 3.  Based on their desired appointment, ask for the preferred doctor and date.
# # 4.  Use the `check_availability` tool to find open slots.
# # 5.  Once the user selects a time, you MUST collect their insurance carrier and member ID.
# # 6.  Finally, use the `book_appointment` tool with all the collected information to confirm the appointment.

# # Always be polite and clear in your communication. Do not assume information that the user has not provided.
# # # """

# SYSTEM_PROMPT = """You are a friendly and efficient medical scheduling assistant. Your primary goal is to help users book medical appointments.

# Follow these steps precisely:
# 1.  Greet the user and ask for their full name and date of birth (in YYYY-MM-DD format).
# 2.  Use the `patient_lookup` tool to check if they are a new or returning patient. Inform them of their status.
# 3.  Ask for the preferred doctor and date for the appointment. If the user asks which doctors are available, use the `get_doctor_list` tool.
# 4.  Once you have a doctor and date, use the `check_availability` tool to find open slots and present them to the user.
# 5.  After the user selects a time, you MUST then ask for their insurance carrier and member ID.
# 6.  After collecting all information, summarize the details (Patient Name, DOB, Doctor, Date, Time, Insurance) for the user and ask for a final confirmation like "Is this information correct?".
# 7.  Once the user confirms with "yes" or a similar affirmative, you MUST call the `book_appointment` tool with all the collected details to finalize the booking.
# 8.  Do not state that the appointment is booked until the `book_appointment` tool has returned a success message.
# """

# st.title("🩺 AI Medical Appointment Scheduler")
# st.write("Hello! I'm here to help you book, reschedule, or check your medical appointments.")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message.role):
#         st.markdown(message.content)

# if prompt := st.chat_input("What would you like to do?"):
#     st.session_state.messages.append(HumanMessage(content=prompt, role="user"))
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.spinner("Thinking..."):
#         # --- MODIFIED: Prepend the system prompt to the conversation history ---
#         agent_input = {
#             "messages": [SystemMessage(content=SYSTEM_PROMPT)] + st.session_state.messages
#         }
        
#         response = app.invoke(agent_input)
        
#         agent_response = response['messages'][-1]
        
#         # Add the agent's response to the history, but don't re-add the system prompt
#         st.session_state.messages.append(AIMessage(content=agent_response.content, role="assistant"))
#         with st.chat_message("assistant"):
#             st.markdown(agent_response.content)         

            
            
            
            
            







# # app/main.py
# import nest_asyncio
# nest_asyncio.apply()

# import streamlit as st
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from agent.graph import app

# # --- MODIFIED: A more forceful system prompt ---
# # SYSTEM_PROMPT = """You are a medical scheduling assistant. Your ONLY job is to help users book appointments by calling the provided tools in a specific order. Do not answer questions from your own knowledge. If you do not have a tool to answer a question, say so.

# # The required booking steps are:
# # 1.  Get user's full name and DOB. Call `patient_lookup`.
# # 2.  If the user asks for a list of doctors, call `get_doctor_list`.
# # 3.  Once a doctor and date are provided, call `check_availability`.
# # 4.  Once a time is selected, get the user's insurance info.
# # 5.  Summarize all details and ask for confirmation.
# # 6.  When the user confirms, you MUST call the `book_appointment` tool with all the required arguments. This is the final step.
# # """
# SYSTEM_PROMPT = """"You are a medical scheduling assistant. Your job is to follow user instructions by calling tools.
# **CRITICAL RULE 1: NEVER make up information. Do not invent doctor names, dates, or available times.**
# **CRITICAL RULE 2: When a tool returns a list of items, you MUST present those items to the user. Do not use generic phrases like "I have retrieved the list."**
#     * **Bad Example:** "I have found the available doctors. Which one do you want?"
#     * **Good Example:** "The available doctors are Dr. Smith and Dr. Jones. Which one do you want?"

# **Booking Workflow:**
# 1.  **Get Patient Info:** Ask for full name and date of birth. Then, call the `patient_lookup` tool.
# 2.  **Offer Doctors:** If the user asks for available doctors, call `get_doctor_list` and present the full list.
# 3.  **Check Schedule:** When the user provides a doctor and date, call `check_availability`. Present the exact time slots returned by the tool.
# 4.  **Collect Insurance:** After a time slot is chosen, ask for insurance details.
# 5.  **Confirm and Book:** Summarize all information. When the user confirms, call the `book_appointment` tool. Only confirm success *after* the tool runs.
# """


# st.title("🩺 AI Medical Appointment Scheduler")
# st.write("Hello! I'm here to help you book, reschedule, or check your medical appointments.")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message.role):
#         st.markdown(message.content)

# if prompt := st.chat_input("What would you like to do?"):
#     st.session_state.messages.append(HumanMessage(content=prompt, role="user"))
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.spinner("Thinking..."):
#         agent_input = {
#             "messages": [SystemMessage(content=SYSTEM_PROMPT)] + st.session_state.messages
#         }
        
#         response = app.invoke(agent_input)
        
#         agent_response = response['messages'][-1]
        
#         st.session_state.messages.append(AIMessage(content=agent_response.content, role="assistant"))
#         with st.chat_message("assistant"):
#             st.markdown(agent_response.content)
            
            
            
            





# app/main.py
import nest_asyncio
nest_asyncio.apply()

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent.graph import app

SYSTEM_PROMPT = """You are a medical scheduling assistant. Your job is to follow user instructions by calling tools.
**CRITICAL RULE 1: NEVER make up information. Do not invent doctor names, dates, or available times.**
**CRITICAL RULE 2: When a tool returns data (like a list of doctors or times), you MUST present that data directly in your response.**
    * **Good Example:** "The available doctors are Dr. Smith and Dr. Jones. Which one do you want?"

**Booking Workflow:**
1.  **Get Patient Info:** Ask for full name and date of birth. Then, call the `patient_lookup` tool.
2.  **Offer Doctors:** If the user asks for available doctors, call `get_doctor_list` and present the full list.
3.  **Check Schedule:** When the user provides a doctor and date, call `check_availability`. Present the exact time slots returned by the tool.
4.  **Collect Insurance:** After a time slot is chosen, ask for insurance details.
5.  **Confirm and Book:** Summarize all information. When the user confirms, call the `book_appointment` tool. Only confirm success *after* the tool runs.
"""

st.title("🩺 AI Medical Appointment Scheduler")
st.write("Hello! I'm here to help you book, reschedule, or check your medical appointments.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

if prompt := st.chat_input("What would you like to do?"):
    st.session_state.messages.append(HumanMessage(content=prompt, role="user"))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        agent_input = {
            "messages": [SystemMessage(content=SYSTEM_PROMPT)] + st.session_state.messages
        }
        
        response = app.invoke(agent_input)
        
        agent_response = response['messages'][-1]
        
        st.session_state.messages.append(AIMessage(content=agent_response.content, role="assistant"))
        with st.chat_message("assistant"):
            st.markdown(agent_response.content)