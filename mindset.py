import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title== "Data sweeper",layout='wide' )

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
)
#title and description
st.title("Datasweeper Sterling Intergrater By M Areeb Shaikh")
st.write("Transfoam your files between CVS and excel formats with build-in data cleaning and visualization Creating the project for quater 3!")

#file uploader
uploaded_files = st.file_uploader("upload your file (accepts cvs or excel):",type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_cvs(file)
        elif file_ext == "xlsx":
            df =pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        #file details
        st.write("preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("Dta cleaning option")
        if st.cheakbox(f"clean data for {file.name}"):
            col1, col2 = st.colums(2)

            with col1:
                if st.button(f"remove duplicate from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("duplicates removed!")

            with col2:
                if st.button(f"fill missing values for {file.name}"):
                    numeric_cols =df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing value have been filled!")

        st.subheader("Select Coloums to keep")
        columns = st.multiselect(f"choose columns for {file.nme}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion Options

        st.subheader("conversion options")
        conversion_type = st.radio(f"convert {file.name} to:", ["CVS" , "Excel"], key=file.name)
        if st.button(f"Conver{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CVS":
                df.to.cvs(buffer, index=False)
                file_name = file.name.replace(file_ext,".cvs")
                mime_type = "text/cvs"

            elif conversion_type =="Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
                buffer.seek(0)

                st.download_button(
                    label=f"Download{file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                
                )

st.success("All files processed successfully!")
        


        