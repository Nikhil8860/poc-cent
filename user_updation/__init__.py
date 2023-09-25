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
            return HttpResponse("You have not provided patient_id in the request body", status_code=400)
        container = get_db_container(container_name)
        item = container.query_items(query=f'select * from users where users.email="{input_json["email"]}"',
                                     enable_cross_partition_query=True)
        all_user_data = [i for i in item]
        if len(all_user_data):
            return HttpResponse("User already Exists!!", status_code=400)
        try:
            response = container.create_item(body=input_json)
            if response:
                logging.info("User details updated!!!")
                return HttpResponse("records inserted!!", status_code=200)
        except exceptions.CosmosHttpResponseError:
            return HttpResponse(f"Error occured when creating item with item{input_json['id']}", status_code=400)
        return HttpResponse("user created", status_code=201)
    return HttpResponse("Invalid HTTP method it should be POST", status_code=400)
