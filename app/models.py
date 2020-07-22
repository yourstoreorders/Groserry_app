from . import db


# product Models

class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  product_name =  db.Column(db.String(128), unique=True, nullable=False)
  product_description = db.Column(db.String(255), nullable=False)
  price_per_unit = db.Column(db.Float,nullable=False)

  product_type_id = db.Column(db.Integer,db.ForeignKey('product_type.id'), nullable=False)
  unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
  
  stock_details = db.relationship('Stock', backref='stock_details', lazy=True)


  def __repr__(self):
    return f"Product({self.product_name})"

class Unit(db.Model):
  __tablename__ = "units"
  id = db.Column(db.Integer, primary_key=True)
  unit_name =  db.Column(db.String(64), unique=True, nullable=False)
  unit_short =  db.Column(db.String(8), unique=True, nullable=True)

  products = db.relationship('Product', backref='items', lazy=True)

  def __repr__(self):
    return f"unit({self.unit_name} {self.unit_short})"


class ProductType(db.Model):
  __tablename__ = "product_type"
  id = db.Column(db.Integer, primary_key=True)
  type_name =  db.Column(db.String(64), unique=True, nullable=False)

  products = db.relationship('Product', backref='items', lazy=True)

  def __repr__(self):
    return f"Product_type({self.type_name})"

class Stock(db.Model):
  __tablename__ = "stock"
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
 
  in_stock = db.Column(db.Numeric(10,3),nullable=False)
  last_update_time = db.Column(db.DateTime,unique=True ,nullable=False)

  def __repr__(self):
    return f"Stock({self.product_id})"

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

class Admin(db.Model):
  __tablename__ = "admin"
  id = db.Column(db.Integer, primary_key=True)

  first_name =  db.Column(db.String(64), nullable=False)
  last_name =  db.Column(db.String(64), nullable=True)

  username = db.Column(db.String(128), unique=True, nullable=False)
  password_hash = db.Column(db.String(128),unique = True,nullable=False)

  ref_store = db.relationship('ShopDetails',backref='stores')

  def __repr__(self):
    return f"Admin:\nName:{self.first_name} {self.last_name}\nUserName:{self.username}"



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
  
class OderStatus(db.Model):
  __tablename__ = "order_status"
  id = db.Column(db.Integer, primary_key=True)

  status_time = db.Column(db.DateTime,unique=True, nullable=False)
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


