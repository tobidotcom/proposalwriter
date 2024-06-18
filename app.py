import os
import streamlit as st
from openai import OpenAI

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

Problem Statement
In recent years, [Client Name] has faced several challenges related to [briefly outline key challenges or pain points, such as declining market share, operational inefficiencies, or competitive pressures]. These challenges have hindered the organization's ability to [achieve specific goals or objectives, such as maximizing profitability, enhancing customer satisfaction, or expanding market reach]. To address these issues effectively, [Client Name] requires strategic guidance and actionable solutions tailored to its unique needs and circumstances.

Proposed Solution
(Company Name) proposes a comprehensive solution aimed at addressing the key challenges facing [Client Name] and unlocking opportunities for sustainable growth and success. Our approach will encompass the following key components:

Strategic Analysis: We will conduct a thorough assessment of [Client Name]'s current market position, competitive landscape, and internal capabilities to identify areas of strength and opportunities for improvement.

Operational Optimization: Through data-driven analysis and best practices benchmarking, we will identify opportunities to streamline operations, optimize processes, and enhance efficiency across key functional areas.

Market Expansion Strategy: Leveraging our industry expertise and market insights, we will develop a tailored market expansion strategy to help [Client Name] capitalize on emerging trends, penetrate new markets, and diversify its revenue streams.

Organizational Transformation: We will work closely with [Client Name] to drive organizational change and foster a culture of innovation, agility, and continuous improvement to support long-term growth and sustainability.

Approach
Our approach to implementing the proposed solution will involve a phased and collaborative process, as follows:

Discovery Phase: We will commence the engagement with a series of discovery sessions to gain a deep understanding of [Client Name]'s business objectives, challenges, and opportunities.

Analysis Phase: Based on the insights gathered during the discovery phase, we will conduct a comprehensive analysis of [Client Name]'s internal and external environments to identify strategic priorities and develop actionable recommendations.

Strategy Development: Working closely with [Client Name]'s leadership team, we will collaboratively develop a tailored strategy aligned with the organization's vision, mission, and values.

Implementation and Monitoring: Following the approval of the strategy, we will support [Client Name] in implementing the recommended initiatives and monitoring progress against key performance indicators (KPIs) to ensure alignment with strategic objectives and desired outcomes.

Value Proposition
At (Company Name), we pride ourselves on our ability to deliver measurable value and tangible results to our clients. By partnering with us, [Client Name] can expect to benefit from:

Actionable Insights: Our data-driven approach and industry expertise enable us to provide actionable insights and strategic guidance tailored to [Client Name]'s unique needs and objectives.

Collaborative Partnership: We view our client relationships as true partnerships, built on trust, transparency, and mutual respect. We will work closely with [Client Name] to co-create solutions and drive sustainable business outcomes.

Long-Term Impact: Our solutions are designed to deliver long-term value and sustainable impact, ensuring that [Client Name] is well-positioned for success in an ever-changing market landscape.

Team Expertise
The success of our engagement with [Client Name] will be driven by the collective expertise and experience of our consulting team. Led by [Lead Consultant Name], our team comprises seasoned professionals with diverse backgrounds and skill sets, including:

[Lead Consultant Name]: [Brief bio highlighting relevant experience and expertise]
[Team Member 1]: [Brief bio highlighting relevant experience and expertise]
[Team Member 2]: [Brief bio highlighting relevant experience and expertise]
[Additional Team Members]: [Brief bios highlighting relevant experience and expertise]

Case Studies
As evidence of our ability to deliver results, we would like to share the following case studies of similar projects we have successfully completed:

[Case Study 1 Title]: [Brief overview of the project, objectives, approach, and outcomes]
[Case Study 2 Title]: [Brief overview of the project, objectives, approach, and outcomes]
[Case Study 3 Title]: [Brief overview of the project, objectives, approach, and outcomes]

Client Testimonials
Don't just take our word for it. Here's what some of our satisfied clients have to say about their experience working with (Company Name):

"Working with (Company Name) has been a game-changer for our organization. Their strategic insights and actionable recommendations have enabled us to achieve significant improvements in [specific outcomes]." - [Client Testimonial 1]

"The (Company Name) team demonstrated an exceptional level of professionalism, expertise, and commitment throughout our engagement. Their strategic guidance and collaborative approach were instrumental in helping us navigate complex challenges and achieve our business objectives." - [Client Testimonial 2]

"We are extremely pleased with the results of our partnership with (Company Name). Their innovative solutions and deep industry knowledge have positioned us for sustained growth and success in the years to come." - [Client Testimonial 3]

Next Steps
We are excited about the opportunity to collaborate with [Client Name] and support your organization on its journey towards excellence. To discuss the details of our proposal further or address any questions or concerns you may have, please feel free to contact [Lead Consultant Name] at [Lead Consultant Email] or [Lead Consultant Phone Number]. We look forward to the possibility of working together and making a meaningful impact on your organization's success.

Conclusion
In conclusion, McKinsey & Company is committed to partnering with [Client Name] to address its strategic challenges, unlock opportunities for growth and innovation, and drive sustainable business outcomes. With our proven expertise, collaborative approach, and relentless focus on delivering value, we are confident in our ability to support [Client Name] on its journey towards excellence. Thank you for considering our proposal, and we look forward to the opportunity to work together.

Appendix
[Include any additional supporting materials, such as detailed analyses, charts, graphs, or references, that supplement the main proposal content.]

Contact Information
[Provide contact details for the primary point of contact at McKinsey & Company, including name, title, email, and phone number.]
"""

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


