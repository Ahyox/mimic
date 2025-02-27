import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def display_sankey(procedure_code_A, diagnosis_code_B, procedures, diagnoses):
    if procedures.empty or diagnoses.empty:
        st.warning("No data found for the given codes.")
        st.stop()

    procedures_A = procedures[procedures["icd_code"].astype(str).str.strip() == procedure_code_A]
    diagnoses_B = diagnoses[diagnoses["icd_code"].astype(str).str.strip() == diagnosis_code_B]

    # Merge all diagnoses to patients who had Procedure A
    merged_data = procedures_A.merge(
        diagnoses, 
        on=["subject_id", "hadm_id"], 
        how="left", 
        suffixes=("_proc", "_diag")
    )

    print(procedures.head())

    # Replace NaN values and classify outcomes
    merged_data["icd_code_diag"].fillna("No Diagnosis", inplace=True)

    # Group by diagnosis type (or outcomes) after Procedure A
    outcome_data = merged_data["icd_code_diag"].value_counts().reset_index()
    outcome_data.columns = ["outcome", "count"]

    # Ensure all possible outcomes are represented, even if the count is 0
    outcome_mapping = {"No Diagnosis": 0}
    for index, row in outcome_data.iterrows():
        outcome_mapping[row["outcome"]] = row["count"]

    # Define Nodes and Labels for the Sankey Diagram
    labels = [f"Procedure A ({procedure_code_A})"] + list(outcome_mapping.keys())
    sources = [0] * len(outcome_mapping)  # All flows start from Procedure A
    targets = list(range(1, len(outcome_mapping) + 1))  # Flow targets are outcomes
    values = list(outcome_mapping.values())

    # Sankey Diagram for Procedure A to All Possible Outcomes
    st.subheader("Procedure A to All Possible Outcomes")
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["#636EFA"] + ["#EF553B"] * (len(outcome_mapping) - 1)  # Colors for each outcome
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=["#AB63FA"] * len(outcome_mapping)  # Same color for all flows
        )
    ))
    #fig.update_layout(title_text="Procedure A to All Possible Outcomes", font_size=12)
    st.plotly_chart(fig)


def auto_generated_sankey(sources, targets, values, labels):
    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
        pad=15, thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    ))
    st.plotly_chart(fig)