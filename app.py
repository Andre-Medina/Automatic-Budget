''''
main file used to run the server

-----
'''

# Import Flask and other packages
from flask import Flask, render_template, jsonify, request
from markupsafe import Markup

ROOT_DIR = ""

# Import modules from modules subdirectory
import modules as md


statements = md.statements.Statements()

# Create an instance of Flask class
app = Flask(__name__)

# Define routes and functions for your app
@app.route("/")
def index():
    print('routing')
    # Use some_function from utils module
    result_1 = 'hello '
    # Use some_class from models module
    result_2 = ' world'
    some_result = "This is some result"
    some_object = {"name": "This is some object"}
    # Render index.html template with some variables
    return render_template(
        "index.html", 
        result = some_result, 
        object = some_object, 
        result_1 = result_1, 
        result_2 = result_2, 
        result_3 = result_1 + result_2,
        )





@app.route("/elements")
def elements():
    return render_template(
        'elements.html'
    )

@app.route("/test")
def test():
    return render_template(
        'test.html'
    )

@app.route("/data/<data_type>/<extra>", methods=['GET'])
def get_data(data_type, extra):
    response_object = {'status': 'success'}
    if request.method == "GET":
        
        if data_type == "level":
            if extra == "1":
                response_object['data'] =  md.json_read(ROOT_DIR + md.CLASSIFICATION_JSON_DIR_LVL_1)

            elif extra == "2":
                response_object['data'] = md.json_read(ROOT_DIR + md.CLASSIFICATION_JSON_DIR_LVL_2)

        elif data_type == "statement":
            extra
            transaction = request.args.get('transaction', default = 0, type = int)
            response_object['data'] = statements.get_transaction(extra, transaction)

        else:
            response_object['data'] = "page not found"

    else:
        response_object['data'] = "please use get"
    
    return jsonify(response_object)





# Run the app if this file is executed as the main script
if __name__ == "__main__":
    print('starting')
    # hosts local LAN
    # app.run(host="0.0.0.0", port=5000)
    app.run()
    