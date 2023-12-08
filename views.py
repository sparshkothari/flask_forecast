from flask import Blueprint, render_template, request
from werkzeug.wrappers.response import Response
import json
from models import ModelRequestObj, DataObj
from forecast.models.container import Container

views_bp = Blueprint('views_bp', __name__)


@views_bp.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@views_bp.route('/profile', methods=['GET'])
def profile():
    return render_template("profile.html")


@views_bp.route('/simulate', methods=['POST'])
def simulate():
    base_model = str(request.form["baseModel"])
    timeframe_multiplier = float(request.form["timeframeMultiplier"])
    timeframe_increment_multiplier = float(request.form["timeframeIncrementMultiplier"])
    timeframe_unit = int(request.form["timeframeUnit"])
    q = ModelRequestObj(base_model=base_model,
                        timeframe_multiplier=timeframe_multiplier,
                        timeframe_increment_multiplier=timeframe_increment_multiplier,
                        timeframe_unit=timeframe_unit)

    container_obj = Container(q)
    o = json.dumps(container_obj.run())

    DataObj.drop_collection()
    database_obj = DataObj(data_string=o)
    database_obj.save()

    response_data = o
    response_status = 200
    return Response(response_data, response_status)


@views_bp.route('/data', methods=['GET'])
def data():
    if DataObj.objects:
        o = DataObj.objects.first().data_string
        response_data = o
        response_status = 200
        return Response(response_data, response_status)
    else:
        response_data = json.dumps([])
        response_status = 200
        return Response(response_data, response_status)
