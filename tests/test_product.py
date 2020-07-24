import unittest
from app import create_app, db
from app.models import Product,Unit, ProductType

class ProductTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  def test_insert_Units(self):
    unit = Unit(unit_name="Kilogram",unit_short="kg")
    db.session.add(unit)
    db.session.commit()
    self.assertTrue(Unit.query.filter_by(unit_name="Kilogram").first() == unit)

  def test_insert_product_type(self):
    pt = ProductType(
      type_name="Pulses"
      )
    db.session.add(pt)
    db.session.commit()
    self.assertTrue(ProductType.query.filter_by(type_name="Pulses").first() == pt)
  
  def test_insert_product(self):
    pt = ProductType(
      type_name="Pulses"
      )
    
    unit = Unit(unit_name="Kilogram",unit_short="kg")

    db.session.add(pt)
    db.session.add(unit)
    db.session.commit()

    unit = Unit.query.filter_by(unit_name="Kilogram").first()
    producttype = ProductType.query.filter_by(type_name="Pulses").first()
    p = Product(
      product_name = "rice",
      product_description = "basmatic rice",
      price_per_unit = 123,
      product_items =  producttype,
      unit_items = unit,
      )
    db.session.add(p)
    db.session.commit()
    self.assertTrue(Product.query.filter_by(product_name="rice").first() == p)


