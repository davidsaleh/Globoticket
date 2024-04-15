from flask import Flask, request, jsonify  
from flask import render_template
from flask_cors import CORS 
import requests  
import os  
from dotenv import load_dotenv  
  
load_dotenv()  # take environment variables from .env.  
api_key = os.getenv("TICKETMASTER_API_KEY")  # replace with your actual API key  
  
app = Flask(__name__)  
CORS(app)  # This will enable CORS for all routes  

@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/events', methods=['GET'])  
def get_events():  
    city = request.args.get('city', default = '*', type = str)  
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&apikey={api_key}"  
        
    response = requests.get(url)  
  
    if response.status_code == 200:  
        events = response.json()  
        return jsonify(events)  
    else:  
        return jsonify({"error": "API request failed"}), response.status_code  
  
@app.route('/events/<event_id>/images', methods=['GET'])  
def get_event_images(event_id):  
    locale = request.args.get('locale', default = '*', type = str)  
    domain = request.args.getlist('domain')  # getlist will return a list of domain parameters  
    domain = ','.join(domain)  # join the list into a comma-separated string  
        
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}/images.json?apikey={api_key}&locale={locale}&domain={domain}"  
        
    response = requests.get(url)  
  
    if response.status_code == 200:  
        images = response.json()  
        return jsonify(images)  
    else:  
        return jsonify({"error": "API request failed"}), response.status_code    
  
if __name__ == '__main__':  
    app.run(debug=True)  
