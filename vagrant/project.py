from database_setup import MenuItem, Restaurant, session_scope
from flask import (Flask, request, render_template, redirect, url_for,
jsonify)


# instantiate app as Flask instance
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def list_restaurants():
    with session_scope() as session:
        rest_list = session.query(Restaurant).all()
        return render_template('restaurants.html', restaurants=rest_list)


@app.route('/restaurant/add_restaurant/',
           methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        if request.form['new_restaurant']:
            # Open new session and add new instance of restaurant
            # using the value returned in POST request
            with session_scope() as session:
                new_rest = Restaurant(name=request.form['new_restaurant'])
                session.add(new_rest)
            return redirect(url_for('list_restaurants'))
    return render_template('add_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit_restaurant/',
           methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    if request.method == 'POST':
        if request.form['new_name']:
            # UPDATE the restaurant name using the value
            # returned in POST request.
            with session_scope() as session:
                session.query(Restaurant).\
                        filter_by(Id=restaurant_id).\
                        update({Restaurant.name: request.form['new_name']},
                               synchronize_session=False)
            return redirect(url_for('list_restaurants'))

    # Get name of Restaurant for placeholder attribute
    # and return form
    with session_scope() as session:
        rest_name = session.query(Restaurant.name).\
                            filter_by(Id=restaurant_id).one()
        return render_template('edit_restaurant.html',
                               restaurant_id=restaurant_id,
                               name=rest_name[0])


@app.route('/restaurant/<int:restaurant_id>/delete_restaurant/',
           methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    if request.method == 'POST':
        # Delete restaurant based on ID that was passed in
        # and send back to restaurant list
        # *****TO-DO****** - ADD FLASH MESSAGE FOR CONFIRMATION
            with session_scope() as session:
                session.query(Restaurant).\
                        filter_by(Id=restaurant_id).\
                        delete(synchronize_session=False)
            return redirect(url_for('list_restaurants'))

    # Get name of Restaurant for placeholder attribute
    # and return form
    with session_scope() as session:
        rest_name = session.query(Restaurant.name).\
                            filter_by(Id=restaurant_id).one()
        return render_template('delete_restaurant.html',
                               restaurant_id=restaurant_id,
                               name=rest_name[0])


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/list_menu/')
def list_menu_items(restaurant_id):
        with session_scope() as session:
            rest_name = session.query(Restaurant.name).\
                                filter_by(Id=restaurant_id).one()
            menu_list = session.query(MenuItem).\
                                filter_by(restaurant_id=restaurant_id)
            return render_template('list_menu.html',
                                   items=menu_list,
                                   rest_name=rest_name[0],
                                   restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/add_item/',
           methods=['GET', 'POST'])
def add_menu_item(restaurant_id):
    if request.method == 'POST':
        if request.form['new_item']:
            # Open new session and add new instance of MenuItem
            # using the value returned in POST request
            with session_scope() as session:
                new_item = MenuItem(name=request.form['new_item'],
                                    restaurant_id=restaurant_id)
                session.add(new_item)
            return redirect(url_for('list_menu_items',
                                    restaurant_id=restaurant_id))
    return render_template('add_menu_item.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/edit_item',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, item_id):
    if request.method == 'POST':
        with session_scope() as session:
            # Loop is to prevent repetitive code to test/query
            # all values that should be updated from the form
            for entry in request.form.keys():
                # If the value for a key is not empty, update it
                # with the value submitted via the form
                if request.form[entry]:
                    session.query(MenuItem).\
                            filter_by(Id=item_id).\
                            update({entry: request.form[entry]},
                                   synchronize_session=False)
        return redirect(url_for('list_menu_items',
                                restaurant_id=restaurant_id))

    # Seperate session context for read-only operation
    with session_scope() as session:
        # Grab menu item object to pass into template
        # for placeholder values
        menu_item = session.query(MenuItem).\
                            filter_by(restaurant_id=restaurant_id,
                                      Id=item_id).one()
        return render_template('edit_menu_item.html',
                               restaurant_id=restaurant_id,
                               menu_item=menu_item)


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/delete_item',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, item_id):
    if request.method == 'POST':
        # Delete menu item based on item ID:restaurant ID pair
        # that was passed in and send back to restaurant list
        # *****TO-DO****** - ADD FLASH MESSAGE FOR CONFIRMATION
            with session_scope() as session:
                session.query(MenuItem).\
                        filter_by(Id=item_id,
                                  restaurant_id=restaurant_id).\
                        delete(synchronize_session=False)
            return redirect(url_for('list_menu_items',
                                    restaurant_id=restaurant_id))

    # Get Item object for placeholder attribute and other fields
    # and return form
    with session_scope() as session:
        menu_item = session.query(MenuItem).\
                            filter_by(Id=item_id,
                                      restaurant_id=restaurant_id).one()
        return render_template('delete_item.html',
                               restaurant_id=restaurant_id,
                               menu_item=menu_item)


@app.route('/restaurants/json/')
def json_list_restaurants():
    with session_scope() as session:
        rest_list = session.query(Restaurant).all()

        json_list = []
        for restaurant in rest_list:
            json_list.append(restaurant.serialize)

        return jsonify(Restaurants=json_list)


@app.route('/restaurant/<int:restaurant_id>/json/')
def json_list_menu(restaurant_id):
    with session_scope() as session:
        restaurant = session.query(Restaurant).\
                            filter_by(Id=restaurant_id).one()
        menu_list = session.query(MenuItem).\
                            filter_by(restaurant_id=restaurant_id)
        json_list = []
        for menu_item in menu_list:
            json_list.append(menu_item.serialize)

        return jsonify(MenuItems=json_list,
                       Restaurant=restaurant.serialize)


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/json/')
def json_list_menu_item(restaurant_id, item_id):
    with session_scope() as session:
        restaurant = session.query(Restaurant).\
                            filter_by(Id=restaurant_id).one()
        menu_item = session.query(MenuItem).\
                            filter_by(restaurant_id=restaurant_id,
                                      Id=item_id).one()

        return jsonify(MenuItem=menu_item.serialize,
                       Restaurant=restaurant.serialize)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
