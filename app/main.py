from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.auth import verify_token
from ml_ai.recommender import recommend
from fastapi import Body
from ml_ai.accurate_recommender import recommend_best


app = FastAPI()

@app.get("/")
def root():
    return {"status": "Internity Backend Running"}

# ALLOW BROWSER REQUESTS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow from any frontend for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from app.database import create_user_if_not_exists



@app.get("/protected")
def protected(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Token missing")

    token = authorization.split(" ")[1]
    user = verify_token(token)

    create_user_if_not_exists(user["uid"], user["email"])

    return {"message": "Welcome", "uid": user["uid"]}



@app.post("/recommend")
def get_recommendation(data: dict = Body(...)):
    return recommend(data)



@app.post("/accurate")
def accurate_recommend(data: dict):
    return recommend_best(data["user"], data["recommendations"])


