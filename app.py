import os
import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import inch
from PIL import Image as PILImage

# Set the OpenAI API key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Create the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set the page configuration
st.set_page_config(page_title="One-Click Proposal Writer")

# Proposal template
proposal_template = """
# Proposal

## Executive Summary

[Executive Summary]

## Company Background

[Company Background]

## Proposed Solution

[Proposed Solution]

## Pricing

[Pricing]

## Terms and Conditions

[Terms and Conditions]
"""

# Function to generate the PDF
def generate_pdf(proposal_text, file_name, user_biz_name, user_name, logo_image):
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add a cover page with company logo
    cover_title = Paragraph("Proposal", styles["Heading1"])
    cover_title.style.alignment = TA_CENTER
    elements.append(cover_title)
    elements.append(Spacer(1, 24))
    if logo_image:
        logo = Image(logo_image, width=2*inch, height=2*inch)
        logo.hAlign = "CENTER"
        elements.append(logo)
    elements.append(Spacer(1, 36))

    # Add the proposal text to the PDF
    proposal_style = ParagraphStyle(
        name="ProposalStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=16,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
    )
    proposal_paragraph = Paragraph(proposal_text, proposal_style)
    elements.append(proposal_paragraph)

    # Add a footer with company details
    footer_style = ParagraphStyle(
        name="FooterStyle",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
    )
    footer_text = f"{user_biz_name} | {user_name}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(Spacer(1, 36))
    elements.append(footer)

    # Build the PDF
    doc.build(elements)

    return file_name

# Streamlit app
st.title("One-Click Proposal Writer")

# User input fields
prospect_biz_name = st.text_input("Prospect Business Name")
prospect_address = st.text_input("Prospect Address")
prospect_phone = st.text_input("Prospect Phone")
prospect_email = st.text_input("Prospect Email")
user_biz_name = st.text_input("Your Business Name")
user_name = st.text_input("Your Name")
offer_details = st.text_area("Offer + Pricing Details")
client_linkedin_url = st.text_input("Client's LinkedIn URL (optional)")
client_website_url = st.text_input("Client's Website URL (optional)")

# Logo upload
logo_image = None
uploaded_file = st.file_uploader("Upload your company logo (optional)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    logo_image = PILImage.open(uploaded_file)
    logo_image = logo_image.convert("RGB")
    logo_image.save("assets/company_logo.png")
    logo_image = "assets/company_logo.png"

# Scrape data from LinkedIn and website
client_linkedin_data = ""
if client_linkedin_url:
    response = requests.get(client_linkedin_url)
    soup = BeautifulSoup(response.content, "html.parser")
    client_linkedin_data = soup.get_text()

client_website_data = ""
if client_website_url:
    response = requests.get(client_website_url)
    soup = BeautifulSoup(response.content, "html.parser")
    client_website_data = soup.get_text()

# Form submission
submitted = st.button("Generate Proposal")

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
        max_tokens=3000,
        temperature=0.7,
    )

    proposal = response.choices[0].message.content

    # Generate the PDF with the generated proposal text
    pdf_file = generate_pdf(proposal, f"{prospect_biz_name}_proposal.pdf", user_biz_name, user_name, logo_image)

    # Download button
    with open(pdf_file, "rb") as file:
        btn = st.download_button(
            label="Download Proposal",
            data=file.read(),
            file_name=pdf_file,
            mime="application/pdf"
        )
