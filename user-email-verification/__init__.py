import logging

from azure.functions import HttpRequest, HttpResponse
from azure.communication.email import EmailClient


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        email = req.params.get('email')
        connection_string = "endpoint=https://user-email-verification.unitedstates.communication.azure.com/;accesskey=1U63cY9SQpKEaRDbdi9+CdvUIBv1gNswMmUhk3ZKr2dE1YRY/PNpHxAFxesLbc99m3OAIBGWbOIJ+le+U68XWA=="
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
            "senderAddress": "DoNotReply@ce9c5975-4045-4846-9eea-c054060ce01d.azurecomm.net"
        }

        poller = client.begin_send(message)
        result = poller.result()
        return HttpResponse(f"Email send Successfully to {email}", status_code=200)
    except Exception as e:
        return HttpResponse("Error while sending an email", status_code=400)
