import os


def serve():
    os.system("cd src && uvicorn main:app --reload")
