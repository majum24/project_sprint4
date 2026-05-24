import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Diabetes Risk Analysis")

df = pd.read_csv("diabetes_012_health_indicators_BRFSS2015.csv")

# map variables
df["Sex"] = df["Sex"].map({0: "female", 1: "male"})
df["Diabetes_Status"] = df["Diabetes_012"].map({
    0: "No Diabetes",
    1: "Prediabetes",
    2: "Diabetes"
})

age_map = {
    1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39",
    5: "40-44", 6: "45-49", 7: "50-54", 8: "55-59",
    9: "60-64", 10: "65-69", 11: "70-74", 12: "75-79", 13: "80+"
}

df["Age_Group"] = df["Age"].map(age_map)

# Sidebar filters
st.sidebar.header("Filters")

selected_age = st.sidebar.selectbox(
    "Select age group",
    ["All"] + list(age_map.values())
)

selected_sex = st.sidebar.selectbox(
    "Select sex",
    ["All", "female", "male"]
)

# Apply filters
filtered_df = df.copy()

if selected_age != "All":
    filtered_df = filtered_df[filtered_df["Age_Group"] == selected_age]

if selected_sex != "All":
    filtered_df = filtered_df[filtered_df["Sex"] == selected_sex]

st.write(f"Showing data for: **{selected_age} | {selected_sex}**")

# Gender Distribution
st.subheader("Gender Distribution")

gender_pct = (filtered_df["Sex"].value_counts(normalize=True) * 100).round(2)
st.bar_chart(gender_pct)

# BMI vs Physical Health
st.subheader("BMI vs Physical Health")

sample_df = filtered_df.sample(
    min(2000, len(filtered_df)),
    random_state=42
)

fig, ax = plt.subplots()

sns.scatterplot(
    data=sample_df,
    x="BMI",
    y="PhysHlth",
    hue="Diabetes_Status",
    alpha=0.3,
    ax=ax
)

plt.title("BMI vs Physical Health by Diabetes Status")
plt.xlabel("BMI (Body Mass Index)")
plt.ylabel("Days of Poor Physical Health")

st.pyplot(fig)