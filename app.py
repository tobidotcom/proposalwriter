import os
import streamlit as st
from openai import OpenAI

# Set the OpenAI API key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Create the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set the page configuration
set_page_config(page_title="One-Click Proposal Writer")

# Function to call OpenAI API
def generate_proposal(user_inputs, model_name):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_inputs}
        ]
    )
    return response.choices[0].message.content

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

    # Fine-tuned model name
    fine_tuned_model = st.text_input("Fine-tuned Model Name", value="gpt-3.5-turbo", key="fine_tuned_model")

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

    proposal = generate_proposal(user_inputs, fine_tuned_model)
    st.subheader("Generated Proposal")
    st.write(proposal)

