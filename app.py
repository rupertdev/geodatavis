from flask import Flask, render_template, request
from backend.utils.geo import get_ipv4_networks_for_bbox
from flask_cors import CORS

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/ipv4bbox', methods=['POST'])
def ipv4bbox():
    return get_ipv4_networks_for_bbox(request.get_json().get('bbox'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")