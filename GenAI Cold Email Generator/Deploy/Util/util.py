import dotenv

from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate

class Utils:
    def __init__(self):
        self.email_prompt = EMAIL_PROMPT = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are a business development executive at ABCQP Services. ABCQP Services is an AI & software consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools.
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability,
            process optimization, cost reduction, and heightened overall efficiency.
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase ABCQP Services's portfolio: {link_list}
            Remember you are a business development executive at ABCQP Services.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        self.collection_name = 'portfolio'

    def string_to_json_object(self, response: str) -> JsonOutputParser:
        '''
        Convert string object to JSON object

        :param response: String input in json format
        :return: JSON object of that string
        '''
        json_parser = JsonOutputParser()
        return json_parser.parse(response.content)

    def load_job_details(self, url):
        loader = WebBaseLoader(url)
        return loader.load().pop().page_content

    def load_env(self):
        return dotenv.load_dotenv('api.env')