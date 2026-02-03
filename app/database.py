from firebase_admin import firestore

db = firestore.client()



def create_user_if_not_exists(uid, email):
    ref = db.collection("users").document(uid)
    if not ref.get().exists:
        ref.set({
            "email": email,
            "created_at": firestore.SERVER_TIMESTAMP
        })



