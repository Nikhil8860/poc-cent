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
        checked_fields = ['first_name', 'last_name', 'insurance_carrier_name', 'member_id', 'dob', 'gender',
                          'home_zip_code', 'state']
        if not all(key in req_body for key in checked_fields):
            return HttpResponse(json.dumps({"msg": "Error is request Body", "status_code": 400}), status_code=400,
                                mimetype="application/json")
        member_id = req_body.get('member_id')

        if member_id:
            item = container.query_items(query=f'select * from users where users.member_id="{member_id}"',
                                         enable_cross_partition_query=True)
            all_user_data = [i for i in item]
            if all_user_data:
                users_data = all_user_data[0]
                is_verified = users_data["is_verified"]
                if is_verified == 'true':
                    return HttpResponse(json.dumps({"msg": "User Already Verified", "status_code": 200}),
                                        status_code=200, mimetype="application/json")
                current_datetime = datetime.now()
                current_date_time = current_datetime.strftime("%m/%d/%Y")
                users_data['is_verified'] = 'true'
                users_data['verified_at'] = current_date_time
                patient_id = users_data["patient_id"]
                res = container.upsert_item(body=users_data)
                return HttpResponse(
                    json.dumps({"msg": "Verification is successful, click 'continue' to complete Sign-up.",
                                "patient_id": patient_id, "center_id": 123, "status_code": 200}),
                    status_code=200, mimetype="application/json")
            return HttpResponse(json.dumps({"msg": "Data not Found", "status_code": 404}), status_code=404,
                                mimetype="application/json")

    else:
        return HttpResponse(json.dumps({"msg": "Method should be POST", "status_code": 400}), status_code=400,
                            mimetype="application/json")
