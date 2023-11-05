import os
from dotenv import load_dotenv

load_dotenv()

def serve():
    os.system("cd src && uvicorn main:app --host 0.0.0.0 --port 80 --reload")
