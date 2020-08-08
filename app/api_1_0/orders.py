from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import OrderStatus, PlacedOrder , OrderedItem ,StatusCatalog, Product
from ..email import send_email


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

    data = {}
    data['order_details'] = newPlacedOrder.to_json()
    data['ordered_items'] = order_items(newPlacedOrder.id)
    #params:(subject_text, )
    send_email('New Order Received','email_template',data)

    return jsonify(newPlacedOrder.to_json())
  

def order_items(order_id):


  items = db.session.query(OrderedItem.quantity,OrderedItem.price,Product.id, Product.product_name,Product.price_per_unit).join(Product,OrderedItem.product_id == Product.id ).\
    filter(OrderedItem.placed_order_id == order_id).all()

  responseObj = {}

  itemList = []
  total_amount = 0.0

  for item in items:
    itemObj = {}
    itemObj['product_id'] = item.id
    itemObj['product_name'] = item.product_name
    itemObj['quantity'] = item.quantity
    price = float(item.quantity) * float(item.price_per_unit)
    total_amount += price
    itemObj['price']  = str(price)

    itemList.append(itemObj)
  
  responseObj['items'] = itemList

  responseObj['total_amount'] = total_amount
  
  return responseObj