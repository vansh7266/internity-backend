import firebase_admin
from firebase_admin import credentials,auth


firebase_path = "/etc/secrets/firebase.json"

cred = credentials.Certificate(firebase_path)
firebase_admin.initialize_app(cred)





def verify_token(id_token: str):
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token






