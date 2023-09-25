import logging
import json
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container
from datetime import datetime


def main(req: HttpRequest) -> HttpResponse:
    logging.info('User verification trigger function processed a request.')
    container_name = 'users'
    container = get_db_container(container_name)
    if req.method == 'POST':
        req_body = req.get_json()
        checked_fields = ['first_name', 'last_name', 'insurance_carrier_name', 'member_id', 'dob', 'gender']
        if not all(key in req_body for key in checked_fields):
            return HttpResponse("Error is request body", status_code=400)
        email = req_body.get('email')

        if email:
            item = container.query_items(query=f'select * from users where users.email="{email}"',
                                         enable_cross_partition_query=True)
            all_user_data = [i for i in item]
            if all_user_data:
                users_data = all_user_data[0]
                is_verified = users_data["is_verified"]
                if is_verified == 'true':
                    return HttpResponse("User is already verified", status_code=400)
                current_datetime = datetime.now()
                current_date_time = current_datetime.strftime("%m/%d/%Y")
                users_data['is_verified'] = 'true'
                users_data['verified_at'] = current_date_time
                patient_id = users_data["patient_id"]
                print(users_data)
                res = container.upsert_item(body=users_data)
                print(res)
                return HttpResponse(json.dumps({"patient_id": patient_id, "center_id": "id_d"}))
            return HttpResponse("Data not found", status_code=404)
        else:
            return HttpResponse(
                "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
                status_code=200
            )
    else:
        return HttpResponse("Method should be POST", status_code=400)