from flask import Flask

app = Flask(__name__) # Holds a flask instance
from api import views