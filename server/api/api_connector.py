import requests
from server.api.endpoint_interface import EndpointInterface
import server.database.models as models

CODEFORCES_BASE_URL = 'http://codeforces.com/api'


class UserContestResults(EndpointInterface):
    endpoint_url = '/user.status'

    def __init__(self):
        self.rawdata = {}
        self.submissions = []
        self.contestTasks = []
        self.cfTasks = []

    def get(self, handle: str, contestCode: int):
        self.contestTasks = models.get_tasks_in_contest(contestCode)
        self.cfTasks = [(str(task['codeforces_id'])+task['codeforces_index']) for task in self.contestTasks]
        try:
            self.rawdata = (requests.get((CODEFORCES_BASE_URL + self.endpoint_url),
                            params = {
                                'handle':handle,
                                'from':1,
                                'count':100
                            },
                            allow_redirects=False,
                            stream=True)).json()
        except requests.exceptions.RequestException as exception:
                return exception
        else:
            self.extract_submissions(contestCode)
            self.insert_to_database(handle)
            return True

    def extract_submissions(self, contestCode: int):
        try:
            if self.rawdata:
                self.submissions = [submission for submission in self.rawdata['result']
                    if (str(submission['contestId']) + submission['problem']['index']) in self.cfTasks]
        except Exception as exception: # pylint: disable=broad-except
            print(exception)

    def insert_to_database(self, handle: str):
        if self.submissions:
            for submission in self.submissions:
                verdict,time = submission['verdict'], submission['creationTimeSeconds']
                user = models.get_userid(handle)
                task = [task['taskid'] for task in self.contestTasks
                    if (str(task['codeforces_id']) + task['codeforces_index']) ==
                    (str(submission['contestId']) + submission['problem']['index'])][0]
                models.insert_submits_task(
                    user,
                    task,
                    verdict,
                    time
                )


class Tasks(EndpointInterface):
    endpoint_url = '/problemset.problems'

    def __init__(self):
        self.rawdata = {}
        self.problems = []

    def get(self, tags=None):
        try:
            if tags is not None:
                self.rawdata = (requests.get((CODEFORCES_BASE_URL + self.endpoint_url),
                    params=dict(tags=str(tags)),
                    allow_redirects=False,
                    stream=True)).json()
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
