import json
import logging
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    print("------------------------------")
    if req.method == 'POST':
        req_body = req.get_json()
        container_name = 'member'
        container = get_db_container(container_name)
        checked_fields = ['patient_id', 'center_id']
        if not all(key in req_body for key in checked_fields):
            return HttpResponse(json.dumps({"msg": "Error is request Body", "status_code": 400}), status_code=400,
                                mimetype="application/json")
        patient_id = req_body.get("patient_id")
        center_id = req_body.get("center_id")
        query = f"select * from {container_name} where " \
                f"{container_name}.patinet_id='{patient_id}' " \
                f"and {container_name}.center_id='{center_id}'"
        item = container.query_items(query=query,
                                     enable_cross_partition_query=True)
        data = [i for i in item]
        if data:
            return HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")
        return HttpResponse(json.dumps(
            {"msg": f"No Data found for patient_id={patient_id} and center_id={center_id}", "status_code": 400}),
            status_code=400,
            mimetype="application/json")
    return HttpResponse(json.dumps({"msg": "Method should be POST", "status_code": 400}), status_code=400)
