'''
This file will contain the database operations for the users.
'''
from datetime import datetime
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel

async def ping_server():
  # Replace the placeholder with your Atlas connection string
  uri = os.getenv("MONGO_CON")

  # Set the Stable API version when creating a new client
  client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

  # Send a ping to confirm a successful connection
  try:
      await client.admin.command('ping')

      return client
      print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
      print(e)

class Users(BaseModel):
   user_id: str
   name: str
   email: str
   created_at: datetime=datetime.utcnow()#Default value is current time
   updated_at: datetime=datetime.utcnow()#Default value is current time
 

async def insert_user(user_id:str,name:str,email:str,created_at:datetime,updated_at:datetime):
   
   try:
    client = await ping_server()
    db=client.job_hunter
    collection=db.users
    user_info=Users(user_id=user_id,name=name,email=email,created_at=created_at,updated_at=updated_at)
    # Convert Pydantic model to dictionary before inserting
    user_dict = user_info.dict()
    await collection.insert_one(user_dict)
    print("User inserted successfully")
    return True
   
   except Exception as e:
      print(e)
      return None

async def upsert_user(user_id:str,updated_at:datetime):
   try:
      client = await ping_server()
      db=client.job_hunter
      collection=db.users
      await collection.update_one({"user_id": user_id}, {"$set": {"updated_at": updated_at}})
      print("User updated successfully")

      return True
   except Exception as e:
      print(e)
      return None

async def get_user(user_id:str):
   try:
      client = await ping_server()
      db=client.job_hunter
      collection=db.users
      user=await collection.find_one({"user_id": user_id})
      print("User found in the database")
      return True
   except Exception as e:
      print(e)
      return False
