from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class ItemList(Resource):
    def get(self):
        return {'items': ['item1', 'item2']}

api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)