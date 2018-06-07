[![Waffle.io - Columns and their card count](https://badge.waffle.io/flxwu/contest.io.png?columns=all)](https://waffle.io/flxwu/contest.io?utm_source=badge) [![Build Status](https://travis-ci.org/flxwu/contest.io.svg?branch=master)](https://travis-ci.org/flxwu/contest.io) [![CodeFactor](https://www.codefactor.io/repository/github/flxwu/contest.io/badge)](https://www.codefactor.io/repository/github/flxwu/contest.io) [![Maintainability](https://api.codeclimate.com/v1/badges/94bd6495607faf304515/maintainability)](https://codeclimate.com/github/flxwu/contest.io/maintainability) [![Gitter Room](https://img.shields.io/gitter/room/contest-io/Lobby.svg)](https://gitter.im/contest-io/Lobby) [![Package Version](https://img.shields.io/github/package-json/v/flxwu/contest.io.svg)](https://github.com/flxwu/contest.io/blob/master/package.json) [![MIT License](https://img.shields.io/github/license/flxwu/contest.io.svg)](https://github.com/flxwu/contest.io/blob/master/LICENSE) [![Last Commit](https://img.shields.io/github/last-commit/flxwu/contest.io.svg)](https://github.com/flxwu/contest.io/commits/master)
# contest.io - Create opinionated programming contests for your team! 

## Setup

#### Pre-Requirements
- yarn 
- virtualenv
- sqlite3

Initialize VirtualEnv
```
virtualenv -p python3.6 venv
```

Activate it (must be done in every new shell in the working directory) and install the python dependencies
```
source venv/bin/activate
pip3 install -r requirements.txt
```

Install npm dependencies
```
yarn install
cd client/ && yarn install
```

Create/Recreate database (also on changes to `server/database/schema.sql`)
```
yarn db-rewrite
```

## Running

Run the flask setup
```
pip3 install -e .
```

Start Vue Development Server and Flask Backend
```
yarn dev
// navigate to localhost:3000 for FrontEnd
// navigate to localhost:5000 for BackEnd
```

_If you want to only serve the Frontend (not recommended)_
```
cd client/ && yarn dev
```

## .env Variables

We are applying the [12-factor](http://12factor.net/) principles to protect our application secrets. Therefore, the app settings are managed using [dotenv](https://github.com/theskumar/python-dotenv). For the BackEnd to work, save the following values in your root `.env` file:

```
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
SECRET_KEY=...
```
Replace the dots with your own variables. For the Github Client ID and Secret, register contest.io as a new Github OAuth application [here](https://github.com/settings/applications/new). You may name it something like 'contest.io-dev-YOUR_USERNAME'. **Set the authorization callback url to http://localhost:5000/api/github-callback**

The `SECRET_KEY` variable can be set to whatever you want.

# API Docs

**For the returned objects, see the database [schema](server/database/schema.sql)**

### `/api/tasks`

| Method | Parameter | HTTP Header <br> and Body | Description | Required | Example |
|---|---|---|---|---|---|
| GET | tags | - | Comma-seperated list of tags <br> to be matched by <br> the returned tasks <br> _Returns the task_ | No | `/api/tasks?tags=graphs,implementation` |

### `/api/contest`

| Method | Parameter | HTTP Header <br> and Body | Description | Required | Example |
|---|---|---|---|---|---|
| GET | code | - | The contest's hexadecimal code <br> _Returns the contest_ | Yes | `/api/contest?code=f9bf78b9a18ce6d46a0cd2b0b86df9da` |
| POST | - | `Content-Type = application/json` <br> <br> { <br> `"contestname": "testContest-1"`, <br> `"date_start": "2017-05-12"`, <br> `"date_end": "2017-06-12"`, <br> `"visible": 1`, <br> `"contestgroups": [1, 2, 3]` <br> } | Add a new contest <br> _Return the new contest's code_ | - | - |
| DELETE | code | - | The contest's hexadecimal code <br> _Deletes the contest_ | Yes | `/api/contest?code=f9bf78b9a18ce6d46a0cd2b0b86df9da` |
