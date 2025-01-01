import streamlit as st
import json
import os

# Define a path for the saved data file
DATA_FILE = 'community_data.json'

# Function to load saved data
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.warning("The data file is corrupted. Starting with an empty dataset.")
            return {}
    else:
        return {}

# Function to save data
def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Load the existing data when the app starts
saved_data = load_data()

# Display the existing community data
st.title("This is an app for sharing your thoughts")
st.write("This app allows everyone to contribute their ideas, and the data gets saved automatically")

# Show and manage the current data
if saved_data:
    st.write("### The current data as of now:")
    for name, contributions in saved_data.items():
        st.write(f"**{name}:**")
        for i, contribution in enumerate(contributions, 1):
            st.write(f"{i}. {contribution}")
else:
    st.write("No data found. Start contributing!")

# Option to clear all data within the data display section
st.subheader("Manage Data")
clear_data = st.button("Show all data")



# Allow users to add new data
st.subheader("Add Your Contribution")

name = st.text_input("Your Name:")
contribution = st.text_area("Your Contribution (e.g., idea, feedback, suggestion):")

# Handle form submission
if st.button("Submit"):
    if name and contribution:
        # Check if the user already contributed
        if name in saved_data:
            # Avoid duplicate contributions from the same user
            if contribution not in saved_data[name]:
                saved_data[name].append(contribution)
                save_data(saved_data)
                st.success(f"Thank you for your new contribution, {name}!")
            else:
                st.warning(f"You've already submitted this contribution, {name}. Try a different idea or suggestion!")
        else:
            # If the user is new, create an entry with the first contribution
            saved_data[name] = [contribution]
            save_data(saved_data)
            st.success(f"Thank you for your contribution, {name}!")
    else:
        st.error("Please fill in both fields before submitting.")
