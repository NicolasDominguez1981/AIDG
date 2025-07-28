import streamlit as st
import pandas as pd
import io
from github import Github
import base64

st.title("TCS Uruguay AI Initiatives.")

# Form fields
name = st.text_input("Name")
employee_number = st.text_input("Employee Number")
profile_type = st.selectbox("Profile Type", ["Non-Technical", "Somewhat technical", "Technical"])

# GitHub details
GITHUB_TOKEN = "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"
REPO_NAME = "NicolasDominguez1981/AIDG"
FILE_PATH = "employee_data.xlsx"

if st.button("Submit"):
    if not name or not employee_number:
        st.error("Please fill in all fields.")
    else:
        try:
            # Authenticate with GitHub
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(REPO_NAME)
            contents = repo.get_contents(FILE_PATH)

            # Download and update Excel
            excel_bytes = base64.b64decode(contents.content)
            df = pd.read_excel(io.BytesIO(excel_bytes))
            new_row = {"Name": name, "Employee Number": employee_number, "Profile Type": profile_type}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Save to bytes
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            # Update file on GitHub
            repo.update_file(
                path=FILE_PATH,
                message="Update employee data",
                content=output.read(),
                sha=contents.sha
            )
            st.success("Data saved to GitHub successfully!")
        except Exception as e:
            st.error(f"Error saving data: {e}")
