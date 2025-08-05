from flask import Blueprint, render_template, request
from werkzeug.wrappers.response import Response
import json
from utils import UtilsJSONEncoder
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
    base_model = int(request.form["baseModel"])
    limit_bounds = bool(request.form["limitBounds"] == "1")
    q = ModelRequestObj(base_model=base_model,
                        index_start=0.0,
                        index_stop=0.0,
                        increment=0.0,
                        limit_bounds=limit_bounds)

    container_obj = Container(q)
    o = json.dumps(container_obj.run(), cls=UtilsJSONEncoder)

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
