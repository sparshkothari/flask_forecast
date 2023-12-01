from flask import Blueprint, render_template, session, request
from werkzeug.wrappers.response import Response
import json
from models import WaterForecastObj
from water_forecast.water_forecast import WaterForecast

views_water_forecast_bp = Blueprint('views_water_forecast_bp', __name__)


@views_water_forecast_bp.route('/water_forecast', methods=['GET'])
def water_forecast():
    return render_template("waterForecast/waterForecast.html")


@views_water_forecast_bp.route('/simulate_water_forecast', methods=['POST'])
def simulate_water_forecast():
    water_forecast_model = int(request.form["waterForecastModel"])
    water_forecast_obj = WaterForecast(water_forecast_model=water_forecast_model)

    water_forecast_obj_dict_string = json.dumps(water_forecast_obj.run())
    water_forecast_database_obj = WaterForecastObj(water_forecast_obj_dict_string=water_forecast_obj_dict_string)
    water_forecast_database_obj.save()
    return Response("Success", 200)


@views_water_forecast_bp.route('/water_forecast_obj_dict', methods=['GET'])
def water_forecast_obj_dict():
    if WaterForecastObj.objects:
        water_forecast_database_obj = WaterForecastObj.objects.first()
        water_forecast_obj_dict_string = water_forecast_database_obj.water_forecast_obj_dict_string
        WaterForecastObj.drop_collection()
        return Response(water_forecast_obj_dict_string, 200)
    else:
        error_string = "Error: No object"
        session["error_response"] = error_string
        return Response(error_string, 400)
