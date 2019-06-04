from flask import Flask, render_template, request
from backend.utils.geo import get_ipv4_networks_for_bbox
from flask_cors import CORS

application = Flask(__name__,
    static_folder = "./dist/static",
    template_folder = "./dist")

cors = CORS(application, resources={r"/api/*": {"origins": "*"}})

@application.route('/api/ipv4bbox', methods=['POST'])
def ipv4bbox():
    return get_ipv4_networks_for_bbox(request.get_json().get('bbox'))

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0')