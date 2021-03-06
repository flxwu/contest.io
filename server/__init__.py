from flask import Flask, jsonify, render_template,send_from_directory,request, g, session, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.routing import BaseConverter
from http import HTTPStatus
import json
import requests
import flask_github
import server.api.api_connector as api_connector
import server.database.models as models
import server.settings as settings


class RegexConverter(BaseConverter):
    def __init__(self, urlMap, *items):
        super(RegexConverter, self).__init__(urlMap)
        self.regex = items[0]


def get_queryparam(p: str): return request.args.get(  # pylint: disable=invalid-name
    p) if request.args.get(p) else None


app = Flask(__name__,  # pylint: disable=invalid-name
            static_folder="../dist",
            template_folder="../dist")

# CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}  # pylint:disable=invalid-name
            )
# Flask app config
app.config['GITHUB_CLIENT_ID'] = settings.GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = settings.GITHUB_CLIENT_SECRET
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

app.url_map.converters['regex'] = RegexConverter

# Set Endpoints
TasksEndpoint = api_connector.Tasks()  # pylint: disable=invalid-name
UserContestResultsEndpoint = api_connector.UserContestResults() # pylint: disable=invalid-name  

# Github-Flask
github = flask_github.GitHub(app)  # pylint: disable=invalid-name


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = models.select_user(
            params=('*'),
            conditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERID,
                    session['user_id'])))


@app.route('/')
def index():
    # if app.debug:
    #     return requests.get('http://localhost:3000/index.html').text
    return render_template("index.html")


@app.route('/api/github-login')
def auth_githublogin():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/api/github-logout')
def auth_githublogout():
    session.pop('user_id', None)
    session.pop('oauth_token', None)
    return redirect(url_for('index'))


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user['oauth_token']


@app.route('/api/github-callback')
@github.authorized_handler
def auth_githubcallback(oauthToken):
    nextUrl = request.args.get('next') or url_for('index')
    if oauthToken is None:
        flash("Authorization failed.")
        return redirect(nextUrl)

    user = models.select_user(params=('*'), conditions=(
        '{}=\"{}\"'.format(settings.DB_COLUMNS.USER_OAUTH_TOKEN, oauthToken)))
    if user is None:
        models.insert_user(
            'defaultUser', settings.NORMAL_USERTYPE, oauthToken)
    user = models.select_user(params=('*'), conditions=(
        '{}=\"{}\"'.format(settings.DB_COLUMNS.USER_OAUTH_TOKEN, oauthToken)))

    session['user_id'] = user['userid']
    session.pop('oauth_token', None)
    session['oauth_token'] = oauthToken
    return redirect(nextUrl)


@app.route('/api/github-user')
def auth_user():
    # update inserted User
    try:
        userData = github.get('user')
        userLoginName = userData['login']
    except flask_github.GitHubError as githubError:
        return str(githubError)

    # check if user already exists
    user = models.select_user(params=('*'), conditions=(
        '{}=\"{}\"'.format(settings.DB_COLUMNS.USER_USERNAME, userLoginName)))
    if user is None:
        models.update_user(
            updatedValues=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.USER_USERNAME, userLoginName)),
            setConditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.USER_USERID,
                session.get('user_id', None)
            )))
    else:
        models.delete_user(
            deleteConditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERNAME,
                    'defaultUser')))
        models.update_user(
            updatedValues=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_OAUTH_TOKEN, session.get(
                        'oauth_token', None)),
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_AVATAR_URL, userData['avatar_url']),
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USEREMAIL, userData['email'])
            ),
            setConditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERNAME, userLoginName)))
        user = models.select_user(
            params=('*'),
            conditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERNAME,
                    userLoginName)))
        session.pop('user_id', None)
        session['user_id'] = user['userid']
    return jsonify(dict(id=user['userid'], ghdata=userData))


@app.route('/api/tasks', methods=['GET', 'POST'])
def api_tasks():
    if request.method == 'GET':
        returnJSON = None
        apiResponse = None

        def tasks_json_modify(taskJson: dict):
            taskJson['tasktags'] = json.loads(taskJson['tasktags'])
            return taskJson

        if get_queryparam('tags') is None:
            tasksInDatabase = models.select_task(params=('*'))
        else:
            tasksInDatabase = models.select_task(
                params=('*'),
                conditions=(
                    '{} LIKE "%{}%"'.format(
                        settings.DB_COLUMNS.TASK_TASKTAGS,
                        get_queryparam('tags'))))

        if tasksInDatabase is not None:
            returnJSON = tasksInDatabase
        else:
            # response = TasksEndpoint.get(tags=queryparam_tags())
            apiResponse = TasksEndpoint.get(tags=get_queryparam('tags'))
            if get_queryparam('tags') is None:
                returnJSON = models.select_task(params=('*'))
            else:
                tagsArray = str(get_queryparam('tags')).split(';')
                combinedTags = []
                for tag in tagsArray:
                    combinedTags.append('{} LIKE "%{}%"'.format(
                        settings.DB_COLUMNS.TASK_TASKTAGS,
                        tag))
                returnJSON = models.select_task(
                    params=('*'),
                    conditions=(tuple(combinedTags)))
        if (isinstance(apiResponse, requests.exceptions.RequestException)):
            return str(apiResponse)
        else:
            return jsonify([tasks_json_modify(task) for task in returnJSON])
    elif request.method == 'POST':
        return None
    else:
        return None


@app.route('/api/contest', methods=['GET', 'POST', 'DELETE'])
def api_contest():
    """
    Contest Endpoint: POST with Content-Type = application/json
    {
            "contestname": "testContest-1",
            "contestadmin": 1,
            "date_start": "2017-05-12",
            "date_end": "2017-06-12",
            "visible": 1,
            "usergroups": [1, 2, 3] (groupids),
            "tasks": [1,2,3] (taskids)
    }
    """
    if request.method == 'GET':
        if get_queryparam('code') is None:
            content = {"Error": "\'code\' parameter missing"}
            return json.dumps(content), HTTPStatus.BAD_REQUEST, {'ContentType':'application/json'}

        # get contest JSON
        contestJSON = models.select_contest(
            params=('*'),
            conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.CONTEST_CONTESTCODE,
                get_queryparam('code')
            ))
        )

        # get array of all contest's tasks
        tasksInContestJSON = models.get_tasks_in_contest(
            get_queryparam('code'))

        # get array of all contest's groups
        groupsInContestJSON = models.select_group_in_contest(
            params=('*'),
            conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.GROUP_IN_CONTEST_CONTEST,
                get_queryparam('code')
            ))
        )

        returnJSON = contestJSON
        returnJSON["tasks"] = tasksInContestJSON
        returnJSON["usergroups"] = groupsInContestJSON

        return jsonify(returnJSON)
    elif request.method == 'POST':
        postJSON = request.get_json()
        if not postJSON:
            return None
        else:
            # insert contest to db contest table
            contestCode = models.insert_contest(
                postJSON[settings.DB_COLUMNS.CONTEST_CONTESTNAME],
                postJSON[settings.DB_COLUMNS.CONTEST_CONTESTADMIN],
                postJSON[settings.DB_COLUMNS.CONTEST_DATE_START],
                postJSON[settings.DB_COLUMNS.CONTEST_DATE_END],
                postJSON[settings.DB_COLUMNS.CONTEST_VISIBLE]
            )

            # insert taskids with contestcode in db contains_task table
            for taskID in postJSON["tasks"]:
                models.insert_contains_task(
                    contestCode,
                    taskID
                )

            # insert groupIds with contestcode in db group_in_contest table
            for groupID in postJSON["usergroups"]:
                models.insert_group_in_contest(
                    groupID,
                    contestCode
                )

            # return the contestcode
            return contestCode

    elif request.method == 'DELETE':
        if get_queryparam('code') is None:
            content = {"Error": "\'code\' parameter missing"}
            return json.dumps(content), HTTPStatus.BAD_REQUEST, {'ContentType':'application/json'}
        models.delete_contest(
            deleteConditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.CONTEST_CONTESTCODE,
                get_queryparam('code')
            ))
        )
        return ('', 204)
    else:
        return None


@app.route('/api/contests.joined', methods=['GET', 'POST', 'DELETE'])
def api_contests_join():
    """
    Join/Leave a contest, GET all contests a user is in
    """
    if request.method == 'GET':
        user = get_queryparam('user')
        returnJSON = models.select_joined_contest(
            params=('*'),
            conditions=('{}=\"{}\"'.format(
                    settings.DB_COLUMNS.JOINED_CONTEST_USER,
                    user
                )
            )
        )
        return jsonify(returnJSON)
    elif request.method == 'POST':
        postJSON = request.get_json()
        models.insert_joined_contest(
            postJSON[settings.DB_COLUMNS.JOINED_CONTEST_USER],
            postJSON[settings.DB_COLUMNS.JOINED_CONTEST_CONTEST]
        )
        return ('', 204)
    elif request.method == 'DELETE':
        postJSON = request.get_json()
        models.delete_joined_contest(
            postJSON[settings.DB_COLUMNS.JOINED_CONTEST_USER],
            postJSON[settings.DB_COLUMNS.JOINED_CONTEST_CONTEST]
        )
        return ('', 204)


@app.route('/api/contest.results', methods=['GET'])
def api_contest_results():
    user = get_queryparam('user')
    contest = get_queryparam('contest')
    force = get_queryparam('force')
    returnJSON = None

    resultsInDatabase = models.get_latest_submissions(user, contest)

    if resultsInDatabase is not None and force is None:
        returnJSON = resultsInDatabase
    else:
        # if no db entries, fetch user's contest submissions from cf api and insert them into db
        cfHandle = models.get_cfhandle(user)
        if cfHandle is None or cfHandle is "defaultUser":
            content = {"Error": "user's cf handle wrong or missing"}
            return json.dumps(content), HTTPStatus.BAD_REQUEST, {'ContentType':'application/json'}
        UserContestResultsEndpoint.get(cfHandle, contest)
        returnJSON = models.get_latest_submissions(user, contest)

    return jsonify(returnJSON)


@app.route('/api/contest.joined', methods=['GET'])
def api_contest_join():
    """
    GET all joined users in a contest
    """
    contestcode = get_queryparam('code')
    returnJSON = models.select_joined_contest(
        params=('user'),
        conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.JOINED_CONTEST_CONTEST,
                contestcode
            )
        )
    )
    return jsonify(returnJSON)


@app.route('/api/contests', methods=['GET'])
def api_contests():
    if request.method == 'GET':
        if get_queryparam('visible'):
            # get all visible contests
            contests = models.select_contest(
                params=('*'),
                conditions=('{}=\"{}\"'.format(
                    settings.DB_COLUMNS.CONTEST_VISIBLE,
                    1))
            )
            return jsonify(contests)
        elif get_queryparam('admin'):
            # get all contests created by "admin"
            contests = models.select_contest(
                params=('*'),
                conditions=('{}=\"{}\"'.format(
                    settings.DB_COLUMNS.CONTEST_CONTESTADMIN,
                    get_queryparam('admin')))
            )
            return jsonify(contests)
        else:
            return None
    else:
        return None


@app.route('/api/user', methods=['GET'])
def api_user():
    if request.method == 'GET':
        # TODO: return user
        return None
    else:
        return None


@app.route('/api/user.cfhandle', methods=['POST'])
def api_user_cfhandle():
    """
        POST endpoint to set a user's codeforces handle
    """
    models.update_user(
        updatedValues=('{}=\"{}\"'.format(
            settings.DB_COLUMNS.USER_CODEFORCES_HANDLE,
            request.get_json()['handle']
        )),
        setConditions=('{}=\"{}\"'.format(
            settings.DB_COLUMNS.USER_USERID,
            request.get_json()['user']
        ))
    )
    return request.get_json()['handle']


@app.route('/api/usergroup', methods=['GET', 'POST'])
def api_usergroup():
    """
    Contest Endpoint: POST with Content-Type = application/json
    {
        "groupname": groupname (String)
        "groupadmin": userID of group admin
    }
    }
    """
    if request.method == 'GET':
        returnJSON = models.select_usergroup(
            params=('*'),
            conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.USERGROUP_GROUPID,
                get_queryparam('group')
            ))
        )
        return jsonify(returnJSON)
    elif request.method == 'POST':
        # add a new Usergroup
        postJSON = request.get_json()
        if not postJSON:
            return None
        else:
            usergroupID = models.insert_usergroup(
                postJSON[settings.DB_COLUMNS.USERGROUP_GROUPNAME],
                postJSON[settings.DB_COLUMNS.USERGROUP_GROUPADMIN])
            models.insert_in_usergroup(
                usergroupID,
                postJSON[settings.DB_COLUMNS.USERGROUP_GROUPADMIN])
            return str(usergroupID)
    else:
        return None


@app.route('/api/usergroup.memberships', methods=['GET'])
def api_usergroup_membership():
    memberships = models.get_memberships_of(
        user=get_queryparam('user'), admin=get_queryparam('admin'))
    return jsonify(memberships)


@app.route('/api/usergroup.members', methods=['GET', 'POST'])
def api_usergroup_members():
    """
    Contest Endpoint: POST with Content-Type = application/json
    {
        "usergroup": usergroupID
        "user": userID
    }
    """
    if request.method == 'GET':
        userIDsInGroup = models.select_in_usergroup(
            params=(settings.DB_COLUMNS.IN_USERGROUP_USER),
            conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.IN_USERGROUP_USERGROUP,
                get_queryparam('group')
            ))
        )
        userObjects = []
        for userID in userIDsInGroup:
            userObjects.append(
                models.select_user(
                    params=('*'),
                    conditions=('{}=\"{}\"'.format(
                        settings.DB_COLUMNS.USER_USERID, userID))
                )
            )
        return jsonify(userObjects)
    elif request.method == 'POST':
        # add user to group
        postJSON = request.get_json()
        if not postJSON:
            return None
        else:
            models.insert_in_usergroup(
                postJSON[settings.DB_COLUMNS.IN_USERGROUP_USERGROUP],
                postJSON[settings.DB_COLUMNS.IN_USERGROUP_USER])
    else:
        return None


@app.route('/js/<path:path>')
def send_js(path):
    return app.send_static_file('js/{}'.format(path))

@app.route('/css/<path:path>')
def send_css(path):
    return app.send_static_file('css/{}'.format(path))

@app.route('/favicon.ico')
def send_favicon():
    return app.send_static_file('favicon.ico')

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def catch_all(path): # pylint: disable=unused-argument
    return render_template("index.html")
