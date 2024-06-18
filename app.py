import requests
import streamlit as st
from streamlit.commands.page_config import set_page_config

# Set the page configuration
set_page_config(page_title="One-Click Proposal Writer")

# Get the OpenAI API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Function to call OpenAI API
def generate_proposal(user_inputs):
    API_URL = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_inputs}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit app
st.title("One-Click Proposal Writer")

with st.form("proposal_form"):
    # Prospect Business Details
    st.subheader("Prospect Business Details")
    prospect_biz_name = st.text_input("Business Name", key="prospect_biz_name")
    prospect_address = st.text_input("Address", key="prospect_address")
    prospect_phone = st.text_input("Phone", key="prospect_phone")
    prospect_email = st.text_input("Email", key="prospect_email")

    # User's Business Details
    st.subheader("Your Business Details")
    user_biz_name = st.text_input("Business Name", key="user_biz_name")
    user_name = st.text_input("Your Name", key="user_name")

    # Offer + Pricing
    st.subheader("Offer + Pricing Details")
    offer_details = st.text_area("Describe your offer and pricing", key="offer_details")

    # Submit button
    submitted = st.form_submit_button("Generate Proposal")

# Call the function after form submission
if submitted:
    user_inputs = f"""
    Prospect Business Details:
    Business Name: {prospect_biz_name}
    Address: {prospect_address}
    Phone: {prospect_phone}
    Email: {prospect_email}

    Your Business Details:
    Business Name: {user_biz_name}
    Your Name: {user_name}

    Offer + Pricing Details:
    {offer_details}
    """

    proposal = generate_proposal(user_inputs)
    st.subheader("Generated Proposal")
    st.write(proposal)

