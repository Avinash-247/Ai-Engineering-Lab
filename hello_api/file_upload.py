# from fastapi import FastAPI,File,UploadFile
# from typing import Annotated
# app=FastAPI()

# # @app.post("/file")
# # def create_user(File: Annotated[bytes,File()]):
# #     return {"file_Size":len(File)}

# @app.post("/uploadfile")
# def create_upload_file(file:UploadFile):
#     return {"upload_file":file.filename}
