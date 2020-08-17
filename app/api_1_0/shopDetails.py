from flask import jsonify, request, url_for
from . import api 
from .. import db
from ..models import ShopDetails
from app.exceptions import ValidationError

@api.route('/shopdetails/',methods=['GET'])
def get_shopdetails():
  lists = ShopDetails.query.all()
  return jsonify({ 'details': [element.to_json() for element in lists] })


@api.route('/shopdetails/<int:id>')
def get_shopdetail(id):
  element = ShopDetails.query.filter_by(id=id).first()
  return jsonify({ 'detail': element.to_json() })

