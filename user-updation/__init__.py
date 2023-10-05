import logging
import json
from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import exceptions
from get_db_object import get_db_container
from secure_password import encrypt_pwd, decrypt_pwd
from cryptography.fernet import Fernet


def main(req: HttpRequest) -> HttpResponse:
    logging.info('HTTP trigger function processed a request.')
    container_name = 'users'
    if req.method == 'POST':
        input_json = req.get_json()
        key = Fernet.generate_key()
        fernet = Fernet(key)
        old_password = str(input_json.get('old_password'))
        encrypted_pwd = encrypt_pwd(old_password, fernet)
        input_json['old_password'] = encrypted_pwd.decode()
        decrypted_pwd = decrypt_pwd(input_json['old_password'], fernet)  # Decode password
        if not input_json.get("patient_id"):
            return HttpResponse(json.dumps({"msg": "Error is request Body", "status_code": 400}), status_code=400,
                                mimetype="application/json")
        container = get_db_container(container_name)
        item = container.query_items(query=f'select * from users where users.email="{input_json["email"]}"',
                                     enable_cross_partition_query=True)
        all_user_data = [i for i in item]
        if len(all_user_data):
            container.upsert_item(body=input_json)
            return HttpResponse(json.dumps({"msg": "User updated", "status_code": 200}), status_code=200,
                                mimetype="application/json")
        try:
            response = container.create_item(body=input_json)
            if response:
                logging.info("User details updated!!!")
                return HttpResponse(json.dumps({"msg": "record inserted", "status_code": 200}), status_code=200,
                                    mimetype="application/json")
        except exceptions.CosmosHttpResponseError:
            return HttpResponse(json.dumps(
                {"msg": f"Error occur when creating item with item{input_json['id']}", "status_code": 400}),
                                status_code=400,
                                mimetype="application/json")
        return HttpResponse(json.dumps({"msg": "user created", "status_code": 201}), status_code=201,
                            mimetype="application/json")
    return HttpResponse(json.dumps({"msg": "Method should be POST", "status_code": 400}), status_code=400,
                        mimetype="application/json")
