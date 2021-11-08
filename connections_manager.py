from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from threading import Lock
import string
import random
import os.path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources_pool.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
lock = Lock()


class Resource(db.Model):
    """
    The resource model as represented in the database.
    """
    ip = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    busy = db.Column(db.Boolean, nullable=False)

    def get_dict(self):
        return {'ip': self.ip, 'username': self.username, 'password': self.password}


@app.route('/', methods=['GET', 'POST'])
def get_resource():
    """
    Handles the requests for resources.
    :return: On successful GET request returns the resource as json in the defined format.
    On successful POST request returns the released resource ip in json (the same that was received).
    On failure, if full or invalid request returns '400 Bad Request' HTTP response.
    """
    if request.method == 'GET':
        # Locks to avoid delivering same resource for different requests.
        with lock:
            free_resource = db.session.query(Resource).filter_by(busy=False).first()
            if not free_resource:
                # There are no free resources.
                abort(400)
            free_resource.busy = True
            db.session.commit()
        resource = free_resource.get_dict()
        resource['debug'] = True
        return resource

    if request.method == 'POST':
        content = request.json
        # Checks if the body consists of only 'ip' field as defined.
        if not content or ['ip'] != list(content.keys()):
            abort(400)
        resource_to_release = db.session.query(Resource).filter_by(ip=content['ip']).first()
        if not resource_to_release or not resource_to_release.busy:
            abort(400)
        resource_to_release.busy = False
        db.session.commit()
        return content


def generate_resources(amount: int) -> None:
    """
    Initializes the database and generates the requested amount of random resources.
    Assumes that the database is not existing yet.
    :param amount: The amount of resources.
    """
    db.create_all()
    for num in range(amount):
        resource = Resource(
            ip='127.0.5.{}'.format(num),
            username='user{}'.format(num),
            password=''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            busy=False,
        )
        db.session.add(resource)
    db.session.commit()


if __name__ == '__main__':
    if not os.path.isfile('resources_pool.db'):
        generate_resources(amount=20)
    app.run(debug=True, host='0.0.0.0', port=7080)
