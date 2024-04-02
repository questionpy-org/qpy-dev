## QuestionPy Development Environment

### Requirements

- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/engine/install/) (for running Moodle)
- [pyenv](https://github.com/pyenv/pyenv/blob/master/README.md#installation) (for installing multiple Python versions)

### Quick Start

```sh
$ git clone git@github.com:questionpy-org/qpy-dev.git
$ cd qpy-dev
$ poetry install --no-root
$ alias poe="poetry run poe"
$ poe venv:install
$ poe moodle:start
$ poe qpy:serve
```

### Usage

#### Running tasks

The most commonly used tasks.

| Task           | Description                                                                                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `venv:install` | **Collect and install all dependencies in dev environment.**<br>Can be executed when updating dependencies in a sub-project, switching branches, etc.                                    |
| `qpy:watch`    | **Run QuestionPy dev server in watch mode.**                                                                                                                                             |
| `docs:watch`   | **Start docs dev server in watch mode.**                                                                                                                                                 |
| `check`        | **Run all checks on projects.**<br>Runs checks *sequentially* against your current dev environment.<br>Preserves log output.                                                             |
| `toxp`         | **Run all checks on projects using tox.**<br>Runs checks *in parallel* in separate virtual environments (suppressing log output).<br>Runs test suites against supported Python versions. |
| `up`           | **Bump all versions in `pyproject.toml`.**                                                                                                                                               |
| `moodle:*`     | **Manage Moodle dev stack.**                                                                                                                                                             |

See the online help for a list of all available commands.

```sh
$ poe --help
```

#### Configuration

```sh
$ cp .env .env.local
```

Edit `.env.local` to your liking.

#### Tips

##### Persistent `poe` Alias

Add `poe` as an alias to your login shell.

```sh
$ echo 'alias poe="poetry run poe"' >> ~/.bash_profile
```

###### Install Python Versions

Install all required Python versions for testing. Pyenv is easiest, but other
methods work too.

```sh
$ pyenv install 3.11 3.12
```

##### Moodle start/stop hooks

Run arbitrary shell commands on Moodle start/shutdown. The example adds an
exception to the firewall, so Moodle can access the host QuestionPy server.

```sh
MOODLE_DOCKER_POST_START_HOOK="IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' qpy-dev-moodle-webserver-1); sudo iptables -A INPUT -s $IP/16 -j ACCEPT"
MOODLE_DOCKER_PRE_STOP_HOOK="IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' qpy-dev-moodle-webserver-1); sudo iptables -D INPUT -s $IP/16 -j ACCEPT"
```

### PR Waterfall

This repository does not address the PR waterfall issue directly that occurs
when pushing commits that include breaking changes. But it does encourage to
check against the other packages before pushing.

When pushing code/merging PRs that involve multiple repositories, you will need
to respect the package's dependency graph, meaning you have to adhere to a
particular order to avoid failed CI pipelines.

1. questionpy-common
1. questionpy-server
1. questionpy-sdk
1. questionpy-docs

Also, related PRs should be grouped and accepted in a timely manner to reduce
friction for other developers as much as possible.
