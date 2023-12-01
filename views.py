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
    forecast_base_model = str(request.form["forecastBaseModel"])
    forecast_environment = int(request.form["forecastEnvironment"])
    forecast_timeframe = float(request.form["forecastTimeframe"])
    forecast_container_obj = ForecastModelContainer(
        forecast_base_model=forecast_base_model,
        forecast_environment=forecast_environment,
        forecast_timeframe=forecast_timeframe)
    model_obj_dict_string = json.dumps(forecast_container_obj.run())

    ForecastObj.drop_collection()
    forecast_database_obj = ForecastObj(model_obj_dict_string=model_obj_dict_string)
    forecast_database_obj.save()

    response_data = model_obj_dict_string
    response_status = 200
    return Response(response_data, response_status)


@views_bp.route('/forecast_obj_dict', methods=['GET'])
def forecast_obj_dict():
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
