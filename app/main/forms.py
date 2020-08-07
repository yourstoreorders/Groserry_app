from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, SubmitField, PasswordField, IntegerField,FloatField, SelectField,HiddenField
from wtforms.validators import Required, DataRequired, Length, Email

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
  
  unit_id = SelectField('Unit',choices=[(1,'Kilogram'),(2,'Liter')],coerce= int)
  product_type_id = SelectField('Category',choices=[(1,'fruits'),(2,'vegetables')],coerce= int)
  stock = IntegerField('Quantity',validators=[DataRequired()])
  
  submit = SubmitField('Add Product')

class UpdateProduct(FlaskForm):
  product_id = IntegerField('Id',validators=[DataRequired()],render_kw={'readonly':'true'})
  product_name   = StringField('Name', validators=[DataRequired(), Length(1, 64)])
  product_new_image  = FileField('New Picture',validators=[FileAllowed(['png','jpg'])])
  product_description   = StringField('Description', validators=[Length(1, 64)])
  price_per_unit  = FloatField('Price', validators=[DataRequired()])
  
  unit_id = SelectField('Unit',choices=[(1,'Kilogram'),(2,'Liter')],coerce= int)
  product_type_id = SelectField('Category',choices=[(1,'fruits'),(2,'vegetables')],coerce= int)
  stock = IntegerField('Quantity',validators=[DataRequired()])
  
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