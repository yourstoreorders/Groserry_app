from flask import jsonify, request, url_for
from . import api 
from .. import db
from ..models import ShopDetails


@api.route('/shopdetails/',methods=['GET'])
def get_shopdetails():
  lists = ShopDetails.query.all()
  return jsonify({ 'units': [element.to_json() for element in lists] })


@api.route('/shopdetails/<int:id>')
def get_shopdetail(id):
  element = ShopDetails.query.filter_by(id=id).first()
  return jsonify({ 'unit': element.to_json() })

