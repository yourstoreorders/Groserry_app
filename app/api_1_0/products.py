
from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import Product


@api.route('/product/',methods=['GET'])
def get_products():
  lists = Product.query.all()
  return jsonify({ 'products': [element.to_json() for element in lists]})


@api.route('/product/<int:id>')
def get_product(id):
  element = Product.query.filter_by(id=id).first()
  return jsonify({ 'product': element.to_json() })


@api.route('/product/', methods=['POST'])
@auth.login_required
def new_product():
    element = Product.from_json(request.json)
    db.session.add(element)
    db.session.commit()
    return jsonify(element.to_json()), 201, \
        {'Location': url_for('api.get_product', id=element.id)}


@api.route('/product/<int:id>', methods=['PUT'])
@auth.login_required
def edit_product(id):
    element = Product.query.get_or_404(id)

    element.product_name = request.json.get('product_name', element.product_name)
    element.product_description = request.json.get('product_description', element.product_description)
    element.price_per_unit = request.json.get('price_per_unit', element.price_per_unit)
    element.unit_id = request.json.get('unit_id', element.unit_id)
    element.product_type_id = request.json.get('product_type_id', element.product_type_id)

   
    db.session.add(element)
    db.session.commit()
    return jsonify(element.to_json())

@api.route('/product/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_product(id):
    element = Product.query.get_or_404(id)
    db.session.delete(element)
    db.session.commit()
    return jsonify(element.to_json())