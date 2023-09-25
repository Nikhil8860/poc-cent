import logging
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
            return HttpResponse("You have not provided patient_id in request body", status_code=400)
        try:
            container.create_item(request_body)
            return HttpResponse("Record created successfully in appointment container.", status_code=200)

        except Exception as e:
            return HttpResponse("Error while inserting the appointment", status_code=400)
