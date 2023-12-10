from flask import Flask, json, Response, request
from app.utils import read_csv, format_csv_data, find_row_by_id
from sentence_transformers import SentenceTransformer, util
import torch, pickle
import pandas as pd

app = Flask(__name__)

with open('./app/models/embedding.pkl', 'rb') as file:
    embeddings = pickle.load(file)

with open('./app/models/sentences.pkl', 'rb') as file:
    sentences = pickle.load(file)

model = SentenceTransformer('all-MiniLM-L6-v2')
csv_dataset_path = './app/dataset/franchise_walbiz.csv'
df = pd.read_csv(csv_dataset_path)

@app.route('/franchises/discover', methods=['POST'])
def recommend():
    data = request.get_json()
    franchise_you_like = data['discover']
    cosine_scores = util.cos_sim(embeddings, model.encode(franchise_you_like))
    top_similar_franchise = torch.topk(cosine_scores, dim=0, k=5, sorted=True)
    
    recommendations = []
    for i in top_similar_franchise.indices:
        # Use the index i to retrieve information from the DataFrame
        franchise_info = df.iloc[i.item()]
        
        recommendation_dict = {
            'id': str(franchise_info['franchise_id']),
            'name': franchise_info['franchise_name'],
            'type': franchise_info['franchise_type'],
            'category': franchise_info['franchise_category'],
            'costs': str(franchise_info['costs']),
            'logoImageUrl': franchise_info['logo_image_url'],
            'imageUrl': franchise_info['image_url']
            # Add more key-value pairs as needed for other information
        }
        recommendations.append(recommendation_dict)
    
    response = {'franchises': recommendations}
    return json.dumps(response, indent=2)
