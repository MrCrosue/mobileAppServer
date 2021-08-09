from app import db
from flask import url_for
from datetime import datetime, date

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Group(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index=True, unique=True)
    fio = db.Column(db.String(64))
    caption = db.Column(db.Text)
    scopes = db.relationship('Scope', backref='group', lazy='dynamic')
    track_geos = db.relationship('Track_geo', lazy = 'dynamic')

    def __repr__(self):
        return '<Group {}>'.format(self.name)
        
    def to_dict(self):
        data = {'id': self.id,
         'login': self.login,
         'fio': self.fio,
         'caption': self.caption,
         '_object_links':{'self': url_for('general_bp.get_group', id=self.id),
            'next':url_for('general_bp.get_scopes', id = self.id)
            }
         }
        return data

    def from_dict(self, data):
        for field in ['login', 'fio', 'caption']:
            if field in data:
                setattr(self, field, data[field])

class Track_geo(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False)
    geo_latitude = db.Column(db.DECIMAL(12,8), nullable=False)
    geo_longitude = db.Column(db.DECIMAL(12,8), nullable=False)
    fk_group_id =  db.Column(db.Integer, db.ForeignKey('group.id'))

    def to_dict(self):
        data = {
            'id':self.id,
            'date':self.date,
            'geo_latitude':self.geo_latitude,
            'geo_longitude':self.geo_longitude,
        }
        return data
    
    def from_dict(self, data):
        for field in ['date', 'geo_latitude', 'geo_longitude', 'fk_group_id']:
            if field in data:
                setattr(self, field, data[field])

class Object(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    cipher = db.Column(db.String(64), index=True, unique=True)
    scopes = db.relationship('Scope', backref='project', lazy='dynamic')
    
    def __repr__(self):
        return '<Object {}>'.format(self.name) 

    def to_dict(self):
        data = {'id': self.id,
         'name': self.name,
         'cipher': self.cipher,      
         }
        return data


    def from_dict(self, data):
        for field in ['name', 'cipher']:
            if field in data:
                setattr(self, field, data[field])

class Object_geo(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False)
    geo_latitude = db.Column(db.DECIMAL(12,8), nullable=False)
    geo_longitude = db.Column(db.DECIMAL(12,8), nullable=False)
    fk_scope_id =  db.Column(db.Integer, db.ForeignKey('scope.id'))

    def to_dict(self):
        data = {
            'id':self.id,
            'date':self.date,
            'geo_latitude':self.geo_latitude,
            'geo_longitude':self.geo_longitude,
        }
        return data
    
    def from_dict(self, data):
        for field in ['date', 'geo_latitude', 'geo_longitude', 'fk_scope_id']:
            if field in data:
                setattr(self, field, data[field])

class Scope(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fk_group = db.Column(db.Integer, db.ForeignKey('group.id'))
    fk_object = db.Column(db.Integer, db.ForeignKey('object.id'))
    full_work = db.Column(db.Text)
    status = db.Column(db.Integer)
    drilling_works = db.relationship('Drilling_work', lazy = 'dynamic')
    object_geos = db.relationship('Object_geo', lazy = 'dynamic')

    def to_dict(self):
        data = {
            'id':self.id,
            'project':self.project.name,
            'cipher':self.project.cipher,
            'full_work':self.full_work,
            'fk_object':self.fk_object,
            'fk_group':self.fk_group,
            'status':self.status,
            '_object_links_for_drilling':{
                'self': url_for('general_bp.update_scoup', id=self.id),
                'drilling_link': url_for('drilling_work_bp.get_drilling_works', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['fk_group', 'fk_object', 'full_work', 'status']:
            if field in data:
                setattr(self, field, data[field])


class Type_drilling(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    drilling_works = db.relationship('Drilling_work', lazy = 'dynamic')

    def to_dict(self):
        data = {
            'id':self.id,
            'name':self.name
        }
        return data


class Drilling_work(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fk_scope = db.Column(db.Integer, db.ForeignKey('scope.id'))
    fk_drilling_type = db.Column(db.Integer, db.ForeignKey('type_drilling.id'))
    methodology = db.Column(db.Text)
    wells = db.relationship('Well', lazy = 'dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'fk_scope': self.fk_scope,
            'fk_drilling_type': Type_drilling.query.filter_by(id = self.fk_drilling_type).first().name,
            'methodology': self.methodology,
            '_object_links':{
                'self': url_for('drilling_work_bp.get_drilling_work', id = self.id),
                'next': url_for('drilling_work_bp.get_wells', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['fk_scope', 'fk_drilling_type', 'methodology']:
            if field in data:
                setattr(self, field, data[field])    

class Well(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    number = db.Column(db.Integer)
    diameter = db.Column(db.Float)
    depth = db.Column(db.Float)
    start_work = db.Column(db.DateTime)
    end_work = db.Column(db.DateTime)
    x = db.Column(db.DECIMAL(12,4))
    y = db.Column(db.DECIMAL(12,4))
    lat = db.Column(db.String(128))
    lon = db.Column(db.String(128))
    start_water = db.Column(db.Float)
    end_water = db.Column(db.Float)
    fk_drilling_work = db.Column(db.Integer, db.ForeignKey('drilling_work.id'))
    layers = db.relationship('Layer', lazy = 'dynamic')
    samples = db.relationship('Sample', lazy = 'dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'diameter': self.diameter,
            'depth': self.depth,
            'start_work': self.start_work,
            'end_work': self.end_work,
            'x': self.x,
            'y': self.y,
            'lat':self.lat,
            'lon':self.lon,
            'start_water': self.start_water,
            'end_water': self.end_water,
            'fk_drilling_work':self.fk_drilling_work,
            '_object_links': {
                'self': url_for('drilling_work_bp.get_well', id=self.id), 
                'next': url_for('drilling_work_bp.get_layers', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'number', 'diameter', 'depth', 'start_work', 'end_work', 'x', 'y','lat', 'lon', 'start_water', 'end_water', 'fk_drilling_work']:
            if field in data:
                setattr(self, field, data[field])    

class Type_layer(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name
        }
        return data

class Layer(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_depth = db.Column(db.Float)
    end_depth = db.Column(db.Float)
    fk_type_layer = db.Column(db.String(256))
    fk_well = db.Column(db.Integer, db.ForeignKey('well.id'))

    def to_dict(self):
        data = {
            'id': self.id,
            'start_depth': self.start_depth,
            'end_depth': self.end_depth,
            'fk_type_layer': self.fk_type_layer,
            'fk_well': self.fk_well,
            '_object_links':{
                'self': url_for('drilling_work_bp.get_layer', id=self.id),
                'next': ""
            }
        }
        return data

    def from_dict(self, data):
         for field in ['start_depth', 'end_depth', 'fk_type_layer', 'fk_well']:
            if field in data:
                setattr(self, field, data[field])  



class Sample(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    depth = db.Column(db.Float)
    monolit = db.Column(db.Boolean)
    sample = db.Column(db.Boolean)
    korozia = db.Column(db.Boolean)
    give_water = db.Column(db.Boolean)
    fk_type_layer = db.Column(db.String(256))
    fk_well = db.Column(db.Integer, db.ForeignKey('well.id'))

    def to_dict(self):
        data = {
            'id':self.id,
            'depth':self.depth,
            'monolit':self.monolit,
            'sample':self.sample,
            'korozia':self.korozia,
            'give_water':self.give_water,
            'fk_type_layer':self.fk_type_layer,
            'fk_well':self.fk_well,
            '_object_links':{
                'self': url_for('drilling_work_bp.get_sample', id=self.id),
                'next': ""
            }
        }
        return data

    def from_dict(self, data):
        for field in ['depth', 'monolit', 'sample', 'korozia', 'give_water', 'fk_type_layer', 'fk_well']:
            if field in data:
                setattr(self, field, data[field])