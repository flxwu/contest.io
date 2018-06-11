from dotenv import load_dotenv
from pathlib import Path
import os

ENV_PATH = Path(os.path.dirname(os.path.realpath(__file__))) / '../.env'
load_dotenv(verbose=True, dotenv_path=ENV_PATH)

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

SECRET_KEY = os.environ.get('SECRET_KEY')

ADMIN_USERTYPE = 'admin'
NORMAL_USERTYPE = 'normal'

class DB_COLUMNS: #pylint: disable=invalid-name
    USER_USERID = 'userid'
    USER_USERNAME = 'username'
    USER_CODEFORCES_HANDLE = 'codeforces_handle'
    USER_USERTYPE = 'usertype'
    USER_DATE_JOINED = 'date_joined'
    USER_OAUTH_TOKEN = 'oauth_token'
    
    TASK_TASKID = 'taskid'
    TASK_TASKNAME = 'taskname'
    TASK_TASKTAGS = 'tasktags'
    TASK_CODEFORCES_URL = 'codeforces_url'
    
    CONTEST_CONTESTCODE = 'contestcode'
    CONTEST_CONTESTNAME = 'contestname'
    CONTEST_DATE_START = 'date_start'
    CONTEST_DATE_END = 'date_end'
    CONTEST_VISIBLE = 'visible'

    USERGROUP_GROUPID = 'groupid'
    USERGROUP_GROUPNAME = 'groupname'
    USERGROUP_GROUPADMIN = 'groupadmin'
    
    CONTAINS_TASK_CONTEST = 'contest'
    CONTAINS_TASK_TASK = 'task'

    GROUP_IN_CONTEST_USERGROUP = 'usergroup'
    GROUP_IN_CONTEST_CONTEST = 'contest'

    IN_USERGROUP_USERGROUP = 'usergroup'
    IN_USERGROUP_USER = 'user'
