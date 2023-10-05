import logging
import json
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    container_name = 'appointments'
    container = get_db_container(container_name)
    if req.method == 'POST':
        request_body = req.get_json()
        patient_id = request_body.get('patient_id')
        if not patient_id:
            return HttpResponse(json.dumps({"msg": "Error is request Body", "status_code": 400}), status_code=400,
                                mimetype="application/json")
        try:
            container.create_item(request_body)
            return HttpResponse(
                json.dumps({"msg": "Record created successfully in appointment container.", "status_code": 201}),
                status_code=201,
                mimetype="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"msg": "Error while inserting the appointment", "status_code": 400}),
                                status_code=400,
                                mimetype="application/json")
