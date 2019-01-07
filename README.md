2434-youtube-wikiwiki
===

CLI app to generate statement for WIKIWIKI.jp from にじさんじ's Youtube video list.

Requirements for development
---
- Python>=3.5
- virtualenv

Getting Started
---
### Clone this repository
```
$ pip3 install virtualenv
$ git clone https://github.com/KarageAgeta/2434-youtube-wikiwiki.git
$ cd 2434-youtube-wikiwiki
```

### Edit `.env.copy`
```
$ cp .env.copy .env
$ vi .env
```

### Activate venv and install requirements
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -e ".[debug]"
```

### Set Flasak App path
```
$ export FLASK_APP=run.py
```

Commands
---
Get Youtube video list and generate statement for WIKIWIKI.jp
```
$ flask generate-youtube-wikiwiki
```

flake8
---
```
$ flake8 run.py myapp
```

License
---
```
Copyright 2018 Yoko Karasaki

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
