from app import db
from app.geo import geo_bp
from flask import request, url_for
from app.models import Track_geo, Object_geo
from flask import jsonify
from app.errors import bad_request
from datetime import datetime, timedelta
from flask.wrappers import Response
import json



@geo_bp.route('/groups/<int:id>/geos/', methods = ['GET'])
def get_group_geos(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    start_date = datetime.strptime(request.args.get('start_date'), "%Y-%m-%d%H:%M:%S").date()
    end_date = datetime.strptime(request.args.get('end_date'), "%Y-%m-%d%H:%M:%S").date()
    end_date = end_date + timedelta(1)
    data =  Track_geo.to_collection_dict(Track_geo.query.filter_by(fk_group_id = id).filter(Track_geo.date >= start_date).filter(Track_geo.date <= end_date), page, per_page, 'geo.get_group_geos', id = id, start_date = request.args.get('start_date'), end_date = request.args.get('end_date'))
    response = Response(
            response = json.dumps(data, ensure_ascii=False, default=str),
            status = 200, 
            mimetype='application/json'
            )
    return response


@geo_bp.route('/scopes/<int:id>/geos/', methods = ['GET'])
def get_object_geos(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    start_date = datetime.strptime(request.args.get('start_date'), "%Y-%m-%d%H:%M:%S").date()
    end_date = datetime.strptime(request.args.get('end_date'), "%Y-%m-%d%H:%M:%S").date()
    end_date = end_date + timedelta(1)
    data = Object_geo.to_collection_dict(Object_geo.query.filter_by(fk_scope_id = id).filter(Object_geo.date >= start_date).filter(Object_geo.date <= end_date), page, per_page, 'geo.get_object_geos', id = id, start_date = request.args.get('start_date'), end_date = request.args.get('end_date'))  
    response = Response(
            response = json.dumps(data, ensure_ascii=False, default=str),
            status = 200, 
            mimetype='application/json'
            )  
    return response

@geo_bp.route('/scopes/<int:id>/geos/', methods = ['POST'])
def create_scope_geos(id):
    data = request.get_json() or {}
    if 'fk_scope_id' not in data or 'geo_latitude' not in data or 'geo_longitude' not in data or 'date' not in data:
        return bad_request('Поля fk_scope_id, geo_latitude, geo_longitude, date обязательны')
    geo_scope = Object_geo()
    geo_scope.from_dict(data)
    db.session.add(geo_scope)
    db.session.commit()
    response = Response(
            response = json.dumps(geo_scope.to_dict(), ensure_ascii=False, default=str),
            status = 201, 
            mimetype='application/json'
            )
    return response

@geo_bp.route('/groups/<int:id>/geos/', methods = ['POST'])
def create_track_geos(id):
    data = request.get_json() or {}
    if 'fk_group_id' not in data or 'geo_latitude' not in data or 'geo_longitude' not in data or 'date' not in data:
        return bad_request('Поля fk_group_id, geo_latitude, geo_longitude, date обязательны')
    track = Track_geo()
    track.from_dict(data)
    db.session.add(track)
    db.session.commit()
    response = Response(
            response = json.dumps(track.to_dict(), ensure_ascii=False, default=str),
            status = 201, 
            mimetype='application/json'
            )
    return response
    