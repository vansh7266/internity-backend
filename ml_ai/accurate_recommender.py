import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "dummy.csv")

df = pd.read_csv(CSV_PATH)


def recommend_best(user_data, recommended_list):
    user_data = {
        "skills": user_data.get("skills", []),
        "interests": user_data.get("interests", [])
    }

    id_list = [i["InternshipID"] for i in recommended_list]

    df1 = df[df['InternshipID'].isin(id_list)][['InternshipID','Skills','Interests']]

    df1['Skills'] = df1['Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df1['Interests'] = df1['Interests'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    df1['Skills'] = df1['Skills'].apply(lambda x:[i.replace(" ","").lower() for i in x])
    df1['Interests'] = df1['Interests'].apply(lambda x:[i.replace(" ","").lower() for i in x])

    df1['features'] = df1['Skills'] + df1['Interests']
    df1['features'] = df1['features'].apply(lambda x:" ".join(x))

    def to_list(x):
        return x if isinstance(x, list) else [x]

    b1 = [i.replace(" ","").lower() for i in to_list(user_data['skills'])]
    b2 = [i.replace(" ","").lower() for i in to_list(user_data['interests'])]

    user_features_str = " ".join(b1 + b2)

    document = [user_features_str] + df1['features'].tolist()

    cv = CountVectorizer()
    vector = cv.fit_transform(document)

    scores = cosine_similarity(vector[0], vector[1:]).flatten()
    best_index = np.argmax(scores)

    best_id = int(df1.iloc[best_index]['InternshipID'])

    best = [i for i in recommended_list if i["InternshipID"] == best_id][0]

    return best
