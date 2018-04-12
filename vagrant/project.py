from database_setup import MenuItem, Restaurant, create_db_session
from flask import Flask, request

# instantiate app as Flask instance
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def list_restaurants():
    return 'This is the GET response from list_restaurants!'

@app.route('/restaurant/add_restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        return 'This is the POST response from add_restaurant!'
    return 'This is the GET response from add_restaurant!'

def edit_restaurant():
    pass

def delete_restaurant():
    pass

def list_menu_items():
    pass

def add_menu_item():
    pass

def edit_menu_item():
    pass

def delete_menu_item():
    pass



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
