from openai import OpenAI
import streamlit as st

openai_key = st.secrets["openai"]
client = OpenAI(
    api_key= openai_key["key"],
)

class TextGenerator:
    def __init__(self, msg, tone=None):
        self.message = msg
        self.tone = tone

    def generate(self, should_return_json=True):
        try:
            system_prompt = """I have four MIMIC-IV data tables in my MySQL database (defaultdb).
            Table 'admissions' has columns (hadm_id, subject_id, admittime, dischtime),
            'diagnoses_icd' has (subject_id, hadm_id, icd_code, icd_version),
            'patients' has (subject_id, gender, anchor_age, anchor_year),
            and 'procedures_icd' has (subject_id, hadm_id, icd_code, icd_version).

            I want your response to be in this JSON format:
            {
            "query" : "SELECT ....... {procedure_A} and {diagnosis_B}",
            "query_param_count": 2,
            "sankey_code": ""
            }
            
            Use placeholders in curly braces like {placeholder}.
            In the query, don't forget to dot the table name with the database name like mimicdb.table_name.

            For the Sankey diagram, write a function named create_sankey(df), where df is the DataFrame obtained from the SQL query.
            This function should generate a **Sankey diagram using Streamlit and Plotly**. It should:
            - Extract relevant columns from `df`
            - Define **nodes** and **links** dynamically based on the data
            - Assign **labels** for nodes
            - Build the **Sankey diagram**
            - Return a Plotly figure

            The function **must not include any import statements**.

            For query_param_count, return the count of placeholders (`{}`) used in the query.

            For every prompt from now, you must return both the SQL query and the create_sankey(df) function.
            """
            message_array = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.message},
            ]
        
            if should_return_json:
                response = client.chat.completions.create(
                    messages=message_array,
                    model="gpt-4o",
                    response_format={"type": "json_object"}
                )
            else:
                response = client.chat.completions.create(
                    messages=message_array,
                    model="gpt-4-1106-preview",
                    temperature=0.8,
                    presence_penalty=2,
                    top_p=1
                )

        except Exception as e:
            return f"Error: {str(e)}"

        return response.choices[0].message.content

