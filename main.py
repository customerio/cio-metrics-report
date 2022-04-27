from flask import Flask
import os
from flask import Flask, request
from dotenv import load_dotenv
import generator

load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True

@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response

##########################################
### Handle incoming request
##########################################
@app.route('/generate', methods=['POST'])
def generateReport():
    req = request.get_json()
    return generator.buildReport(req)

##########################################
### Run Server
##########################################

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))