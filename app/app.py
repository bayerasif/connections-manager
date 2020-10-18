from flask import Flask, request
from resources_generator import ResourcesGenerator
app = Flask(__name__)

generator = ResourcesGenerator(max_amount=20)


@app.route('/', methods=['GET'])
def get_resource():
    resource = generator.get_resource()
    if not resource:
        return 'No More Resources'
    return resource


@app.route('/', methods=['POST'])
def post_resource():
    content = request.json
    generator.release_resource(content)
    return 'GOOD'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7080)
