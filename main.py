from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Depends, Body
from utils.query_watt import scrape_website
import pandas as pd
import itertools
from csv import writer
from fastapi.responses import FileResponse
from pprint import pprint

app = FastAPI()







@app.post("/upload")
async def query(question: Annotated[str | None, Body()], file: UploadFile = File(...)):
    
    csv_name = file.filename
    store = f"files/{csv_name}"
    
    contents = await file.read()
    with open(store, 'wb') as f:
        f.write(contents)
        
    
    df = pd.read_csv(store)
    transformed_data = df.groupby('company_name')[['homepage_url']].apply(lambda x: x.values.tolist()).to_dict()
    limited_data = dict(itertools.islice(transformed_data.items(), 3))
    result_dict = {}
    

    for i, j in limited_data.items():
        res = scrape_website(question, j[0][0])
        result_dict[i] = res
        
    with open(f'file_res/{csv_name}', 'a', encoding="utf16", newline='') as fd:
        csv_writer = writer(fd, delimiter=",")

        csv_writer.writerow([
                    'Name of Company',
                    question
                    ])
        for name, result in result_dict.items():
            print(name, result)
            csv_writer.writerow([
                name,
                result
                ])
        
    return FileResponse(f'file_res/{csv_name}', media_type='application/octet-stream', filename=csv_name)

    