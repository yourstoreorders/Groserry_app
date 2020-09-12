import secrets
import os
from sqlalchemy import exc
from config import config
from flask import request, redirect, url_for, session , flash
from flask import render_template, jsonify
from . import main
from .. import db
from .. models import Admin,Product,Unit,ProductType,\
  Stock ,PlacedOrder, OrderStatus, StatusCatalog, OrderedItem,\
  WeightDeliveryCharge, DeliveryCharge,\
  ShopDetails, PaymentMethod,PaymentStatus
from . forms import LoginForm, AddProduct, UpdateProduct, DeleteProduct,\
  AddCategory,UpdateCategory, DeleteCategory, \
  DeleteOrder, UpdateOrder,\
  AddressAddCharge, AddressUpdateCharge,AddressDeleteCharge,\
  WeightAddCharge, WeightUpdateCharge,WeightDeleteCharge,\
  ChangeUsernameForm, ChangePasswordForm, ChangeShopDetailForm
  

from flask_login import login_required,logout_user, login_user, current_user

@main.context_processor
def inject_user():
    return dict(shop_name= ShopDetails.query.all()[0].shop_name)


@main.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = Admin.query.filter_by(username=form.username.data.lower()).first()
    if user is not None and user.verify_password(form.password.data):
        login_user(user)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.dashboard')
        return redirect(next)

    flash('Invalid email or password.')
  return render_template('login.html',form=form)



@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

  print(os.path.join(url_for('static',filename='product_images'),"hrhrhr.txt"))

  return render_template('index.html',name = current_user.username)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))


def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  
  _, f_ext = os.path.splitext(form_picture.filename)

  picture_filename = random_hex + f_ext

  picture_path = os.path.join("app/" +url_for('static',filename="product_images"),picture_filename)
  form_picture.save(picture_path)


  return picture_filename

def delete_picture(picture_filename):
  try:
    os.remove(os.path.join("app" +url_for('static',filename="product_images"),picture_filename))
  except:
    flash("could not remove image file!")
    
@main.route('/products', methods=['GET', 'POST'])
@login_required
def products():
  add_form = AddProduct()

  update_form = UpdateProduct()

  delete_form = DeleteProduct()

  add_form.unit_id.choices = [(unit.id, unit.unit_name) for unit in Unit.query.all()]
  add_form.product_type_id.choices = [(category.id, category.type_name) for category in ProductType.query.all()]

  update_form.unit_id.choices = [(unit.id, unit.unit_name) for unit in Unit.query.all()]
  update_form.product_type_id.choices = [(category.id, category.type_name) for category in ProductType.query.all()]
  
  products = Product.query.all()

  if add_form.validate_on_submit():
    add_form_data = dict()
    if add_form.product_image.data:
      picture_file = save_picture(add_form.product_image.data)
      for items in add_form:
        add_form_data[items.id] = items.data
      
      add_form_data["product_image"] = picture_file
      try:
        element = Product.from_dict(add_form_data)
        db.session.add(element)
        db.session.commit()
      except exc.SQLAlchemyError as e:
        
        flash("Something went wrong,Duplicate Entry!","danger")
        return redirect(url_for('main.products'))

      

      stock = Stock(product_id = element.id,in_stock= add_form_data["stock"])
      db.session.add(stock)
      db.session.commit()
      flash('Product Added')

      return redirect(url_for('main.products'))
    # flash('Something went wrong!')


  if update_form.validate_on_submit():
    update_form_data = dict()
    picture_file = ""
    if update_form.product_new_image.data:
      picture_file = save_picture(update_form.product_new_image.data)

    for items in update_form:
      update_form_data[items.id] = items.data

    update_form_data["product_new_image"] = picture_file


    element = Product.query.get_or_404(update_form_data["product_id"])
    
    element.product_name = update_form_data.get('product_name', element.product_name)
    
    if(picture_file !=""):
      old_product_image = element.product_image
      element.product_image = update_form_data.get("product_new_image")

      delete_picture(old_product_image)
    
    element.product_description = update_form_data.get('product_description', element.product_description)
    
    element.price_per_unit = update_form_data.get('price_per_unit', element.price_per_unit)
    element.unit_id = update_form_data.get('unit_id', element.unit_id)
    element.product_type_id = update_form_data.get('product_type_id', element.product_type_id)
    element.product_weight = update_form_data.get('product_weight', element.product_weight)
    
    
    try:
        db.session.add(element)
        db.session.commit()
    except exc.SQLAlchemyError as e:
       
        flash("Something went wrong,Duplicate Entry!","danger")
        return redirect(url_for('main.products'))
    
    stock = Stock.query.get_or_404(element.id)

    stock.in_stock = update_form_data.get('stock', stock.in_stock)
    db.session.add(stock)
    db.session.commit()

    flash('Product Updated')

    return redirect(url_for('main.products'))


  if delete_form.validate_on_submit():
    delete_form_data = dict()
    for items in delete_form:
      delete_form_data[items.id] = items.data

    element = Product.query.get_or_404(delete_form_data["product_id"])
    old_product_image = element.product_image

    try:
      
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong","danger")
    else:
      delete_picture(old_product_image)
      flash('Product Deleted',"success")

    
    flash('Product Deleted')
    return redirect(url_for('main.products'))
  
  # flash('Something went wrong!')
  return render_template('products.html',products = products,add_form=add_form,update_form= update_form, delete_form= delete_form)

@main.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
  add_form = AddCategory()

  update_form = UpdateCategory()

  delete_form = DeleteCategory()

  categories = ProductType.query.all()


  if add_form.submit1.data and  add_form.validate_on_submit():

    # print("add form")
    add_form_data = dict()
    
    for items in add_form:
      add_form_data[items.id] = items.data

    try:
      element = ProductType.from_dict(add_form_data)
      db.session.add(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      flash("Something went wrong,Duplicate Entry!","danger")
      return redirect(url_for('main.categories'))
      
    

    flash('Category Added')

    return redirect(url_for('main.categories'))

  if update_form.submit2.data and update_form.validate_on_submit():

    # print("update form")
    update_form_data = dict()

    for items in update_form:
      update_form_data[items.id] = items.data

    element = ProductType.query.get_or_404(update_form_data["type_id"])
    
    element.type_name = update_form_data.get('type_name', element.type_name)
    
    try:
      db.session.add(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      flash("Something went wrong,Duplicate Entry!","danger")
      return redirect(url_for('main.categories'))
  

    flash('Category Updated')

    return redirect(url_for('main.categories'))


  if delete_form.submit3.data and delete_form.validate_on_submit():

    # print("delete called")
    delete_form_data = dict()
    for items in delete_form:
      delete_form_data[items.id] = items.data

    element = ProductType.query.get_or_404(delete_form_data["type_id"])
    
    try:
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong")
    else:
      flash('Category Deleted')

    return redirect(url_for('main.categories'))

  return render_template('categories.html',categories = categories,add_form = add_form, update_form = update_form, delete_form = delete_form )




# orders
@main.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():

  # orders = PlacedOrder.query.join(OrderStatus, PlacedOrder.order_status_id == OrderStatus.id).\
  #   filter(OrderStatus.status_catalog_id == StatusCatalog.new_id().id).all()[::-1]
  
  orders = db.session.query(
          PlacedOrder,PaymentMethod,PaymentStatus
      ).join(
        OrderStatus, PlacedOrder.order_status_id == OrderStatus.id
      ).filter(
        OrderStatus.status_catalog_id == StatusCatalog.new_id().id
      ).filter(
        PlacedOrder.payment_method == PaymentMethod.id
      ).filter(
        PlacedOrder.payment_status == PaymentStatus.id
      ).all()[::-1]
  update_form = UpdateOrder()

  update_form.order_status.choices = [(status.id, status.status_name) for status in StatusCatalog.query.all()]

  delete_form = DeleteOrder()



  if update_form.submit2.data and update_form.validate_on_submit():
    
    update_form_data = dict()
    for items in update_form:
      update_form_data[items.id] = items.data

    order  = PlacedOrder.query.get_or_404(update_form_data["order_id"])
    orderStatus = OrderStatus.query.get_or_404(order.order_status_id)
    
    
    orderStatus.status_catalog_id = update_form_data.get('order_status', orderStatus.status_catalog_id)
    if(orderStatus.status_catalog_id == StatusCatalog.old_id().id):
      for item in order.ref_items:
        stock = Stock.query.filter_by(product_id = item.product_id).first()
        
        if stock is not None:
            if(stock.in_stock < item.quantity):
              flash('Someting went wrong! Stock in sufficeint!')
              return redirect(url_for('main.orders'))
            else:
              stock.in_stock = 0 if (stock.in_stock - item.quantity <= 0) else stock.in_stock - item.quantity
              db.session.add(stock)
        else:
          flash('Someting went wrong! Products Not in stock')
          return redirect(url_for('main.orders'))

    

    db.session.add(orderStatus)
    db.session.commit()
  

    flash('Order Updated')

    return redirect(url_for('main.orders'))

  

  if delete_form.submit3.data and delete_form.validate_on_submit():

    delete_form_data = dict()
    for items in delete_form:
      delete_form_data[items.id] = items.data

    element = PlacedOrder.query.get_or_404(delete_form_data["order_id"])
    
    try:
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong")
    else:
      flash('Order Deleted')

    return redirect(url_for('main.orders'))


  return render_template('orders.html',orders = orders,update_form = update_form, delete_form = delete_form)


@main.route('/order_items/<int:order_id>', methods=['GET'])
@login_required
def order_items(order_id):
  
  # it = db.session.query(Product, OrderedItem).outerjoin(Product, OrderedItem,Product.id == OrderedItem.product_id ).all()
  
  
  # items = Product.query.join(OrderedItem, OrderedItem.product_id == Product.id).\
  #   filter_by(placed_order_id = order_id).all()
  # items = OrderedItem.query.filter_by(placed_order_id = order_id).all()
  order  = PlacedOrder.query.filter_by(id=order_id).first() 
  if order is None:
    flash("Invalid order!")
    return {}

  delivery_charge = order.delivery_charge

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
  responseObj['delivery_charge'] = float(delivery_charge)
  responseObj['total_amount'] = total_amount  + float(delivery_charge)
  
  return jsonify(responseObj)



@main.route('/old_orders', methods=['GET', 'POST'])
@login_required
def old_orders():
  # orders = PlacedOrder.query.join(OrderStatus, PlacedOrder.order_status_id == OrderStatus.id).\
  #   filter(OrderStatus.status_catalog_id == StatusCatalog.old_id().id).all()

  orders = db.session.query(
          PlacedOrder,PaymentMethod,PaymentStatus
      ).join(
        OrderStatus, PlacedOrder.order_status_id == OrderStatus.id
      ).filter(
        OrderStatus.status_catalog_id == StatusCatalog.old_id().id
      ).filter(
        PlacedOrder.payment_method == PaymentMethod.id
      ).filter(
        PlacedOrder.payment_status == PaymentStatus.id
      ).all()[::-1]


  delete_form = DeleteOrder()

  

  if delete_form.submit3.data and delete_form.validate_on_submit():

    delete_form_data = dict()
    for items in delete_form:
      delete_form_data[items.id] = items.data

    element = PlacedOrder.query.get_or_404(delete_form_data["order_id"])
    
    try:
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong")
    else:
      flash('Order Deleted')

    return redirect(url_for('main.old_orders'))


  return render_template('old_orders.html',orders = orders, delete_form = delete_form)


@main.route('/delivery_charges', methods=['GET', 'POST'])
@login_required
def delivery_charges():
  
  # address forms
  address_add_form = AddressAddCharge()
  address_update_form = AddressUpdateCharge()
  address_delete_form = AddressDeleteCharge()


  # weight forms
  weight_add_form = WeightAddCharge(request.form)
  weight_update_form = WeightUpdateCharge(request.form)
  weight_delete_form = WeightDeleteCharge()


  address_charges = DeliveryCharge.query.all()

  weight_charges = WeightDeliveryCharge.query.all()

  if address_add_form.submit1.data and  address_add_form.validate_on_submit():

    # print("add form")
    address_add_form_data = dict()
    
    for items in address_add_form:
      address_add_form_data[items.id] = items.data
      
    element = DeliveryCharge.from_dict(address_add_form_data)
    db.session.add(element)
    db.session.commit()

    flash('Delivery Charge For Address Added')

    return redirect(url_for('main.delivery_charges'))

  # weight charge add form
  if request.method == "POST" and weight_add_form.submit4.data and  weight_add_form.validate_on_submit():
    print("sds")
    weight_add_form_data = dict()
    
    for items in weight_add_form:
      weight_add_form_data[items.id] = items.data
      
    element = WeightDeliveryCharge.from_dict(weight_add_form_data)
    db.session.add(element)
    db.session.commit()

    flash('Delivery Charge For Weight Added')

    return redirect(url_for('main.delivery_charges'))

  if address_update_form.submit2.data and address_update_form.validate_on_submit():

    # print("update form")
    update_form_data = dict()

    for items in address_update_form:
      update_form_data[items.id] = items.data

    element = DeliveryCharge.query.get_or_404(update_form_data["charge_id"])
    
    element.address_pin = update_form_data.get('address_pin', element.address_pin)
    element.amount = update_form_data.get('amount', element.amount)
    
    db.session.add(element)
    db.session.commit()
  

    flash('Delivery Charge Updated')

    return redirect(url_for('main.delivery_charges'))
  
  if request.method == "POST" and weight_update_form.submit5.data and weight_update_form.validate_on_submit():

    # print("update form")
    update_form_data = dict()

    for items in weight_update_form:
      update_form_data[items.id] = items.data

    element = WeightDeliveryCharge.query.get_or_404(update_form_data["charge_id"])
    
    element.start_weight = update_form_data.get('start_weight', element.start_weight)
    element.end_weight = update_form_data.get('end_weight', element.end_weight)
    
    element.amount = update_form_data.get('amount', element.amount)
    
    db.session.add(element)
    db.session.commit()
  

    flash('Delivery Charge Updated')

    return redirect(url_for('main.delivery_charges'))

# address delete form

  if address_delete_form.submit3.data and address_delete_form.validate_on_submit():

    # print("delete called")
    delete_form_data = dict()
    for items in address_delete_form:
      delete_form_data[items.id] = items.data

    element = DeliveryCharge.query.get_or_404(delete_form_data["charge_id"])
    
    try:
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong")
    else:
      flash('Delivery Charge For Address Deleted')

    return redirect(url_for('main.delivery_charges'))

# Weight delete form
  if request.method == "POST" and weight_delete_form.submit6.data and weight_delete_form.validate_on_submit():

    # print("delete called")
    delete_form_data = dict()
    for items in weight_delete_form:
      delete_form_data[items.id] = items.data

    element = WeightDeliveryCharge.query.get_or_404(delete_form_data["charge_id"])
    
    try:
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong")
    else:
      flash('Delivery Charge For Weight Deleted')

    return redirect(url_for('main.delivery_charges'))



  

  return render_template('delivery_charges.html',\
    address_charges = address_charges,\
    address_add_form = address_add_form,\
    address_update_form = address_update_form,\
    address_delete_form = address_delete_form,\
      
    weight_charges = weight_charges,\
    weight_add_form = weight_add_form,\
    weight_update_form = weight_update_form,\
    weight_delete_form = weight_delete_form)





@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

  changeUsernameForm = ChangeUsernameForm()
  changePasswordForm = ChangePasswordForm()


  changeShopDetailForm = ChangeShopDetailForm()

  shop = ShopDetails.query.all()[0]
  
  if changeShopDetailForm.submit3.data and changeShopDetailForm.validate_on_submit():

    changeShopDetailFormData= {}
    for item in changeShopDetailForm:
      changeShopDetailFormData[item.id] = item.data


    shop.shop_name = changeShopDetailFormData.get('shop_name', shop.shop_name)
    shop.shop_email = changeShopDetailFormData.get('shop_email', shop.shop_email)
    shop.contact_phone = changeShopDetailFormData.get('contact_phone', shop.contact_phone)
    shop.details = changeShopDetailFormData.get('details', shop.details)
    shop.address = changeShopDetailFormData.get('address', shop.address)

    db.session.add(shop)
    db.session.commit()
    flash('Your Shop details has been updated.')
    return redirect(url_for('main.settings'))

  else:
    changeShopDetailForm = ChangeShopDetailForm(\
    shop_name = shop.shop_name,shop_email=  shop.shop_email,contact_phone = shop.contact_phone,\
    details = shop.details,address = shop.address)




  if  changeUsernameForm.submit1.data and changeUsernameForm.validate_on_submit():
        if current_user.verify_password(changeUsernameForm.password.data):
            new_username =  changeUsernameForm.username.data.lower()
            current_user.username = new_username
            db.session.add(current_user)
            db.session.commit()
            flash('Your Username has been updated.')
            return redirect(url_for('main.settings'))
        else:
            flash('Invalid  password.')


  if changePasswordForm.submit2.data and changePasswordForm.validate_on_submit():
        if current_user.verify_password(changePasswordForm.old_password.data):
            current_user.password = changePasswordForm.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.settings'))
        else:
            flash('Invalid password.')
  
  

  return render_template('settings.html',\
    changeUsernameForm = changeUsernameForm,\
      changePasswordForm=changePasswordForm,\
      changeShopDetailForm= changeShopDetailForm)
