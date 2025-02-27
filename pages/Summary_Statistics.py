import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import util.statistic as stat
#import matplotlib.pyplot as plt
#import seaborn as sns

st.markdown("# More Insight 🎉")

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


if st.button("Submit", type="primary"):
    if not procedure_code_A or not diagnosis_code_B:
        st.warning("Please enter valid codes.")
        st.stop()
    else:
        query = f"""
            SELECT p.subject_id, p.gender, p.anchor_age, d.icd_code as diagnosis, a.admittime, a.dischtime
            FROM procedures_icd proc
            INNER JOIN diagnoses_icd d ON proc.subject_id = d.subject_id AND proc.hadm_id = d.hadm_id
            INNER JOIN patients p ON proc.subject_id = p.subject_id
            INNER JOIN admissions a ON proc.hadm_id = a.hadm_id
            WHERE proc.icd_code = '{procedure_code_A}' 
            AND d.icd_code = '{diagnosis_code_B}';
        """

        with engine.connect() as conn:
            df = pd.read_sql(query, conn) 
            stat.summary_statistics(df)

