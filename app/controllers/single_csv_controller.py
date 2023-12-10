from flask import Flask, json, Response
from app.utils import read_csv, find_row_by_id

app = Flask(__name__)

@app.route('/franchises/<int:franchise_id>', methods=['GET'])
def display_single_csv(franchise_id):
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    selected_row = find_row_by_id(csv_data, franchise_id)

    if selected_row:
        formatted_row = {
            "id" : row["franchise_id"],
            "name": row["franchise_name"],
            "description": row["description"],
            "type": row["franchise_type"],
            "category": row["franchise_category"],
            "costs": row["costs"],
            "totalOutlets": row["total_outlets"],
            "websiteUrl": row["website_url"],
            "phoneNumber": row["phone_number"],
            "emailAddress": row["email_address"],
            "yearEstablished": row["year_established"],
            "companyName": row["company_name"],
            "companyAddress": row["company_address"],
            "netProfitsPerMonth": row["net_profits_per_month"],
            "licenseDurationInYears": row["license_duration_in_years"],
            "royaltyFeesPerMonth": row["royalty_fees_per_month"],
            "returnOfInvestment": row["return_of_investments"],
            "logoImageUrl": row["logo_image_url"],
            "imageUrl": row["image_url"]
        }
        json_data = json.dumps(formatted_row, indent=2, sort_keys=False)
        return Response(json_data, content_type='application/json')
    else:
        return Response(json.dumps({'error': 'Franchise ID not found'}), content_type='application/json'), 404
