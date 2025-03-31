from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()
origins = [
    "*"
]

class Contract (BaseModel):
    j1:str
    j2:str
    address:str


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uri=os.environ.get('mongo_uri')
print(uri)
client = MongoClient(uri,server_api=ServerApi('1'))

try:

    client.admin.command('ping')
    print("Pinged")
    db = client['RPS']
    collection = db['RPSDATA']
except Exception as e:
    print(e)



@app.post("/api/addContract/")
async def addContract(contract:Contract):
    print(contract)
    j1=contract.j1.capitalize()
    j2=contract.j2.capitalize()
    collection.insert_one({"j1":j1,"j2":j2,"address":contract.address})

    return ({"status":"OK"})

@app.get("/api/myContracts/{address:str}/")
async def myContracts(address):
    print(address)
    docs=collection.find({"j1":address.capitalize()}, {'_id': 0}).to_list()
    return ({"contracts":docs})

@app.get("/api/myChallenges/{address:str}/")
async def myChallenges(address):
    docs=collection.find({"j2":address.capitalize()}, {'_id': 0}).to_list()
    print(docs)
    return ({"contracts":docs})

@app.delete("/api/deleteContract/{address}/")
async def deleteContract(address):
    collection.delete_one({"address":address})
    return ({"status":"OK"})
