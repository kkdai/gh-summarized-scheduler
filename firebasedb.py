import os
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin
firebase_url = os.environ["FIREBASE_URL"]
# service_account_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
# cred = credentials.Certificate(service_account_info)
cred = credentials.ApplicationDefault()

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {"databaseURL": firebase_url})


# 新增資料: add data to specified path
def add_data(path: str, data: dict):
    ref = db.reference(path)
    return ref.push(data)


# 檢查資料: get data from specified path
def get_data(path: str):
    ref = db.reference(path)
    return ref.get()


# 刪除資料: delete data at specified path
def delete_data(path: str):
    ref = db.reference(path)
    ref.delete()
