from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import DeliveryCharge
from app.exceptions import ValidationError

@api.route('/deliverycharge/',methods=['GET'])
def get_delivery_charges():
  lists = DeliveryCharge.query.all()
  return jsonify({ 'charges': [element.to_json() for element in lists] })


@api.route('/deliverycharge/<int:id>')
def get_delivery_charge(id):
  element = DeliveryCharge.query.filter_by(address_pin=id).first()
  return jsonify({ 'charge': "None" if element is None else element.to_json() })

@api.route('/deliverychargefrompin/<int:pin>')
def get_delivery_charge_for_address(pin):
  element = DeliveryCharge.query.filter_by(address_pin=str(pin)).first()

  if element is None:
    element = DeliveryCharge.query.filter_by(address_pin="others").first()
  

  return jsonify({ 'charge': "None" if element is None else element.to_json() })