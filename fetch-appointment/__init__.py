import json
import logging
import math
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container
from utils import get_difference


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    print("------------------------------")
    print(req.params)
    container_name = 'appointments'
    container = get_db_container(container_name)
    patient_id = req.params.get('patient_id')
    appointment_status = req.params.get('appointment_status')
    if not patient_id and not appointment_status:
        return HttpResponse(
            json.dumps({"msg": "patient_id and appointment_status not in request parameters", "status_code": 400}),
            status_code=400,
            mimetype="application/json")
    elif patient_id and appointment_status == 'completed':
        item = container.query_items(query=f'select * from appointments '
                                           f'where appointments.patient_id="{patient_id}" and '
                                           f'appointments.appointment_status="completed"',
                                     enable_cross_partition_query=True)
    elif patient_id and appointment_status == 'pending':
        item = container.query_items(query=f'select * from appointments '
                                           f'where appointments.patient_id="{patient_id}" and '
                                           f'appointments.appointment_status="pending"',
                                     enable_cross_partition_query=True)
    elif patient_id and appointment_status == 'cancelled':
        item = container.query_items(query=f'select * from appointments '
                                           f'where appointments.patient_id="{patient_id}" and '
                                           f'appointments.appointment_status="cancelled"',
                                     enable_cross_partition_query=True)
    else:
        item = container.query_items(query=f'select * from appointments '
                                           f'where appointments.patient_id="{patient_id}"',
                                     enable_cross_partition_query=True)

    data = [i for i in item]
    sorted_data = sorted(data, key=lambda d: d['appointment_date'])
    # merging the appointment_date and appointment_time for getting the hours difference
    [i.update({'hours_diff': math.ceil(get_difference(i.get("appointment_date") + ' ' + i.get('appointment_time')))})
     for i in sorted_data]
    # getting latest 3 records based on date
    if not appointment_status:
        sorted_data = [i for i in sorted_data if i.get('hours_diff') >= 0][:3]
    else:
        sorted_data = [i for i in sorted_data]
    if len(data):
        return HttpResponse(json.dumps(sorted_data), status_code=200, mimetype="application/json", )
    return HttpResponse(
        json.dumps({"msg": "Data does not exists", "status_code": 400}),
        status_code=400,
        mimetype="application/json")
