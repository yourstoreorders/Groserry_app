from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import OrderStatus, PlacedOrder , OrderedItem ,StatusCatalog


@api.route('/order/', methods=['POST'])
# @auth.login_required
def new_order():

    print("id" ,StatusCatalog.new_id().id )
    newOrderStatus = OrderStatus.from_data(StatusCatalog.new_id().id)
    db.session.add(newOrderStatus)
    db.session.commit()

    newPlacedOrder = PlacedOrder.from_json(request.json.get("order_details"),newOrderStatus.id)
    db.session.add(newPlacedOrder)
    db.session.commit()

    for item in request.json.get("order_items"):
      newOrderItem = OrderedItem.from_json(item,newPlacedOrder.id)
      db.session.add(newOrderItem)

    db.session.commit()
    return jsonify(newPlacedOrder.to_json())
  

