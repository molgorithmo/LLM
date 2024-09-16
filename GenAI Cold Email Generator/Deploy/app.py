import pandas as pd
import uuid
import chromadb
import streamlit as st
import dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from Util.util import Utils
from Database.db_client import *
from langchain_core.output_parsers import JsonOutputParser

dotenv.load_dotenv('GenAI Cold Email Generator\api.env')

class ColdEmailGenerator:
    def __init__(self) -> None:
        '''
        init
        '''
        self.llm = ChatGroq(
            temperature=0,
            model_name='llama-3.1-70b-versatile'
        )
        self.utils = Utils()
        self.vc = VectorClient()

    def etl_json(self, url: str, company_name: str) -> JsonOutputParser:
        '''
        1. Extract the page content from the link
        2. Transform the page content to json string format
        3. Load the content as JSON Object
        
        :param url: Job's URL
        :param company_name: Name of the company whose job url is provided.
        :return: JSON Object
        '''
        page_data = self.utils.load_job_details(url)
        scraping_prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of the company {company}.
            Your job is to extract the job postings and return them in JSON format
            contaning the following keys: `role,` `experience,` `skills` and `description.`
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        scraping_chain = scraping_prompt | self.llm
        json_response_str = scraping_chain.invoke(
            {
                'page_data': page_data,
                'company': company_name
            }
        )

        return self.utils.string_to_json_object(json_response_str)
    
    def query_collection(self, query: any, collection)-> str:
        
        return collection.query(
            query_texts=query, 
            n_results=2
            ).get('metadatas', [])
    
    def instantiate_collection(self, df):
        self.vc.insert_data_to_collection(df)
        return self.vc.get_collection()

    def get_email_from_llm(self, json_response: JsonOutputParser, queried_links: list) -> str:
        email_chain = self.utils.email_prompt | self.llm
        return email_chain.invoke(
            input={
                'job_description': json_response['description'],
                'link_list': queried_links
            }
        )

if __name__ == '__main__':
    
    # Loading the environment variable
    Utils().load_env()

    st.header("Cold Email Generator :email:")
    
    portfolio_data = pd.read_csv('.\Data\my_portfolio.csv')

    with st.form(key='my_form'):
        url = st.text_input('Enter job URL', placeholder='https://')
        company_name = st.text_input('Enter companies name', placeholder='e.g. Nike')
        generate_button = st.form_submit_button(label='Generate')
    
    if generate_button:

        ceg = ColdEmailGenerator()
        json_response = ceg.etl_json(url, company_name)

        collection = ceg.instantiate_collection(portfolio_data)

        links = ceg.query_collection(json_response['skills'], collection)

        response = ceg.get_email_from_llm(
            json_response,
            links
            )
    
        st.write(response.content)


