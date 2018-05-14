from flask import Flask, jsonify, render_template, request, g, session, redirect, url_for, flash
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


app = Flask(__name__,  # pylint: disable=invalid-name
            static_folder="../client/dist/static",
            template_folder="../client/dist")
# CORS
CORS(app)
# Flask app config
app.config['GITHUB_CLIENT_ID'] = settings.GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = settings.GITHUB_CLIENT_SECRET
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

app.url_map.converters['regex'] = RegexConverter

# Set Endpoints
TasksEndpoint = api_connector.Tasks()  # pylint: disable=invalid-name

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


@app.route('/robots.txt')
def serve_robots():
    return app.send_static_file('robots.txt')


@app.route('/favicon.ico')
def serve_favicon():
    return app.send_static_file('favicon.ico')


@app.route('/')
def index():
    if app.debug:
        return requests.get('http://localhost:3000/index.html').text
    return render_template("index.html")


@app.route('/github-login')
def auth_githublogin():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/github-logout')
def auth_githublogout():
    session.pop('user_id', None)
    session.pop('oauth_token', None)
    return redirect(url_for('index'))


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user[-1]


@app.route('/github-callback')
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

    session['user_id'] = user[0]
    session.pop('oauth_token', None)
    session['oauth_token'] = oauthToken
    return redirect(nextUrl)


@app.route('/github-user')
def auth_user():
    # update inserted User
    userData = github.get('user')
    userLoginName = userData['login']

    # check if user already exists
    user = models.select_user(params=('*'), conditions=(
        '{}=\"{}\"'.format(settings.DB_COLUMNS.USER_USERNAME, userLoginName)))
    if user is None:
        models.update_user(
            updatedValues=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.USER_USERNAME, userLoginName)),
            set_conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.USER_USERID,
                session.get('user_id', None)
            )))
    else:
        models.delete_user(
            delete_conditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERNAME,
                    'defaultUser')))
        models.update_user(
            updatedValues=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_OAUTH_TOKEN, session.get(
                        'oauth_token', None))), set_conditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERNAME, userLoginName)))
        user = models.select_user(
            params=('*'),
            conditions=(
                '{}=\"{}\"'.format(
                    settings.DB_COLUMNS.USER_USERNAME,
                    userLoginName)))
        session.pop('user_id', None)
        session['user_id'] = user[0]
    return str(userData)


@app.route('/api/tasks', methods=['GET', 'POST'])
def api_tasks():
    if request.method == 'GET':
        returnJSON = None

        def queryparam_tags():
            return request.args.get('tags') if request.args.get('tags') else None

        def tasks_json_modify(taskJson: dict):
            taskJson['tasktags'] = json.loads(taskJson['tasktags'])
            return taskJson

        if queryparam_tags() is None:
            tasksInDatabase = models.select_task(params=('*'))
        else:
            tasksInDatabase = models.select_task(
                params=('*'),
                conditions=(
                    '{} LIKE "%{}%"'.format(
                        settings.DB_COLUMNS.TASK_TASKTAGS,
                        queryparam_tags())))

        if tasksInDatabase is not None:
            returnJSON = tasksInDatabase
        else:
            # response = TasksEndpoint.get(tags=queryparam_tags())
            TasksEndpoint.get(tags=queryparam_tags())
            if queryparam_tags() is None:
                returnJSON = models.select_task(params=('*'))
            else:
                tagsArray = str(queryparam_tags()).split(';')
                combinedTags = []
                for tag in tagsArray:
                    combinedTags.append('{} LIKE "%{}%"'.format(
                            settings.DB_COLUMNS.TASK_TASKTAGS,
                            tag))
                returnJSON = models.select_task(
                    params=('*'),
                    conditions=(tuple(combinedTags)))
        return jsonify([tasks_json_modify(task) for task in returnJSON])
    elif request.method == 'POST':
        return None
    else:
        return None


@app.route('/api/contests', methods=['GET', 'POST', 'DELETE'])
def api_contests():
    """
    Contest Endpoint: POST with Content-Type = application/json
    {
            "contestname": "testContest-1",
            "date_start": "2017-05-12",
            "date_end": "2017-06-12",
            "visible": 1,
            "contestgroups": [1, 2, 3]
    }
    """
    if request.method == 'GET':
        def queryparam_code(): return request.args.get(
            'code') if request.args.get('code') else None

        if queryparam_code() is None:
            content={"Error": "\'code\' parameter missing"}
            return content, HTTPStatus.BAD_REQUEST
        returnJSON=models.select_contest(
            params=('*'),
            conditions=('{}=\"{}\"'.format(
                settings.DB_COLUMNS.CONTEST_CONTESTCODE,
                queryparam_code()
            ))
        )
        return jsonify(returnJSON)
    elif request.method == 'POST':
        postJSON=request.get_json()
        if not postJSON:
            return None
        else:
            contestCode=models.insert_contest(
                postJSON[settings.DB_COLUMNS.CONTEST_CONTESTNAME],
                postJSON[settings.DB_COLUMNS.CONTEST_DATE_START],
                postJSON[settings.DB_COLUMNS.CONTEST_DATE_END],
                postJSON[settings.DB_COLUMNS.CONTEST_VISIBLE],
                postJSON[settings.DB_COLUMNS.CONTEST_CONTESTGROUPS]
            )
            return contestCode
    elif request.method == 'DELETE':
        return None
    else:
        return None


@app.route('/sockjs-node/<path>')
def sockjs(path):

    if app.debug:
        return requests.post(
            'http://localhost:3000/sockjs-node/{}'.format(path))
    return render_template('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

    if app.debug:
        return requests.get('http://localhost:3000/{}'.format(path)).text
    return render_template('index.html')
