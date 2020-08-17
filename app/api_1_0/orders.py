from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import OrderStatus, PlacedOrder , OrderedItem ,StatusCatalog, Product,ShopDetails
from ..email import send_email
from app.exceptions import ValidationError

@api.route('/order/', methods=['POST'])
# @auth.login_required
def new_order():

    newOrderStatus = OrderStatus.from_data(StatusCatalog.new_id().id)
    db.session.add(newOrderStatus)
    
    error = {}
    error["error"] = ""

    try:
      newPlacedOrder = PlacedOrder.from_json(request.json.get("order_details"),newOrderStatus)
    except ValidationError as e1:
      error["error"] = str(e1)
      return jsonify(error)
    except exc.SQLAlchemyError as e2:
      error["error"] = str(e2)
      return jsonify(error)
      
    
    db.session.add(newPlacedOrder)
    db.session.commit()

    for item in request.json.get("order_items"):
      newOrderItem = OrderedItem.from_json(item,newPlacedOrder.id)
      db.session.add(newOrderItem)

    db.session.commit()

    data = {}
    data['order_details'] = newPlacedOrder.to_json()
    data['ordered_items'] = order_items(newPlacedOrder.id)
    data['total_amount'] = float(newPlacedOrder.delivery_charge) + float(data['ordered_items']["sub_total"])

    shop = ShopDetails.query.all()[0]
    send_email(shop.shop_email,'New Order Received','email_template',data)

    return jsonify(data)
  

def validate_order_request(json_data):
  pass

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

  responseObj['sub_total'] = total_amount
  
  return responseObj