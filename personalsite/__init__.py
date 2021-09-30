# Import Flask for flask app object
from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager

# Create flask app object
app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
jwt = JWTManager(app)

# Import all views
import personalsite.views