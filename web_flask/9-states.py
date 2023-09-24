#!/usr/bin/python3
"""A python script that starts a Flask web app and runs the HBNB
storage, check for file and database storage
"""


from flask import Flask, render_template
from models import storage
import models
from models.state import State
from models.city import City
app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    storage.close()


s = sorted(storage.all(State).values(), key=lambda state: state.name)


@app.route('/states', strict_slashes=False)
def states():
    return render_template('9-states.html', states=s)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    stat = None
    for items in s:
        if items.id == id:
            stat = items
    return render_template('9-states.html', state_id=stat)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
