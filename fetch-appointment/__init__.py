import json
import logging

from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    container_name = 'appointments'
    container = get_db_container(container_name)
    patient_id = req.params.get('patient_id')
    if not patient_id:
        return HttpResponse("patient_id not in request parameters", status_code=400)
    item = container.query_items(query=f'select * from appointments '
                                       f'where appointments.patient_id="{patient_id}" and '
                                       f'appointments.appointment_status="completed"',
                                 enable_cross_partition_query=True)

    data = [i for i in item]
    # getting latest 3 records based on date
    sorted_data = sorted(data, key=lambda d: d['appointment_date'])[:2]
    if len(data):
        return HttpResponse(json.dumps(sorted_data), status_code=200, mimetype="application/json",)
    return HttpResponse("Data does not exists!!", status_code=400)
