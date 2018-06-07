# Table Of Contents

- [1. Abstract](#1-abstract)
- [2. Ausblick](#2-ausblick)
- [3. Dokumentation – Front-End (Vue.js)](#3-dokumentation-%E2%80%93-front-end)
  * [3.1. Das Framework - Vue.js](#31-das-framework---vuejs)
    + [3.1.1. Wozu ein Framework?](#311--wozu-ein-framework)
    + [3.1.2. Warum Vue?](#312--warum-vue)
  * [3.2 Weitere verwendete Bibliotheken](#32--weitere-verwendete-bibliotheken)
- [4. Dokumentation – Back-End (Flask)](#4-dokumentation--back-end-flask)
  * [4.0. Wofür ein Back-End-Framework?](#40-wofur-ein-back-end-framework)
  * [4.1. Warum Flask?](#41-warum-flask)
    + [4.1.1 Weitere verwendete externe Bibliotheken](#411-weitere-verwendete-externe-bibliotheken)
  * [4.2. Security](#42-security)
  * [4.3. Coding Style und Linting](#43-coding-style-und-linting)
  * [4.4 Datenbank](#44-datenbank)
- [5. Continious Integration und Maintanability](#5-continious-integration-und-maintanability)
  * [5.1. Continious Integration](#51-continious-integration)
    + [5.1.1. Travis CI](#511-travis-ci)
    + [5.1.2. CodeFactor und CodeClimate](#512-codefactor-und-codeclimate)
- [6. Code](#6-code)
  * [6.1 Code – Front-End](#61-code-front-end)
  * [6.2 Code – Back-End](#62-code-back-end)

## 1. Abstract   

Contest.io soll eine einfache Plattform zur Erstellung von Programmierwettbewerben sein. Mit einstellbarem Zeitraum und individuelle Zusammenstellung von Aufgaben kann die Plattform auch als Ergänzung zum Unterricht dienen, da passend zum Lernmaterial Aufgaben bereitgestellt werden kann, wo der Lehrer individuellen Vorschritt genau Nachverfolgen kann.   


## 2. Ausblick  

In Zukunft können zusätzliche Funktionen wie zum Beispiel ein Punkte-System und somit ein Rang-System eingeführt werden. Neben Codeforces könne weitere Fragenkataloge angeschlossen werden, um das Aufgabensortiment zu erweitern. Das Aufräumen von Optimieren von code ist ebenfalls möglich, jedoch ist dazu wenig Bedarf, da unser code bereits durch einige Prüfungs-Tools als gut bewertet wurde. Mehrere Möglichkeiten des Einloggens können ebenfalls implementiert werden, sowie erweiterte Profil- und Gruppenfunktionen.


# 3. Dokumentation – Front-End

## 3.1.	Das Framework - ([Vue.js](https://vuejs.org))

### 3.1.1. Was ist das Front-End?	Und Wozu ein Framework?   

Das Front-End beschreibt der Teil einer Webseite, mit dem der User direkt interagiert. Was der User sieht, worin er tippt, worauf er klickt: das alles gehört zum Fronr-End.

Ein Front-End Framework erlaubt das Schaffen dynamische Webseiten und Single-Page-Applications, die für komplexe Web-Apps wie dieses Projekt, wenn nicht unbedingt notwendig, jedenfalls ungemein nützlich sind.  

Das Framework erlaubt auch sogenanntes 'lokal testing', das heißt, dass das Framework problemlos auf dem Computer des Developers einen test-server aufbaut und darauf läuft. Zum testen kann der Devloper nun diesen server per Browser ansteuern und sieht die fertige Webseite, wie sie nach dem finalen 'deploy' (das aufsetzen auf den echten server) aussehen und funktionieren wird. So können bugs erkannt und eliminiert werden.

### 3.1.2.	Warum Vue?  

Für contest.io haben wir uns für das relative neue Framework Vue.js 2.0 entschieden, da es schnell und komprimierter ist und trotzdem große Leistung besitzt. Vue besitzt ebenfalls eine große Community mit vielen hilfreichen Plugins, die einem das Programmieren erleichtern.  

Vue sorgt dafür, dass nur veränderte Komponenten neu vom server geladen werden, und minimiert somit unnötige downloads und Berechnungen. Der Vue-Router erlaubt einfache Navigation von Seiten und verhindert auch unnötigen Web-Traffic.

## 3.2	Weitere verwendete Bibliotheken  

Jedes größere Projekt mit Frameworks benötigt außerdem einige zusätzlichen Tools. Allgemein haben wir ([Vuetify](https://vuetifyjs.com)) als Design-Plugin genommen, welches das standardisierte Google-Material-Design auf die Webseite überträgt. ([Axios](https://github.com/axios/axios)) erlaubt die Verbindung von Front- und Back-End. ([Webpack](https://webpack.js.org)) kompiliert den Vue code, um ihn für den Browser lesbar zu machen. Außerdem wurden einige kleine Plugins wie `vue-moment` auch benutzt.

# 4. Dokumentation – Back-End ([Flask](flask.pocoo.org))

## 4.0. Wofür ein Back-End-Framework?

Das Back-End ist bei einer "Full-Stack"-Webapplikation, also einer Applikation bestehend aus Front-End und Back-End, der Begriff für den Server und den darauf laufende Software. Nun fragt man sich, wofür man denn überhaupt ein Back-End braucht, und das ist eine berechtigte Frage, denn: Lange funktionierten Webseiten ohne Serverstruktur, reine _Client-Websiten_ also. Und auch heute wird wieder mehr auf _serverless-architecture_ gesetzt, auch wenn hierbei letztendlich die Serverarbeit vom Cloud-Provider betrieben wird.

Dass wir uns dennoch für ein Back-End entschieden haben, liegt letztendlich an zwei wesentlichen Gründen:

1. Wir benötigen eine Datenbank für alle unsere Operationen rund um die Aufgaben, Wettbewerbe, Nutzer und Gruppen. Diese aus dieser Datenbank verfügbaren Daten müssen überall gleich und verfügbar sein, egal wo der Nutzer gerade über seinen Client - bzw. das Front-End - auf unseren Dienst zugreift.
2. Echtzeit-Analyse ist nur mit einem Server möglich. In unserem Fall bedeutet dies, dass alle Nutzer zur selben Zeit angezeigt bekommen, wie weit ein Wettbewerb fortgeschritten ist oder wie weit die Mitstreiter sind.

## 4.1. Warum Flask?

Im Vorfeld stand relativ schnell für uns fest, dass wir im Back-End entweder das auf Node.js basierende JavaScript-BackEnd-Framework [Express.js](https://github.com/expressjs/express) oder etwas eher Neues verwenden würden. Express.js hatte den Vorteil, dass wir beide Erfahrung mit JavaScript und dem Framework haben und vor allem der Einstieg deutlich leichter gewesen wäre. Viel entscheidender war jedoch, dass Express.js als JavaScript-Framework deutlich kompatibler mit unserem Front-End Framework Vue.js sein würde.

Dennoch ist es letztendlich Flask geworden, da ich recht gut Python beherrsche und bereits Erfahrung mit [Django](https://djangoproject.com/), einem extrem funktionsreichen und komplexen Python-BackEnd-Framework, hatte, und wir etwas Neues ausprobieren wollten. Jedoch war die Erfahrung mit _Django_ aufgrund der extremen Größe und Komplexität eher negativ und da wir nicht vor hatten, Facebook nachzubauen, entschieden wir uns für die schnellere, einfacher zu erlernende und deutlich unkomplexere Alternative Flask. Nachdem wir also nach einiger Recherche sichergestellt hatten, dass Vue.js und Flask größtenteils reibungsfrei kombinierbar sind, stand diese Entscheidung also fest.

### 4.1.1 Weitere verwendete externe Bibliotheken

- [requests](http://docs.python-requests.org/) - Netzwerkoperationen
- [gunicorn](http://gunicorn.org/) - HTTP Server für Flask
- [autopep8](https://github.com/hhatto/autopep8) - Coding-Style-Convention (s. [hier](#43-coding-style-und-linting))
- [pylint](https://github.com/PyCQA/pylint) - "Linting" (s. [hier](#43-coding-style-und-linting))
- [python-dotenv](https://github.com/theskumar/python-dotenv) - .env support (s. [hier](#42-security))

## 4.2 Datenbank
Folglich ist das ER-Diagramm abgebildet. Als Query-Language dient [Sqlite3](https://www.sqlite.org/)
![ER Diagramm](er-diagram.png)

## 4.3. Dateienstruktur

## 4.4. Security
Da auch wir einige _Secrets_, also "geheime" Schlüssel wie die Api Keys von Github, in unserem Back-End verwenden, entschied ich mich, die [12-factor](http://12factor.net/)-Prinzipien anzuwenden, um diese Schlüssel nicht der Öffentlichkeit zu offenbaren, zumal wir unseren Code öffentlich auf Github hosten.

Aus diesem Grund verwenden wir die Python-Version von `dotenv`, eine ursprünglich für Node.js(JavaScript) entwickelte Software zum Laden von globalen Umgebungsvariablen aus einer `.env` Datei.
Dies bedeutet, wir deklarieren in unseren `.env` Dateien die benötigten _Secrets_:
```bash
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
SECRET_KEY=...
```
Diese werden dann vom Back-End geladen und benutzt, dabei wird die Datei von Git ignoriert, das heißt jeder inklusive uns, der das Projekt lokal ausprobieren/entwickeln möchte, muss eine solche Datei erstellen, einen eigenen Github Api-Key generieren und diesen einfügen.

## 4.5. Coding Style und Linting
Linting bezeichnet das Analysieren von Code auf potenzielle Fehler, wie vergessene Klammern, falsche Einrückungen oder fehlerhafte Variablendeklerationen.
Dafür wird im Back-End die Software `pylint` benutzt.

Coding Style bezeichnet das Aussehen des Codes - und dafür gibt es Konventionen. Die in Python am weitesten verbreiteste is `autopep8`. Dieses Programm formatiert automatisch den Code und meldet Verstöße gegen die Konvention.


# 5. Continious Integration und Maintainability
Wir haben von Anfang an versucht, unser Projekt möglichst "maintainable" zu halten: Dies bedeutet, dass wir potenziellen Nachfolgern oder Mitprogrammieren den Einstieg durch weitesgehende Automatisierungen vereinfachen.

## 5.1. Continious Integration

Continious Integration beschreibt den automatisierten Prozess des Zusammenfügens, Packetierens, Testens und letztlich Vertriebs der Software.
Wesentliches Ziel ist also die Steigerung der Softwarequalität, da dadurch menschliche Eingriffe in das "Deployment" vermieden werden.

### 5.1.1. Travis CI
Hauptwerkzeug unserer Continious Integration ist der Dienst bzw. die Software [Travis CI](travis-ci.org).

Travis arbeitet mit sogenannten `builds`: In unserem Fall wird ein `build` jedes mal ausgeführt, wenn ein neuer Commit gepusht wird.

Unsere Konfiguration sieht dabei wie folgt aus:
```yaml
matrix:
  include:
    - language: python
      python:
        - "3.6"
      node_js:
        - "node"
      env:
        - FLASK=1.0.2
      install:
        - pip3 install Flask==$FLASK
        - pip3 install -r requirements.txt
        - pip3 install -e .
        - yarn add eslint
        - yarn install
        - cd client/ && yarn install
        - cd ../
      before_script:
        - chmod +x .travis/writetoenv.sh && ./.travis/writetoenv.sh
        - yarn db-rewrite
        - chmod +x .travis/deploy.sh
      script:
        - pylint server
        - cd client/ && yarn lint --fix
        - cd ../
        - cd client/ && yarn build
        # - nosetests
        - cd ../
        - ./.travis/deploy.sh
      cache:
        directories:
          - "node_modules"
          - "client/node_modules"
```

Die Kommandos sind dabei in der POSIX-Sprache `bash`, ebenfalls wie die beiden Skripte `deploy.sh` und `writetoenv.sh`. Im Wesentlichen werden bei jedem `build` folgende Schritte ausgeführt:

1. Alle Front-End und Back-End Abhängigkeiten installiert
2. Die von uns im Travis-CI User-Interface festgesetzten Umgebungsvariablen werden in die `.env` Datei geschrieben um vom Back-End geladen werden zu können
3. Die Datenbank wird kompiliert
4. Sowohl Front-End als auch Back-End werden einem `Linter` unterzogen, das heißt der `build` scheitert wenn Fehler erkannt werden oder wir von unseren Coding-Style Konventionen abgewichen sind.
5. Das Front-End wird kompiliert - aus den vielen Dateien wird eine große komprimierte `.js` Datei (neben den anderen statischen Dateien) gemacht, um das Gesamtpaket klein zu halten und die Performance zu optimieren. Dies ist eine native Funktion von Vue.js.
6. **Wenn der `build` auf der `master` branch ist**, werden die kompilierten sowie von den Lintern überprüften Dateien committed und zurück in unser Repository gepusht. Dies musste in der `bash` Datei [`deploy.sh`](https://github.com/flxwu/contest.io/blob/develop/.travis/deploy.sh) eigenhändig programmiert werden. Ein solcher Commit sieht dann so aus:
![Travis Commit](traviscommit.png)


**Scheitert einer der Schritte 4-6, wird in Github ein rotes Symbol angezeigt** - so mergen wir unsere Pull-Requests erst, wenn der `build` erfolgreich war, also keine Fehler erkannt wurden und alle Schritte reibungsfrei durchlaufen werden konnten.

### 5.1.2. CodeFactor und CodeClimate
Dies sind beides weitere Tools zur Bewertung und Überprüfung unseres Codes auf mögliche Fehler, Ungereimtheiten und vermeintliche unschöne Passagen wie Wiederholungen etc.

![CodeClimate](codeclimate.png)
*CodeFactor und CodeClimate Dashboards*

# 6. Code

## 6.1 Code – Front-End

client/vue.config.js

```
/*eslint-env node*/

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        ws: true,
        changeOrigin: true,
        pathRewrite: {'^/api/': '/api/'},
        xfwd: true    
      }
    }
  }
};
```


client/.eslintrc.js

```
module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": ["eslint:recommended", "plugin:vue/essential"],
    "parserOptions": {
        "parser": "babel-eslint",
        "ecmaVersion": 2017,
        "ecmaFeatures": {
            "experimentalObjectRestSpread": true,
            "jsx": true
        },
        "sourceType": "module"
    },
    "plugins": [
      "vue",  
      "eslint-plugin-vue"
    ],
    "rules": {
        "indent": [
            "error",
            2,
            {"SwitchCase": 1}
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "single"
        ],
        "semi": [
            "error",
            "always"
        ],
        "no-console": 0,
    }
};
```


client/public/index.html

```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="shortcut icon" href="<%= webpackConfig.output.publicPath %>favicon.ico">

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.13/css/all.css" integrity="sha384-DNOHZ68U8hZfKXOrtjWvjxusGo9WQnrNx2sqG0tfsghAvtVlRW3tvkXWZh58N9jp" crossorigin="anonymous">

    <!-- Roboto and Exo 2 Fonts -->
    <link rel="stylesheet" href="//fonts.googleapis.com/css?family=Roboto:400,500,700,400italic|Material+Icons">
    <link href="https://fonts.googleapis.com/css?family=Exo+2" rel="stylesheet">

    <title>contest.io</title>
  </head>
  <body>
    <noscript>
      <strong>We're sorry but client doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
    </noscript>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>
```


client/src/main.js

```
import Vue from 'vue';
import App from './App.vue';
import router from './router';

// Import Vuetify
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css'; // Ensure you are using css-loader

// Import Vue Moment
import moment from 'vue-moment';

// Use Vuetify
Vue.use(Vuetify, {
  theme: {
    primary: '#26A69A',
    secondary: '#00897B',
    accent: '#64DD17',
    error: '#f44336',
    warning: '#ffeb3b',
    info: '#2196f3',
    success: '#4caf50'
  }
});

// Use Vue-Moment for date formatting
Vue.use(moment);

Vue.config.productionTip = false;

new Vue({
  render: h => h(App),
  router
}).$mount('#app');
```


client/src/App.vue

```
<template>
  <div id="app">
    <!-- all elements need to be enclosed in v-app tags -->
    <v-app>

      <NavBar></NavBar>

      <router-view></router-view>

    </v-app>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';
export default {
  name: 'app',
  components: {
    NavBar
  }
};
</script>

<style>
#app {
  font-family: 'Exo 2', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
```


client/router/index.js

```
import Vue from 'vue';
import Router from 'vue-router';

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/contest/:id', component: 'ContestDashboard' },
  { path: '/profile/:id', component: 'Profile' },
  { path: '/contestcreate', component: 'CreateContest' },
  { path: '/dashboard', component: 'Dashboard' },
  { path: '*', component: '404Error' }
];

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  };
});

Vue.use(Router);

export default new Router({
  routes,
  mode: 'history'
});
```


client/src/components/404Error.vue

```
<template>
  <div>
    <div class="display-4 mt-5">404</div>
    <div class="display-2">Not Found</div>
    <div class="mt-4 title"><i>You have reached the Final Frontier!</i></div>
    <div class="subheading"><i>But there is no new life to seek out...</i></div>
  </div>
</template>
```


client/src/components/ContestDashboard.vue

```
<template>
  <div id="contestdashboard">
    <!-- Layout container -->
    <v-container>

      <v-layout>

        <v-flex xs6>

            <!-- Task List -->
            <v-subheader class="display-1" style="margin-top: 2% !important;">Contest {{ name }}</v-subheader>

            <router-link tag="v-avatar" to="/profile/1" class="grey lighten-4 avatar vlink" size="35px">
              <img src="https://vuetifyjs.com/static/doc-images/lists/1.jpg" alt="avatar">
              <div><v-subheader style="width: 200px;">Herr Hörner</v-subheader></div>
            </router-link>
            <v-expansion-panel popout>

             <v-expansion-panel-content v-for="item in items" :key="item.taskid">

               <div slot="header">{{ item.taskname }} <br><small style="float: left; margin-top: 9px; margin-right: 10px;">Difficulty ({{ item.codeforces_index }}): </small>
                   <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="float:left; width: 100px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="float:left; width: 100px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="float:left; width: 100px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="float:left; width: 100px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="float:left; width: 100px;" value="100" color="red"></v-progress-linear>
                   <v-progress-linear v-else style="float:left; width: 100px;" value="100" color="red"></v-progress-linear>
               </div>

              <v-card>

                <!-- Tags -->
                <div class="chiptag">
                  <v-chip small :key="tag"  v-for="tag in JSON.parse(item.tasktags)">{{ tag }}</v-chip>
                </div>

                <v-card-actions>
                  <v-btn flat color="orange" :href="item.codeforces_url">Solve</v-btn>
                </v-card-actions>

              </v-card>

             </v-expansion-panel-content>

           </v-expansion-panel>

        </v-flex>

        <v-flex xs2>
        </v-flex>

        <v-flex xs4>
          <v-card class="cardprogress">

            <v-card-title primary-title>
              <div  style="width: 100% !important">
                <h3 class="headline mb-0">Progress</h3>
                <v-divider></v-divider>
                <div>0 / {{ items.length }} Tasks completed (<span>{{ (0 / items.length) * 100 }}%</span>)</div>
                <div>Time remaining: 5 days, 11 hours</div>
              </div>
            </v-card-title>

          </v-card>
        </v-flex>

      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'contestdashboard',
  components: {},
  data() {
    return {
      items: [],
      name: ''
    };
  },
  mounted() {
    axios.get('/api/contests?code=' + this.$route.params.id).then(response => {
      this.items = response.data.tasks;
      this.name = response.data.contestname;
    });
  }
};
</script>

<style scoped>
.cardprogress {
	margin-top: 30% !important;
}
.avatar {
	margin-left: -52% !important;
	margin-bottom: 2%;
	margin-top: 1%;
}
.chiptag {
	margin-left: 10px;
}
.vlink {
	cursor: pointer;
}
</style>
```


client/src/components/CreateContest.vue

```
<template>
  <div id="createcontest">
    <!-- Layout container -->
    <v-container>
      <!-- Required field alerts -->
      <v-alert
        :value="alertTask"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        At least one task must be selected!
      </v-alert>

      <v-alert
        :value="alertDate"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        An ending date for the contest must be selected!
      </v-alert>

      <v-alert
        :value="alertName"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        A name for the contest must be entered!
      </v-alert>

      <v-alert
        :value="alertAxios"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        An error occured when attempting to create contest! ( {{ this.axiosError }} )
      </v-alert>

      <v-form>
        <v-layout>

          <!-- Add tasks -->
          <v-flex xs10 id="taskselection">
            <v-text-field prepend-icon="search" v-model="searchtitle" label="Search by name" solo-inverted class="mx-0 search" clearable flat></v-text-field>
            <div style="width: 100%;">
              <v-select style="float: right; width: 50%; margin-top: -32px;" v-model="selectedtags" label="Search by tags" chips tags solo prepend-icon="filter_list" append-icon="" clearable>
                <template slot="selection" slot-scope="data">
                  <v-chip :selected="data.selected" close @input="removeSelectedTag(data.item)" >
                    <span>{{ data.item }}</span>&nbsp;
                  </v-chip>
                </template>
              </v-select>
            </div>
            <div style="height: 320px; overflow: scroll; margin-top: 40px; min-width: 100%;">
              <v-list>

                <template v-if="!filteredItems.length">

                  <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>

                  <v-list-tile-content v-else>
                     <v-list-tile-title style="color: red; text-align: center;">No tasks match search parameters!</v-list-tile-title>
                  </v-list-tile-content>

                </template>

                <template v-for="item in filteredItems">

                  <!-- Detail view popup -->
                  <v-dialog v-model="detailPopup" max-width="500px" :key="item.taskid + '-popup'">
                    <v-card>
                      <v-card-title>
                        Detail
                      </v-card-title>
                      <v-card-text>
                        {{ item.taskname }}<br>
                        <small style="margin-right: 10px; float: left; margin-top: 8px; margin-left: 40%;">Difficulty ({{ item.codeforces_index }}): </small>
                        <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="width: 50px; margin-right: 50px; float: left;" value="20" buffer-value="20" color="green"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="width: 50px; margin-right: 50px; float: left;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="width: 50px; margin-right: 50px; float: left;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="width: 50px; margin-right: 50px; float: left;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="width: 50px; margin-right: 50px; float: left;" value="100" color="red"></v-progress-linear>
                        <v-progress-linear v-else style="width: 50px; margin-right: 50px; float: left;" value="100" color="red"></v-progress-linear><br>

                      </v-card-text>

                      <!-- Tags -->
                      <div class="text-xs-center chiptag">
                        <v-chip :key="tag" small v-for="tag in item.tasktags" >{{ tag }}</v-chip>
                      </div>

                      <v-card-actions>

                        <v-btn flat color="orange" :href="item.codeforces_url" target="blank">Solve</v-btn>
                        <v-btn color="primary" flat @click.stop="detailPopup=false">Close</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                   <v-divider :key="item.taskid + '-divider'"></v-divider>

                   <v-list-tile avatar :key="item.taskid + '-avatar2'" @click="() => {}">

                     <v-list-tile-action>
                         <v-icon @click="addTask(item.taskid)">add</v-icon>
                     </v-list-tile-action>

                    <v-list-tile-content @click="detailPopup=true">
                       <v-list-tile-title v-html="item.taskname"></v-list-tile-title>
                    </v-list-tile-content>

                    <small style="position: absolute; left: 380px;">Difficulty ({{ item.codeforces_index }}): </small>
                    <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="100" color="red"></v-progress-linear>
                    <v-progress-linear v-else style="position: absolute; left: 465px; top: 12px; width: 50px;" value="100" color="red"></v-progress-linear>

                    <v-chip :key="tag" small v-for="tag in item.tasktags.slice(0, 2)" >{{ tag }}</v-chip>

                   </v-list-tile>

                 </template>

             </v-list>
            </div>

            <!-- Task list -->
            <v-subheader style="margin-top: 5%;"> Tasks Selected so far </v-subheader>

            <p v-if="!tasks.length" style="color: red;">No tasks selected! Browse above tasks and click the '+' icon to add them!</p>
            <v-expansion-panel popout>

             <v-expansion-panel-content v-for="item in tasks" :key="item.id">

               <div slot="header">
                  {{ item.taskname }}<br>
                  <small style="float: left; margin-top: 9px; margin-right: 10px;">Difficulty ({{ item.codeforces_index }}): </small>
                   <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="float:left; width: 50px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="float:left; width: 50px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="float:left; width: 50px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="float:left; width: 50px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="float:left; width: 50px;" value="100" color="red"></v-progress-linear>
                   <v-progress-linear v-else style="float:left; width: 50px;" value="100" color="red"></v-progress-linear>
               </div>

              <v-card>



                <!-- Tags -->
                <div class="text-xs-center chiptag">
                  <v-chip :key="tag" small v-for="tag in item.tasktags" >{{ tag }}</v-chip>
                </div>

                <v-card-actions>
                  <v-btn flat color="red" @click="removeTask(item.taskid)">Remove</v-btn>
                  <v-btn flat color="orange" :href="item.codeforces_url" target="blank">Solve</v-btn>
                </v-card-actions>

              </v-card>

             </v-expansion-panel-content>

           </v-expansion-panel>
          </v-flex>

          <!-- Divider -->
          <v-flex xs1></v-flex>

          <!-- Misc Setup (Start / End time), Groups, etc. -->
          <v-flex xs4>
            <v-card>
              <v-card-text>
                <v-text v-if="contestdate">Contest End: {{ contestdate | moment("dddd, MMMM Do YYYY") }} (23:59)</v-text>
                <v-btn small color="primary" dark @click.stop="dialog2 = true">Choose a date...*</v-btn>

                <v-dialog v-model="dialog2" max-width="500px">
                  <v-card>
                    <v-card-title>
                      Choose an end date for the contest
                    </v-card-title>
                    <v-card-text>
                      <v-date-picker v-model="contestdate" :min="now"></v-date-picker><br>
                      <small>Note: Contests always end at 23:59!</small>
                    </v-card-text>
                    <v-card-actions>
                      <v-btn color="primary" flat @click.stop="dialog2=false">Close</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <br>
                <v-text>Groups:</v-text><br><v-divider></v-divider>
                <v-chip :key="group.name" v-for="group in selectedgroups" close @input="unselectGroup(group.name)">   {{ group.name }}</v-chip>
                <v-menu v-if="groups.length">
                  <v-btn small color="primary" dark slot="activator" fab><v-icon>add</v-icon></v-btn>
                  <!-- TODO: Get all groups this person is admin of -->
                  <v-list>
                    <v-list-tile v-if="!groups.length && !selectedgroups.length" style="color: red;">You are not a group admin!</v-list-tile>
                    <v-list-tile v-else v-for="group in groups" :key="group.name" @click="selectGroup(group.name)">
                      <v-list-tile-title><v-icon style="margin-top: -5px;">add</v-icon>  {{ group.name }}</v-list-tile-title>
                    </v-list-tile>
                  </v-list>
                </v-menu>
              </v-card-text>
            </v-card>

            <v-text-field required style="margin-top: 20px;" v-model="contestname" id="contestname" name="contestname" label="Contest Name"></v-text-field>
            <v-checkbox label="Public" v-model="visible"></v-checkbox>
            <v-btn type="button" large class="light-green accent-3 green--text text--darken-4" style="margin-top: 10px; width: 100%; margin-left: 0px;" to="" @click="postContest()">Create Contest</v-btn>
          </v-flex>

        </v-layout>
      </v-form>

    </v-container>
  </div>
</template>

<script>
// eslint-disable-next-line
import moment from 'vue-moment'
import axios from 'axios';
export default {
  name: 'createcontest',
  components: {
  },
  data () {
    return {
      searchtitle: '',
      searchtags: '',
      contestdate: '',
      dialog2: false,
      contestname: '',
      visible: false,
      detailPopup: false,
      first: 0,
      alertTask: false,
      alertDate: false,
      alertName: false,
      alertAxios: false,
      axiosError: '',
      items: [],
      selectedtags: [],
      tasks: [],
      groups: [ { name: 'Group 1' }, { name: 'Group 2' }, { name: 'Group 3' }, { name: 'Group 4' }, { name: 'Group 5' } ],
      selectedgroups: [],
      empty: [],
      loading: true
    };
  },
  methods: {
    // This method moves task object from items array to tasks array
    addTask(id) {
      var temp = this.items.find(x => x.taskid === id);
      this.items.splice(this.items.indexOf(temp), 1);
      this.tasks.push(temp);
    },
    // This method moves task object from tasks array to items array
    removeTask(id) {
      var temp = this.tasks.find(x => x.taskid === id);
      this.tasks.splice(this.tasks.indexOf(temp), 1);
      this.items.push(temp);
    },
    // Add groups to selection
    selectGroup(name) {
      var temp = this.groups.find(x => x.taskname === name);
      this.groups.splice(this.groups.indexOf(temp), 1);
      this.selectedgroups.push(temp);
    },
    // Remove groups to selection
    unselectGroup(name) {
      var temp = this.selectedgroups.find(x => x.taskname === name);
      this.selectedgroups.splice(this.selectedgroups.indexOf(temp), 1);
      this.groups.push(temp);
    },
    removeSelectedTag(item) {
      this.selectedtags.splice(this.selectedtags.indexOf(item), 1);
      this.selectedtags = [...this.selectedtags];
    },
    // This posts data to api
    postContest() {
      // Ensure required fields are filled out
      if(this.tasks.length == 0) {
        this.alertTask = true;
        setTimeout(() => {
          this.alertTask = false;
        }, 10000);
        return false;
      }
      if(this.contestdate == '') {
        this.alertDate = true;
        setTimeout(() => {
          this.alertDate = false;
        }, 10000);
        return false;
      }
      if(this.contestname == '') {
        this.alertName = true;
        setTimeout(() => {
          this.alertName = false;
        }, 10000);
        return false;
      }
      let config = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      };
      // Create AXIOS Post request
      axios.post('/api/contests', {
        'contestname': this.contestname,
        'date_start': new Date().toISOString().substring(0, 19),
        'date_end': this.contestdate,
        'visible': this.visible,
        'contestgroups': this.selectedgroups,
        'tasks': this.tasks.map(task => task.taskid)
      }, config)
        .then(function (resp) {
          window.location = '/contest/' + resp.data;
        })
        .catch(function (error) {
          this.axiosError = error;
          this.alertAxios = true;
          setTimeout(() => {
            this.alertAxios = false;
          }, 30000);
        });
    }
  },
  computed: {
    // Get current date
    now: function () {
      return new Date().toISOString().substring(0, 10);
    },
    filteredItems() {
      return this.items.filter(item => {
        return item.taskname.toLowerCase().includes(this.searchtitle.toLowerCase()) && this.selectedtags.every(selectedtag => item.tasktags.includes(selectedtag));
      });
    }
  },
  mounted() {
    axios.get('/api/tasks?tags=geometry')
      .then(response => {
        this.items = response.data;
        this.loading = false;
      });
  }
};
</script>

<style scoped>
.vlink {
  cursor: pointer;
}
#taskselection {
  margin-left: -10%;
}
.search {
  width: 45%;
  margin-bottom: -15px;
}
</style>
```


client/src/components/NavBar.vue

```
<template>
  <div id="navbar">

    <!-- Toolbar -->
    <v-toolbar dark color="primary">
      <!-- Side Bar Icon -->
      <v-toolbar-side-icon @click="drawer = true"></v-toolbar-side-icon>

      <router-link to="/" tag="v-toolbar-title" class="titlenavbar">Contest.io</router-link>

      <v-spacer></v-spacer>

      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn to="/dashboard" flat>Dashboard</v-btn>
        <v-btn flat href="/api/github-logout" v-if="loggedIn">Logout</v-btn>
        <v-btn flat @click="loginDialog=true" v-if="!loggedIn">Login</v-btn>
        <v-dialog v-model="loginDialog" max-width="500px">
        <v-card>
          <v-card-title>
            Login
          </v-card-title>
          <v-card-text>
            <v-btn color="grey darken-4" style="color: white" href="/api/github-login"><span style="font-size: 2em; margin-right: 10px;"><i class="fab fa-github"></i></span> Login with Github</v-btn>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="loginDialog=false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      </v-toolbar-items>

    </v-toolbar>

    <!-- Navigation sidebar -->

    <v-navigation-drawer
      v-model="drawer"
      temporary
      dark
      absolute
    >
      <v-list class="pt-0" dense>
        <span style="float: left; margin: 20px; margin-top: 15px;" class="title">Navigation</span>
        <v-btn small flat fab style="float: right; margin-top: 10px;" @click.stop="drawer = false"><v-icon>chevron_left</v-icon></v-btn>
        <v-divider light></v-divider>
        <v-list-tile v-for="link in links" :key="link.title" :to="link.url">
          <v-list-tile-action>
            <v-icon>arrow_right</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ link.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'navbar',
  components: {
  },
  data() {
    return {
      loginDialog: false,
      github: '',
      loggedIn: false,
      user: {},
      drawer: false,
      links: [
        { title: 'Home', url: '/' },
        { title: 'Contests', url: 'contests' }
      ]
    };
  },
  // See if a user is logged in
  created: function () {
    axios.get('/api/github-user')
      .then(resp => {
        if(!(resp.data == '401: Bad credentials')) {
          this.loggedIn = true;
          this.user = resp.data;
          console.log(resp);
        }
      });
  }
};
</script>

<style>
.titlenavbar:hover {
  cursor: pointer;
}
</style>
```



## 6.2 Code – Back-End
