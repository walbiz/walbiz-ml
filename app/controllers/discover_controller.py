from flask import Flask, json, Response, request
from app.utils import read_csv, format_csv_data, find_row_by_id
from sentence_transformers import SentenceTransformer, util
import torch, pickle
import pandas as pd

app = Flask(__name__)

def initialize_data():
    with open('./app/models/embedding.pkl', 'rb') as file:
        embeddings = pickle.load(file)

    with open('./app/models/sentences.pkl', 'rb') as file:
        sentences = pickle.load(file)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    csv_dataset_path = './app/dataset/franchise_walbiz.csv'
    df = pd.read_csv(csv_dataset_path)

    return embeddings, sentences, model, df

@app.route('/franchises/discover', methods=['POST'])
def recommend():
    embeddings, sentences, model, df = initialize_data()

    data = request.get_json()
    print(data)
    franchise_you_like = data['discover']
    cosine_scores = util.cos_sim(embeddings, model.encode(franchise_you_like))
    top_similar_franchise = torch.topk(cosine_scores, dim=0, k=5, sorted=True)
    
    recommendations = []
    for i in top_similar_franchise.indices:
        row = df.iloc[i.item()]
        
        recommendation_dict = {
            "id": str(row["franchise_id"]),
            "name": row["franchise_name"],
            "type": row["franchise_type"],
            "category": row["franchise_category"],
            "costs": str(row["costs"]),
            "logoImageUrl": row["logo_image_url"],
        }
        recommendations.append(recommendation_dict)
    
    json_data = json.dumps({'franchises': recommendations}, indent=2, sort_keys=False)
    return Response(json_data, content_type='application/json')