from flask import jsonify, request, url_for
from . import api 
from .. import db
from ..models import PaymentMethod, PaymentStatus
from app.exceptions import ValidationError

@api.route('/paymentdetails/',methods=['GET'])
def get_paymentdetails():
  details = dict()
  

  payment_methods = PaymentMethod.query.all()
  payment_status = PaymentStatus.query.all()

  details["payment_methods"] = [element.to_json() for element in payment_methods]
  details["payment_status"] = [element.to_json() for element in payment_status]
  return jsonify({ 'payment_details': details })

