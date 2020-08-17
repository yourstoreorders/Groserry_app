import os
from flask import current_app, request, url_for
from datetime import datetime
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.exceptions import ValidationError

import pytz
from pytz import timezone

def convert_time(utc_time):
  # tz = timezone('Asia/Kolkata')
  tm = utc_time.astimezone(timezone('Asia/Kolkata'))
  return tm

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# product Models

class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  product_name =  db.Column(db.String(128), unique=True, nullable=False)
  product_description = db.Column(db.String(255), nullable=False)
  price_per_unit = db.Column(db.Numeric(10,2),nullable=False)
  product_image = db.Column(db.String(256),nullable=False)

  product_type_id = db.Column(db.Integer,db.ForeignKey('product_type.id'), nullable=False)
  unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
  

  stock_details = db.relationship('Stock', cascade="all,delete", backref='stock_details', lazy=True)
  ordered_items = db.relationship('OrderedItem',cascade="all,delete", backref='ordered_items', lazy=True)

  # def __repr__(self):
  #   return f"Product({self.product_name})"

  @property
  def get_product(self):
    return Product.query.join(Unit).all()
  
  def to_json(self):
       print(self.stock_details[0].in_stock)
       json_unit = {
           'url': url_for('api.get_product', id=self.id),
           'product_id':self.id,
           'product_name': self.product_name,
           'product_image': os.path.join(url_for('static',filename='product_images',_external=True)\
              , self.product_image),
           'product_description': self.product_description,
           'price_per_unit': str(self.price_per_unit),
           'unit': Unit.get_unit(self.unit_id).unit_name,
           'product_type': ProductType.get_productType(self.product_type_id).type_name,
           'in_stock' : self.stock_details[0].in_stock
       }
       return json_unit
  
  @staticmethod
  def from_dict(dict_post):
    name = dict_post['product_name']
    description = dict_post['product_description']
    price = dict_post['price_per_unit']
    unit_id = dict_post['unit_id']
    product_type_id = dict_post['product_type_id']
    product_image = dict_post['product_image']

    if (name is None or name == ''):
        raise ValidationError('doesnot have a name')

    if (price is None or price == ''):
        raise ValidationError('doesnot have a price')
    
    if (unit_id is None or unit_id == ''):
        raise ValidationError('doesnot have a unit id')
    
    if (product_type_id is None or product_type_id == ''):
        raise ValidationError('doesnot have a product type id')
    
    if (product_image is None or product_image == ''):
        raise ValidationError('doesnot have a image')
    
    product_type = ProductType.query.filter_by(id=int(product_type_id)).first()
    unit = Unit.query.filter_by(id=int(unit_id)).first()

    if(product_type is None or unit is None):
       raise ValidationError('invalid product type or unit')

    return Product(product_name=name,
                  product_description =  description,
                  price_per_unit = float(price),
                  unit_items = unit,
                  product_items = product_type,
                  product_image = product_image)

  @staticmethod
  def from_json(json_post):
    name = json_post.get('product_name')
    description = json_post.get('product_description')
    price = json_post.get('price_per_unit')
    unit_id = json_post.get('unit_id')
    product_type_id = json_post.get('product_type_id')

    if (name is None or name == ''):
        raise ValidationError('doesnot have a name')

    if (price is None or price == ''):
        raise ValidationError('doesnot have a price')
    
    if (unit_id is None or unit_id == ''):
        raise ValidationError('doesnot have a unit id')
    
    if (product_type_id is None or product_type_id == ''):
        raise ValidationError('doesnot have a product type id')
    
    product_type = ProductType.query.filter_by(id=int(product_type_id)).first()
    unit = Unit.query.filter_by(id=int(unit_id)).first()

    if(product_type is None or unit is None):
       raise ValidationError('invalid product type or unit')

    return Product(product_name=name,
                  product_description =  description,
                  price_per_unit = float(price),
                  unit_items = unit,
                  product_items = product_type)



class Unit(db.Model):
  __tablename__ = "units"
  id = db.Column(db.Integer, primary_key=True)
  unit_name =  db.Column(db.String(64), unique=True, nullable=False)
  unit_short =  db.Column(db.String(8), unique=True, nullable=True)

  ref_products = db.relationship('Product',backref='unit_items', lazy=True)

  def __repr__(self):
    return f"unit({self.unit_name} {self.unit_short})"
  
  @staticmethod
  def get_unit(id):
    return Unit.query.filter_by(id=id).first()
  
  def to_json(self):
       json_unit = {
           'url': url_for('api.get_unit', id=self.id),
           'unit_name': self.unit_name,
           'unit_short': self.unit_short,
           'products_count': self.ref_products
       }
       return json_unit
  
  @staticmethod
  def from_json(json_post):
    name = json_post.get('unit_name')
    short = json_post.get('unit_short')
    if (name is None or name == ''):
        raise ValidationError('doesnot have a name')

    return Unit(unit_name =name, unit_short =short)
  
  @staticmethod
  def insert_units():
    units = [
      {'unit_name':'Kilogram','unit_short':'kg'},
      {'unit_name':'Gram','unit_short':'gram'},
      {'unit_name':'Milligram','unit_short':'mg'},
      {'unit_name':'Liter','unit_short':'L'},
      {'unit_name':'Milliliter','unit_short':'ml'},
      {'unit_name':'Dozen','unit_short':'dz'},
      {'unit_name':'Packet','unit_short':'pkt'},
      {'unit_name':'Package','unit_short':'pkg'},
      {'unit_name':'Bag','unit_short':'bg'},
      {'unit_name':'Box','unit_short':'bx'},
      {'unit_name':'Meter','unit_short':'m'},
      {'unit_name':'Centimeter','unit_short':'cm'},
      {'unit_name':'Millimeter','unit_short':'mm'}
    ]

    for u in units:
        unit = Unit.query.filter_by(unit_name=u['unit_name']).first()
        if unit is None:
            unit = Unit(**u)
            db.session.add(unit)
    
    db.session.commit()

  


class ProductType(db.Model):
  __tablename__ = "product_type"
  id = db.Column(db.Integer, primary_key=True)
  type_name =  db.Column(db.String(64), unique=True, nullable=False)

  ref_products = db.relationship('Product', backref='product_items', lazy=True)

  def __repr__(self):
    return f"Product_type({self.type_name})"

  @staticmethod
  def get_productType(id):
    return ProductType.query.filter_by(id=id).first()

  
  def to_json(self):
        json_productType = {
            'url': url_for('api.get_category', id=self.id),
            'category_name': self.type_name,
            'products_count': [element.to_json() for element in self.ref_products]
        }
        return json_productType
  
  @staticmethod
  def from_json(json_post):
    name = json_post.get('type_name')
    if (name is None or name == ''):
        raise ValidationError('doesnot have a name')
    return ProductType(type_name =name)
  
  @staticmethod
  def from_dict(dict_post):
    name = dict_post['type_name']
    if (name is None or name == ''):
        raise ValidationError('doesnot have a name')
    return ProductType(type_name =name)


  @staticmethod
  def insert_categories():
    categories = [
      {'type_name':'Dairy'},
      {'type_name':'Rice'},
      {'type_name':'Fruits'},
      {'type_name':'Dry Fruits'},
      {'type_name':'Dal and Pulses'},
      {'type_name':'Personal Care'},
      {'type_name':'Spices'},
      {'type_name':'Oils'}

    ]

    for cat in categories:
        category = ProductType.query.filter_by(type_name=cat['type_name']).first()
        if category is None:
            category = ProductType(**cat)
            db.session.add(category)
    
    db.session.commit()



class Stock(db.Model):
  __tablename__ = "stock"
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
 
  in_stock = db.Column(db.Integer,nullable=False)
  last_update_time = db.Column(db.DateTime,unique=True ,nullable=False,default=datetime.utcnow)

  def __repr__(self):
    return f"Stock({self.product_id})"

  @property
  def get_stockUnits(self):
    return self.in_stock


class OrderedItem(db.Model):
  __tablename__ = "order_item"
  id = db.Column(db.Integer, primary_key=True)

  quantity = db.Column(db.Integer,nullable=False)
  price  = db.Column(db.Numeric(10,3),nullable=False)

  product_id =  db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
  placed_order_id = db.Column(db.Integer,db.ForeignKey('placed_order.id'),nullable=False)
  
  def __repr__(self):
    return f"OrderedItem: id:{self.id}\nquantity:{self.quantity}\nprice:{self.price}"

  def to_json(self):
    json_unit = {
          'product_id': self.product_id,
          'quantity': self.quantity,
          'placed_order_id':self.placed_order_id,
       }
    return json_unit

  
  
  @staticmethod
  def from_json(post_json,placed_order_id):
    quantity = post_json.get('quantity')
    price = post_json.get('price')

    product_id = post_json.get('product_id')

    return OrderedItem(quantity = quantity, price = price , product_id = product_id, placed_order_id = placed_order_id)


class PlacedOrder(db.Model):
  __tablename__ = "placed_order"
  id = db.Column(db.Integer, primary_key=True)

  time_placed = db.Column(db.DateTime,unique=True, nullable = True,default=datetime.utcnow)
  details = db.Column(db.Text,nullable=True)
  delivery_address = db.Column(db.Text,nullable=False)
  delivery_address_pin = db.Column(db.String(6),nullable=True)
  delivery_charge = db.Column(db.Numeric(10,3),nullable=False)

  customer_name = db.Column(db.String(128), nullable=False)

  customer_contact_phone = db.Column(db.String(10), nullable=False)
  customer_address = db.Column(db.Text, nullable=False)
  customer_address_pin = db.Column(db.String(6),nullable=False)


  
  # customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
  order_status_id =  db.Column(db.Integer,db.ForeignKey('order_status.id'),nullable=False)
  
  ref_items = db.relationship('OrderedItem',cascade="all,delete", backref='items', lazy=True)

  def __repr__(self):
    return f"PlacedOrder: id:{self.id}\ntime_place:{self.time_placed}\ndelivert_address:{self.delivery_address}"
  
  @staticmethod
  def from_json(post_json,order_status):
    details = post_json.get('details')
    # if (details is None or details == ''):
    #     raise ValidationError('doesnot have a customer name')

    delivery_address = post_json.get('delivery_address')
    if (delivery_address is None or delivery_address == ''):
        raise ValidationError('doesnot have a delivery address')

    delivery_address_pin = post_json.get('delivery_address_pin')
    if (delivery_address_pin is None or delivery_address_pin == ''):
        raise ValidationError('doesnot have a delivery address pin')

    if(delivery_address_pin.strip() != ''):
      charge = DeliveryCharge.get_delivery_charge(int(delivery_address_pin.strip(),base=10))

    if charge is None:
      charge = DeliveryCharge.get_default_charge()

    delivery_charge =  charge.amount

    customer_name = post_json.get('customer_details').get('customer_name')
    if (customer_name is None or customer_name == ''):
        raise ValidationError('doesnot have a customer name')

    customer_contact_phone = post_json.get('customer_details').get('contact_phone')
    if (customer_contact_phone is None or customer_contact_phone == ''):
        raise ValidationError('doesnot have a customer phone')

    customer_address = post_json.get('customer_details').get('contact_address')
    if (customer_address is None or customer_address == ''):
        raise ValidationError('doesnot have a customer address')

    customer_address_pin = post_json.get('customer_details').get('address_pin') 
    if (customer_address_pin is None or customer_address_pin == ''):
        raise ValidationError('doesnot have a customer address pin')

    return PlacedOrder(details = details, delivery_address = delivery_address,\
      delivery_address_pin = delivery_address_pin, delivery_charge = delivery_charge,\
      customer_name= customer_name, customer_contact_phone= customer_contact_phone ,\
      customer_address = customer_address,customer_address_pin = customer_address_pin,\
      order = order_status)
  
  def to_json(self):
       json_unit = {
           'order_id': self.id,
           'time_placed': convert_time(self.time_placed),
           'details': self.details,
           'delivery_address': self.delivery_address,
           'delivery_address_pin':self.delivery_address_pin,
           'delivery_charge':str(self.delivery_charge),
           'ordered_items': [element.to_json() for element in self.ref_items],
           'customer_details': {
              'customer_name': self.customer_name,
              'customer_contact_phone':self.customer_contact_phone,
              'customer_address':self.customer_address,
              'customer_address_pin':self.customer_address_pin,
           }
       }
       return json_unit

class DeliveryCharge(db.Model):
  __tablename__ = "delivery_charge"
  id = db.Column(db.Integer, primary_key=True)
  address_pin =  db.Column(db.String(6), unique=True, nullable=False)
  amount = db.Column(db.Numeric(4,2),nullable=False)


  def __repr__(self):
    return f"Delivery_charge({self.address_pin})"

  @staticmethod
  def get_delivery_charge(pin):
    return DeliveryCharge.query.filter_by(address_pin=str(pin)).first()
  
  @staticmethod
  def get_default_charge():
    return DeliveryCharge.query.filter_by(address_pin="others").first()
  


  
  def to_json(self):
        json_deliveryCharge = {
            'url': url_for('api.get_delivery_charge', id=self.id),
            'address_pin': self.address_pin,
            'amount': str(self.amount)
        }
        return json_deliveryCharge
  
  # @staticmethod
  # def from_json(json_post):
  #   name = json_post.get('type_name')
  #   if (name is None or name == ''):
  #       raise ValidationError('doesnot have a name')
  #   return ProductType(type_name =name)
  
  @staticmethod
  def from_dict(dict_post):
    address_pin = dict_post['address_pin']
    amount  = dict_post['amount']

    if (address_pin is None or address_pin == ''):
        raise ValidationError('doesnot have a pin')
    
    if (amount is None or amount == ''):
        raise ValidationError('doesnot have a amount')

    return DeliveryCharge(address_pin = address_pin,amount=amount)

  @staticmethod
  def insert_default_charge():
    charges = [
      {'address_pin':'others','amount':200}
    ]

    for c in charges:
        dc = DeliveryCharge.query.filter_by(address_pin=c['address_pin']).first()
        if dc is None:
            dc = DeliveryCharge(**c)
            db.session.add(dc)
    
    db.session.commit()


class OrderStatus(db.Model):
  __tablename__ = "order_status"
  id = db.Column(db.Integer, primary_key=True)

  status_time = db.Column(db.DateTime,unique=True, nullable=False,default=datetime.utcnow)
  details = db.Column(db.Text,nullable=True)

  status_catalog_id =  db.Column(db.Integer,db.ForeignKey('status_catalog.id'), nullable=False)

  ref_order = db.relationship('PlacedOrder',cascade="all,delete", backref='order', lazy=True)

  def __repr__(self):
    return f"OrderStatus:\nid:{self.id}\ndetails:{self.details}"
  
  @staticmethod
  def from_data(status_catalog_id,details=""):
    return OrderStatus(details = details,status_catalog_id = status_catalog_id )


class StatusCatalog(db.Model):
  __tablename__ = "status_catalog"
  id = db.Column(db.Integer, primary_key=True)
  status_name = db.Column(db.String(128),nullable=False)

  ref_orders = db.relationship('OrderStatus', backref='orders', lazy=True)

  def __repr__(self):
    return f"StatusCatalog ({self.status_name})"
  
  @staticmethod
  def new_id():
    return StatusCatalog.query.filter_by(status_name = "new order").first()
  
  @staticmethod
  def old_id():
    return StatusCatalog.query.filter_by(status_name = "delivered").first()


  @staticmethod
  def insert_order_status():
    status = [
      {'status_name':'new order'},
      {'status_name':'delivered'}
    ]

    for s in status:
        status = StatusCatalog.query.filter_by(status_name=s['status_name']).first()
        if status is None:
            status = StatusCatalog(**s)
            db.session.add(status)
    
    db.session.commit()
  

# class Delivery(db.Model):
#   __tablename__ = "delivery"
#   id = db.Column(db.Integer, primary_key=True)
#   delivery_time_placed = db.Column(db.DateTime,unique= True, nullable=False)
#   delivery_time_actual = db.Column(db.DateTime,unique = True, nullable=True)
#   notes = db.Column(db.Text,nullable=True)

#   placed_order_id = db.Column(db.Integer, db.ForeignKey('placed_order.id'),nullable=False)
#   employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),nullable=True)

#   def __repr__(self):
#     return f"Delivery:\n id : {self.id}\ntime:{self.delivery_time_placed}\noder_id:{self.placed_order_id}"




# class Customer(db.Model):
#   __tablename__ = "customer"
#   id = db.Column(db.Integer, primary_key=True)

#   first_name =  db.Column(db.String(128), nullable=False)
#   last_name =  db.Column(db.String(128), nullable=True)

#   contact_email =  db.Column(db.String(128), unique=False, nullable=True)
#   contact_phone =  db.Column(db.String(10), unique=True, nullable=False)

#   customer_address =  db.Column(db.Text, nullable=False)
#   delivery_address =  db.Column(db.Text, nullable=True)

#   ref_orders = db.relationship('PlacedOrder',backref='orders',lazy=True)

#   def __repr__(self):
#     return f"Customer:\nName:{self.first_name} {self.last_name}\ncontant:{self.contact_email},{self.contact_phone}\naddress:{self.customer_address}"

#   def to_json(self):
#         json_customer = {
#             # 'url': url_for('api.edit_customer', id=self.id),
#             'customer_id':self.id,
#             'category_name': self.first_name+" " + self.last_name,
#             # 'products_count': [element.to_json() for element in self.ref_products]
#         }
#         return json_customer
  
#   @staticmethod
#   def from_json(json_post):
#     first_name = json_post.get('first_name')
#     last_name = json_post.get('last_name')
#     contact_email = json_post.get('contact_email')
#     contact_phone = json_post.get('contact_phone')
#     customer_address = json_post.get('customer_address')

#     delivery_address = json_post.get('delivery_address')


#     if (first_name is None or first_name == ''):
#         raise ValidationError('doesnot have a first_name')
#     if (last_name is None or last_name == ''):
#         raise ValidationError('doesnot have a last_name')

#     if (contact_phone is None or contact_phone == ''):
#         raise ValidationError('doesnot have a contact_phone')
    
#     if (customer_address is None or customer_address == ''):
#         raise ValidationError('doesnot have a customer_address')
    
      
#     return Customer(first_name = first_name, last_name = last_name,\
#       contact_email = contact_email,contact_phone= contact_phone,\
#         customer_address= customer_address,delivery_address = delivery_address)



# class Employee(db.Model):
#   __tablename__ = "employee"
#   id = db.Column(db.Integer, primary_key=True)

#   first_name =  db.Column(db.String(128), nullable=False)
#   last_name =  db.Column(db.String(128), nullable=True)
#   contact_phone =  db.Column(db.String(10), unique=True, nullable=False)

#   ref_delivery = db.relationship('Delivery',backref="deliveries")
#   def __repr__(self):
#     return f"Employee: \nid:{self.id}\nName:{self.first_name} {self.last_name}\nConatact:{self.contact_phone}"



class Admin(db.Model,UserMixin):
  __tablename__ = "admin"
  id = db.Column(db.Integer, primary_key=True)

  username = db.Column(db.String(128), unique=True, nullable=False)
  password_hash = db.Column(db.String(128),unique = True,nullable=False)

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

 
  def generate_auth_token(self, expiration):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': self.id}).decode('utf-8')
  
  @staticmethod
  def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except:
      return None
    return Admin.query.get(data['id'])


  def generate_reset_token(self, expiration=3600):
      s = Serializer(current_app.config['SECRET_KEY'], expiration)
      return s.dumps({'reset': self.id}).decode('utf-8')

  @staticmethod
  def reset_password(token, new_password):
      s = Serializer(current_app.config['SECRET_KEY'])
      try:
          data = s.loads(token.encode('utf-8'))
      except:
          return False
      user = Admin.query.get(data.get('reset'))
      if user is None:
          return False
      user.password = new_password
      db.session.add(user)
      return True

  def __repr__(self):
    return f"Admin:\nName:{self.first_name} {self.last_name}\nUserName:{self.username}"
  

  @staticmethod
  def insert_default_admin():
    users= [
      {'username':'devadmin','password':'hardtoguesspass'},
      {'username':'appadmin','password':'apppass'}
    ]

    for u in users:
        user = Admin.query.filter_by(username=u['username']).first()
        if user is None:
            user = Admin(**u)
            db.session.add(user)
    
    db.session.commit()

  

class ShopDetails(db.Model):
  __tablename__ = "shop_details"
  id = db.Column(db.Integer, primary_key=True)

  shop_name =  db.Column(db.String(128), unique=True, nullable=False)
  shop_email = db.Column(db.String(64), unique=True, nullable=False)
  contact_phone = db.Column(db.String(10), unique=True, nullable=False)
  details = db.Column(db.Text, nullable=True)
  address = db.Column(db.Text,nullable=False)


  def __repr__(self):
    return f"ShopDetails:\nName:{self.shop_name}\ncontact:{self.contact_phone}\naddress:{self.address}"

  @staticmethod
  def insert_shop_details():
    details= [
      {'shop_name':'My Shop','shop_email':'DefaultMial@gmail.com','contact_phone':'8888888888','details':'best grocery shop','address':'near garmur'}
    ]

    for d in details:
        detail = ShopDetails.query.filter_by(shop_name=d['shop_name']).first()
        if detail is None:
            detail = ShopDetails(**d)
            db.session.add(detail)
    
    db.session.commit()

  def to_json(self):
        json_shopDetails = {
            'url': url_for('api.get_shopdetails', id=self.id),
            'shop_name': self.shop_name,
            'shop_email':self.shop_email,
            'contact_phone': self.contact_phone,
            'details':self.details,
            'address':self.address
        }
        return json_shopDetails
  

