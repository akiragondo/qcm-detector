import requests

class EmailComm():
    def __init__(self):
        self.postEndpoint = "https://0mm3hlaop6.execute-api.us-east-2.amazonaws.com/QCMTest/emailSender"
        self.buffer = []

    def sendEmail(self, body):
        try:
            response = requests.post(self.postEndpoint, data = body)
        except requests.exceptions.HTTPError as error:
            print(error)
            self.buffer.append(body)


