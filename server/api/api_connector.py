import requests
from server.api.endpoint_interface import EndpointInterface
import server.database.models as models

CODEFORCES_BASE_URL = 'http://codeforces.com/api'

class SubmissionResults(EndpointInterface):
    endpoint_url = '/'

class Tasks(EndpointInterface):
    endpoint_url = '/api/tasks'

    def __init__(self):
        self.rawdata = {}
        self.problems = []

    def get(self, tags=None):
        try:
            if tags is not None:
                self.rawdata = (requests.get(
                    '{}/problemset.problems'.format(CODEFORCES_BASE_URL),
                    params=dict(tags=str(tags)),
                    allow_redirects=False,
                    stream=True)
                    .json())
            else:
                self.rawdata = requests.get(
                    '{}/problemset.problems'.format(CODEFORCES_BASE_URL)).json()
        except requests.exceptions.RequestException as exception:
            return exception
        else:
            self.extract_problems()
            self.insert_to_database()
            return True

    def extract_problems(self):
        try:
            if self.rawdata:
                self.problems = self.rawdata['result']['problems']
        except Exception as exception: # pylint: disable=broad-except
            print(exception)

    def insert_to_database(self):
        if self.problems:
            for problem in self.problems:
                contestId, index, name, tags = problem['contestId'], problem[
                    'index'], problem['name'], problem['tags']
                url = "http://codeforces.com/problemset/problem/{}/{}".format(
                    contestId, index)
                models.insert_task(
                    name,
                    tags,
                    url,
                    contestId,
                    index
                )
