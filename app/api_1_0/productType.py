from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import ProductType


@api.route('/producttype/',methods=['GET'])
def get_categories():
  lists = ProductType.query.all()
  return jsonify({ 'categories': [element.to_json() for element in lists] })


@api.route('/producttype/<int:id>')
def get_category(id):
  element = ProductType.query.filter_by(id=id).first()
  return jsonify({ 'category': element.to_json() })


@api.route('/producttype/', methods=['POST'])
@auth.login_required
def new_category():
    element = ProductType.from_json(request.json)
    db.session.add(element)
    db.session.commit()
    return jsonify(element.to_json()), 201, \
        {'Location': url_for('api.get_category', id=element.id)}


@api.route('/producttype/<int:id>', methods=['PUT'])
@auth.login_required
def edit_category(id):
    element = ProductType.query.get_or_404(id)

    element.type_name = request.json.get('type_name', element.type_name)
    db.session.add(element)
    db.session.commit()
    return jsonify(element.to_json())

@api.route('/producttype/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_category(id):
    element = ProductType.query.get_or_404(id)
    db.session.delete(element)
    db.session.commit()
    return jsonify(element.to_json())