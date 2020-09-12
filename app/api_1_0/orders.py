from flask import jsonify, request, url_for
from . import api 
from . authentication import auth
from .. import db
from ..models import OrderStatus, PlacedOrder , OrderedItem ,\
  StatusCatalog, Product,ShopDetails, DeliveryCharge, WeightDeliveryCharge,\
  PaymentMethod,PaymentStatus
from ..email import send_email
from app.exceptions import ValidationError
from sqlalchemy import exc

@api.route('/confirmorder/', methods=['POST'])
# @auth.login_required
def confirm_order():
  post_json = request.json.get("order_details")
  
  error = {}
  error["error"] = ""

  order_id = post_json.get('order_id')
  
  if(order_id is None or order_id == ''):
    error["error"] ="order is Null"
    return jsonify(error)
  
  order  = PlacedOrder.query.filter_by(id = int(order_id)).first()
   
  if(order is None):
    error["error"] = "order id doesn't exit"
    return jsonify(error)
  elif(order.payment_status == PaymentStatus.get_done().id):
    error["error"] = "already paid!"
    return jsonify(error)

  amount_paid = post_json.get('amount_paid')

  if (float(order.total_amount) != float(amount_paid)):
    error["error"] = "amount missmatch!"
    return jsonify(error)


  payment_method = post_json.get('payment_method')

  paym = PaymentMethod.query.filter_by(id = int(payment_method)).first()

  if(paym is None or paym == PaymentMethod.default_id()):
    error["error"] = "payment mehtod doesn't  exits!"
    return jsonify(error)

  payment_status = post_json.get('payment_status')

  pays = PaymentStatus.query.filter_by(id = int(payment_status)).first()

  if(pays is None):
    error["error"] = "payment status doesn't  exits!"
    return jsonify(error)

  payment_transaction_id = post_json.get("transaction_id")
  
  if ( payment_transaction_id is None or payment_transaction_id == ''):
    error["error"] = "Empty transaction id!"
    return jsonify(error)
  
  if(check_transaction(order_id,payment_transaction_id) != True):
    error["error"] = "invalid transaction id!"
    return jsonify(error)

  order.payment_status = int(payment_status)
  order.payment_method = int(payment_method)

  db.session.add(order)
  try:
    db.session.commit() 
  except exc.SQLAlchemyError as e2:
    error["error"] = "couldnot confirm"
    return jsonify(error)
  
  return jsonify({'success':'order placed'})



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
      db.session.close()
      return jsonify(error)
    except exc.SQLAlchemyError as e2:
      error["error"] = str(e2)
      return jsonify(error)
      db.session.close()
      
    
    db.session.add(newPlacedOrder)
    

    for item in request.json.get("order_items"):
      
      try:
        newOrderItem = OrderedItem.from_json(item,newPlacedOrder)
      except ValidationError as e1:
        error["error"] = str(e1)
        db.session.close()
        return jsonify(error)
      except exc.SQLAlchemyError as e2:
        error["error"] = str(e2)
        return jsonify(error)
        db.session.close()
      
      db.session.add(newOrderItem)

    db.session.commit()

    data = {}
    
    data['ordered_items'] = order_items(newPlacedOrder.id)

    total_wt = float(data['ordered_items']['total_weight'])

    element = WeightDeliveryCharge.get_delivery_charge(total_wt)
    if element is None:
      weight_delivery_charge = 0
    else:
      weight_delivery_charge = float(element.amount)
    
    data['delivery_charges'] = {
      "address_charge":str(float(newPlacedOrder.delivery_charge)),
      "weight_charge": str(weight_delivery_charge)
      }
    

    data['total_amount'] = str(float(newPlacedOrder.delivery_charge) +\
       float(data['ordered_items']["sub_total"]) + weight_delivery_charge)

    data['order_details'] = newPlacedOrder.to_json()
    
    newPlacedOrder.delivery_charge = float(newPlacedOrder.delivery_charge) + weight_delivery_charge
    newPlacedOrder.total_amount = float(data['total_amount'])

    db.session.add(newPlacedOrder)
    db.session.commit()


    shop = ShopDetails.query.all()[0]
    send_email(shop.shop_email,'New Order Received','email_template',data)
    return jsonify(data)


def order_items(order_id):

  items = db.session.query(\
    OrderedItem.quantity,\
    OrderedItem.price,Product.id,\
    Product.product_name,Product.price_per_unit,Product.product_weight).join(Product,OrderedItem.product_id == Product.id ).\
    filter(OrderedItem.placed_order_id == order_id).all()

  responseObj = {}

  itemList = []
  total_amount = 0.0
  total_weight = 0.0

  for item in items:
    itemObj = {}
    itemObj['product_id'] = item.id
    itemObj['product_name'] = item.product_name
    itemObj['quantity'] = item.quantity
    itemObj['product_weight'] = float(item.product_weight)
    
    weight = float(item.product_weight)*int(item.quantity)
    total_weight += weight
    
    price = float(item.quantity) * float(item.price_per_unit)  
    total_amount += price

    itemObj['price']  = str(price)

    itemList.append(itemObj)
  
  responseObj['items'] = itemList

  responseObj['total_weight'] = total_weight
  responseObj['sub_total'] = total_amount
  
  return responseObj


# Check transaction
def check_transaction(order_id,transaction_id):
  return True