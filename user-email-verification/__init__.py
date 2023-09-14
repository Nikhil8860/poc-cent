import logging

from azure.functions import HttpRequest, HttpResponse
from azure.communication.email import EmailClient


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    email = req.params.get('email')
    connection_string = "endpoint=https://demo-comm-123.unitedstates.communication.azure.com/;accesskey=eznEF8QrdCYb/AlIsJetWdybuRbUrYitfWJZW7d1kAwNWvF2xuh8Be1wKJ9QMRdS8BWh/pIbGBCNusrecTzpvw=="
    client = EmailClient.from_connection_string(connection_string)
    message = {
        "content": {
            "subject": "This is the subject",
            "plainText": "This is the body",
            "html": "<html><h1>This is the body</h1></html>"
        },
        "recipients": {
            "to": [
                {
                    "address": f"{email}",
                    "displayName": "Nikhil Sharma"
                }
            ]
        },
        "senderAddress": "DoNotReply@3aae6646-df4e-4e6a-b42f-add04869325c.azurecomm.net"
    }

    poller = client.begin_send(message)
    result = poller.result()
    return HttpResponse(f"Email send Successfully to {email}")
