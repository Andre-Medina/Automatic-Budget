''''
main file used to run the server

-----
'''

# Import Flask and other packages
from flask import Flask, render_template, url_for

# Import modules from modules subdirectory
from modules import *

# Create an instance of Flask class
app = Flask(__name__)

# Define routes and functions for your app
@app.route("/")
def index():
    # Use some_function from utils module
    result_1 = 'hello '
    # Use some_class from models module
    result_2 = ' world'
    some_result = "This is some result"
    some_object = {"name": "This is some object"}
    # Render index.html template with some variables
    return render_template("index.html", result=some_result, object=some_object, result_1=result_1, result_2=result_2, result_3 = result_1 + result_2)

# Run the app if this file is executed as the main script
if __name__ == "__main__":
    app.run()
