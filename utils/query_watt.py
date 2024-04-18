import requests
import pandas as pd
from pprint import pprint
from csv import writer
import itertools
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)

webpilot_api_key =  os.getenv("WEBPILOT_API_KEY")


def scrape_website(question, company_url):
    print(webpilot_api_key, 'api key')

    url = 'https://beta.webpilotai.com/api/v1/watt'

    headers = {
    'Authorization': f'Bearer {webpilot_api_key}'
    }

    body = {
        "model": "wp-watt-3.52-16k",
        "content": f"""
            As an experienced and detailed researcher, your task is to determine whether a list of given companies belongs in a particular sector. You will be provided with a sector name and definition, along with a list of companies that we are analyzing to be part of the sector.
            Here is the sector name: Mobility Focused Behavior/Telematic Data Platforms
            Here is the sector definition: The sector focuses on firms that gather and interpret mobility and telematics data, offering advanced analytics to refine transport systems and inform customer behaviors. These companies utilize technology to analyze movement data, optimizing operational efficiency, safety, and user engagement in mobility.
            
            If your are asked to create a list of items, Please generate a comma-separated list of the items. 

            Please access these websites and answer the following questions,  list the items with each items comma separated
            {company_url}

            Questions:
            {question}

        """
    }


    res = requests.post(url, json=body, headers=headers)
    
    print(res, 'res')

    json_res = res.json()


    return json_res['content']