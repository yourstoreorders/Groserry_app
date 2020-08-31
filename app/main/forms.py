from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, SubmitField, PasswordField, IntegerField,FloatField, SelectField,HiddenField
from wtforms.validators import Required, DataRequired, Length, Email,EqualTo

class LoginForm(FlaskForm):
  username   = StringField('Username', validators=[DataRequired(), Length(1, 64)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Log In')



# Product Forms
class AddProduct(FlaskForm):
  product_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)])
  product_image  = FileField('Picture',validators=[FileAllowed(['png','jpg','jpeg'])])
  product_description   = StringField('Description', validators=[Length(1, 64)])
  price_per_unit  = FloatField('Price', validators=[DataRequired()])
  product_weight = IntegerField('Weight', default = 0, validators=[DataRequired()])
  
  unit_id = SelectField('Unit',choices=[(1,'Kilogram'),(2,'Liter')],coerce= int)
  product_type_id = SelectField('Category',choices=[(1,'fruits'),(2,'vegetables')],coerce= int)
  stock = IntegerField('Stock',validators=[DataRequired()])
  
  submit = SubmitField('Add Product')

class UpdateProduct(FlaskForm):
  product_id = IntegerField('Id',validators=[DataRequired()],render_kw={'readonly':'true'})
  product_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)])
  product_new_image  = FileField('New Picture',validators=[FileAllowed(['png','jpg'])])
  product_description   = StringField('Description', validators=[Length(1, 64)])
  price_per_unit  = FloatField('Price', validators=[DataRequired()])
  product_weight = IntegerField('Weight', validators=[DataRequired()])
  
  unit_id = SelectField('Unit',choices=[(1,'Kilogram'),(2,'Liter')],coerce= int)
  product_type_id = SelectField('Category',choices=[(1,'fruits'),(2,'vegetables')],coerce= int)
  stock = IntegerField('Stock',validators=[DataRequired()])
  
  submit = SubmitField('Update Product')

class DeleteProduct(FlaskForm):
  # id = HiddenField("sadasd")
  product_id = HiddenField('Id',validators=[DataRequired()], render_kw={'readonly':'true'})
  product_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)],render_kw={'readonly':'true'})
  
  submit = SubmitField('Delete Product')




# Category Forms
class AddCategory(FlaskForm):
  type_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)])
  submit1 = SubmitField('Add Category')

class UpdateCategory(FlaskForm):
  type_id = IntegerField('Id',validators=[DataRequired()],render_kw={'readonly':'true'})
  type_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)])
  
  submit2 = SubmitField('Update Category')

class DeleteCategory(FlaskForm):
  type_id = HiddenField('Id',validators=[DataRequired()], render_kw={'readonly':'true'})
  type_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)],render_kw={'readonly':'true'})
  
  submit3 = SubmitField('Delete Category')



# Order Forms

class UpdateOrder(FlaskForm):
  order_id = IntegerField('Id',validators=[DataRequired()], render_kw={'readonly':'true'})
  order_status = SelectField('Status',choices=[],coerce= int)

  submit2 = SubmitField('Update Order')

class DeleteOrder(FlaskForm):
  order_id = IntegerField('Id',validators=[DataRequired()], render_kw={'readonly':'true'})
  order_from = StringField('Name', validators=[DataRequired(), Length(1, 64)],render_kw={'readonly':'true'})
  
  submit3 = SubmitField('Delete Order')



  # Charge Forms
class AddCharge(FlaskForm):
  address_pin   = StringField('PIN', validators=[DataRequired(), Length(6, 6)])
  amount   = FloatField('Amount', validators=[DataRequired()])
  submit1 = SubmitField('Add Delivery Charge')

class UpdateCharge(FlaskForm):
  charge_id = IntegerField('Id',validators=[DataRequired()],render_kw={'readonly':'true'})
  address_pin   = StringField('PIN', validators=[DataRequired(), Length(6, 6)])
  amount   = FloatField('Amount', validators=[DataRequired()])
  
  submit2 = SubmitField('Update Delivery Charge')

class DeleteCharge(FlaskForm):
  charge_id = HiddenField('Id',validators=[DataRequired()], render_kw={'readonly':'true'})
  address_pin   = StringField('PIN', validators=[DataRequired(), Length(6, 6)],render_kw={'readonly':'true'})
  amount   = FloatField('Amount', validators=[DataRequired()],render_kw={'readonly':'true'})
  
  submit3 = SubmitField('Delete Delivery Charge')


#Setting Forms
class ChangeUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(5, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit1 = SubmitField('Update Username')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit2 = SubmitField('Update Password')


class ChangeShopDetailForm(FlaskForm):
  shop_name =  StringField('New Name', validators=[DataRequired(), Length(5, 64)])
  shop_email = StringField('Shop Email', validators=[DataRequired(), Length(1, 64),Email()])
  contact_phone = StringField('Phone', validators=[DataRequired(), Length(10,10)])
  details = StringField('Details', validators=[DataRequired(), Length(0,64)])
  address = StringField('Address', validators=[DataRequired(), Length(0,255)])
  
  submit3 = SubmitField('Update Shop Details')
