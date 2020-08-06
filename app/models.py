import os
from flask import current_app, request, url_for
from datetime import datetime
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# product Models

class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  product_name =  db.Column(db.String(128), unique=True, nullable=False)
  product_description = db.Column(db.String(255), nullable=False)
  price_per_unit = db.Column(db.Numeric(10,3),nullable=False)
  product_image = db.Column(db.String(256),nullable=False)

  product_type_id = db.Column(db.Integer,db.ForeignKey('product_type.id'), nullable=False)
  unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
  

  stock_details = db.relationship('Stock', cascade="all,delete", backref='stock_details', lazy=True)


  # def __repr__(self):
  #   return f"Product({self.product_name})"

  @property
  def get_product(self):
    return Product.query.join(Unit).all()
  
  def to_json(self):
       print(self.stock_details[0].in_stock)
       json_unit = {
           'url': url_for('api.get_product', id=self.id),
           'product_name': self.product_name,
           'product_image': os.path.join(url_for('static',filename='product_images',_external=True)\
              , self.product_image),
           'product_description': self.product_description,
           'price_per_unit': str(self.price_per_unit),
           'unit': self.unit_id,
           'product_type': self.product_type_id,
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

  ref_products = db.relationship('Product', backref='unit_items', lazy=True)

  def __repr__(self):
    return f"unit({self.unit_name} {self.unit_short})"
  
  def get_unit(self,id):
    return Unit.query.filter_by(id=id).first
  
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

  


class ProductType(db.Model):
  __tablename__ = "product_type"
  id = db.Column(db.Integer, primary_key=True)
  type_name =  db.Column(db.String(64), unique=True, nullable=False)

  ref_products = db.relationship('Product', backref='product_items', lazy=True)

  def __repr__(self):
    return f"Product_type({self.type_name})"

  
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


class ShopDetails(db.Model):
  __tablename__ = "shop_details"
  id = db.Column(db.Integer, primary_key=True)

  shop_name =  db.Column(db.String(128), unique=True, nullable=False)

  contact_phone = db.Column(db.String(10), unique=True, nullable=False)
  details = db.Column(db.Text, nullable=True)
  address = db.Column(db.Text,nullable=False)

  admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

  def __repr__(self):
    return f"ShopDetails:\nName:{self.shop_name}\ncontact:{self.contact_phone}\naddress:{self.address}"


class OrderedItem(db.Model):
  __tablename__ = "order_item"
  id = db.Column(db.Integer, primary_key=True)

  quantity = db.Column(db.Integer,nullable=False)
  price  = db.Column(db.Numeric(10,3),nullable=False)

  product_id =  db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
  placed_order_id = db.Column(db.Integer,db.ForeignKey('placed_order.id'),nullable=False)
  def __repr__(self):
    return f"OrderedItem: id:{self.id}\nquantity:{self.quantity}\nprice:{self.price}"

class PlacedOrder(db.Model):
  __tablename__ = "placed_order"
  id = db.Column(db.Integer, primary_key=True)

  time_placed = db.Column(db.DateTime,unique= True,nullable=False)
  details = db.Column(db.Text,nullable=True)
  delivery_address = db.Column(db.Text,nullable=False)

  customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
  order_status_id =  db.Column(db.Integer,db.ForeignKey('order_status.id'),nullable=False)
  

  ref_items = db.relationship('OrderedItem', backref='items', lazy=True)

  def __repr__(self):
    return f"PlacedOrder: id:{self.id}\ntime_place:{self.time_placed}\ndelivert_address:{self.delivery_address}"
  
class OrderStatus(db.Model):
  __tablename__ = "order_status"
  id = db.Column(db.Integer, primary_key=True)

  status_time = db.Column(db.DateTime,unique=True, nullable=False,default=datetime.utcnow)
  details = db.Column(db.Text,nullable=True)
  status_catalog_id =  db.Column(db.Integer,db.ForeignKey('status_catalog.id'), nullable=False)

  def __repr__(self):
    return f"OrderStatus:\nid:{self.id}\ndetails:{self.details}"

class StatusCatalog(db.Model):
  __tablename__ = "status_catalog"
  id = db.Column(db.Integer, primary_key=True)
  status_name = db.Column(db.String(128),nullable=False)


  ref_orders = db.relationship('OrderStatus', backref='orders', lazy=True)

  def __repr__(self):
    return f"StatusCatalog ({self.status_name})"

class Delivery(db.Model):
  __tablename__ = "delivery"
  id = db.Column(db.Integer, primary_key=True)
  delivery_time_placed = db.Column(db.DateTime,unique= True, nullable=False)
  delivery_time_actual = db.Column(db.DateTime,unique = True, nullable=True)
  notes = db.Column(db.Text,nullable=True)

  placed_order_id = db.Column(db.Integer, db.ForeignKey('placed_order.id'),nullable=False)
  employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),nullable=True)

  def __repr__(self):
    return f"Delivery:\n id : {self.id}\ntime:{self.delivery_time_placed}\noder_id:{self.placed_order_id}"




class Customer(db.Model):
  __tablename__ = "customer"
  id = db.Column(db.Integer, primary_key=True)

  first_name =  db.Column(db.String(128), nullable=False)
  last_name =  db.Column(db.String(128), nullable=True)

  contact_email =  db.Column(db.String(128), unique=False, nullable=True)
  contact_phone =  db.Column(db.String(10), unique=True, nullable=False)

  customer_address =  db.Column(db.Text, nullable=False)
  delivery_address =  db.Column(db.Text, nullable=True)

  ref_orders = db.relationship('PlacedOrder',backref='orders',lazy=True)

  def __repr__(self):
    return f"Customer:\nName:{self.first_name} {self.last_name}\ncontant:{self.contact_email},{self.contact_phone}\naddress:{self.customer_address}"

class Employee(db.Model):
  __tablename__ = "employee"
  id = db.Column(db.Integer, primary_key=True)

  first_name =  db.Column(db.String(128), nullable=False)
  last_name =  db.Column(db.String(128), nullable=True)
  contact_phone =  db.Column(db.String(10), unique=True, nullable=False)

  ref_delivery = db.relationship('Delivery',backref="deliveries")
  def __repr__(self):
    return f"Employee: \nid:{self.id}\nName:{self.first_name} {self.last_name}\nConatact:{self.contact_phone}"



class Admin(db.Model,UserMixin):
  __tablename__ = "admin"
  id = db.Column(db.Integer, primary_key=True)

  first_name =  db.Column(db.String(64), nullable=False)
  last_name =  db.Column(db.String(64), nullable=True)

  username = db.Column(db.String(128), unique=True, nullable=False)
  password_hash = db.Column(db.String(128),unique = True,nullable=False)

  ref_store = db.relationship('ShopDetails',backref='stores')

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

  






