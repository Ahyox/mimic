import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

#procedure_code_A = "45.23" #diagnosis_code_B = "K91.89"
def summary_statistics(df):
    if df.empty:
        st.warning("No data found for the given codes.")
        st.stop()

    col1, col2 = st.columns(2)
    # Calculate additional statistics
    anchor_age = df['anchor_age']
    age_mean = df['anchor_age'].mean()
    age_median = df['anchor_age'].median()
    gender_distribution = df['gender'].value_counts(normalize=True) * 100

    # Calculate length of stay
    df['admittime'] = pd.to_datetime(df['admittime'])
    df['dischtime'] = pd.to_datetime(df['dischtime'])
    df['length_of_stay'] = (df['dischtime'] - df['admittime']).dt.days
    los_mean = df['length_of_stay'].mean()
    los_median = df['length_of_stay'].median()

    # Display calculated statistics
    print(f"Average Age: {age_mean:.2f}")
    print(f"Median Age: {age_median:.2f}")
    print(f"Gender Distribution:\n{gender_distribution}")
    print(f"Average Length of Stay: {los_mean:.2f} days")
    print(f"Median Length of Stay: {los_median:.2f} days")


    st.title("Visualization of Procedure A → Diagnosis B")

    # Age Distribution Histogram
    st.subheader("Age Distribution")
    fig = px.histogram(
        df, x='anchor_age', title='Age Distribution for Procedure A → Diagnosis B',
        labels={'anchor_age': 'Age'}, color_discrete_sequence=['skyblue'], 
        nbins=20  # Increase number of bins for better granularity
    )
    fig.update_layout(
        bargap=0.1,  # Reduce bar width for better separation
        xaxis_title="Age",
        yaxis_title="Count",
        xaxis=dict(tickmode="linear", tick0=10, dtick=5)
    )
    st.plotly_chart(fig)

    # Gender Distribution Pie Chart
    st.subheader("Gender Distribution")
    fig = px.pie(df, names='gender', title='Gender Distribution for Procedure A → Diagnosis B',
                color_discrete_sequence=['#66b3ff', '#99ff99'], hole=0.3)
    st.plotly_chart(fig)

    # Length of Stay Boxplot
    st.subheader("Length of Stay")
    fig = px.box(df, x='length_of_stay', title='Length of Stay for Procedure A → Diagnosis B',
                labels={'length_of_stay': 'Days'}, color_discrete_sequence=['orange'])
    fig.update_layout(
        yaxis_title="Days",
        xaxis_title="Length of Stay"
    )
    st.plotly_chart(fig)

    # Time Analysis: Distribution of Diagnosis B over Time
    st.subheader("Monthly Distribution of Diagnosis B")
    df['month'] = df['admittime'].dt.month
    monthly_distribution = df['month'].value_counts().sort_index().reset_index()
    monthly_distribution.columns = ['Month', 'Count']

    fig = px.bar(
        monthly_distribution, x='Month', y='Count', title='Monthly Distribution of Diagnosis B after Procedure A',
        labels={'Month': 'Month', 'Count': 'Number of Cases'}, color_discrete_sequence=['purple']
    )
    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=1, dtick=1),  # Ensure each month is clearly labeled
        yaxis_title="Number of Cases",
        xaxis_title="Month"
    )
    st.plotly_chart(fig)
