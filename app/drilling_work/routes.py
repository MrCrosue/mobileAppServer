import app
from flask.wrappers import Response
from app import db
from app.drilling_work import drilling_work_bp
from flask import request
from app.models import Drilling_work, Well, Type_drilling, Type_layer, Layer, Sample
from flask import jsonify
from app.errors import bad_request
import json




@drilling_work_bp.route('/scopes/<int:id>/drilling_works/', methods = ['GET'])
def get_drilling_works(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data =  Drilling_work.to_collection_dict(Drilling_work.query.filter_by(fk_scope = id), page, per_page, 'drilling_work_bp.get_drilling_works', id = id)
    return jsonify(data)

@drilling_work_bp.route('/types_drilling/', methods = ['GET'])
def get_type_drilling():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data =  Type_drilling.to_collection_dict(Type_drilling.query, page, per_page, 'drilling_work_bp.get_type_drilling')
    return jsonify(data)

@drilling_work_bp.route('/drilling_works/', methods = ['POST'])
def create_drilling_work():
    data = request.get_json() or {}
    if 'fk_scope' not in data or 'fk_drilling_type' not in data:
        return bad_request('Поля fk_scope и fk_drilling_type обязательно должны присутствовать')
    drilling_work = Drilling_work()
    drilling_work.from_dict(data)
    db.session.add(drilling_work)
    db.session.commit()
    response = jsonify(drilling_work.to_dict())
    response.status_code = 201
    return response

@drilling_work_bp.route('/drilling_works/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_drilling_work(id):
    if request.method == 'GET':    
        return jsonify(Drilling_work.query.get_or_404(id).to_dict())
    elif request.method == 'DELETE':
        drilling_work = Drilling_work.query.get_or_404(id)
        db.session.delete(drilling_work)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        drilling_work = Drilling_work.query.get_or_404(id)
        data = request.get_json() or {}
        drilling_work.from_dict(data)
        db.session.commit()
        response = jsonify(drilling_work.to_dict())
        return response

@drilling_work_bp.route('/drilling_works/<int:id>/wells/', methods = ['GET'])
def get_wells(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Well.to_collection_dict(Well.query.filter_by(fk_drilling_work = id), page, per_page, 'drilling_work_bp.get_wells', id = id)
    return Response(response=json.dumps(data, ensure_ascii=False, default=str), status = 200, mimetype='application/json') 

@drilling_work_bp.route('/wells/', methods = ['POST'])
def create_well():
    data = request.get_json() or {}
    if 'name' not in data or 'number' not in data or 'diameter' not in data or 'depth' not in data or 'x' not in data or 'y' not in data or 'fk_drilling_work' not in data:
        return bad_request('Поля name, number, diameter, depth, x, y, fk_drilling_work обязательно должны присутствовать')
    well = Well()
    well.from_dict(data)
    db.session.add(well)
    db.session.commit()
    response = Response(
        response = json.dumps(well.to_dict(), ensure_ascii=False, default=str),
        status = 201, 
        mimetype='application/json'
    )  
    return response

@drilling_work_bp.route('/wells/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_well(id):
        if request.method == 'GET':    
            return Response(response = json.dumps(Well.query.get_or_404(id).to_dict(), ensure_ascii=False, default=str), status=200, mimetype='application/json')    
        elif request.method == 'DELETE':
            well = Well.query.get_or_404(id)
            db.session.delete(well)
            db.session.commit()
            return '', 204
        elif request.method == 'PUT':
            well = Well.query.get_or_404(id)
            data = request.get_json() or {}
            well.from_dict(data)
            db.session.commit()
            response = Response(
                response = json.dumps(well.to_dict(), ensure_ascii=False, default=str),
                status = 201, 
                mimetype='application/json'
                )
            return response

@drilling_work_bp.route('/types_layer/', methods = ['GET'])
def get_types_layer():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data =  Type_layer.to_collection_dict(Type_layer.query, page, per_page, 'drilling_work_bp.get_types_layer')
    return jsonify(data)

@drilling_work_bp.route('/wells/<int:id>/layers/', methods = ['GET'])
def get_layers(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data =  Layer.to_collection_dict(Layer.query.filter_by(fk_well = id), page, per_page, 'drilling_work_bp.get_layers', id = id)
    return jsonify(data)

@drilling_work_bp.route('/layers/', methods = ['POST'])
def create_layer():
    data = request.get_json() or {}
    if 'fk_well' not in data or 'start_depth' not in data or 'end_depth' not in data or 'fk_type_layer' not in data :
        return bad_request('Поля fk_well, start_depth, end_depth, fk_type_layer  обязательно должны присутствовать')
    layer = Layer()
    layer.from_dict(data)
    db.session.add(layer)
    db.session.commit()
    response = jsonify(layer.to_dict())
    response.status_code = 201
    return response

@drilling_work_bp.route('/layers/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_layer(id):
    if request.method == 'GET':    
            return jsonify(Layer.query.get_or_404(id).to_dict())
    elif request.method == 'DELETE':
        layer = Layer.query.get_or_404(id)
        db.session.delete(layer)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        layer = Layer.query.get_or_404(id)
        data = request.get_json() or {}
        layer.from_dict(data)
        db.session.commit()
        response = jsonify(layer.to_dict())
        return response

@drilling_work_bp.route('/wells/<int:id>/samples/', methods = ['GET'])
def get_samples(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data =  Sample.to_collection_dict(Sample.query.filter_by(fk_well = id), page, per_page, 'drilling_work_bp.get_samples', id = id)
    return jsonify(data)

@drilling_work_bp.route('/samples/', methods = ['POST'])
def create_sample():
    data = request.get_json() or {}
    if 'fk_well' not in data or 'fk_type_layer' not in data:
        return bad_request('Поля fk_well, fk_type_layer обязательно должны присутствовать')
    sample = Sample()
    sample.from_dict(data)
    db.session.add(sample)
    db.session.commit()   
    response = jsonify(sample.to_dict())
    response.status_code = 201
    return response

@drilling_work_bp.route('/samples/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def get_sample(id):
    if request.method == 'GET':    
            return jsonify(Sample.query.get_or_404(id).to_dict())
    elif request.method == 'DELETE':
        sample = Sample.query.get_or_404(id)
        db.session.delete(sample)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        sample = Sample.query.get_or_404(id)
        data = request.get_json() or {}
        sample.from_dict(data)
        db.session.commit()
        response = jsonify(sample.to_dict())
        return response