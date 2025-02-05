'''
This file is a reference to collecting pdf data and storing it in the database.
'''

from .users import ping_server

from pydantic import BaseModel

class PDF(BaseModel):
    pdf_id: str
    user_name:str
    email:str
    primary_skill_set:str
    years_of_experience:str


async def insert_pdf(pdf_id:str,user_name:str,email:str,primary_skill_set:str,years_of_experience:str):
    client = await ping_server()
    db = client["job_hunter"]
    collection = db["pdf_data"]
    data = PDF(pdf_id=pdf_id, user_name=user_name, email=email, primary_skill_set=primary_skill_set, years_of_experience=years_of_experience).dict()
    try:
        await collection.insert_one(data)
        print("PDF data inserted successfully")
        return True
    except Exception as e:
        print(e)
        return False





