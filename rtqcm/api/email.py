import requests
import json


class EmailComm:
    def __init__(self):
        self.postEndpoint = "https://0mm3hlaop6.execute-api.us-east-2.amazonaws.com/QCMTest/emailSender"
        self.verifyEndpoint = "https://0mm3hlaop6.execute-api.us-east-2.amazonaws.com/QCMTest/emailVerify"
        self.buffer = []

    def send_email(self, body):
        try:
            response = requests.post(self.postEndpoint, data=body)
            return response
        except requests.exceptions.HTTPError as error:
            print(error)
            self.buffer.append(body)

    def verify_email(self, email):
        json_data = json.dumps(
            {
                'to': email
            }
        )
        try:
            response = requests.post(self.verifyEndpoint, data=json_data)
            return response
        except requests.exceptions.HTTPError as error:
            print(error)
            return error
