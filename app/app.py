from flask import Flask, request, abort
from resources_manager import ResourcesManager

app = Flask(__name__)

manager = ResourcesManager(max_amount=20)


@app.route('/', methods=['GET', 'POST'])
def get_resource():
    if request.method == 'GET':
        resource = manager.get_resource()
        if not resource:
            abort(400)
        return resource

    if request.method == 'POST':
        content = request.json
        if not manager.is_busy(content):
            abort(400)
        manager.release_resource(content)
        return content


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7080)
