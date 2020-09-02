from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import DeliveryCharge, WeightDeliveryCharge
from app.exceptions import ValidationError

@api.route('/deliverycharge/',methods=['GET'])
def get_delivery_charges():
  address_lists = DeliveryCharge.query.all()
  weight_lists = WeightDeliveryCharge.query.all()
  charges = dict()
  charges['address_charges'] = [element.to_json() for element in address_lists]
  charges['weight_charges'] = [element.to_json() for element in weight_lists]
  return jsonify({ 'charges': charges })
  

@api.route('/deliverycharge/<int:id>')
def get_delivery_charge(id):
  element = DeliveryCharge.query.filter_by(address_pin=id).first()
  return jsonify({ 'charge': "None" if element is None else element.to_json() })

@api.route('/weightdeliverycharge/<int:id>')
def get_weight_delivery_charge(id):
  element = WeightDeliveryCharge.query.filter_by(id= id).first()
  return jsonify({ 'charge': "None" if element is None else element.to_json() })

@api.route('/deliverychargefrompin/<int:pin>')
def get_delivery_charge_for_address(pin):
  element = DeliveryCharge.query.filter_by(address_pin=str(pin)).first()

  if element is None:
    element = DeliveryCharge.query.filter_by(address_pin="others").first()

  return jsonify({ 'charge': "None" if element is None else element.to_json() })


@api.route('/deliverychargeforweight/<int:weight>')
def get_delivery_charge_for_weight(weight):
  weight = int(weight)
  element = WeightDeliveryCharge.get_delivery_charge(weight)

  if element is None:
    element = WeightDeliveryCharge.get_default_charge()

  return jsonify({ 'charge': "None" if element is None else element.to_json() })