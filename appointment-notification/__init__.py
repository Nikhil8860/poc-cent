import logging
import json
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container
from utils import get_formatted_date, get_current_date, get_difference
import math


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
    sorted_data = sorted(data, key=lambda d: d['appointment_date'])
    [i.update({'hours_diff': math.ceil(get_difference(i.get("appointment_date") + ' ' + i.get('appointment_time')))})
     for i in sorted_data]
    sorted_data = [i for i in sorted_data if i.get('hours_diff') > 0]
    for i in sorted_data:
        if i.get("hours_diff") > 71 and i.get('hours_diff') <= 72:
            # need to send Notification
            pass
        elif i.get("hours_diff") > 23 and i.get('hours_diff') <= 24:
            # need to send Notification
            pass
    if len(data):
        return HttpResponse(json.dumps(sorted_data), status_code=200, mimetype="application/json", )
    return HttpResponse("Data does not exists!!", status_code=400)
