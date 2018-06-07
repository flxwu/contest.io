# Table Of Contents

- [1. Abstract](#1-abstract)
    + [1.1. Motivation](#11-motivation)
    + [1.2. Contest.io - Programmierwettbewerbe für den Informatikunterricht und die Privatnutzung](#12-contestio---programmierwettbewerbe-fur-den-informatikunterricht-und-die-privatnutzung)
- [2. Ausblick](#2-ausblick)
- [3. Version Control](#3-version-control)
- [4. Dokumentation – Front-End](#4-dokumentation--front-end)
  * [4.1. Das Framework - Vue.js](#41das-framework---vuejs)
    + [4.1.1. Was ist das Front-End? Und Wozu ein Framework?](#411-was-ist-das-front-endund-wozu-ein-framework)
    + [4.1.2. Warum Vue?](#412--warum-vue)
  * [4.2 Weitere verwendete Bibliotheken](#42--weitere-verwendete-bibliotheken)
- [5. Dokumentation – Back-End ([Flask](flask.pocoo.org))](#5-dokumentation-%E2%80%93-back-end-flaskflaskpocooorg)
  * [5.0. Wofür ein Back-End-Framework?](#50-wofur-ein-back-end-framework)
  * [5.1. Warum Flask?](#51-warum-flask)
    + [5.1.1 Weitere verwendete externe Bibliotheken](#511-weitere-verwendete-externe-bibliotheken)
  * [5.2 Datenbank](#52-datenbank)
  * [5.4. Dateienstruktur](#54-dateienstruktur)
        * [`__init__.py`](#__init__py)
  * [5.4. Security](#54-security)
  * [5.5. Coding Style und Linting](#55-coding-style-und-linting)
- [6. Continious Integration und Maintainability](#6-continious-integration-und-maintainability)
  * [6.1. Continious Integration](#61-continious-integration)
    + [6.1.1. Travis CI](#611-travis-ci)

## 1. Abstract   

### 1.1. Motivation
Programmierwettbewerbe und die dazugehörenden Plattformen wie **Codeforces** sind unter versierten Informatik(-studenten) sehr beliebt. Nach anfänglicher Testphase hat sich herausgestellt, dass das Konzept, die Aufgaben und die generelle Idee auch vielseitig im Informatikunterricht an der Schule eingesetzt werden kann, jedoch kamen recht früh Probleme auf:

1. Die Runden finden immer zu festen Zeiten statt und sind immer zweistündig, bieten also zeitlich sehr geringe Flexibilität.
2. Viele Aufgaben gehen weit über den Schulstoff hinaus und somit sind nur ein Bruchteil der Aufgaben im schulischen Rahmen lösbar. Dies stellt in sofern ein Problem dar, dass die Codeforces-Runden immer 5-7, nach Schwierigkeit gestaffelte Aufgaben inkludieren, wovon dann für die meisten Schüler nur die ersten beiden realistisch lösbar sind.
3. Es gibt kein "Lehrer-Schüler" System.

Insbesondere unter Betrachtung des dritten Punktes taten sich viele Möglichkeiten auf, eine eigene solche Plattform zu erweitern - Es sollte Gruppen/Klassen geben, in welchen die Admins/Lehrer in Echtzeit mitverfolgen können, wie weit jeder ihrer Schüler ist. So kann der Lehrer eine Runde aus den seiner Meinung nach passenden Aufgaben erstellen, diese seinen Klassen A,B und C zuweisen und innerhalb jeder Klasse mitverfolgen, welche Aufgaben welchen Schülern Probleme bereiten.

### 1.2. Contest.io - Programmierwettbewerbe für den Informatikunterricht und die Privatnutzung
Diese Plattform nannten wir **contest.io**. Contest.io soll die Probleme 1. und 2. durch ein System lösen, in welchem jeder (in erster Linie jedoch die Admins/Lehrer) jederzeit Runden aus selbst erwählten Aufgaben erstellen kann und diese entweder öffentlich - also für jeden zugänglich - oder privat mit fester Zuweisung an Gruppen/Klassen machen kann. Des Weiteren ermöglicht unsere Plattform das bereits erwähnte Analysieren der Leistungen von Gruppen/Klassen.

## 2. Ausblick  

In Zukunft können zusätzliche Erweiterungen wie zum Beispiel Folgende implementiert werden:

- Punkte-System und somit ein Rang-System mit "Elo"
- Einschließen weiterer Fragekataloge neben Codeforces
- Weitere Möglichkeiten des Einloggens 
- Detailliertere und funktionsreichere Profile und Gruppen

# 3. Version Control

# 4. Dokumentation – Front-End

## 4.1.	Das Framework - ([Vue.js](https://vuejs.org))

### 4.1.1. Was ist das Front-End?	Und Wozu ein Framework?   

Das Front-End beschreibt der Teil einer Webseite, mit dem der User direkt interagiert. Was der User sieht, worin er tippt, worauf er klickt: das alles gehört zum Fronr-End.

Ein Front-End Framework erlaubt das Schaffen dynamische Webseiten und Single-Page-Applications, die für komplexe Web-Apps wie dieses Projekt, wenn nicht unbedingt notwendig, jedenfalls ungemein nützlich sind.  

Das Framework erlaubt auch sogenanntes 'lokal testing', das heißt, dass das Framework problemlos auf dem Computer des Developers einen test-server aufbaut und darauf läuft. Zum testen kann der Devloper nun diesen server per Browser ansteuern und sieht die fertige Webseite, wie sie nach dem finalen 'deploy' (das aufsetzen auf den echten server) aussehen und funktionieren wird. So können bugs erkannt und eliminiert werden.

### 4.1.2.	Warum Vue?  

Für contest.io haben wir uns für das relative neue Framework Vue.js 2.0 entschieden, da es schnell und komprimierter ist und trotzdem große Leistung besitzt. Vue besitzt ebenfalls eine große Community mit vielen hilfreichen Plugins, die einem das Programmieren erleichtern.  

Vue sorgt dafür, dass nur veränderte Komponenten neu vom server geladen werden, und minimiert somit unnötige downloads und Berechnungen. Der Vue-Router erlaubt einfache Navigation von Seiten und verhindert auch unnötigen Web-Traffic.

## 4.2	Weitere verwendete Bibliotheken  

Jedes größere Projekt mit Frameworks benötigt außerdem einige zusätzlichen Tools. Allgemein haben wir ([Vuetify](https://vuetifyjs.com)) als Design-Plugin genommen, welches das standardisierte Google-Material-Design auf die Webseite überträgt. ([Axios](https://github.com/axios/axios)) erlaubt die Verbindung von Front- und Back-End. ([Webpack](https://webpack.js.org)) kompiliert den Vue code, um ihn für den Browser lesbar zu machen. Außerdem wurden einige kleine Plugins wie `vue-moment` auch benutzt.

# 5. Dokumentation – Back-End ([Flask](flask.pocoo.org))

## 5.0. Wofür ein Back-End-Framework?

Das Back-End ist bei einer "Full-Stack"-Webapplikation, also einer Applikation bestehend aus Front-End und Back-End, der Begriff für den Server und den darauf laufende Software. Nun fragt man sich, wofür man denn überhaupt ein Back-End braucht, und das ist eine berechtigte Frage, denn: Lange funktionierten Webseiten ohne Serverstruktur, reine _Client-Websiten_ also. Und auch heute wird wieder mehr auf _serverless-architecture_ gesetzt, auch wenn hierbei letztendlich die Serverarbeit vom Cloud-Provider betrieben wird.

Dass wir uns dennoch für ein Back-End entschieden haben, liegt letztendlich an zwei wesentlichen Gründen:

1. Wir benötigen eine Datenbank für alle unsere Operationen rund um die Aufgaben, Wettbewerbe, Nutzer und Gruppen. Diese aus dieser Datenbank verfügbaren Daten müssen überall gleich und verfügbar sein, egal wo der Nutzer gerade über seinen Client - bzw. das Front-End - auf unseren Dienst zugreift.
2. Echtzeit-Analyse ist nur mit einem Server möglich. In unserem Fall bedeutet dies, dass alle Nutzer zur selben Zeit angezeigt bekommen, wie weit ein Wettbewerb fortgeschritten ist oder wie weit die Mitstreiter sind.

## 5.1. Warum Flask?

Im Vorfeld stand relativ schnell für uns fest, dass wir im Back-End entweder das auf Node.js basierende JavaScript-BackEnd-Framework [Express.js](https://github.com/expressjs/express) oder etwas eher Neues verwenden würden. Express.js hatte den Vorteil, dass wir beide Erfahrung mit JavaScript und dem Framework haben und vor allem der Einstieg deutlich leichter gewesen wäre. Viel entscheidender war jedoch, dass Express.js als JavaScript-Framework deutlich kompatibler mit unserem Front-End Framework Vue.js sein würde.

Dennoch ist es letztendlich Flask geworden, da ich recht gut Python beherrsche und bereits Erfahrung mit [Django](https://djangoproject.com/), einem extrem funktionsreichen und komplexen Python-BackEnd-Framework, hatte, und wir etwas Neues ausprobieren wollten. Jedoch war die Erfahrung mit _Django_ aufgrund der extremen Größe und Komplexität eher negativ und da wir nicht vor hatten, Facebook nachzubauen, entschieden wir uns für die schnellere, einfacher zu erlernende und deutlich unkomplexere Alternative Flask. Nachdem wir also nach einiger Recherche sichergestellt hatten, dass Vue.js und Flask größtenteils reibungsfrei kombinierbar sind, stand diese Entscheidung also fest.

### 5.1.1 Weitere verwendete externe Bibliotheken

- [requests](http://docs.python-requests.org/) - Netzwerkoperationen
- [gunicorn](http://gunicorn.org/) - HTTP Server für Flask
- [autopep8](https://github.com/hhatto/autopep8) - Coding-Style-Convention (s. [hier](#43-coding-style-und-linting))
- [pylint](https://github.com/PyCQA/pylint) - "Linting" (s. [hier](#43-coding-style-und-linting))
- [python-dotenv](https://github.com/theskumar/python-dotenv) - .env support (s. [hier](#42-security))

## 5.2 Datenbank
Folglich ist das ER-Diagramm abgebildet. Als Query-Language dient [Sqlite3](https://www.sqlite.org/)
![ER Diagramm](er-diagram.png)

## 5.4. Dateienstruktur
```
server/
├── api
│   ├── api_connector.py
│   ├── endpoint_interface.py // interface für alle Klassen in api_connector
│   └── __init__.py // leer, nur zur kennzeichnung als Python-Paket
├── database
│   ├── __init__.py // leer, nur zur kennzeichnung als Python-Paket
│   ├── models.py
│   └── schema.sql // sqlite3 schema - abgeleitet aus ER-Diagramm
├── __init__.py 
└── settings.py
```

### 5.4.1. Wichtigste Dateien
##### `__init__.py`
Diese Datei wird zu Beginn aufgerufen und enthält alle [API-Endpunkte](https://github.com/flxwu/contest.io/blob/master/README.md), die vom Front-End aufgerufen werden. Diese stellen die Schnittstelle vom Server/Datenbank zur Außenwelt und dem Front-End dar, des Weiteren gibt es API-Endpunkte für die Authentication mit Github.

#### `settings.py`
Diese Datei lädt die Umgebungsvariablen aus der `.env` Datei (s. [hier](#42-security)) und enthält alle Spaltennamen der Datenbank als Konstanten, um im Code Tippfehler zu vermeiden.

#### `models.py`
Hier finden sich sämtliche Methoden zur direkten Interaktion mit der Datenbank - Einfügen, Lesen, Aktualisieren, Löschen.

### `api_connector.py`
Hier sind mehrere Klassen, die jeweilig Daten von der Codeforces-API holen, diese zu für uns kompatiblen Formaten umwandeln und die benötigten Daten extrahieren, wie zum Beispiel die Aufgaben.

## 5.4. Security
Da auch wir einige _Secrets_, also "geheime" Schlüssel wie die Api Keys von Github, in unserem Back-End verwenden, entschied ich mich, die [12-factor](http://12factor.net/)-Prinzipien anzuwenden, um diese Schlüssel nicht der Öffentlichkeit zu offenbaren, zumal wir unseren Code öffentlich auf Github hosten.

Aus diesem Grund verwenden wir die Python-Version von `dotenv`, eine ursprünglich für Node.js(JavaScript) entwickelte Software zum Laden von globalen Umgebungsvariablen aus einer `.env` Datei.
Dies bedeutet, wir deklarieren in unseren `.env` Dateien die benötigten _Secrets_:
```bash
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
SECRET_KEY=...
```
Diese werden dann vom Back-End geladen und benutzt, dabei wird die Datei von Git ignoriert, das heißt jeder inklusive uns, der das Projekt lokal ausprobieren/entwickeln möchte, muss eine solche Datei erstellen, einen eigenen Github Api-Key generieren und diesen einfügen.

## 5.5. Coding Style und Linting
Linting bezeichnet das Analysieren von Code auf potenzielle Fehler, wie vergessene Klammern, falsche Einrückungen oder fehlerhafte Variablendeklerationen.
Dafür wird im Back-End die Software `pylint` benutzt.

Coding Style bezeichnet das Aussehen des Codes - und dafür gibt es Konventionen. Die in Python am weitesten verbreiteste is `autopep8`. Dieses Programm formatiert automatisch den Code und meldet Verstöße gegen die Konvention.


# 6. Continious Integration und Maintainability
Wir haben von Anfang an versucht, unser Projekt möglichst "maintainable" zu halten: Dies bedeutet, dass wir potenziellen Nachfolgern oder Mitprogrammieren den Einstieg durch weitesgehende Automatisierungen vereinfachen.

## 6.1. Continious Integration

Continious Integration beschreibt den automatisierten Prozess des Zusammenfügens, Packetierens, Testens und letztlich Vertriebs der Software.
Wesentliches Ziel ist also die Steigerung der Softwarequalität, da dadurch menschliche Eingriffe in das "Deployment" vermieden werden.

### 6.1.1. Travis CI
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

### 6.1.2. CodeFactor und CodeClimate
Dies sind beides weitere Tools zur Bewertung und Überprüfung unseres Codes auf mögliche Fehler, Ungereimtheiten und vermeintliche unschöne Passagen wie Wiederholungen etc.

![CodeClimate](codeclimate.png)
*CodeFactor und CodeClimate Dashboards*
