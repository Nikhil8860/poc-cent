import logging
import json
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    container_name = 'users'
    container = get_db_container(container_name)
    email = req.params.get('email')
    if not email:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            email = req_body.get('email')

    if email:
        item = container.query_items(query=f'select * from users where users.email="{email}"',
                                     enable_cross_partition_query=True)
        all_user_data = [i for i in item]
        if all_user_data:
            users_data = all_user_data[0]
            id_d = users_data["id"]
            patient_id = users_data["patient_id"]
            created_date = users_data["Created_date"]
            first_name = users_data["first_name"]
            middle_name = users_data["middle_name"]
            last_name = users_data["last_name"]
            insurance_carrier_name = users_data["insurance_carrier_name"]
            gender = users_data["gender"]
            member_id = users_data["member_id"]
            dob = users_data["dob"]
            home_zip_code = users_data["home_zip_code"]
            last_visit_date = users_data["last_visit_date"]
            email = users_data["email"]
            old_password = users_data["old_password"]
            is_verified = users_data["is_verified"]
            verified_at = users_data["verified_at"]
            mpin = users_data["MPIN"]
            is_locked = users_data["is_locked"]
            is_tmp_password = users_data["is_tmp_password"]
            last_login_date = users_data["last_login_date"]
            return HttpResponse(json.dumps({"patient_id": patient_id, "center_id": id_d}))
        return HttpResponse("Data not found", status_code=404)
    else:
        return HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
