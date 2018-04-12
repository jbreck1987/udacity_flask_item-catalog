from database_setup import MenuItem, Restaurant, create_db_session
from flask import Flask, request

# instantiate app as Flask instance
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def list_restaurants():
    return 'This is the GET response from list_restaurants!'


@app.route('/restaurant/add_restaurant/',
           methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        return 'This is the POST response from add_restaurant!'
    return 'This is the GET response from add_restaurant!'


@app.route('/restaurant/<int:restaurant_id>/edit_restaurant/',
           methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    if request.method == 'POST':
        return '''This is the POST response from
                 edit_restaurant for ID {}!'''.format(restaurant_id)
    return '''This is the GET response from
              edit_restaurant for ID {}!'''.format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete_restaurant/',
           methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    if request.method == 'POST':
        return '''This is the POST response from
                 delete_restaurant for ID {}!'''.format(restaurant_id)
    return '''This is the GET response from
              delete_restaurant for ID {}!'''.format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/list_menu/')
def list_menu_items(restaurant_id):
    return '''This is the GET response from
              list_menu_items for ID {}!'''.format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/add_item/',
           methods=['GET', 'POST'])
def add_menu_item(restaurant_id):
    if request.method == 'POST':
        return '''This is the POST response from
                 add_menu_item for ID {}!'''.format(restaurant_id)
    return '''This is the GET response from
              add_menu_item for ID {}!'''.format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/delete_item',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, item_id):
    if request.method == 'POST':
        return '''This is the POST response from
                 edit_menu_item for rest ID {} and item ID {}!
                 '''.format(restaurant_id, item_id)
    return '''This is the GET response from
              edit_menu_item for rest ID {}! and
              item ID {}'''.format(restaurant_id, item_id)


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/delete_item',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, item_id):
    if request.method == 'POST':
        return '''This is the POST response from
                 delete_menu_item for rest ID {} and item ID {}!
                 '''.format(restaurant_id, item_id)
    return '''This is the GET response from
              delete_menu_item for rest ID {}! and
              item ID {}'''.format(restaurant_id, item_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
