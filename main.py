from fastapi import FastAPI
import motor.motor_asyncio 

app = FastAPI()
connection_url = "mongodb+srv://apaul45:password123apaul@cluster0.qr58u.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
db = motor.motor_asyncio.AsyncIOMotorClient(connection_url).torqatadb
imdb_collection = db.get_collection("imdb_shows")
user_collection = db.get_collection("users")

import crud
import aggregation
import user

app.include_router(crud.router)
app.include_router(aggregation.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"msg": "Welcome to my backend"}