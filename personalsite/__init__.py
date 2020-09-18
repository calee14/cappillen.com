# Import Flask for flask app object
from flask import Flask
from config import Config

# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://3fcef6e888f047bd9f52298a7e13b729@o424091.ingest.sentry.io/5355434",
#     integrations=[FlaskIntegration()]
# )

# Create flask app object
app = Flask(__name__)
app.config.from_object(Config)


# Import all views
import personalsite.views