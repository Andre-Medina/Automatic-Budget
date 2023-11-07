''''
main file used to run the server

-----
'''

# Import Flask and other packages
from flask import Flask, render_template, jsonify, request
import json
from markupsafe import Markup

ROOT_DIR = ""

# Import modules from modules subdirectory
import modules as md




statements = md.statements.Statements()

# Create an instance of Flask class
app = Flask(__name__)


# moves files around
md.move_statements()


#  ██ ███    ██ ██████  ███████ ██   ██ 
#  ██ ████   ██ ██   ██ ██       ██ ██  
#  ██ ██ ██  ██ ██   ██ █████     ███   
#  ██ ██  ██ ██ ██   ██ ██       ██ ██  
#  ██ ██   ████ ██████  ███████ ██   ██ 
#  
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

#  ██████   █████  ████████  █████  
#  ██   ██ ██   ██    ██    ██   ██ 
#  ██   ██ ███████    ██    ███████ 
#  ██   ██ ██   ██    ██    ██   ██ 
#  ██████  ██   ██    ██    ██   ██ 
#  
@app.route("/data/<data_type>/<extra>", methods=['GET','POST'])
def get_data(data_type, extra):
    response_object = {
        "Content-Type": "application/json",
        "data": [],
        "message": "",
        }
    

    #  █▀▀ █▀▀ ▀█▀ 
    #  █▄█ ██▄  █  
    #  
    if request.method == "GET":

        #  █   █▀▀ █ █ █▀▀ █   
        #  █▄▄ ██▄ ▀▄▀ ██▄ █▄▄ 
        #  
        if data_type == "level":
            if extra == "1":
                response_object['data'] =  md.json_read(ROOT_DIR + md.CLASSIFICATION_JSON_DIR_LVL_1)
                response_object["message"] = 'success'
                response_object['status'] = 200

            elif extra == "2":
                response_object['data'] = md.json_read(ROOT_DIR + md.CLASSIFICATION_JSON_DIR_LVL_2)
                response_object["message"] = 'success'
                response_object['status'] = 200

            elif extra == "3":
                response_object['data'] = md.json_read(ROOT_DIR + md.CLASSIFICATION_JSON_DIR_LVL_3)
                response_object["message"] = 'success'
                response_object['status'] = 200


        #  █▀ ▀█▀ ▄▀█ ▀█▀ █▀▀ █▀▄▀█ █▀▀ █▄ █ ▀█▀ 
        #  ▄█  █  █▀█  █  ██▄ █ ▀ █ ██▄ █ ▀█  █  
        #  
        elif data_type == "statement":
            extra
            transaction = request.args.get('transaction', default = 0, type = int)
            transaction_new = True if request.args.get('new') == '1' else False

            print(f'finding transaction: {transaction}, looking for new: {transaction_new}')
            # if looking for a new transaction
            if transaction_new:
                result = statements.get_transaction_new(extra, transaction)

            # otherwise old method
            else:
                result = statements.get_transaction(extra, transaction)

            # extracting results
            (
                response_object['data'],
                response_object["message"],
                response_object['status'],
            ) = result



        #  █▀▀ █▀█ █▄ █ █▀▀ █ █▀▀ 
        #  █▄▄ █▄█ █ ▀█ █▀  █ █▄█ 
        #  
        elif data_type == "config" and extra == "statment_accounts":
            response_object['data'] = md.COMMON_STATEMENT_ACCOUNTS
            response_object["message"] = 'success'
            response_object['status'] = 200
            
        elif data_type == "config" and extra == "all_accounts":
            response_object['data'] = md.ALL_ACCOUNT_LIKE
            response_object["message"] = 'success'
            response_object['status'] = 200
            
        elif data_type == "config" and extra == "movement_types":
            response_object['data'] = md.MOVEMENT_TYPES
            response_object["message"] = 'success'
            response_object['status'] = 200


        else:
            response_object["message"] = 'page not found'
            response_object['status'] = 400


    #  █▀█ █▀█ █▀ ▀█▀ 
    #  █▀▀ █▄█ ▄█  █  
    #  dont need to post data, only code and message
    elif request.method == "POST":
        if data_type == "statement":
            response_object['message'], response_object['status'] = statements.post_transaction(json.loads(request.data.decode()))

        else:
            response_object['message'] = "page not found"
            response_object['status'] = 404
        
    else:
        response_object['message'] = "please use get"
        response_object['status'] = 400
    
    print('---Returning data----')
    print(response_object)
    print('---------------------')
    return jsonify(response_object), f"{response_object['status']} {response_object['message']}"





#  ███████ ████████  █████  ██████  ████████ 
#  ██         ██    ██   ██ ██   ██    ██    
#  ███████    ██    ███████ ██████     ██    
#       ██    ██    ██   ██ ██   ██    ██    
#  ███████    ██    ██   ██ ██   ██    ██    
#  
# Run the app if this file is executed as the main script
if __name__ == "__main__":
    print('starting')
    # hosts local LAN
    # app.run(host="0.0.0.0", port=5000)
    app.run()
    