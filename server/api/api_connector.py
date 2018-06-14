import requests
from server.api.endpoint_interface import EndpointInterface
import server.database.models as models
import sqlite3

CODEFORCES_BASE_URL = 'http://codeforces.com/api'


class UserContestResults(EndpointInterface):
    endpoint_url = '/user.status'

    def __init__(self):
        self.rawdata = {}
        self.submissions = []
        self.contest_tasks = []
        self.cf_tasks = []

    def get(self, handle: str, contestCode: int): # pylint: disable=arguments-differ
        self.contest_tasks = models.get_tasks_in_contest(contestCode)
        self.cf_tasks = [(str(task['codeforces_id'])+task['codeforces_index']) for task in self.contest_tasks]
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
            self.extract_submissions()
            self.insert_to_database(handle)
            return self.submissions

    def extract_submissions(self):
        try:
            if self.rawdata:
                self.submissions = [submission for submission in self.rawdata['result']
                    if (str(submission['contestId']) + submission['problem']['index']) in self.cf_tasks]
        except Exception as exception: # pylint: disable=broad-except
            print(exception)

    def insert_to_database(self, handle: str): # pylint: disable=arguments-differ
        if self.submissions:
            for submission in reversed(self.submissions):
                verdict,time = submission['verdict'], submission['creationTimeSeconds']
                user = models.get_userid(handle)
                task = [task['taskid'] for task in self.contest_tasks
                    if (str(task['codeforces_id']) + task['codeforces_index']) ==
                    (str(submission['contestId']) + submission['problem']['index'])][0]
                try:
                    models.insert_submits_task(
                        user,
                        task,
                        verdict,
                        time
                    )
                except sqlite3.IntegrityError:
                    models.update_submits_task(
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

    def get(self, tags=None): # pylint: disable=arguments-differ
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
