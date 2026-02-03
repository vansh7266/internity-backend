import firebase_admin
from firebase_admin import credentials, auth




cred = credentials.Certificate("/Users/vanshgupta/Desktop/vansh/BACKEND/app/internity-backend-firebase-adminsdk-fbsvc-2c040a9c67.json")
firebase_admin.initialize_app(cred)




def verify_token(id_token: str):
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token






