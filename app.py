import os
import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# Set the OpenAI API key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Create the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set the page configuration
st.set_page_config(page_title="One-Click Proposal Writer")

# Proposal template
proposal_template = """
Proposal
Company Name: [user_biz_name]
[prospect_biz_name] Proposal  

Executive Summary
(Company Name) presents this proposal to [Client Name] with the aim of addressing the strategic challenges facing your organization and driving sustainable growth and success. Our proposal outlines a comprehensive approach to [briefly summarize the main objectives of the proposal, such as optimizing operations, entering new markets, or improving profitability]. Through a combination of data-driven analysis, strategic insights, and actionable recommendations, we are confident in our ability to deliver tangible results that align with your organization's goals.

Introduction
Dear [Client Name],
We are thrilled to present this proposal to you and your esteemed organization. At (Company Name), we are committed to partnering with our clients to tackle their most pressing challenges and unlock opportunities for growth and innovation. With our extensive experience, industry expertise, and proven track record of success, we are confident that we can provide valuable insights and strategic guidance to support your organization's journey towards excellence.

Client Background
[Client Name] is a leading [industry/sector] organization that has been at the forefront of [industry/sector] for [number of years]. With a strong reputation for [highlight key strengths or achievements], your organization has consistently demonstrated resilience and adaptability in a rapidly evolving market landscape. However, as the [industry/sector] continues to undergo significant transformations, it has become imperative for [Client Name] to reassess its strategic priorities and explore new avenues for growth and innovation.

... (rest of the template)
"""

# Web scraper function
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        return text
    except Exception as e:
        return f"Error scraping website: {e}"

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

    # Optional Fields
    st.subheader("Optional Fields")
    client_linkedin, client_linkedin_data = None, None
    client_linkedin_input = st.text_input("Learn from Client's LinkedIn", key="client_linkedin", value="", help="Provide the client's LinkedIn profile URL (optional)")
    client_linkedin_submit = st.form_submit_button("Learn from LinkedIn")
    if client_linkedin_submit:
        client_linkedin_data = scrape_website(client_linkedin_input)

    client_website, client_website_data = None, None
    client_website_input = st.text_input("Learn from Client's Website", key="client_website", value="", help="Provide the client's website URL (optional)")
    client_website_submit = st.form_submit_button("Learn from Website")
    if client_website_submit:
        client_website_data = scrape_website(client_website_input)

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

    if client_linkedin_data:
        user_inputs += f"\n\nLearn from Client's LinkedIn:\n{client_linkedin_data}"

    if client_website_data:
        user_inputs += f"\n\nLearn from Client's Website:\n{client_website_data}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a proposal writing assistant. Your task is to generate a complete and compelling sales proposal using the provided template and user inputs. The proposal must be fully fleshed out, with all sections filled in and no placeholders left. The proposal should be tailored to the specific prospect and offer details provided."},
            {"role": "user", "content": f"{user_inputs}\n\nProposal Template:\n{proposal_template}"}
        ],
        max_tokens=3000,  # Increase the maximum token limit to ensure a complete proposal
        temperature=0.7,  # Adjust the temperature to balance coherence and creativity
    )

    proposal = response.choices[0].message.content
    st.subheader("Generated Proposal")
    st.write(proposal)

