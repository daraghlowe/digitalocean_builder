# Development

## Running Locally

You must have [docker for mac](https://www.docker.com/docker-mac) installed locally to run this project.

With that installed, you should always be able to run:

```bash
make run
```

in the root of the project to bring up a local version of the application. You can then view your running application
at 127.0.0.1:8000/

You can also run

```bash
make shell
```

to open a bash shell on the running application.

### Using PyCharm

In order to have a nice development experience in PyCharm, there are a few basic
steps required.  Start by opening the base directory of this project in PyCharm,
then do the following:

#### 1. Enable Django support

Navigate to the [Django configuration](https://www.jetbrains.com/help/pycharm/django-2.html):

* `PyCharm > Preferences` (or press ⌘,)
* `Languages & Frameworks > Django` on the left menu
* Ensure that the `Enable Django Support` box is checked
* Ensure the follow values are set and then click the `Apply` button:

| Setting             | Value                                           |
|---------------------|-------------------------------------------------|
| Django project root | `[Git Root]/[Django root]` ex: `my-app/my-app`  |
| Settings            | `config/settings/dev.py`                        |
| Manage script      | `manage.py` (this should auto-populate)          |

#### 2. Configure the Python Interpreter

The docker-compose setup creates a "dev" sidecar container for use by PyCharm.
This container has the same version of Python as the application, as well as all
of the same libraries, with a few extra tools for running tests, linting, etc.
It also contains an SSH daemon, so that PyCharm (or other editors) can connect
to this container for development, rather than having to install Python locally
or configure a virtualenv.

The next step is to configure PyCharm to use this dev sidecar.  Be sure that
it is running (via `make up`) before this next step is performed.

Navigate to the [Remote Interpreter via SSH Configuration]:

* `PyCharm > Preferences` (or press ⌘,)
* `Project: [Project Name] > Project Interpreter`
* Click the gear to the right of the `Project Interpreter` dropdown
* Select `Add Remote`

In the model dialog, select `SSH Credentials` and ensure the following values
are set, then click the `OK` button:

| Setting          | Value                 |
|------------------|-----------------------|
| Host             | localhost             |
| Port             | 9922                  |
| Username         | root                  |
| Password         | password              |
| Interpreter Path | /usr/local/bin/python |

Also, setup 'Path Mappings' to:
Local: ~/Users/z.smith/Code/rdokr/rdokr # wherever your code is on your machine
Remote: /app # wherever your code is on the dev sidecar

*Note:*  If you have configured this interpreter previously, either for this or
another project, you can simply select the interpreter in the dropdown.  It should
have a generated name that looks something like this:

`3.6.1 (ssh://root@localhost:9922/usr/local/bin/python)` (the specific Python version number may be different if the dev
container uses a different base image)

#### 3. Configure the path mappings

So now you can edit files locally with PyCharm, but use the the dev sidecar to
introspect libraries for intellisense, run unit tests, etc.  However, you have to
tell PyCharm how to map file paths inside the container to file paths on your host machine.
This is done via [interpreter paths].  On the same `Project Interpreter` section from the previous step:

* Click the `...` box to right right of the `Path mappings` dropdown
* In the modal dialog, click the `+` bottom towards the bottom left (or press ⌘N)
* Add the following entry:

| Local Path    | Remote Path |
|---------------|-------------|
| $PROJECT_DIR$ | /workspace  |

*Note:* Type `$PROJECT_DIR$` exactly, this is not meant to be substituted.  This
tells PyCharm to use the base directory of the project for the mapping.

Next, be sure to **RESTART PYCHARM** so that the project directory will be interpreted correctly.  At this point the
intellisense and unit test runners should work.

## Updating Dependencies

We use [pip-tools](https://github.com/jazzband/pip-tools) to manage the project dependencies. Please update the
requirements.in file to add or restrict dependencies. Requirements.txt will automatically be updated when you run:

```bash
make build
```

requirements.indexes includes our private gemfury repo as an extra index. This is where we pull our custom python
packages from.

## Migrations

Use the following make command to make migrations.

```bash
make makemigrations
```

The migrations are automatically applied each time the web container is restarted.

## Connecting to the local DB

There is a make target that will connect you to the db when the application is running:

```bash
make psql
```

[Remote Interpreter via SSH Configuration]: https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html
[interpreter paths]: https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-reloading-interpreter-paths.html
