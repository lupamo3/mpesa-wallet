# standard python imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from app.models.item import ItemModel
from app.util.logz import create_logger
import requests
import os
import json


class Item(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('price', type=float, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True,
                        help='Must enter the store id')

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        self.logger.info(f'returning item: {item.json()}')
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        self.logger.info(f'parsed args: {Item.parser.parse_args()}')

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(
                name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'], data['account_number'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

            return {'message': 'item has been deleted'}

    @jwt_required()
    def put(self, name):
        # Create or Update
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['account_number'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {
            'items': [item.json() for item in ItemModel.query.all()]}  # More pythonic
        ##return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #Alternate Lambda way

    def post(self):
        # consumer_key = "aQGAuq8eK4ZGE6gjRaKAenyUbAcCHm5n"
        # consumer_secret = "dstGxFop99StU988"
        # basic_auth = "YVFHQXVxOGVLNFpHRTZnalJhS0FlbnlVYkFjQ0htNW46ZHN0R3hGb3A5OVN0VTk4OA=="
        try:
            MPESA_AUTHORIZATION = os.getenv("MPESA_AUTHORIZATION")
            url = os.getenv("MPESA_SANDBOX_URL")
            headers = {
                'Authorization': 'Basic {}'.format(MPESA_AUTHORIZATION)
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            access_token = data["access_token"]
            return access_token
        except Exception as e:
            self.logger.error(f'error: {e}')
            return jsonify({"message": "Something went wrong"}), 400

            
class Mpesa(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        try:
            url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v2/simulate"

            payload = json.dumps({
            "ShortCode": "174379",
            "CommandID": "CustomerPayBillOnline",
            "Amount": "20",
            "Msisdn": "254708374149",
            "BillRefNumber": "leta"
            })
            headers = {
            'Authorization': 'Bearer Fc3d3s6WuWLzUxZA0SALK1PXvHnI',
            'Content-Type': 'application/json',
            'Cookie': 'incap_ses_1018_2742146=HpHAXw7zryv+VZFkjaogDrj/X2MAAAAAdwqR0GAQ5tSSizj+2kVkQA==; visid_incap_2742146=JKOitNnwRreQNa4gz+z5PDjxX2MAAAAAQUIPAAAAAAA4g/eIoKbEXPwsBpFd78bK'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            return response
        except Exception as e:
            self.logger.error(f'error: {e}')
            return jsonify({"message": "Something went wrong"}), 400

    def get(self):
        


