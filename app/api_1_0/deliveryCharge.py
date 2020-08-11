from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import DeliveryCharge


@api.route('/deliverycharge/',methods=['GET'])
def get_delivery_charges():
  lists = DeliveryCharge.query.all()
  return jsonify({ 'charges': [element.to_json() for element in lists] })


@api.route('/deliverycharge/<int:pin>')
def get_delivery_charge(pin):
  element = DeliveryCharge.query.filter_by(address_pin=str(pin)).first()
  return jsonify({ 'charge': "None" if element is None else element.to_json() })

@api.route('/deliverychargefrompin/<int:pin>')
def get_delivery_charge_for_address(pin):
  element = DeliveryCharge.query.filter_by(address_pin=str(pin)).first()
  return jsonify({ 'charge': "None" if element is None else element.to_json() })