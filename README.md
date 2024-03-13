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

#### Available Tasks

See the online help for a list of available commands and their descriptions.

```
$ poe --help
```

#### Configuration

```
$ cp .env .env.local
```

Edit `.env.local` to your liking.

#### Tips

##### Persistent `poe` Alias

Add `poe` as an alias to your login shell.

```sh
$ echo 'alias poe="poetry run poe"' >> ~/.bash_profile
```

##### Running `tox`

`poe toxp` is probably the most useful command as it runs all checks in parallel
against your current dev code. Run it whenever you are about to create PRs or
push code.

###### Install Python Versions

Install all required Python versions for testing. Pyenv is easiest, but other
methods work too.

```
$ pyenv install 3.9 3.10 3.11
```

##### Moodle start/stop hooks

Run an arbitrary shell command on Moodle start/shutdown. The examples add an
exception to the firewall, so Moodle can access the host QuestionPy server.

```
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
