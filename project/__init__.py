# Flask configuration
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db: SQLAlchemy = SQLAlchemy(app)

# Give access to the aplication context for the database operations
app.app_context().push()

# Important! Keep this at the ends
from project import routes
