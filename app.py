from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

from views.home import home_bp
from views.views_water_forecast import views_water_forecast_bp
from views.view_error import view_error_bp

import sys

sys.dont_write_bytecode = True

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MONGODB_SETTINGS'] = {
    "db": "waterForecast",
}
db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app)
app.register_blueprint(home_bp)
app.register_blueprint(view_error_bp)
app.register_blueprint(views_water_forecast_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)