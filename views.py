from flask import Blueprint, render_template, session, request
from werkzeug.wrappers.response import Response
import json
from models import ForecastObj
from water_forecast.forecast_models.forecast_model_container import ForecastModelContainer

views_bp = Blueprint('views_bp', __name__)


@views_bp.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@views_bp.route('/water_forecast_profile', methods=['GET'])
def water_forecast_profile():
    return render_template("waterForecastProfile.html")


@views_bp.route('/simulate_water_forecast', methods=['POST'])
def simulate_water_forecast():
    forecast_model = str(request.form["forecastModel"])
    forecast_timeframe = float(request.form["forecastTimeframe"])
    forecast_container_obj = ForecastModelContainer(
        forecast_model_name=forecast_model,
        forecast_timeframe=forecast_timeframe)
    model_obj_dict_string = json.dumps(forecast_container_obj.run())

    ForecastObj.drop_collection()
    forecast_database_obj = ForecastObj(model_obj_dict_string=model_obj_dict_string)
    forecast_database_obj.save()

    response_data = model_obj_dict_string
    response_status = 200
    return Response(response_data, response_status)


@views_bp.route('/water_forecast_obj_dict', methods=['GET'])
def water_forecast_obj_dict():
    if ForecastObj.objects:
        forecast_database_obj = ForecastObj.objects.first()
        model_obj_dict_string = forecast_database_obj.model_obj_dict_string

        response_data = model_obj_dict_string
        response_status = 200
        return Response(response_data, response_status)
    else:
        response_data = json.dumps([])
        response_status = 200
        return Response(response_data, response_status)
