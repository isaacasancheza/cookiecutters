from chalice import Chalice


app = Chalice(app_name='{{ cookiecutter.app_name }}')


@app.route('/', methods=['GET'])
def index():
    return {}
