from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import Unit


@api.route('/unit/',methods=['GET'])
def get_units():
  lists = Unit.query.all()
  return jsonify({ 'units': [element.to_json() for element in lists] })


@api.route('/unit/<int:id>')
def get_unit(id):
  element = Unit.query.filter_by(id=id).first()
  return jsonify({ 'unit': element.to_json() })


@api.route('/unit/', methods=['POST'])
@auth.login_required
def new_unit():
    element = Unit.from_json(request.json)
    db.session.add(element)
    db.session.commit()
    return jsonify(element.to_json()), 201, \
        {'Location': url_for('api.get_unit', id=element.id)}


@api.route('/unit/<int:id>', methods=['PUT'])
@auth.login_required
def edit_unit(id):
    element = Unit.query.get_or_404(id)

    element.unit_name = request.json.get('unit_name', element.unit_name)
    element.unit_short = request.json.get('unit_short', element.unit_short)
    db.session.add(element)
    db.session.commit()
    return jsonify(element.to_json())

@api.route('/unit/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_unit(id):
    element = Unit.query.get_or_404(id)
    db.session.delete(element)
    db.session.commit()
    return jsonify(element.to_json())