import secrets
import os
from sqlalchemy import exc
from config import config
from flask import request, redirect, url_for, session , flash
from flask import render_template, jsonify
from . import main
from .. import db
from .. models import Admin,Product,Unit,ProductType, Stock
from . forms import LoginForm, AddProduct, UpdateProduct, DeleteProduct , AddCategory,UpdateCategory, DeleteCategory

from flask_login import login_required,logout_user, login_user, current_user


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
      element = Product.from_dict(add_form_data)
      db.session.add(element)
      db.session.commit()

      stock = Stock(product_id = element.id,in_stock= add_form_data["stock"])
      db.session.add(stock)
      db.session.commit()
      flash('Product Added')

      return redirect(url_for('main.products'))
    flash('Something went wrong!')


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
      element.product_image = update_form_data.get("product_new_image")
    
    element.product_description = update_form_data.get('product_description', element.product_description)
    
    element.price_per_unit = update_form_data.get('price_per_unit', element.price_per_unit)
    element.unit_id = update_form_data.get('unit_id', element.unit_id)
    element.product_type_id = update_form_data.get('product_type_id', element.product_type_id)

   
    db.session.add(element)
    db.session.commit()
    
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
    
    try:
      db.session.delete(element)
      db.session.commit()
    except exc.SQLAlchemyError as e:
      db.session.rollback()
      flash("Could not delete, Something went wrong","danger")
    else:
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
      
    element = ProductType.from_dict(add_form_data)
    db.session.add(element)
    db.session.commit()

    flash('Category Added')

    return redirect(url_for('main.categories'))

  if update_form.submit2.data and update_form.validate_on_submit():

    # print("update form")
    update_form_data = dict()

    for items in update_form:
      update_form_data[items.id] = items.data

    element = ProductType.query.get_or_404(update_form_data["type_id"])
    
    element.type_name = update_form_data.get('type_name', element.type_name)
    
    db.session.add(element)
    db.session.commit()
  

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

@main.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
  return render_template('orders.html',name = current_user.username)