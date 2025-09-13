
# # # # # # # # # agent/graph.py

# # # # # # # # from typing import Literal
# # # # # # # # from langgraph.graph import StateGraph, END
# # # # # # # # from langgraph.prebuilt import ToolNode

# # # # # # # # # Import your agent state and tools
# # # # # # # # from .state import AgentState
# # # # # # # # from tools.db_tools import patient_lookup
# # # # # # # # from tools.calendar_tools import check_availability, book_appointment
# # # # # # # # from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# # # # # # # # from tools.general_tools import get_doctor_list
# # # # # # # # from langchain_community.chat_models import ChatOllama

# # # # # # # # # --- NEW: Import a tool formatting helper ---
# # # # # # # # from langchain_core.utils.function_calling import convert_to_openai_tool

# # # # # # # # # --- 1. Initialize Your LLM and Tools ---

# # # # # # # # llm = ChatOllama(model="llama3")

# # # # # # # # tools = [
# # # # # # # #     patient_lookup, 
# # # # # # # #     check_availability, 
# # # # # # # #     book_appointment, 
# # # # # # # #     send_confirmation_email,
# # # # # # # #     send_confirmation_sms,
# # # # # # # #     get_doctor_list 
# # # # # # # # ]

# # # # # # # # # --- MODIFIED: Use the .bind() method instead of .bind_tools() ---
# # # # # # # # # 1. Convert our Python functions into a format that the model understands
# # # # # # # # formatted_tools = [convert_to_openai_tool(t) for t in tools]

# # # # # # # # # 2. Bind them to the LLM using the .bind() method
# # # # # # # # llm_with_tools = llm.bind(tools=formatted_tools)
# # # # # # # # # --------------------------------------------------------------------

# # # # # # # # tool_node = ToolNode(tools)

# # # # # # # # # --- 2. Define the Agent's Nodes ---

# # # # # # # # def call_model(state: AgentState):
# # # # # # # #     """Invokes the LLM with the conversation history."""
# # # # # # # #     print("---CALLING MODEL---")
# # # # # # # #     messages = state['messages']
# # # # # # # #     response = llm_with_tools.invoke(messages)
# # # # # # # #     return {"messages": [response]}

# # # # # # # # # --- 3. Define the Graph's Router (Conditional Edge) ---

# # # # # # # # def should_continue(state: AgentState) -> Literal["tools", "end"]:
# # # # # # # #     """Acts as a router, deciding the next step based on the LLM's response."""
# # # # # # # #     print("---ROUTING---")
# # # # # # # #     last_message = state['messages'][-1]
    
# # # # # # # #     if hasattr(last_message, 'tool_calls') and last_message.tool_calls and len(last_message.tool_calls) > 0:
# # # # # # # #         print("---DECISION: CALL TOOLS---")
# # # # # # # #         return "tools"
    
# # # # # # # #     print("---DECISION: END---")
# # # # # # # #     return "end"

# # # # # # # # # --- 4. Assemble the Graph ---

# # # # # # # # workflow = StateGraph(AgentState)
# # # # # # # # workflow.add_node("agent", call_model)
# # # # # # # # workflow.add_node("tools", tool_node)
# # # # # # # # workflow.set_entry_point("agent")
# # # # # # # # workflow.add_conditional_edges(
# # # # # # # #     "agent",
# # # # # # # #     should_continue,
# # # # # # # #     {"tools": "tools", "end": END}
# # # # # # # # )
# # # # # # # # workflow.add_edge("tools", "agent")
# # # # # # # # app = workflow.compile()








# # # # # # # # agent/graph.py

# # # # # # # from typing import Literal
# # # # # # # from langgraph.graph import StateGraph, END
# # # # # # # from langgraph.prebuilt import ToolNode

# # # # # # # # Import your agent state and tools
# # # # # # # from .state import AgentState
# # # # # # # from tools.db_tools import patient_lookup
# # # # # # # from tools.calendar_tools import check_availability, book_appointment
# # # # # # # from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# # # # # # # from tools.general_tools import get_doctor_list
# # # # # # # from langchain_community.chat_models import ChatOllama

# # # # # # # # --- 1. Initialize Your LLM and Tools ---

# # # # # # # llm = ChatOllama(model="llama3")

# # # # # # # tools = [
# # # # # # #     patient_lookup, 
# # # # # # #     check_availability, 
# # # # # # #     book_appointment, 
# # # # # # #     send_confirmation_email,
# # # # # # #     send_confirmation_sms,
# # # # # # #     get_doctor_list 
# # # # # # # ]

# # # # # # # # --- MODIFIED: Switched back to the standard .bind_tools() method ---
# # # # # # # # This is the most reliable way to make the agent use its tools.
# # # # # # # llm_with_tools = llm.bind_tools(tools)
# # # # # # # # --------------------------------------------------------------------

# # # # # # # tool_node = ToolNode(tools)

# # # # # # # # --- 2. Define the Agent's Nodes ---

# # # # # # # def call_model(state: AgentState):
# # # # # # #     """Invokes the LLM with the conversation history."""
# # # # # # #     print("---CALLING MODEL---")
# # # # # # #     messages = state['messages']
# # # # # # #     response = llm_with_tools.invoke(messages)
# # # # # # #     return {"messages": [response]}

# # # # # # # # --- 3. Define the Graph's Router (Conditional Edge) ---

# # # # # # # def should_continue(state: AgentState) -> Literal["tools", "end"]:
# # # # # # #     """Acts as a router, deciding the next step based on the LLM's response."""
# # # # # # #     print("---ROUTING---")
# # # # # # #     last_message = state['messages'][-1]
    
# # # # # # #     if hasattr(last_message, 'tool_calls') and last_message.tool_calls and len(last_message.tool_calls) > 0:
# # # # # # #         print("---DECISION: CALL TOOLS---")
# # # # # # #         return "tools"
    
# # # # # # #     print("---DECISION: END---")
# # # # # # #     return "end"

# # # # # # # # --- 4. Assemble the Graph ---

# # # # # # # workflow = StateGraph(AgentState)
# # # # # # # workflow.add_node("agent", call_model)
# # # # # # # workflow.add_node("tools", tool_node)
# # # # # # # workflow.set_entry_point("agent")
# # # # # # # workflow.add_conditional_edges(
# # # # # # #     "agent",
# # # # # # #     should_continue,
# # # # # # #     {"tools": "tools", "end": END}
# # # # # # # )
# # # # # # # workflow.add_edge("tools", "agent")
# # # # # # # app = workflow.compile()








# # # # # # # agent/graph.py

# # # # # # from typing import Literal
# # # # # # from langgraph.graph import StateGraph, END
# # # # # # from langgraph.prebuilt import ToolNode

# # # # # # # Import your agent state and tools
# # # # # # from .state import AgentState
# # # # # # from tools.db_tools import patient_lookup
# # # # # # from tools.calendar_tools import check_availability, book_appointment
# # # # # # from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# # # # # # from tools.general_tools import get_doctor_list
# # # # # # from langchain_community.chat_models import ChatOllama

# # # # # # # NEW: Import a tool formatting helper
# # # # # # from langchain_core.utils.function_calling import convert_to_openai_tool

# # # # # # # --- 1. Initialize Your LLM and Tools ---

# # # # # # llm = ChatOllama(model="llama3")

# # # # # # tools = [
# # # # # #     patient_lookup, 
# # # # # #     check_availability, 
# # # # # #     book_appointment, 
# # # # # #     send_confirmation_email,
# # # # # #     send_confirmation_sms,
# # # # # #     get_doctor_list 
# # # # # # ]

# # # # # # # --- MODIFIED: Use the .bind() method workaround ---
# # # # # # # 1. Convert our Python functions into a format that the model understands
# # # # # # formatted_tools = [convert_to_openai_tool(t) for t in tools]

# # # # # # # 2. Bind them to the LLM using the compatible .bind() method
# # # # # # llm_with_tools = llm.bind(tools=formatted_tools)
# # # # # # # --------------------------------------------------------------------

# # # # # # tool_node = ToolNode(tools)

# # # # # # # --- 2. Define the Agent's Nodes ---

# # # # # # def call_model(state: AgentState):
# # # # # #     """Invokes the LLM with the conversation history."""
# # # # # #     print("---CALLING MODEL---")
# # # # # #     messages = state['messages']
# # # # # #     response = llm_with_tools.invoke(messages)
# # # # # #     return {"messages": [response]}

# # # # # # # --- 3. Define the Graph's Router (Conditional Edge) ---

# # # # # # def should_continue(state: AgentState) -> Literal["tools", "end"]:
# # # # # #     """Acts as a router, deciding the next step based on the LLM's response."""
# # # # # #     print("---ROUTING---")
# # # # # #     last_message = state['messages'][-1]
    
# # # # # #     if hasattr(last_message, 'tool_calls') and last_message.tool_calls and len(last_message.tool_calls) > 0:
# # # # # #         print("---DECISION: CALL TOOLS---")
# # # # # #         return "tools"
    
# # # # # #     print("---DECISION: END---")
# # # # # #     return "end"

# # # # # # # --- 4. Assemble the Graph ---

# # # # # # workflow = StateGraph(AgentState)
# # # # # # workflow.add_node("agent", call_model)
# # # # # # workflow.add_node("tools", tool_node)
# # # # # # workflow.set_entry_point("agent")
# # # # # # workflow.add_conditional_edges(
# # # # # #     "agent",
# # # # # #     should_continue,
# # # # # #     {"tools": "tools", "end": END}
# # # # # # )
# # # # # # workflow.add_edge("tools", "agent")
# # # # # # app = workflow.compile()









# # # # # # agent/graph.py

# # # # # from typing import Literal
# # # # # from langgraph.graph import StateGraph, END
# # # # # from langgraph.prebuilt import ToolNode

# # # # # # Import your agent state and tools
# # # # # from .state import AgentState
# # # # # from tools.db_tools import patient_lookup
# # # # # from tools.calendar_tools import check_availability, book_appointment
# # # # # from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# # # # # from tools.general_tools import get_doctor_list

# # # # # # Import the Ollama chat model and the tool formatter
# # # # # from langchain_community.chat_models import ChatOllama
# # # # # from langchain_core.utils.function_calling import convert_to_openai_tool

# # # # # # --- 1. Initialize Your LLM and Tools ---

# # # # # # MODIFIED: Add format="json" to force structured output for tool calling.
# # # # # llm = ChatOllama(model="phi3")

# # # # # tools = [
# # # # #     patient_lookup, 
# # # # #     check_availability, 
# # # # #     book_appointment, 
# # # # #     send_confirmation_email,
# # # # #     send_confirmation_sms,
# # # # #     get_doctor_list 
# # # # # ]

# # # # # # Use the .bind() method workaround for tool formatting
# # # # # formatted_tools = [convert_to_openai_tool(t) for t in tools]
# # # # # llm_with_tools = llm.bind(tools=formatted_tools)

# # # # # tool_node = ToolNode(tools)

# # # # # # --- 2. Define the Agent's Nodes ---

# # # # # def call_model(state: AgentState):
# # # # #     """Invokes the LLM with the conversation history."""
# # # # #     print("---CALLING MODEL---")
# # # # #     messages = state['messages']
# # # # #     response = llm_with_tools.invoke(messages)
# # # # #     return {"messages": [response]}

# # # # # # --- 3. Define the Graph's Router (Conditional Edge) ---

# # # # # def should_continue(state: AgentState) -> Literal["tools", "end"]:
# # # # #     """Acts as a router, deciding the next step based on the LLM's response."""
# # # # #     print("---ROUTING---")
# # # # #     last_message = state['messages'][-1]
    
# # # # #     if hasattr(last_message, 'tool_calls') and last_message.tool_calls and len(last_message.tool_calls) > 0:
# # # # #         print("---DECISION: CALL TOOLS---")
# # # # #         return "tools"
    
# # # # #     print("---DECISION: END---")
# # # # #     return "end"

# # # # # # --- 4. Assemble the Graph ---

# # # # # workflow = StateGraph(AgentState)
# # # # # workflow.add_node("agent", call_model)
# # # # # workflow.add_node("tools", tool_node)
# # # # # workflow.set_entry_point("agent")
# # # # # workflow.add_conditional_edges(
# # # # #     "agent",
# # # # #     should_continue,
# # # # #     {"tools": "tools", "end": END}
# # # # # )
# # # # # workflow.add_edge("tools", "agent")
# # # # # app = workflow.compile()






# # # # # agent/graph.py
# # # # from typing import Literal, Optional
# # # # from langgraph.graph import StateGraph, END
# # # # from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
# # # # from langchain_community.chat_models import ChatOllama

# # # # # Local Imports
# # # # from .state import AgentState
# # # # from .schemas import PatientInfo, ScheduleRequest
# # # # from tools.db_tools import patient_lookup
# # # # from tools.calendar_tools import check_availability, book_appointment
# # # # from tools.general_tools import get_doctor_list
# # # # from tools.communication_tools import send_confirmation_email, send_confirmation_sms

# # # # # --- 1. LLM Initialization ---
# # # # llm = ChatOllama(model="phi3")

# # # # # --- 2. Tool Definitions ---
# # # # # Note: We call these tools manually now, so we don't bind them to the LLM here.

# # # # # --- 3. Graph Node Functions ---

# # # # def call_patient_lookup(state: AgentState):
# # # #     """Extracts patient info and calls the lookup tool."""
# # # #     print("---NODE: patient_lookup---")
# # # #     # Use structured output to force data extraction
# # # #     structured_llm = llm.with_structured_output(PatientInfo)
# # # #     extraction_prompt = f"""Extract patient name and date of birth from the last message. Conversation history: {state['messages']}"""
# # # #     patient_data = structured_llm.invoke(extraction_prompt)
    
# # # #     # Call the tool with extracted data
# # # #     status = patient_lookup(name=patient_data.name, dob=patient_data.dob)
# # # #     message = AIMessage(content=f"Welcome, {patient_data.name}! Our records show you are a '{status}' patient. Where should we go from here?")
    
# # # #     return {"messages": [message], "patient_status": status, "patient_name": patient_data.name, "dob": patient_data.dob}

# # # # def call_check_availability(state: AgentState):
# # # #     """Extracts doctor/date info and calls the availability tool."""
# # # #     print("---NODE: check_availability---")
# # # #     structured_llm = llm.with_structured_output(ScheduleRequest)
# # # #     extraction_prompt = f"""Extract doctor name and date from the last message. Conversation history: {state['messages']}"""
# # # #     schedule_data = structured_llm.invoke(extraction_prompt)

# # # #     # Call tool
# # # #     available_slots = check_availability(doctor=schedule_data.doctor, date=schedule_data.date)
# # # #     message = AIMessage(content=f"Available slots for Dr. {schedule_data.doctor} on {schedule_data.date}: {', '.join(available_slots)}")
    
# # # #     return {"messages": [message], "doctor": schedule_data.doctor, "date": schedule_data.date}

# # # # def call_get_doctor_list(state: AgentState):
# # # #     """Calls the tool to list all doctors."""
# # # #     print("---NODE: get_doctor_list---")
# # # #     doctors = get_doctor_list()
# # # #     message = AIMessage(content=f"Here are the available doctors: {', '.join(doctors)}")
# # # #     return {"messages": [message]}

# # # # def call_book_appointment(state: AgentState):
# # # #     """Final booking step. Gathers all data from state and books."""
# # # #     print("---NODE: book_appointment---")
# # # #     # This node would gather final details (insurance, time selection) via more complex logic.
# # # #     # For now, we'll simulate a successful booking based on collected state.
    
# # # #     # Placeholder: In a real flow, you'd extract time and insurance here first.
# # # #     # For now, let's assume we have what we need to book.
# # # #     patient_name = state.get("patient_name", "Unknown Patient")
# # # #     doctor = state.get("doctor", "Unknown Doctor")
# # # #     date = state.get("date", "Unknown Date")
# # # #     patient_status = state.get("patient_status", "returning")

# # # #     # Call tool
# # # #     confirmation = book_appointment(
# # # #         patient_name=patient_name,
# # # #         doctor=doctor,
# # # #         date=date,
# # # #         time="09:00", # Placeholder time
# # # #         patient_status=patient_status,
# # # #         insurance_carrier="N/A", # Placeholder insurance
# # # #         insurance_id="N/A"
# # # #     )
# # # #     message = AIMessage(content=confirmation)
# # # #     return {"messages": [message]}

# # # # def decide_next_step(state: AgentState) -> Literal["lookup", "check_availability", "list_doctors", "book", "end"]:
# # # #     """Router to decide the next logical step based on missing information."""
# # # #     print("---ROUTING---")
# # # #     messages = state["messages"]
# # # #     last_message = messages[-1]

# # # #     if state.get("patient_name") is None:
# # # #         return "lookup"
    
# # # #     # Example logic: if user asks for list of doctors
# # # #     if "list" in last_message.content.lower() and "doctor" in last_message.content.lower():
# # # #         return "list_doctors"

# # # #     if state.get("doctor") is None or state.get("date") is None:
# # # #         return "check_availability"

# # # #     # If all info gathered, proceed to booking
# # # #     if state.get("time") is not None: # 'time' would be set by another node
# # # #         return "book"
        
# # # #     return "end" # Fallback

# # # # # --- 4. Assemble the Graph ---
# # # # workflow = StateGraph(AgentState)

# # # # workflow.add_node("lookup", call_patient_lookup)
# # # # workflow.add_node("check_availability", call_check_availability)
# # # # workflow.add_node("list_doctors", call_get_doctor_list)
# # # # workflow.add_node("book", call_book_appointment)

# # # # workflow.set_entry_point("lookup")

# # # # # Simplified routing for demonstration. A real implementation would be more complex.
# # # # workflow.add_conditional_edges(
# # # #     "lookup",
# # # #     decide_next_step,
# # # #     {"lookup": "lookup", "check_availability": "check_availability", "list_doctors": "list_doctors", "book": "book", "end": END}
# # # # )
# # # # workflow.add_edge("list_doctors", END) # Simplified end
# # # # workflow.add_edge("check_availability", END) # Simplified end
# # # # workflow.add_edge("book", END) # Simplified end

# # # # app = workflow.compile()



# # # # agent/graph.py
# # # import json
# # # from typing import Literal, Optional
# # # from langgraph.graph import StateGraph, END
# # # from langchain_core.messages import AIMessage, SystemMessage

# # # # Local Imports
# # # from .state import AgentState
# # # # We don't need schemas.py for this manual approach
# # # # from .schemas import PatientInfo, ScheduleRequest 
# # # from tools.db_tools import patient_lookup
# # # from tools.calendar_tools import check_availability, book_appointment
# # # from tools.general_tools import get_doctor_list
# # # from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# # # from langchain_community.chat_models import ChatOllama

# # # # --- 1. LLM Initialization ---
# # # llm = ChatOllama(model="phi3")

# # # # --- 2. Tool Definitions ---
# # # # Tools will be called manually, so no binding is necessary here.

# # # # --- 3. Graph Node Functions ---

# # # def call_patient_lookup(state: AgentState):
# # #     """Extracts patient info by forcing JSON output and calls the lookup tool."""
# # #     print("---NODE: patient_lookup---")
    
# # #     # Add a system prompt for this specific task
# # #     system_prompt = """You are a data extraction assistant. Based on the conversation history, extract the patient's full name and date of birth. 
# # #     Respond ONLY with a valid JSON object in the format: {"name": "full name", "dob": "YYYY-MM-DD"}. 
# # #     Do not add any other text, greetings, or explanations."""
    
# # #     # Create the prompt for the LLM
# # #     prompt_messages = [SystemMessage(content=system_prompt), state['messages'][-1]]

# # #     try:
# # #         response = llm.invoke(prompt_messages)
# # #         print(f"--- DEBUG: Raw LLM Output for JSON parsing: {response.content} ---")
        
# # #         # Manually parse the JSON string from the LLM response
# # #         # Clean potential markdown code blocks like ```json ... ```
# # #         clean_response = response.content.strip().replace("```json", "").replace("```", "").strip()
# # #         data = json.loads(clean_response)
        
# # #         name = data.get("name")
# # #         dob = data.get("dob")
        
# # #         if not name or not dob:
# # #             raise ValueError("Missing name or dob in JSON response")

# # #     except (json.JSONDecodeError, ValueError, AttributeError) as e:
# # #         print(f"--- ERROR: Failed to parse JSON or extract data. Error: {e} ---")
# # #         message = AIMessage(content="I'm sorry, I had trouble understanding your details. Could you please state your full name and date of birth clearly?")
# # #         return {"messages": [message]}

# # #     # Call the tool with extracted data
# # #     status = patient_lookup(name=name, dob=dob)
# # #     message = AIMessage(content=f"Welcome, {name}! Our records show you are a '{status}' patient. Where should we go from here?")
    
# # #     return {"messages": [message], "patient_status": status, "patient_name": name, "dob": dob}

# # # def call_check_availability(state: AgentState):
# # #     """Placeholder node for checking availability. Needs implementation similar to call_patient_lookup."""
# # #     print("---NODE: check_availability---")
# # #     message = AIMessage(content="Availability check logic needs to be implemented in this node.")
# # #     return {"messages": [message]}

# # # def call_get_doctor_list(state: AgentState):
# # #     """Calls the tool to list all doctors."""
# # #     print("---NODE: get_doctor_list---")
# # #     doctors = get_doctor_list()
# # #     message = AIMessage(content=f"Here are the available doctors: {', '.join(doctors)}")
# # #     return {"messages": [message]}

# # # def call_book_appointment(state: AgentState):
# # #     """Placeholder node for final booking."""
# # #     print("---NODE: book_appointment---")
# # #     message = AIMessage(content="Booking logic needs to be implemented in this node.")
# # #     return {"messages": [message]}

# # # def decide_next_step(state: AgentState) -> Literal["lookup", "check_availability", "list_doctors", "book", "end"]:
# # #     """Router to decide the next logical step based on missing information."""
# # #     print("---ROUTING---")
# # #     messages = state["messages"]
# # #     last_message = messages[-1].content.lower()

# # #     if state.get("patient_name") is None:
# # #         return "lookup"
    
# # #     if "list" in last_message and "doctor" in last_message:
# # #         return "list_doctors"

# # #     if state.get("doctor") is None or state.get("date") is None:
# # #         return "check_availability"
        
# # #     return "end"

# # # # --- 4. Assemble the Graph ---
# # # workflow = StateGraph(AgentState)

# # # workflow.add_node("lookup", call_patient_lookup)
# # # workflow.add_node("check_availability", call_check_availability)
# # # workflow.add_node("list_doctors", call_get_doctor_list)
# # # workflow.add_node("book", call_book_appointment)

# # # workflow.set_entry_point("lookup")

# # # # Simplified routing for demonstration. 
# # # workflow.add_conditional_edges(
# # #     "lookup",
# # #     decide_next_step,
# # #     {"lookup": "lookup", "check_availability": "check_availability", "list_doctors": "list_doctors", "book": "book", "end": END}
# # # )
# # # # Create basic loops for other nodes for further development
# # # workflow.add_edge("list_doctors", "check_availability") 
# # # workflow.add_edge("check_availability", "book") 
# # # workflow.add_edge("book", END)

# # # app = workflow.compile()







# # # agent/graph.py
# # import json
# # import re  # Import the regular expression library
# # from typing import Literal, Optional
# # from langgraph.graph import StateGraph, END
# # from langchain_core.messages import AIMessage, SystemMessage

# # # Local Imports
# # from .state import AgentState
# # from tools.db_tools import patient_lookup
# # from tools.calendar_tools import check_availability, book_appointment
# # from tools.general_tools import get_doctor_list
# # from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# # from langchain_community.chat_models import ChatOllama

# # # --- 1. LLM Initialization ---
# # llm = ChatOllama(model="phi3")

# # # --- 2. Graph Node Functions ---

# # def call_patient_lookup(state: AgentState):
# #     """Extracts patient info by forcing JSON output and calls the lookup tool."""
# #     print("---NODE: patient_lookup---")
    
# #     # Create a prompt that explicitly asks for JSON output
# #     extraction_prompt = f"""
# #     Based on the following conversation history, extract the patient's full name and date of birth.
# #     Respond ONLY with a valid JSON object in the format: {{"name": "full name", "dob": "YYYY-MM-DD"}}.
# #     Do not add any conversational text, greetings, or explanations around the JSON object.

# #     Conversation History:
# #     {state['messages']}
# #     """
    
# #     try:
# #         response = llm.invoke(extraction_prompt)
# #         response_content = response.content
# #         print(f"--- DEBUG: Raw LLM Output for JSON parsing: {response_content} ---")

# #         # --- MODIFIED: Use regex to find the JSON block ---
# #         match = re.search(r"\{.*\}", response_content, re.DOTALL)
# #         if not match:
# #             raise ValueError("No JSON object found in LLM response.")
        
# #         json_string = match.group(0)
# #         data = json.loads(json_string)
# #         # ----------------------------------------------------
        
# #         name = data.get("name")
# #         dob = data.get("dob")
        
# #         if not name or not dob or name == "":
# #             raise ValueError("Missing name or dob in JSON response. Model returned empty values.")

# #     except (json.JSONDecodeError, ValueError, AttributeError) as e:
# #         print(f"--- ERROR: Failed to parse JSON or extract data. Error: {e} ---")
# #         message = AIMessage(content="I'm sorry, I had trouble understanding your details. Could you please state your full name and date of birth clearly?")
# #         return {"messages": [message]}

# #     # Call the tool with extracted data
# #     status = patient_lookup(name=name, dob=dob)
# #     message = AIMessage(content=f"Welcome, {name}! Our records show you are a '{status}' patient. Where should we go from here?")
    
# #     return {"messages": [message], "patient_status": status, "patient_name": name, "dob": dob}

# # def call_check_availability(state: AgentState):
# #     """Placeholder node for checking availability. Needs implementation similar to call_patient_lookup."""
# #     print("---NODE: check_availability---")
# #     # To implement this, you would follow the same pattern as call_patient_lookup:
# #     # 1. Create extraction prompt for doctor and date.
# #     # 2. Call LLM to get JSON.
# #     # 3. Parse JSON.
# #     # 4. Call check_availability tool with extracted data.
# #     message = AIMessage(content="Availability check logic needs to be implemented in this node.")
# #     return {"messages": [message]}

# # def call_get_doctor_list(state: AgentState):
# #     """Calls the tool to list all doctors."""
# #     print("---NODE: get_doctor_list---")
# #     doctors = get_doctor_list()
# #     message = AIMessage(content=f"Here are the available doctors: {', '.join(doctors)}")
# #     return {"messages": [message]}

# # def call_book_appointment(state: AgentState):
# #     """Placeholder node for final booking."""
# #     print("---NODE: book_appointment---")
# #     message = AIMessage(content="Booking logic needs to be implemented in this node.")
# #     return {"messages": [message]}

# # def decide_next_step(state: AgentState) -> Literal["lookup", "check_availability", "list_doctors", "book", "end"]:
# #     """Router to decide the next logical step based on missing information."""
# #     print("---ROUTING---")
# #     messages = state["messages"]
# #     last_message_content = messages[-1].content.lower()

# #     if state.get("patient_name") is None:
# #         # If the last attempt failed, keep trying to look up.
# #         return "lookup"
    
# #     if "list" in last_message_content and "doctor" in last_message_content:
# #         return "list_doctors"

# #     # Add logic here to check if doctor/date information is present in the conversation
# #     # For now, a simplified routing:
# #     if state.get("doctor") is None:
# #         return "check_availability"
        
# #     return "end"

# # # --- 4. Assemble the Graph ---
# # workflow = StateGraph(AgentState)

# # workflow.add_node("lookup", call_patient_lookup)
# # workflow.add_node("check_availability", call_check_availability)
# # workflow.add_node("list_doctors", call_get_doctor_list)
# # workflow.add_node("book", call_book_appointment)

# # workflow.set_entry_point("lookup")

# # workflow.add_conditional_edges(
# #     "lookup",
# #     decide_next_step,
# #     {"lookup": "lookup", "check_availability": "check_availability", "list_doctors": "list_doctors", "book": "book", "end": END}
# # )
# # workflow.add_edge("list_doctors", "check_availability") 
# # workflow.add_edge("check_availability", "book") 
# # workflow.add_edge("book", END)

# # app = workflow.compile()




# # agent/graph.py

# from typing import Literal
# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import ToolNode

# # Import your agent state and tools
# from .state import AgentState
# from tools.db_tools import patient_lookup
# from tools.calendar_tools import check_availability, book_appointment
# from tools.communication_tools import send_confirmation_email, send_confirmation_sms
# from tools.general_tools import get_doctor_list

# from langchain_community.chat_models import ChatOllama
# from langchain_core.utils.function_calling import convert_to_openai_tool

# # --- 1. Initialize Your LLM and Tools ---

# llm = ChatOllama(model="phi3")

# tools = [
#     patient_lookup, 
#     check_availability, 
#     book_appointment, 
#     send_confirmation_email,
#     send_confirmation_sms,
#     get_doctor_list 
# ]

# # Use the .bind() method workaround for tool formatting
# formatted_tools = [convert_to_openai_tool(t) for t in tools]
# llm_with_tools = llm.bind(tools=formatted_tools)

# tool_node = ToolNode(tools)

# # --- 2. Define the Agent's Nodes ---

# def call_model(state: AgentState):
#     """Invokes the LLM with the conversation history."""
#     print("---CALLING MODEL---")
#     messages = state['messages']
#     response = llm_with_tools.invoke(messages)
#     return {"messages": [response]}

# # --- 3. Define the Graph's Router (Conditional Edge) ---

# def should_continue(state: AgentState) -> Literal["tools", "end"]:
#     """Acts as a router, deciding the next step based on the LLM's response."""
#     print("---ROUTING---")
#     last_message = state['messages'][-1]
    
#     if hasattr(last_message, 'tool_calls') and last_message.tool_calls and len(last_message.tool_calls) > 0:
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
#     {"tools": "tools", "end": END}
# )
# workflow.add_edge("tools", "agent")
# app = workflow.compile()









# agent/graph.py

import os
from dotenv import load_dotenv
from typing import Literal
import pandas as pd

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import your agent state and tools
from .state import AgentState
from tools.db_tools import patient_lookup
from tools.calendar_tools import check_availability, book_appointment
from tools.communication_tools import send_confirmation_email, send_confirmation_sms
from tools.general_tools import get_doctor_list

# Import the Google Gemini model
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. Initialize Your LLM and Tools ---

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please make sure it is set in your .env file.")

# Set up the Google Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=google_api_key)

tools = [
    patient_lookup, 
    check_availability, 
    book_appointment, 
    send_confirmation_email,
    send_confirmation_sms,
    get_doctor_list 
]

# Use the standard .bind_tools() method for Gemini
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
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls and len(last_message.tool_calls) > 0:
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
    {"tools": "tools", "end": END}
)
workflow.add_edge("tools", "agent")
app = workflow.compile()