from database_setup import MenuItem, Restaurant, create_db_session
from flask import Flask, request, render_template, redirect, url_for
from sample_restaurants import restaurants, items, item, restaurant as rest


# instantiate app as Flask instance
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def list_restaurants():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/add_restaurant/',
           methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        return 'Added restaurant {}'.format(request.form['new_restaurant'])
    return render_template('add_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit_restaurant/',
           methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    if request.method == 'POST':
        return 'New name {} to Rest ID {}'.format(request.form['new_name'],
                                                  restaurant_id)
    return render_template('edit_restaurant.html',
                           restaurant_id=restaurant_id,
                           name=rest['name'])


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
    return render_template('list_menu.html', items=items, restaurant='TEST')


@app.route('/restaurant/<int:restaurant_id>/add_item/',
           methods=['GET', 'POST'])
def add_menu_item(restaurant_id):
    if request.method == 'POST':
        return 'Add item {} to Rest {}'.format(request.form['new_item'],
                                               restaurant_id)
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
