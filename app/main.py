import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Enter your portfolio link")
    portfolio_input = st.text_input("Enter your portfolio URL:", value="", key="portfolio_url")

    st.title("📧 Cold Mail Generator")
    job_url_input = st.text_input("Enter job profile URL:", value="", key="job_url")
    submit_button = st.button("Submit", key="submit")

    if submit_button:
        try:
            # Load and clean the portfolio data
            portfolio_loader = WebBaseLoader([portfolio_input])
            portfolio_data = clean_text(portfolio_loader.load().pop().page_content)
            
            # Extract skills and load portfolio
            # skills_data = portfolio.extract_skills_and_match_jobs(portfolio_data, llm)
            # portfolio.load_portfolio(data=skills_data)
            
            # Load and clean the job profile data
            job_loader = WebBaseLoader([job_url_input])
            job_data = clean_text(job_loader.load().pop().page_content)
            jobs = llm.extract_jobs(job_data)
            
            # Match skills and generate email
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
