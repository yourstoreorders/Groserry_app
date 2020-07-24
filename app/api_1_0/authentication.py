from flask import g, jsonify,request
from flask_httpauth import HTTPBasicAuth
from ..models import Admin
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    if username_or_token == '':
        return False
    if password == '':
        g.current_user = Admin.verify_auth_token(username_or_token)
        g.token_used = True
        print("token used")
        return g.current_user is not None
    user = Admin.query.filter_by(username=username_or_token.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    
    return user.verify_password(password)

@auth.error_handler
def auth_error(status):
  print(status)
  return unauthorized('Access Denied : Invalid credentials')



@api.route('/tokens/', methods=['POST'])
@auth.login_required
def get_token():
    if g.current_user == None or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})