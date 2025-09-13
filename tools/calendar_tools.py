
# # # # # # # tools/calendar_tools.py
# # # # # # import pandas as pd
# # # # # # from datetime import datetime
# # # # # # # Import the export function so we can call it directly
# # # # # # from tools.file_tools import export_to_excel

# # # # # # def check_availability(doctor: str, date: str) -> list:
# # # # # #     """Checks the doctor's schedule and returns a list of available time slots."""
# # # # # #     # ... (this function remains the same)
# # # # # #     print(f"🗓️  Checking availability for {doctor} on {date}")
# # # # # #     try:
# # # # # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # # # # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
# # # # # #         available_slots = df[(df['doctor'] == doctor) & (df['date'] == date) & (df['is_available'] == True)]
# # # # # #         if available_slots.empty:
# # # # # #             return ["No available slots found for this day."]
# # # # # #         return available_slots['time'].tolist()
# # # # # #     except FileNotFoundError:
# # # # # #         return ["Error: Schedule data not found."]
# # # # # #     except Exception as e:
# # # # # #         return [f"An error occurred: {e}"]


# # # # # # def book_appointment(doctor: str, date: str, time: str, patient_name: str) -> str:
# # # # # #     """
# # # # # #     Books the appointment for a given patient. Upon success, this tool
# # # # # #     will also automatically log the appointment details for administrative review.
# # # # # #     """
# # # # # #     print(f"✅ Booking appointment for {patient_name} with {doctor} at {time} on {date}")
# # # # # #     try:
# # # # # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # # # # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
# # # # # #         mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # # # # #         matching_slots = df[mask]
        
# # # # # #         if matching_slots.empty:
# # # # # #             return f"Sorry, the slot at {time} is no longer available. Please check the availability again."

# # # # # #         df.loc[mask, 'is_available'] = False
# # # # # #         df.loc[mask, 'patient_name'] = patient_name
# # # # # #         df.to_excel("data/doctor_schedules.xlsx", index=False)
        
# # # # # #         # --- NEW: Automatically call the export function on success ---
# # # # # #         appointment_details = {
# # # # # #             "patient_name": patient_name,
# # # # # #             "doctor": doctor,
# # # # # #             "date": date,
# # # # # #             "time": time
# # # # # #         }
# # # # # #         export_to_excel(appointment_details)
# # # # # #         # -----------------------------------------------------------
        
# # # # # #         return f"Success! The appointment for {patient_name} is confirmed and has been logged."

# # # # # #     except Exception as e:
# # # # # #         return f"An unexpected error occurred while booking: {e}"







# # # # # # tools/calendar_tools.py
# # # # # import pandas as pd
# # # # # from datetime import datetime, timedelta

# # # # # # Import other tools to be called automatically
# # # # # from tools.file_tools import export_to_excel
# # # # # from tools.communication_tools import send_confirmation_email

# # # # # def check_availability(doctor: str, date: str) -> list:
# # # # #     """Checks the doctor's schedule and returns a list of available time slots."""
# # # # #     print(f"🗓️  Checking availability for {doctor} on {date}")
# # # # #     try:
# # # # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # # # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
# # # # #         available_slots = df[(df['doctor'] == doctor) & (df['date'] == date) & (df['is_available'] == True)]
# # # # #         if available_slots.empty:
# # # # #             return ["No available slots found for this day."]
# # # # #         return available_slots['time'].tolist()
# # # # #     except FileNotFoundError:
# # # # #         return ["Error: Schedule data not found."]
# # # # #     except Exception as e:
# # # # #         return [f"An error occurred: {e}"]


# # # # # def book_appointment(
# # # # #     patient_name: str,
# # # # #     doctor: str,
# # # # #     date: str,
# # # # #     time: str,
# # # # #     patient_status: str,
# # # # #     insurance_carrier: str,
# # # # #     insurance_id: str
# # # # # ) -> str:
# # # # #     """
# # # # #     Books a patient's appointment after all information, including insurance, has been collected.
# # # # #     Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
# # # # #     Upon success, it automatically logs the appointment and sends a confirmation email.
# # # # #     You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
# # # # #     """
# # # # #     print(f"✅ Booking appointment for {patient_name} ({patient_status}) with {doctor}")

# # # # #     try:
# # # # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # # # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# # # # #         # --- Smart Scheduling Logic ---
# # # # #         if patient_status.lower() == 'new':
# # # # #             # New patients need two consecutive 30-minute slots (60 minutes total)
# # # # #             start_time_obj = datetime.strptime(time, '%H:%M')
# # # # #             end_time_obj = start_time_obj + timedelta(minutes=30)
# # # # #             second_slot_time = end_time_obj.strftime('%H:%M')
            
# # # # #             print(f"Attempting to book 60-min slot: {time} and {second_slot_time}")

# # # # #             # Find indices for both slots
# # # # #             slot1_mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # # # #             slot2_mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == second_slot_time) & (df['is_available'] == True))
            
# # # # #             slot1_index = df[slot1_mask].index
# # # # #             slot2_index = df[slot2_mask].index

# # # # #             if slot1_index.empty or slot2_index.empty:
# # # # #                 return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

# # # # #             # Book both slots
# # # # #             df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
# # # # #             df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
# # # # #             final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

# # # # #         else: # Returning patients need one 30-minute slot
# # # # #             print(f"Attempting to book 30-min slot: {time}")
# # # # #             mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # # # #             matching_slots = df[mask]

# # # # #             if matching_slots.empty:
# # # # #                 return f"Sorry, the slot at {time} is no longer available. Please check the availability again."

# # # # #             # Book the single slot
# # # # #             df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
# # # # #             final_booking_time = time

# # # # #         # Save the updated schedule back to the Excel file
# # # # #         df.to_excel("data/doctor_schedules.xlsx", index=False)
        
# # # # #         # --- Automatically call export and confirmation tools ---
# # # # #         appointment_details = {
# # # # #             "patient_name": patient_name,
# # # # #             "doctor": doctor,
# # # # #             "date": date,
# # # # #             "time": final_booking_time,
# # # # #             "patient_status": patient_status,
# # # # #             "insurance_carrier": insurance_carrier,
# # # # #             "insurance_id": insurance_id
# # # # #         }
# # # # #         export_to_excel(appointment_details)
# # # # #         send_confirmation_email(patient_email=f"{patient_name.replace(' ', '.').lower()}@example.com", details=str(appointment_details))
        
# # # # #         return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email has been sent."

# # # # #     except Exception as e:
# # # # #         return f"An unexpected error occurred while booking: {e}"




# # # # # tools/calendar_tools.py
# # # # import pandas as pd
# # # # from datetime import datetime, timedelta
# # # # from tools.file_tools import export_to_excel
# # # # from tools.communication_tools import send_confirmation_email

# # # # def check_availability(doctor: str, date: str) -> list:
# # # #     """
# # # #     Checks the doctor's schedule for a specific date to find available time slots.
# # # #     The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
# # # #     """
# # # #     # ... (function logic remains the same)
# # # #     print(f"🗓️  Checking availability for {doctor} on {date}")
# # # #     try:
# # # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-MM-DD')
# # # #         available_slots = df[(df['doctor'] == doctor) & (df['date'] == date) & (df['is_available'] == True)]
# # # #         if available_slots.empty:
# # # #             return ["No available slots found for this day."]
# # # #         return available_slots['time'].tolist()
# # # #     except FileNotFoundError:
# # # #         return ["Error: Schedule data not found."]
# # # #     except Exception as e:
# # # #         return [f"An error occurred: {e}"]

# # # # # ... (book_appointment function remains the same, your previous version is correct) ...
# # # # def book_appointment(patient_name: str, doctor: str, date: str, time: str, patient_status: str, insurance_carrier: str, insurance_id: str) -> str:
# # # #     """
# # # #     Books a patient's appointment after all information, including insurance, has been collected.
# # # #     Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
# # # #     Upon success, it automatically logs the appointment and sends a confirmation email.
# # # #     You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
# # # #     """
# # # #     # ... (function logic remains the same)
# # # #     print(f"✅ Booking appointment for {patient_name} ({patient_status}) with {doctor}")
# # # #     try:
# # # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-MM-DD')
# # # #         if patient_status.lower() == 'new':
# # # #             start_time_obj = datetime.strptime(time, '%H:%M')
# # # #             end_time_obj = start_time_obj + timedelta(minutes=30)
# # # #             second_slot_time = end_time_obj.strftime('%H:%M')
# # # #             print(f"Attempting to book 60-min slot: {time} and {second_slot_time}")
# # # #             slot1_mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # # #             slot2_mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == second_slot_time) & (df['is_available'] == True))
# # # #             slot1_index = df[slot1_mask].index
# # # #             slot2_index = df[slot2_mask].index
# # # #             if slot1_index.empty or slot2_index.empty:
# # # #                 return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."
# # # #             df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
# # # #             df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
# # # #             final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"
# # # #         else:
# # # #             print(f"Attempting to book 30-min slot: {time}")
# # # #             mask = ((df['doctor'] == doctor) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # # #             if df[mask].empty:
# # # #                 return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
# # # #             df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
# # # #             final_booking_time = time
# # # #         df.to_excel("data/doctor_schedules.xlsx", index=False)
# # # #         appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
# # # #         export_to_excel(appointment_details)
# # # #         send_confirmation_email(patient_email=f"{patient_name.replace(' ', '.').lower()}@example.com", details=str(appointment_details))
# # # #         return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email has been sent."
# # # #     except Exception as e:
# # # #         return f"An unexpected error occurred while booking: {e}"













# # # # tools/calendar_tools.py
# # # import pandas as pd
# # # from datetime import datetime, timedelta
# # # from tools.file_tools import export_to_excel
# # # from tools.communication_tools import send_confirmation_email

# # # def check_availability(doctor: str, date: str) -> list:
# # #     """
# # #     Checks the doctor's schedule for a specific date to find available time slots.
# # #     The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
# # #     """
# # #     print(f"🗓️  Checking availability for {doctor} on {date}")
    
# # #     try:
# # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
# # #         # --- MODIFIED: Made the doctor name search case-insensitive ---
# # #         available_slots = df[
# # #             (df['doctor'].str.lower() == doctor.lower()) &  # <-- This is the fix
# # #             (df['date'] == date) & 
# # #             (df['is_available'] == True)
# # #         ]
        
# # #         if available_slots.empty:
# # #             return [f"No available slots found for Dr. {doctor.title()} on this day."]
            
# # #         return available_slots['time'].tolist()
# # #     except FileNotFoundError:
# # #         return ["Error: Schedule data not found."]
# # #     except Exception as e:
# # #         return [f"An error occurred: {e}"]

# # # def book_appointment(
# # #     patient_name: str,
# # #     doctor: str,
# # #     date: str,
# # #     time: str,
# # #     patient_status: str,
# # #     insurance_carrier: str,
# # #     insurance_id: str
# # # ) -> str:
# # #     """
# # #     Books a patient's appointment after all information, including insurance, has been collected.
# # #     Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
# # #     Upon success, it automatically logs the appointment and sends a confirmation email.
# # #     You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
# # #     """
# # #     print(f"✅ Booking appointment for {patient_name} ({patient_status}) with {doctor}")
# # #     try:
# # #         df = pd.read_excel("data/doctor_schedules.xlsx")
# # #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
# # #         # --- MODIFIED: Made the doctor name search case-insensitive here as well ---
# # #         doctor_name_in_file = df['doctor'].str.lower()
        
# # #         if patient_status.lower() == 'new':
# # #             start_time_obj = datetime.strptime(time, '%H:%M')
# # #             end_time_obj = start_time_obj + timedelta(minutes=30)
# # #             second_slot_time = end_time_obj.strftime('%H:%M')
            
# # #             slot1_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # #             slot2_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == second_slot_time) & (df['is_available'] == True))
            
# # #             slot1_index = df[slot1_mask].index
# # #             slot2_index = df[slot2_mask].index

# # #             if slot1_index.empty or slot2_index.empty:
# # #                 return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

# # #             df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
# # #             df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
# # #             final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

# # #         else: # Returning patients
# # #             mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True))
# # #             if df[mask].empty:
# # #                 return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
# # #             df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
# # #             final_booking_time = time

# # #         df.to_excel("data/doctor_schedules.xlsx", index=False)
        
# # #         appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
# # #         export_to_excel(appointment_details)
# # #         send_confirmation_email(patient_email=f"{patient_name.replace(' ', '.').lower()}@example.com", details=str(appointment_details))
        
# # #         return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email has been sent."

# # #     except Exception as e:
# # #         return f"An unexpected error occurred while booking: {e}"











# # # tools/calendar_tools.py
# # import pandas as pd
# # from datetime import datetime, timedelta
# # from tools.file_tools import export_to_excel
# # from tools.communication_tools import send_confirmation_email

# # def check_availability(doctor: str, date: str) -> list:
# #     """
# #     Checks the doctor's schedule for a specific date to find available time slots.
# #     The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
# #     """
# #     print(f"🗓️  Checking availability for {doctor} on {date}")
    
# #     try:
# #         df = pd.read_excel("data/doctor_schedules.xlsx")
# #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
# #         # --- MODIFIED: Made the boolean check robust to handle strings like "true" ---
# #         is_available_mask = df['is_available'].astype(str).str.lower() == 'true'

# #         available_slots = df[
# #             (df['doctor'].str.lower() == doctor.lower()) &
# #             (df['date'] == date) & 
# #             (is_available_mask)  # <-- This is the fix
# #         ]
        
# #         if available_slots.empty:
# #             return [f"No available slots found for Dr. {doctor.title()} on this day."]
            
# #         return available_slots['time'].tolist()
# #     except FileNotFoundError:
# #         return ["Error: Schedule data not found."]
# #     except Exception as e:
# #         return [f"An error occurred: {e}"]

# # def book_appointment(
# #     patient_name: str,
# #     doctor: str,
# #     date: str,
# #     time: str,
# #     patient_status: str,
# #     insurance_carrier: str,
# #     insurance_id: str
# # ) -> str:
# #     """
# #     Books a patient's appointment after all information, including insurance, has been collected.
# #     Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
# #     Upon success, it automatically logs the appointment and sends a confirmation email.
# #     You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
# #     """
# #     print(f"✅ Booking appointment for {patient_name} ({patient_status}) with {doctor}")
# #     try:
# #         df = pd.read_excel("data/doctor_schedules.xlsx")
# #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
# #         # --- MODIFIED: Made the boolean and doctor name checks robust here as well ---
# #         doctor_name_in_file = df['doctor'].str.lower()
# #         is_available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
# #         if patient_status.lower() == 'new':
# #             start_time_obj = datetime.strptime(time, '%H:%M')
# #             end_time_obj = start_time_obj + timedelta(minutes=30)
# #             second_slot_time = end_time_obj.strftime('%H:%M')
            
# #             slot1_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
# #             slot2_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == second_slot_time) & (is_available_mask))
            
# #             slot1_index = df[slot1_mask].index
# #             slot2_index = df[slot2_mask].index

# #             if slot1_index.empty or slot2_index.empty:
# #                 return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

# #             df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
# #             df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
# #             final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

# #         else: # Returning patients
# #             mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
# #             if df[mask].empty:
# #                 return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
# #             df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
# #             final_booking_time = time

# #         df.to_excel("data/doctor_schedules.xlsx", index=False)
        
# #         appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
# #         export_to_excel(appointment_details)
# #         send_confirmation_email(patient_email=f"{patient_name.replace(' ', '.').lower()}@example.com", details=str(appointment_details))
        
# #         return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email has been sent."

# #     except Exception as e:
# #         return f"An unexpected error occurred while booking: {e}"












# # # tools/calendar_tools.py
# # import pandas as pd
# # from datetime import datetime, timedelta

# # # Import other tools to be called automatically
# # from tools.file_tools import export_to_excel
# # from tools.communication_tools import send_confirmation_email, send_confirmation_sms

# # def check_availability(doctor: str, date: str) -> list[str]:
# #     """
# #     Checks the doctor's schedule for a specific date to find available time slots.
# #     The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
# #     """
# #     print(f"--- DEBUG: Inside check_availability tool ---")
# #     print(f"--- DEBUG: Received Doctor: '{doctor}', Date: '{date}' ---")
    
# #     try:
# #         df = pd.read_excel("data/doctor_schedules.xlsx")
        
# #         print(f"--- DEBUG: Raw 'date' column type: {df['date'].dtype} ---")
# #         print(f"--- DEBUG: Raw 'is_available' column type: {df['is_available'].dtype} ---")
        
# #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
# #         doctor_mask = df['doctor'].str.lower() == doctor.lower()
# #         date_mask = df['date'] == date
# #         available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
# #         print(f"--- DEBUG: Matches for Doctor '{doctor.lower()}': {doctor_mask.sum()} ---")
# #         print(f"--- DEBUG: Matches for Date '{date}': {date_mask.sum()} ---")
# #         print(f"--- DEBUG: Matches for 'is_available=true': {available_mask.sum()} ---")
        
# #         available_slots = df[doctor_mask & date_mask & available_mask]
        
# #         print(f"--- DEBUG: Total available slots found: {len(available_slots)} ---")
        
# #         if available_slots.empty:
# #             return [f"No available slots found for Dr. {doctor.title()} on this day."]
            
# #         return available_slots['time'].tolist()
# #     except FileNotFoundError:
# #         return ["Error: Schedule data not found."]
# #     except Exception as e:
# #         return [f"An error occurred: {e}"]


# # def book_appointment(
# #     patient_name: str,
# #     doctor: str,
# #     date: str,
# #     time: str,
# #     patient_status: str,
# #     insurance_carrier: str,
# #     insurance_id: str
# # ) -> str:
# #     """
# #     Books a patient's appointment after all information, including insurance, has been collected.
# #     Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
# #     Upon success, it automatically logs the appointment and sends a confirmation email.
# #     You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
# #     """
# #     print(f"✅ Booking appointment for {patient_name} ({patient_status}) with {doctor}")
# #     try:
# #         df = pd.read_excel("data/doctor_schedules.xlsx")
# #         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
# #         doctor_name_in_file = df['doctor'].str.lower()
# #         is_available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
# #         if patient_status.lower() == 'new':
# #             start_time_obj = datetime.strptime(time, '%H:%M')
# #             end_time_obj = start_time_obj + timedelta(minutes=30)
# #             second_slot_time = end_time_obj.strftime('%H:%M')
            
# #             slot1_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
# #             slot2_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == second_slot_time) & (is_available_mask))
            
# #             slot1_index = df[slot1_mask].index
# #             slot2_index = df[slot2_mask].index

# #             if slot1_index.empty or slot2_index.empty:
# #                 return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

# #             df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
# #             df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
# #             final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

# #         else: # Returning patients
# #             mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
# #             if df[mask].empty:
# #                 return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
# #             df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
# #             final_booking_time = time

# #         df.to_excel("data/doctor_schedules.xlsx", index=False)
        
# #         appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
# #         export_to_excel(appointment_details)
# #         send_confirmation_email(patient_email=f"{patient_name.replace(' ', '.').lower()}@example.com", details=str(appointment_details))
        
# #         return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email has been sent."

# #     except Exception as e:
# #         return f"An unexpected error occurred while booking: {e}"










# # tools/calendar_tools.py
# import pandas as pd
# from datetime import datetime, timedelta

# # Import other tools to be called automatically
# from tools.file_tools import export_to_excel
# # MODIFIED: Import both email and SMS functions
# from tools.communication_tools import send_confirmation_email, send_confirmation_sms

# def check_availability(doctor: str, date: str) -> list[str]:
#     """
#     Checks the doctor's schedule for a specific date to find available time slots.
#     The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
#     """
#     print(f"--- DEBUG: Inside check_availability tool ---")
#     print(f"--- DEBUG: Received Doctor: '{doctor}', Date: '{date}' ---")
    
#     try:
#         df = pd.read_excel("data/doctor_schedules.xlsx")
        
#         print(f"--- DEBUG: Raw 'date' column type: {df['date'].dtype} ---")
#         print(f"--- DEBUG: Raw 'is_available' column type: {df['is_available'].dtype} ---")
        
#         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
#         doctor_mask = df['doctor'].str.lower() == doctor.lower()
#         date_mask = df['date'] == date
#         available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
#         print(f"--- DEBUG: Matches for Doctor '{doctor.lower()}': {doctor_mask.sum()} ---")
#         print(f"--- DEBUG: Matches for Date '{date}': {date_mask.sum()} ---")
#         print(f"--- DEBUG: Matches for 'is_available=true': {available_mask.sum()} ---")
        
#         available_slots = df[doctor_mask & date_mask & available_mask]
        
#         print(f"--- DEBUG: Total available slots found: {len(available_slots)} ---")
        
#         if available_slots.empty:
#             return [f"No available slots found for Dr. {doctor.title()} on this day."]
            
#         return available_slots['time'].tolist()
#     except FileNotFoundError:
#         return ["Error: Schedule data not found."]
#     except Exception as e:
#         return [f"An error occurred: {e}"]


# def book_appointment(
#     patient_name: str,
#     doctor: str,
#     date: str,
#     time: str,
#     patient_status: str,
#     insurance_carrier: str,
#     insurance_id: str
# ) -> str:
#     """
#     Books a patient's appointment after all information, including insurance, has been collected.
#     Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
#     Upon success, it automatically logs the appointment and sends a confirmation email and SMS.
#     You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
#     """
#     print(f"✅ Booking appointment for {patient_name} ({patient_status}) with {doctor}")
#     try:
#         df = pd.read_excel("data/doctor_schedules.xlsx")
#         df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
#         doctor_name_in_file = df['doctor'].str.lower()
#         is_available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
#         if patient_status.lower() == 'new':
#             start_time_obj = datetime.strptime(time, '%H:%M')
#             end_time_obj = start_time_obj + timedelta(minutes=30)
#             second_slot_time = end_time_obj.strftime('%H:%M')
            
#             slot1_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
#             slot2_mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == second_slot_time) & (is_available_mask))
            
#             slot1_index = df[slot1_mask].index
#             slot2_index = df[slot2_mask].index

#             if slot1_index.empty or slot2_index.empty:
#                 return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

#             df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
#             df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
#             final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

#         else: # Returning patients
#             mask = ((doctor_name_in_file == doctor.lower()) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
#             if df[mask].empty:
#                 return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
#             df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
#             final_booking_time = time

#         df.to_excel("data/doctor_schedules.xlsx", index=False)
        
#         appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
#         export_to_excel(appointment_details)
        
#         # --- MODIFIED: Call both email and SMS simulations ---
#         patient_email = f"{patient_name.replace(' ', '.').lower()}@example.com"
#         patient_phone = "555-123-4567" # Using a placeholder phone number for simulation
        
#         send_confirmation_email(patient_email=patient_email, details=str(appointment_details))
#         send_confirmation_sms(patient_phone=patient_phone, details=str(appointment_details))
        
#         # MODIFIED: Updated return message
#         return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email and SMS have been sent."

#     except Exception as e:
#         return f"An unexpected error occurred while booking: {e}"






# tools/calendar_tools.py
import pandas as pd
from datetime import datetime, timedelta
from tools.file_tools import export_to_excel
from tools.communication_tools import send_confirmation_email, send_confirmation_sms

def check_availability(doctor: str, date: str) -> list[str]:
    """
    Checks the doctor's schedule for a specific date to find available time slots.
    The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
    """
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # --- MODIFIED: More robust cleaning of doctor names ---
        doctor_name_in_file = df['doctor'].str.replace('.', '', regex=False).str.lower()
        doctor_to_find = doctor.replace('.', '', regex=False).lower()

        is_available_mask = df['is_available'].astype(str).str.lower() == 'true'

        available_slots = df[
            (doctor_name_in_file == doctor_to_find) &
            (df['date'] == date) & 
            (is_available_mask)
        ]
        
        if available_slots.empty:
            return [f"No available slots found for Dr. {doctor.title()} on this day."]
            
        return available_slots['time'].tolist()
    except Exception as e:
        return [f"An error occurred: {e}"]

def book_appointment(patient_name: str, doctor: str, date: str, time: str, patient_status: str, insurance_carrier: str, insurance_id: str) -> str:
    """
    Books a patient's appointment after all information, including insurance, has been collected.
    Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
    Upon success, it automatically logs the appointment and sends a confirmation email and SMS.
    You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
    """
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # --- MODIFIED: More robust cleaning of doctor names ---
        doctor_name_in_file = df['doctor'].str.replace('.', '', regex=False).str.lower()
        doctor_to_find = doctor.replace('.', '', regex=False).lower()
        is_available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
        if patient_status.lower() == 'new':
            start_time_obj = datetime.strptime(time, '%H:%M')
            end_time_obj = start_time_obj + timedelta(minutes=30)
            second_slot_time = end_time_obj.strftime('%H:%M')
            
            slot1_mask = ((doctor_name_in_file == doctor_to_find) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
            slot2_mask = ((doctor_name_in_file == doctor_to_find) & (df['date'] == date) & (df['time'] == second_slot_time) & (is_available_mask))
            
            slot1_index, slot2_index = df[slot1_mask].index, df[slot2_mask].index

            if slot1_index.empty or slot2_index.empty:
                return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

            df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
            df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
            final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

        else: # Returning patients
            mask = ((doctor_name_in_file == doctor_to_find) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
            if df[mask].empty:
                return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
            df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
            final_booking_time = time

        df.to_excel("data/doctor_schedules.xlsx", index=False)
        
        appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
        export_to_excel(appointment_details)
        
        patient_email = f"{patient_name.replace(' ', '.').lower()}@example.com"
        patient_phone = "555-123-4567"
        
        send_confirmation_email(patient_email=patient_email, details=str(appointment_details))
        send_confirmation_sms(patient_phone=patient_phone, details=str(appointment_details))
        
        return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email and SMS have been sent."
    except Exception as e:
        return f"An unexpected error occurred while booking: {e}"