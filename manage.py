#!/usr/bin/env python
import os

from app import create_app, db
from app.models import Product, Unit,\
  ProductType, Admin, Stock , StatusCatalog, DeliveryCharge , ShopDetails

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db,Admin=Admin ,Product=Product, Unit=Unit,ProductType=ProductType, Stock = Stock, StatusCatalog = StatusCatalog)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
  """Run deployment tasks."""
  from flask_migrate import upgrade

  # migrate database to latest revision
  upgrade()
  # create all tables
  db.create_all()

  # insert default values
  ShopDetails.insert_shop_details()
  Admin.insert_default_admin()
  StatusCatalog.insert_order_status()
  Unit.insert_units()
  DeliveryCharge.insert_default_charge()
  ProductType.insert_categories()




@manager.command
def test():
  """Run the unit tests."""
  import unittest
  tests = unittest.TestLoader().discover('tests')
  
  unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()