from flask import Flask

# Create the Flask app object
app = Flask(__name__)

# Import routes after the app object is created to avoid circular imports
from . import routes  # This import should be at the bottom after app creation
