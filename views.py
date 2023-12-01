from flask import Blueprint, render_template, session, request
from werkzeug.wrappers.response import Response
import json
from models import WaterForecastObj
from water_forecast.water_forecast import WaterForecast

views_bp = Blueprint('views_bp', __name__)


@views_bp.route('/', methods=['GET'])
def index():
    return render_template("home/index.html")


@views_bp.route('/water_forecast_profile', methods=['GET'])
def water_forecast_profile():
    return render_template("waterForecast/waterForecastProfile.html")


@views_bp.route('/simulate_water_forecast', methods=['POST'])
def simulate_water_forecast():
    water_forecast_model = int(request.form["waterForecastModel"])
    water_forecast_timeframe = float(request.form["waterForecastTimeframe"])
    water_forecast_obj = WaterForecast(
        water_forecast_model=water_forecast_model,
        water_forecast_timeframe=water_forecast_timeframe)
    water_forecast_obj_dict_string = json.dumps(water_forecast_obj.run())

    WaterForecastObj.drop_collection()
    water_forecast_database_obj = WaterForecastObj(water_forecast_obj_dict_string=water_forecast_obj_dict_string)
    water_forecast_database_obj.save()

    response_data = water_forecast_obj_dict_string
    response_status = 200
    return Response(response_data, response_status)


@views_bp.route('/water_forecast_obj_dict', methods=['GET'])
def water_forecast_obj_dict():
    if WaterForecastObj.objects:
        water_forecast_database_obj = WaterForecastObj.objects.first()
        water_forecast_obj_dict_string = water_forecast_database_obj.water_forecast_obj_dict_string

        response_data = water_forecast_obj_dict_string
        response_status = 200
        return Response(response_data, response_status)
    else:
        response_data = json.dumps([])
        response_status = 200
        return Response(response_data, response_status)
