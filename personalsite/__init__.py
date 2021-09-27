# Import Flask for flask app object
from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager

# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://3fcef6e888f047bd9f52298a7e13b729@o424091.ingest.sentry.io/5355434",
#     integrations=[FlaskIntegration()]
# )

# Create flask app object
app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/auth'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
app.config.from_object(Config)
jwt = JWTManager(app)


# Import all views
import personalsite.views