from database_setup import MenuItem, Restaurant, session_scope
from flask import Flask, request, render_template, redirect, url_for
from sample_restaurants import restaurants, items, item, restaurant as rest


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
        return 'Rest {}, ID {} was deleted'.format(rest['name'],
                                                   restaurant_id)
    return render_template('delete_restaurant.html',
                           restaurant_id=restaurant_id,
                           name=rest['name'])


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
        return 'New item name {} to Rest {}'.format(request.form['new_name'],
                                                    restaurant_id)
    return render_template('edit_menu_item.html',
                           restaurant_id=restaurant_id,
                           item_id=item_id,
                           name=item['name'])


@app.route('/restaurant/<int:restaurant_id>/<int:item_id>/delete_item',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, item_id):
    if request.method == 'POST':
        return '{} from Rest ID {} was deleted'.format(item['name'],
                                                       restaurant_id)
    return render_template('delete_item.html',
                           restaurant_id=restaurant_id,
                           item_id=item_id,
                           name=item['name'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
