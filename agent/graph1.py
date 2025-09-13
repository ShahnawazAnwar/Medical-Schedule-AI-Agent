
# # # agent/graph.py

# # import os
# # from dotenv import load_dotenv
# # from typing import Literal

# # from langgraph.graph import StateGraph, END
# # # MODIFIED IMPORT: We now use ToolNode which is the modern way to do this.
# # from langgraph.prebuilt import ToolNode

# # # Import your agent state and all the tools you've created
# # from .state import AgentState
# # from tools.db_tools import patient_lookup
# # from tools.calendar_tools import check_availability, book_appointment
# # from tools.file_tools import export_to_excel
# # from tools.communication_tools import send_confirmation_email
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # # --- 1. Initialize Your LLM and Tools ---

# # # Load environment variables from the .env file
# # load_dotenv()

# # # --- ADD THIS BLOCK TO EXPLICITLY CHECK THE KEY ---
# # google_api_key = os.getenv("GOOGLE_API_KEY")
# # # print(f"GOOGLE_API_KEY: {google_api_key}")  # Debugging line to check if the key is loaded
# # if not google_api_key:
# #     raise ValueError("GOOGLE_API_KEY not found. Please make sure it is set in your .env file.")
# # # --------------------------------------------------


# # # Set up the Google Gemini LLM

# # llm = ChatGoogleGenerativeAI(
# #     # model="gemini-pro",
# #     model="gemini-1.5-flash-latest",
# #     google_api_key=google_api_key # Use the variable we just checked
# # )

# # # Create a list of all the tools your agent can use
# # tools = [
# #     patient_lookup, 
# #     check_availability, 
# #     book_appointment, 
# #     export_to_excel, 
# #     send_confirmation_email
# # ]

# # # Bind the tools to the LLM. This tells the LLM what functions it can call.
# # llm_with_tools = llm.bind_tools(tools)


# # # --- 2. Define the Agent's Nodes ---

# # def call_model(state: AgentState):
# #     """Invokes the LLM with the conversation history."""
# #     print("---CALLING MODEL---")
# #     messages = state['messages']
# #     response = llm_with_tools.invoke(messages)
# #     return {"messages": [response]}

# # # NEW: Use the pre-built ToolNode for executing tools.
# # # This is cleaner and replaces the manual `call_tool` function.
# # tool_node = ToolNode(tools)


# # # --- 3. Define the Graph's Router (Conditional Edge) ---

# # def should_continue(state: AgentState) -> Literal["tools", "end"]:
# #     """Acts as a router, deciding the next step based on the LLM's response."""
# #     print("---ROUTING---")
# #     last_message = state['messages'][-1]
    
# #     if last_message.tool_calls:
# #         # If the LLM made a tool call, route to the tool node
# #         print("---DECISION: CALL TOOLS---")
# #         return "tools"
    
# #     # Otherwise, the conversation is over
# #     print("---DECISION: END---")
# #     return "end"


# # # --- 4. Assemble the Graph ---

# # workflow = StateGraph(AgentState)

# # # Add the two main nodes we defined: 'agent' and our new 'tool_node'
# # workflow.add_node("agent", call_model)
# # workflow.add_node("tools", tool_node)

# # # Define the workflow's starting point
# # workflow.set_entry_point("agent")

# # # Add the conditional edge. This is the router that decides the next step.
# # workflow.add_conditional_edges(
# #     "agent",
# #     should_continue,
# #     {
# #         "tools": "tools", # If router returns "tools", go to the 'tools' node
# #         "end": END
# #     }
# # )

# # # The 'tools' node always loops back to the 'agent' node
# # # so the LLM can process the tool's output.
# # workflow.add_edge("tools", "agent")

# # # Compile the graph into a runnable application
# # app = workflow.compile()








# # agent/graph.py

# import os
# from dotenv import load_dotenv
# from typing import Literal

# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import ToolNode

# # Import your agent state and tools
# from .state import AgentState
# from tools.db_tools import patient_lookup
# from tools.calendar_tools import check_availability, book_appointment
# # We NO LONGER need to import export_to_excel here
# from tools.communication_tools import send_confirmation_email
# from langchain_google_genai import ChatGoogleGenerativeAI
# from tools.general_tools import get_doctor_list # <-- ADD THIS IMPORT

# # --- 1. Initialize Your LLM and Tools ---

# load_dotenv()

# google_api_key = os.getenv("GOOGLE_API_KEY")
# if not google_api_key:
#     raise ValueError("GOOGLE_API_KEY not found. Please make sure it is set in your .env file.")

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash-latest",
#     google_api_key=google_api_key
# )

# # MODIFIED: The tools list is now simpler. The LLM doesn't need to know about exporting.
# tools = [
#     patient_lookup, 
#     check_availability, 
#     book_appointment, 
#     send_confirmation_email,
#     get_doctor_list  
# ]

# llm_with_tools = llm.bind_tools(tools)
# tool_node = ToolNode(tools)


# # --- 2. Define the Agent's Nodes ---

# def call_model(state: AgentState):
#     """Invokes the LLM with the conversation history."""
#     print("---CALLING MODEL---")
#     messages = state['messages']
#     response = llm_with_tools.invoke(messages)
#     return {"messages": [response]}

# tool_node = ToolNode(tools)


# # --- 3. Define the Graph's Router (Conditional Edge) ---

# def should_continue(state: AgentState) -> Literal["tools", "end"]:
#     """Acts as a router, deciding the next step based on the LLM's response."""
#     print("---ROUTING---")
#     last_message = state['messages'][-1]
    
#     if last_message.tool_calls:
#         print("---DECISION: CALL TOOLS---")
#         return "tools"
    
#     print("---DECISION: END---")
#     return "end"


# # --- 4. Assemble the Graph ---

# workflow = StateGraph(AgentState)

# workflow.add_node("agent", call_model)
# workflow.add_node("tools", tool_node)

# workflow.set_entry_point("agent")

# workflow.add_conditional_edges(
#     "agent",
#     should_continue,
#     {
#         "tools": "tools",
#         "end": END
#     }
# )

# workflow.add_edge("tools", "agent")

# app = workflow.compile()









# agent/graph.py

import os
from dotenv import load_dotenv
from typing import Literal
import pandas as pd # <-- ADD PANDAS IMPORT HERE

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import your agent state and the REST of your tools
from .state import AgentState
from tools.db_tools import patient_lookup
from tools.calendar_tools import check_availability, book_appointment
from tools.communication_tools import send_confirmation_email
from langchain_google_genai import ChatGoogleGenerativeAI

# --- NEW: Define the problematic tool directly in this file for testing ---
def get_doctor_list() -> list[str]:
    """
    Returns a list of all unique doctor names from the schedule.
    Call this tool when the user asks which doctors are available.
    """
    print("--- Reading doctor list from schedule ---")
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        unique_doctors = df['doctor'].unique().tolist()
        return unique_doctors
    except Exception as e:
        return [f"Error reading doctor list: {e}"]
# --------------------------------------------------------------------

# --- 1. Initialize Your LLM and Tools ---

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please make sure it is set in your .env file.")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=google_api_key
)

# The tools list now uses the get_doctor_list function we just defined above
tools = [
    patient_lookup, 
    check_availability, 
    # book_appointment, 
    #  send_confirmation_email,
    get_doctor_list 
]

llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)


# --- 2. Define the Agent's Nodes ---

def call_model(state: AgentState):
    """Invokes the LLM with the conversation history."""
    print("---CALLING MODEL---")
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# --- 3. Define the Graph's Router (Conditional Edge) ---

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Acts as a router, deciding the next step based on the LLM's response."""
    print("---ROUTING---")
    last_message = state['messages'][-1]
    
    if last_message.tool_calls:
        print("---DECISION: CALL TOOLS---")
        return "tools"
    
    print("---DECISION: END---")
    return "end"


# --- 4. Assemble the Graph ---

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

workflow.add_edge("tools", "agent")

app = workflow.compile()