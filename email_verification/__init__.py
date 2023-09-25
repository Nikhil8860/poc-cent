import logging

from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    container_name = "email_data"
    logging.info('Python HTTP trigger function processed a request.')
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
        item = container.query_items(query=f"select * from email_data where email_data.email='{email}'",
                                     enable_cross_partition_query=True)
        all_email = [i.get("email") for i in item]
        if len(all_email):
            return HttpResponse(f"Hello, {email}. This email is found in DB")
        else:
            return HttpResponse(f"Hello, {email}. This email Not found in DB")
    else:
        return HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
