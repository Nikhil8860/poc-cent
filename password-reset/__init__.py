import logging

from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    input_json = req.get_json()

    container_name = 'users'
    container = get_db_container(container_name)
    item = container.query_items(query=f'select * from users where users.email="{input_json["email"]}"',
                                 enable_cross_partition_query=True)
    all_user_data = [i for i in item]
    if len(all_user_data):
        old_input_data = all_user_data[0]
        old_password = old_input_data.get("old_password")
        if old_password != input_json['password']:
            old_input_data['old_password'] = input_json['password']
            container.upsert_item(body=old_input_data)
            return HttpResponse("password updated successfully. Please login!!", status_code=201)
        return HttpResponse("Please user new password which is not in your last 3 password", status_code=400)
    return HttpResponse("user details does not exists!!", status_code=400)
