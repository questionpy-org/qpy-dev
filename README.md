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

Run all tox tasks in parallel.

```sh
$ poe tox -p
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

### Todos

- **Manage unified single virtual env**
  - [x] Install repo deps in a unified dev venv
    - [x] Installing in less pip calls possible? Maybe just use a tempory `requirements.txt`?
  - [x] "Dependency Merger" (creates list of conflict-free dependencies from all repos)
      - [x] Implement merger
      - [x] Check if repo deps are conflict-free
      - [x] Consider all (optional) groups
        - [x] And remove them from qpy-dev `pyproject.toml`
      - [x] Use `dict[dep.name, tuple[Dep, Pkg]]` for `DependencyMerger._deps`?
      - [x] Use (version constraint) intersection of conflicting deps
        - Raise error if result is empty
      - [x] Consider dep extras: use union of conflicting deps extras
      - (Idea: Choose one or the other interactively when a conflict occurs. Can also be done manually/is probably overkill.)
- **Common developer tasks and workflows**
  - post-checkout hook that set ups venv automatically?
  - [x] Manage Moodle dev stack
    - [x] Tasks
      - [x] start
      - [x] stop
      - [x] reset/remove
      - [x] log tail
      - [x] access to docker-compose command
    - [x] Automate config (`local.yml`)
      - [x] Add `host.docker.internal` to webserver container `/etc/hosts` so QPy server can be specified by using a fixed hostname in Moodle
      - [x] `qtype-questionpy` as bind volume into the webserver container
    - [x] Start/stop hooks (mainly need this for creating/removing a Firewall rule to allow the Moodle webserver container to access the QPy server on my host)
  - [x] QPy server
    - [x] Tasks
      - [x] start dev server
      - [x] watch dev server
    - [x] Create `config.ini`
    - [x] Pass env vars
    - [x] Create cache directories
  - Per repo tasks
    - [x] All some/repos
      - [ ] Lint
        - [x] ruff
        - [ ] PHP_CodeSniffer (https://docs.moodle.org/dev/Linting)
      - [x] Format (check)
      - [x] Type-check
      - [ ] Test
        - [x] pytest
        - [x] coverage/report
        - [ ] phpunit (https://moodledev.io/general/development/process/testing)
    - [ ] git tasks
      - [x] git clone
        - [x] all repos
        - [x] some repos, single repo
      - [ ] git pull/fetch (to see if there have been pushes)
    - [x] tox task
      - [x] make sure dev repos are used in tox
      - [x] add pyenv to requirements/add pyenv instructions
    - [ ] Sync tooling config into QPy repos
      - [x] `ruff_defaults.toml`
      - [ ] Use tomlkit to sync tooling config (`pyproject.toml`)
        - [ ] dependencies: check pylint, flake8, tox is not present
        - [ ] check `tool.tox` is not presence
        - [ ] mypy, check keys/values from qpy-dev config are present and match
        - [ ] `tool.pytest.ini_options`
          - `asyncio_mode = "auto"`, ignore others
          - `tool.coverage.run`
            - `branch = true`
            - `source = [MODULE_NAME]`
        - [ ] ruff
          - check `extend = "ruff_defaults.toml"` option is present
          - check that `extend-*` variants are used
        - [ ] check no `tool.pylint*` are present
  - Docs
    - [ ] Build docs using mkdocs
    - [ ] Open docs in browser
    - [ ] Publish docs
- **Update tooling**
  - [ ] Add ruff (replacing Pylint, Flake8)
    - Possible to have preset rules (like Eslint sharable config)?  
      - No, not yet. https://github.com/astral-sh/ruff/discussions/3363
        - [x] Can be mimicked by using [`extend`](https://docs.astral.sh/ruff/settings/#extend)  
          Solution: Have `ruff_defaults.toml` in `qpy-dev` and create command that sync's it into the QPy repos.  
          Look at [hatch default config](https://hatch.pypa.io/latest/config/static-analysis/#default-settings)  
          https://github.com/pypa/hatch/blob/master/ruff_defaults.toml
  - [ ] Add https://github.com/commitizen-tools/commitizen?
  - [ ] Fix this bug and create PR: https://github.com/nat-n/poethepoet/issues/198
  - [ ] Remove tox config from individual repos
  - [ ] Update GH actions
  - [ ] pre-commit-hook
    - lint/test/...
    - lint conventional commit messages
