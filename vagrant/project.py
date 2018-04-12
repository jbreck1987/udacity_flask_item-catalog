from database_setup import MenuItem, Restaurant, create_db_session
from flask import Flask

# instantiate app as Flask instance
app = Flask(__name__)

@app.route('/test/')
def test():
    return 'app has been instantiated, server is active'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
