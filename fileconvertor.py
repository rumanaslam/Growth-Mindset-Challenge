import streamlit as st
import pandas as pd
from io import BytesIO

# Page configuration
st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader
uploaded_files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"File: {uploaded_file.name}")
        
        # Read file based on extension
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Display dataframe preview
        st.write("Preview:")
        st.dataframe(df.head())

        # Data cleaning options
        if st.checkbox(f"Remove Duplicates - {uploaded_file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates removed!")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {uploaded_file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with mean!")
            st.dataframe(df.head())

        # Column selection
        selected_columns = st.multiselect(f"Select Columns - {uploaded_file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Chart display
        if st.checkbox(f"Show Chart - {uploaded_file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File conversion
        format_choice = st.radio(f"Convert {uploaded_file.name} to:", ["csv", "Excel"], key=uploaded_file.name)
        
        if st.button(f"Download {uploaded_file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_file_name = uploaded_file.name.replace(file_extension, "csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_file_name = uploaded_file.name.replace(file_extension, "xlsx")
            
            output.seek(0)
            st.download_button(
                label="Download File",
                data=output,
                file_name=new_file_name,
                mime=mime_type
            )
            st.success("Processing complete!")