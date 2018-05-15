#!/usr/bin/expect
setup_heroku() {
  sudo curl https://cli-assets.heroku.com/install-standalone.sh | sh
  sudo echo "machine api.heroku.com
  login ${HEROKU_LOGIN}
  password ${HEROKU_TOKEN}
machine git.heroku.com
  login ${HEROKU_LOGIN}
  password ${HEROKU_TOKEN}" > ~/.netrc
}

deploy_to_heroku() {
  if [ $TRAVIS_EVENT_TYPE != "pull_request" ]; then
    if [ $TRAVIS_BRANCH == "master" ]; then
      echo "Detected deploy to master branch..."
      git checkout master
      setup_git
      cd client/ && yarn build
      cd ../
      commit_files
      upload_files
      setup_heroku
      heroku git:remote --app contestio-dev
      heroku config:set FLASK_CONFIG=Production
      heroku config:set SECRET=SECRET_KEY
      heroku config:set WEB_CONCURRENCY=3
      git push heroku
    fi
  fi
}

setup_git() {
  git config --global user.email "mail@flxwu.com"
  git config --global user.name "Felix Wu"
}

commit_files() {
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add origin https://${GH_TOKEN}@github.com/flxwu/contest.io.git > /dev/null 2>&1
  git push --set-upstream origin master 
}

deploy_to_heroku
