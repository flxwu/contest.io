import sqlite3 as sql
import json
import secrets
from dateutil import parser
from datetime import datetime

DATABASE_PATH = 'server/database/database.db'


def dict_factory(cursor, row):
    rowsDict = {}
    for idx, col in enumerate(cursor.description):
        rowsDict[col[0]] = row[idx]
    return rowsDict


def recreate_table(tableName: str):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        cur.execute('DELETE FROM {}'.format(tableName))
        cur.execute(
            'DELETE FROM sqlite_sequence WHERE name = "{}"'.format(tableName))


def insert_task(name: str, tags: list, url: str, cfID: int, cfIndex: str):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        tags = json.dumps(tags)
        cur.execute(
            'INSERT INTO Task (taskname, tasktags, codeforces_url, codeforces_id, codeforces_index) VALUES (?,?,?,?,?)',
            (name, tags, url, cfID, cfIndex)
        )
        cur.close()
        dbcon.commit()


def select_task(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        dbcon.row_factory = dict_factory
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            queryResult = cur.execute('SELECT * FROM Task')
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM Task'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def insert_contest(
        name: str,
        admin: int,
        dateStart: str,
        dateEnd: str,
        visible: int):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        randomCode = secrets.token_hex(8)
        dateStart = parser.parse(dateStart)
        dateEnd = parser.parse(dateEnd)
        cur.execute(
            'INSERT INTO Contest (contestcode, contestname, contestadmin, date_start, date_end, visible) VALUES (?,?,?,?,?)',
            (randomCode,
                name,
                admin,
                dateStart,
                dateEnd,
                visible))
        dbcon.commit()
        return randomCode


def select_contest(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        dbcon.row_factory = dict_factory
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            queryResult = cur.execute('SELECT * FROM Contest')
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM Contest'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def delete_contest(deleteConditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if deleteConditions == ():
            return None
        else:
            if not isinstance(deleteConditions, tuple):
                deleteConditions = (deleteConditions,)

            queryString = 'DELETE FROM Contest WHERE'
            for conditionString in deleteConditions:
                queryString += ' {} AND'.format(conditionString)
            queryString = queryString[:-4]
            cur.execute(queryString)
            dbcon.commit()


def insert_user(name: str, usertype: str, oauthToken: str, email=None, avatarUrl=None):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        cur.execute(
            'INSERT INTO User (username, codeforces_handle, usertype, useremail, avatar_url, oauth_token) VALUES (?,?,?,?,?,?)',
            (name, name, usertype, email, avatarUrl, oauthToken)
        )
        dbcon.commit()


def select_user(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        dbcon.row_factory = dict_factory
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            queryResult = cur.execute('SELECT * FROM User')
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM User'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def update_user(updatedValues=(), setConditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None

        if updatedValues == () and setConditions == ():
            return None
        else:
            # convert one-value tuples to real tuples
            if not isinstance(updatedValues, tuple):
                updatedValues = (updatedValues,)
            if not isinstance(setConditions, tuple):
                setConditions = (setConditions,)

            if updatedValues != ():
                queryString = 'UPDATE User SET'
                # add a format-placeholder for every parameter
                for updateString in updatedValues:
                    queryString += ' {},'.format(updateString)
                queryString = queryString[:-1]
            if setConditions != ():
                queryString += ' WHERE'
                for conditionString in setConditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            cur.execute(queryString)
            dbcon.commit()


def delete_user(deleteConditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if deleteConditions == ():
            return None
        else:
            if not isinstance(deleteConditions, tuple):
                deleteConditions = (deleteConditions,)

            queryString = 'DELETE FROM User WHERE'
            for conditionString in deleteConditions:
                queryString += ' {} AND'.format(conditionString)
            queryString = queryString[:-4]
            cur.execute(queryString)
            dbcon.commit()


def insert_contains_task(
        contest: int,
        task: int):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        cur.execute(
            'INSERT INTO contains_task (contest, task) VALUES (?,?)',
            (contest, task))
        dbcon.commit()


def select_contains_task(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            return None
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM contains_task'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def insert_usergroup(
        groupname: str,
        groupadmin: int):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        cur.execute(
            'INSERT INTO Usergroup (groupname, groupadmin) VALUES (?,?)',
            (groupname, groupadmin))
        groupID = cur.lastrowid
        dbcon.commit()
        return groupID

def select_usergroup(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        dbcon.row_factory = dict_factory        
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            return None
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM Usergroup'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def insert_group_in_contest(
        usergroup: int,
        contest: int):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        cur.execute(
            'INSERT INTO group_in_contest (usergroup, contest) VALUES (?,?)',
            (usergroup, contest))
        dbcon.commit()


def select_group_in_contest(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            return None
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM group_in_contest'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def insert_in_usergroup(
        usergroup: int,
        user: int):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        cur.execute(
            'INSERT INTO in_usergroup (usergroup, user) VALUES (?,?)',
            (usergroup, user))
        dbcon.commit()


def select_in_usergroup(params=(), conditions=()):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        if params == () and conditions == ():
            return None
        else:
            # convert one-value tuples to real tuples
            if not isinstance(params, tuple):
                params = (params,)
            if not isinstance(conditions, tuple):
                conditions = (conditions,)

            if params != ():
                queryString = 'SELECT'
                # add a format-placeholder for every parameter
                for paramString in params:
                    queryString += ' {},'.format(paramString)
                queryString = queryString[:-1]
                queryString += ' FROM in_usergroup'
            if conditions != ():
                queryString += ' WHERE'
                for conditionString in conditions:
                    queryString += ' {} AND'.format(conditionString)
                queryString = queryString[:-4]
            queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    if not response:
        return None
    else:
        return [user[0] for user in response]


def insert_submits_task(user: int, task:int, verdict: str, submission_timestamp: int):
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        submission_time = datetime.fromtimestamp(submission_timestamp)
        cur.execute(
            'INSERT INTO submits_task (user, task, verdict, submission_time) VALUES (?,?,?,?)',
            (user, task, verdict, submission_time))
        dbcon.commit()

# TODO:
# def get_users_in_contest(contestCode: int):
#     queryString = 'SELECT Task.* \
#         FROM in_usergroup, Contest \
#         WHERE in_usergroup.usergroup = Contest AND \
#             contains_task.contest = \"{}\"'.format(contestCode)


def get_tasks_in_contest(contestCode: int):
    queryString = 'SELECT Task.* \
        FROM contains_task, Task \
        WHERE contains_task.task = Task.taskid AND \
            contains_task.contest = \"{}\"'.format(contestCode)
    with sql.connect(DATABASE_PATH) as dbcon:
        dbcon.row_factory = dict_factory
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        queryResult = cur.execute(queryString)

    response = queryResult.fetchall()
    response = response[0] if len(response) == 1 else response
    if not response:
        return None
    else:
        return response


def get_cfhandle(user: int):
    queryString = 'SELECT codeforces_handle \
        FROM User \
        WHERE userid = \"{}\"'.format(user)
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        queryResult = cur.execute(queryString)

    response = queryResult.fetchone()
    if not response:
        return None
    else:
        return response

def get_userid(cfhandle: str):
    queryString = 'SELECT userid \
        FROM User \
        WHERE codeforces_handle = \"{}\"'.format(cfhandle)
    with sql.connect(DATABASE_PATH) as dbcon:
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        queryResult = cur.execute(queryString)

    response = queryResult.fetchone()
    if not response:
        return None
    else:
        return response


def get_latest_submissions(user: str, contestCode: int):
    queryString = 'SELECT submits_task.verdict, submits_task.task \
        FROM submits_task, contains_task \
        WHERE submits_task.task = contains_task.task\
        AND submits_task.user = \"{}\" \
        AND contains_task.contest = \"{}\"'.format(user, contestCode)
    with sql.connect(DATABASE_PATH) as dbcon:
        dbcon.row_factory = dict_factory        
        cur = dbcon.cursor()
        if cur.rowcount == 0:
            return None
        queryResult = cur.execute(queryString)
    
    response = queryResult.fetchall()
    if not response:
        return None
    else:
        return response
