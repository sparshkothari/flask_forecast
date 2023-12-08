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
    index_start = int(request.form["indexStart"])
    index_stop = int(request.form["indexStop"])
    increment = int(request.form["increment"])
    q = ModelRequestObj(base_model=base_model,
                        index_start=index_start,
                        index_stop=index_stop,
                        increment=increment)

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
