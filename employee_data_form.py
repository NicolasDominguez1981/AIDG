import streamlit as st
import pandas as pd
import os

st.title("TCS Uruguay AI Initiatives.")

# Form fields
name = st.text_input("Name")
employee_number = st.text_input("Employee Number")
profile_type = st.selectbox("Profile Type", ["Non-Technical", "Somewhat technical", "Technical"])

# Excel file path
excel_path = "https://raw.githubusercontent.com/NicolasDominguez1981/AIDG/main/employee_data.xlsx"

if st.button("Submit"):
    if not name or not employee_number:
        st.error("Please fill in all fields.")
    else:
        # Prepare data
        new_row = {"Name": name, "Employee Number": employee_number, "Profile Type": profile_type}
        # Check if file exists
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row]
        df.to_excel(excel_path, index=False)
        st.success("Data saved successfully!")
