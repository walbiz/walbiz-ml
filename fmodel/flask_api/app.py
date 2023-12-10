from flask import Flask, request, jsonify
import pickle
from sentence_transformers import SentenceTransformer, util
import torch
import json
import pandas as pd

app = Flask(__name__)

# Load the embeddings and sentences from the pickle files
with open('../models/embedding.pkl', 'rb') as file:
    embeddings = pickle.load(file)
with open('../models/sentences.pkl', 'rb') as file:
    sentences = pickle.load(file)

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the CSV dataset
csv_dataset_path = '../dataset/franchise_walbiz.csv'
df = pd.read_csv(csv_dataset_path)

# @app.route('/franchises', methods=['GET'])
# @app.route('/franchises/:id', methods=['POST'])
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
    return json.dumps(response, indent=2)  # Add indent parameter for formatting

if __name__ == '__main__':
    app.run(debug=True, port=8080)
