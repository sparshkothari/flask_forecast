from flask import Blueprint, render_template, request
from werkzeug.wrappers.response import Response
import json
from models import ForecastObj
from forecast.forecast_models.forecast_model_container import ForecastModelContainer

views_bp = Blueprint('views_bp', __name__)


@views_bp.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@views_bp.route('/forecast_profile', methods=['GET'])
def forecast_profile():
    return render_template("forecastProfile.html")


@views_bp.route('/simulate_forecast', methods=['POST'])
def simulate_forecast():
    base_model = str(request.form["baseModel"])
    timeframe_multiplier = float(request.form["timeframeMultiplier"])
    timeframe_unit = int(request.form["timeframeUnit"])
    timeframe_increment_multiplier = float(request.form["timeframeIncrementMultiplier"])

    forecast_container_obj = ForecastModelContainer(
        base_model=base_model,
        timeframe_multiplier=timeframe_multiplier,
        timeframe_unit=timeframe_unit,
        timeframe_increment_multiplier=timeframe_increment_multiplier)
    o = json.dumps(forecast_container_obj.run())

    ForecastObj.drop_collection()
    forecast_database_obj = ForecastObj(data_string=o)
    forecast_database_obj.save()

    response_data = o
    response_status = 200
    return Response(response_data, response_status)


@views_bp.route('/forecast_data', methods=['GET'])
def forecast_data():
    if ForecastObj.objects:
        o = ForecastObj.objects.first().data_string
        response_data = o
        response_status = 200
        return Response(response_data, response_status)
    else:
        response_data = json.dumps([])
        response_status = 200
        return Response(response_data, response_status)
