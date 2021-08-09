from app import db
from app.general import general_bp
from flask import request
from app.models import Group, Object, Scope
from flask import jsonify
from app.errors import bad_request


@general_bp.route('/groups/', methods = ['GET'])
def get_groups():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Group.to_collection_dict(Group.query, page, per_page, 'general_bp.get_groups')
    return jsonify(data)

@general_bp.route('/groups_name/<string:login>/', methods = ['GET'])
def get_group_by_name(login):
    return jsonify(Group.query.filter_by(login = login).first_or_404().to_dict()) 

@general_bp.route('/groups/<int:id>/', methods = ['GET', 'DELETE', 'PUT'])
def get_group(id):
    if request.method == 'GET':    
        return jsonify(Group.query.get_or_404(id).to_dict())
    elif request.method == 'DELETE':
        group = Group.query.get_or_404(id)
        db.session.delete(group)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        group = Group.query.get_or_404(id)
        data = request.get_json() or {}
        if 'login' not in data:
            return bad_request('Поле login обязательно должно присутствовать')
        group.from_dict(data)
        db.session.commit()
        response = jsonify(group.to_dict())
        return response
    
@general_bp.route('/objects/', methods = ['GET'])
def get_objects():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Object.to_collection_dict(Object.query, page, per_page, 'general_bp.get_objects')
    return jsonify(data)

@general_bp.route('/objects/<int:id>/', methods = ['GET', 'DELETE', 'PUT'])
def get_object(id):
    if request.method == 'GET':
        return jsonify(Object.query.get_or_404(id).to_dict())
    elif request.method == 'DELETE':
        _object = Object.query.get_or_404(id)
        db.session.delete(_object)
        db.session.commit()
        return '', 204
    elif request.method == 'PUT':
        object_ = Object.query.get_or_404(id)
        data = request.get_json() or {}
        if 'name' not in data or 'cipher' not in data:
            return bad_request('Поле name и cipher обязательно должны присутствовать')
        object_.from_dict(data)
        db.session.commit()
        response = jsonify(object_.to_dict())
        return response

@general_bp.route('/groups/<int:id>/scopes/', methods = ['GET'])
def get_scopes(id):
    admin = request.args.get('admin', 0, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    if admin == 1:
        data = Scope.to_collection_dict(Scope.query.filter_by(fk_group = id), page, per_page, 'general_bp.get_scopes', id = id)
    else:
        data = Scope.to_collection_dict(Scope.query.filter_by(fk_group = id).filter_by(status = 0), page, per_page, 'general_bp.get_scopes', id = id)
    return jsonify(data)
    
@general_bp.route('/groups/', methods = ['POST'])
def create_group():
    data = request.get_json() or {}
    if 'login' not in data:
        return bad_request('Поле login обязательно должно присутствовать')
    if Group.query.filter_by(login = data['login']).first():
        return bad_request('Login бригады должен быть уникальным')
    group = Group()
    group.from_dict(data)
    db.session.add(group)
    db.session.commit()
    response = jsonify(group.to_dict())
    response.status_code = 201
    return response

@general_bp.route('/objects/', methods = ['POST'])
def create_object():
    data = request.get_json() or {}
    if 'name' not in data or 'cipher' not in data:
        return bad_request('Поле name и cipher обязательно должны присутствовать')
    if Object.query.filter_by(cipher = data['cipher']).first():
        return bad_request('Шифр объекта должнен быть уникальным')
    object_ = Object()
    object_.from_dict(data)
    db.session.add(object_)
    db.session.commit()
    response = jsonify(object_.to_dict())
    response.status_code = 201
    return response

@general_bp.route('/scoups/', methods = ['POST'])
def create_scoup():
    data = request.get_json() or {}
    if 'fk_group' not in data or 'fk_object' not in data:
        return bad_request('Поля fk_group и fk_object обязательны')
    scope = Scope()
    scope.from_dict(data)
    db.session.add(scope)
    db.session.commit()
    response = jsonify(scope.to_dict())
    response.status_code = 201
    return response


@general_bp.route('/scoups/<int:id>/', methods = ['PUT', 'DELETE', 'GET'])
def update_scoup(id):
    scope = Scope.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.get_json() or {}
        if 'fk_group' not in data or 'fk_object' not in data:
            return bad_request('Поля fk_group и fk_object обязательны')  
        scope.from_dict(data)
        db.session.commit()
        response = jsonify(scope.to_dict())
        return response
    elif request.method == 'DELETE':
        scope = Scope.query.get_or_404(id)
        db.session.delete(scope)
        db.session.commit()
        return '', 204
    else:
        return jsonify(Scope.query.get_or_404(id).to_dict())
