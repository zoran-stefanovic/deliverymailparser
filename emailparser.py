from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def extract_email_info(email_content):
    # Detecting the delivery company
    if 'PostNL' in email_content:
        delivery_company = 'PostNL'
    elif 'DHL' in email_content:
        delivery_company = 'DHL'
    else:
        delivery_company = 'Unknown'

    # Regular expressions for extracting sender, date, and time
    sender_regex = r'Afzender\n(.+)' if delivery_company == 'PostNL' else r'van ([\w\s]+)\.'
    date_regex = r'op (\w+\s\d{1,2} \w+)' if delivery_company == 'PostNL' else r'Verwacht bezorgmoment\n\n(\w+\s\d{1,2} \w+)'
    time_regex = r'(\d{1,2}:\d{2} en \d{1,2}:\d{2})' if delivery_company == 'PostNL' else r'(\d{1,2}\.\d{2} - \d{1,2}\.\d{2})'

    # Extracting information using regex
    sender_match = re.search(sender_regex, email_content)
    date_match = re.search(date_regex, email_content)
    time_match = re.search(time_regex, email_content)

    sender = sender_match.group(1).strip() if sender_match else 'Unknown'
    delivery_date = date_match.group(1).strip() if date_match else 'Unknown'
    delivery_time = time_match.group(1).strip() if time_match else 'Unknown'

    return delivery_company, sender, delivery_date, delivery_time

@app.route('/parse_email', methods=['POST'])
def parse_email():
    email_content = request.json.get('email_content', '')
    parsed_data = extract_email_info(email_content)
    return jsonify({
        "delivery_company": parsed_data[0],
        "sender": parsed_data[1],
        "delivery_date": parsed_data[2],
        "delivery_time": parsed_data[3]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
