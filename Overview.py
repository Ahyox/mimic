import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import util.overview as overview
import util.create_sankey as sankey
import json
import plotly.graph_objects as go

st.markdown("# Overview 🎉")


left_column, right_column = st.columns(2)

# Load credentials from secrets.toml
db_config = st.secrets["mysql"]

# Create connection string
engine = create_engine(
    f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)


# Load Data for Procedure A and Diagnosis B
procedure_column, diagnosis_column = st.columns(2)

with procedure_column:
    procedure_code_A = st.text_input("Enter Procedure Code A")

with diagnosis_column:
    diagnosis_code_B = st.text_input("Enter Diagnosis Code B")


prompt = st.text_input("Enter your search term here")

if st.button("Submit", type="primary"):
    if not procedure_code_A or not diagnosis_code_B:
        st.warning("Please enter valid codes.")
        st.stop()
    else:
        if prompt:
            try:
                response = sankey.TextGenerator(prompt).generate(True)
                response = json.loads(response)

                query = response['query']
                query_param_count = response['query_param_count']

                print("QUERY: ", response)
                query = query.format(procedure_A = "'"+procedure_code_A+"'", diagnosis_B = "'"+diagnosis_code_B+"'")
                
                with engine.connect() as conn:
                    df = pd.read_sql(query, conn) 
                    #st.code(response["sankey_code"], language="python")

                    # Execute the generated code
                    if df.empty:
                        st.warning("No data found for the given inputs.")
                    else:
                        # Execute the received sankey function
                        exec(response['sankey_code'], globals())  # Runs the function in global scope
                        fig = create_sankey(df)  # Call the generated function
                        st.plotly_chart(fig)
            except Exception as e:
                st.error(f"An error occurred: {e}")  
                                
        else:
            # Query to get procedures
            query_procedures = "SELECT subject_id, hadm_id, icd_code FROM procedures_icd"

            # Query to get diagnoses
            query_diagnoses = "SELECT subject_id, hadm_id, icd_code FROM diagnoses_icd"

            with engine.connect() as conn:
                procedures = pd.read_sql(query_procedures, conn)
                diagnoses = pd.read_sql(query_diagnoses, conn)
                overview.display_sankey(procedure_code_A, diagnosis_code_B, procedures, diagnoses)



