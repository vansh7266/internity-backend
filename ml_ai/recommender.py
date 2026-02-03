import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import json
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

# ✅ Only change → relative path
df = pd.read_csv("ml_ai/dummy.csv")

#  This function replaces user.json input
def recommend(data):

    stipend_mean = df.loc[df['Stipend'] != 0, 'Stipend'].mean().astype(int)
    data['Stipend'] = int(data.get('Stipend', 0))

    df['Stipend'] = df['Stipend'].replace(0, stipend_mean)

    df1 = df[['InternshipID','Sector','Location','Education','Skills','Interests','Stipend','Mode']]

    def convert2(obj):
        if isinstance(obj, list):
            return obj
        else:
            return [obj]

    df1['Sector'] = df1['Sector'].apply(convert2)
    df1['Location'] = df1['Location'].apply(convert2)
    df1['Education'] = df1['Education'].apply(convert2)
    df1['Mode'] = df1['Mode'].apply(convert2)

    df1['Sector'] = df1['Sector'].apply(lambda x: [i.replace(" ","").lower() for i in x])
    df1['Location'] = df1['Location'].apply(lambda x: [i.replace(" ","").lower() for i in x])
    df1['Education'] = df1['Education'].apply(lambda x: [i.replace(" ","").lower() for i in x])
    df1['Mode'] = df1['Mode'].apply(lambda x: [i.replace(" ","").lower() for i in x])

    def to_list(x):
        return x if isinstance(x, list) else [x]

    a1 = [i.replace(" ","").lower() for i in to_list(data.get("sector", []))]
    a2 = [i.replace(" ","").lower() for i in to_list(data.get("location", []))]
    a3 = [i.replace(" ","").lower() for i in to_list(data.get("education", []))]
    a4 = [i.replace(" ","").lower() for i in to_list(data.get("mode", []))]


    df2 = df1[
        df1['Sector'].apply(lambda x: any(i in x for i in a1)) &
        df1['Location'].apply(lambda x: any(i in x for i in a2)) &
        df1['Education'].apply(lambda x: any(i in x for i in a3)) &
        df1['Mode'].apply(lambda x: any(i in x for i in a4))
    ]

    if df2.empty:
        return {"Recommended_Internships": []}

    df3 = df2[['InternshipID','Skills','Interests','Stipend']]

    df3['Skills'] = df3['Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df3['Interests'] = df3['Interests'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    df3['Skills'] = df3['Skills'].apply(lambda x: [i.replace(" ","").lower() for i in x])
    df3['Interests'] = df3['Interests'].apply(lambda x: [i.replace(" ","").lower() for i in x])

    df3['features'] = df3['Skills'] + df3['Interests']

    df4 = df3[['InternshipID','features','Stipend']]
    df4['features'] = df4['features'].apply(lambda x: " ".join(x))

    b1 = [i.replace(" ","").lower() for i in to_list(data.get("skills", []))]
    b2 = [i.replace(" ","").lower() for i in to_list(data.get("interests", []))]


    user_features_str = " ".join(b1 + b2)

    cv = CountVectorizer()
    feature_vectors = cv.fit_transform(df4['features'])
    user_vector = cv.transform([user_features_str])

    similarity_scores = cosine_similarity(user_vector, feature_vectors)

    top_n = 10
    top_indices = similarity_scores[0].argsort()[-top_n:][::-1]

    top_internships = df4.iloc[top_indices]['InternshipID'].values
    top_internships_list = top_internships.tolist()

    recommended_full_info = df[df['InternshipID'].isin(top_internships_list)]
    recommended_full_info = recommended_full_info.sort_values(by='Stipend', ascending=False)

    recommended_info_dict = recommended_full_info.to_dict(orient="records")

    output_data = {
        "Recommended_Internships": recommended_info_dict
    }

    # ✅ Only change → return instead of file
    return output_data
