#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass


# In[ ]:


if "today" not in st.session_state:
    st.session_state.today = []

# Set default goals if not already set
default_goals = {
    "Calories_goal_limit": 2500,
    "Protein_goal": 50,
    "Carbs_goal": 200,
    "Fat_goal": 50
}
for key, val in default_goals.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Input Values
with st.sidebar:
    st.header("🎯 Set Your Daily Goals")
    st.session_state["Calories_goal_limit"] = st.number_input("Calories Goal", min_value=0, value=st.session_state["Calories_goal_limit"], step=100)
    st.session_state["Protein_goal"] = st.number_input("Protein Goal (g)", min_value=0, value=st.session_state["Protein_goal"], step=10)
    st.session_state["Carbs_goal"] = st.number_input("Carbs Goal (g)", min_value=0, value=st.session_state["Carbs_goal"], step=10)
    st.session_state["Fat_goal"] = st.number_input("Fat Goal (g)", min_value=0, value=st.session_state["Fat_goal"], step=2)

@dataclass
class Food:
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int


st.title("Calorie & Macro Tracker")

calories_sum = sum(f.calories for f in st.session_state.today)
fat_sum = sum(f.fat for f in st.session_state.today)
protein_sum = sum(f.protein for f in st.session_state.today)
carbs_sum = sum(f.carbs for f in st.session_state.today)
calorie_diff = max(st.session_state["Calories_goal_limit"] - calories_sum, 0)


# Input Values
with st.form("food_form"):
    st.subheader("Add New Food")
    name = st.text_input("Name")
    calories = st.number_input("Calories", min_value=0, step=10)
    protein = st.number_input("Protein (g)", min_value=0, step=1)
    carbs = st.number_input("Carbs (g)", min_value=0, step=1)
    fat = st.number_input("Fat (g)", min_value=0, step=1)
    submitted = st.form_submit_button("Add Food")

    if submitted:
        food = Food(name, calories, protein, carbs, fat)
        st.session_state.today.append(food)
        st.success(f"Added {name}!")

# Visualisation
if st.session_state.today:
    st.subheader("Progress Visualization")

    # initialisation and pie chart breakdown
    calories_sum = sum(f.calories for f in st.session_state.today)
    fat_sum = sum(f.fat for f in st.session_state.today)
    protein_sum = sum(f.protein for f in st.session_state.today)
    carbs_sum = sum(f.carbs for f in st.session_state.today)
    calorie_diff = max(st.session_state["Calories_goal_limit"] - calories_sum, 0)

    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    axs[0, 0].pie([protein_sum, fat_sum, carbs_sum],labels=["Protein", "Fat", "Carbs"],autopct="%1.1f%%")
    axs[0, 0].set_title("Macros Distribution")

    # Actual vs Goal Bar Chart 
    axs[0, 1].bar([0, 1, 2], [protein_sum, fat_sum, carbs_sum], width=0.4, label="Consumed")
    axs[0, 1].bar([0.5, 1.5, 2.5], [st.session_state["Protein_goal"],st.session_state["Fat_goal"],st.session_state["Carbs_goal"]], width=0.4, label="Goal")
    axs[0,1 ].legend()


    # Pie chart for Calories progress
    axs[1, 0].pie([calories_sum, calorie_diff],labels=["Calories Intake Today", "Remaining"],autopct="%1.1f%%")
    axs[1, 0].set_title("Calories Goal Progress")

    # Line chart - Calories over time
    axs[1, 1].plot(list(range(len(st.session_state.today))),[st.session_state["Calories_goal_limit"]] * len(st.session_state.today),label="Calories Goal")
    axs[1, 1].plot(list(range(len(st.session_state.today))),np.cumsum([f.calories for f in st.session_state.today]),label="Calories Eaten")
    axs[1, 1].set_title("Calories Over Time")
    axs[1, 1].legend()

    fig.tight_layout()
    st.pyplot(fig)

else:
    st.info("Add some food to start tracking!")


