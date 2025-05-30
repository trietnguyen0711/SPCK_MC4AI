# firebase_setup.py
import firebase_admin
from firebase_admin import credentials, db

# Chỉ khởi tạo nếu chưa có app nào
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://spckmc4ai-c9bde-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

hash_ref = db.reference("uploaded_hashes")
