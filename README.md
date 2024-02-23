## QuestionPy Development Environment

### Requirements

- [Poetry](https://python-poetry.org/docs/#installation)

### Quick Start

```sh
$ git clone git@github.com:questionpy-org/qpy-dev.git
$ cd qpy-dev
$ poetry install --no-root
$ alias poe="poetry run poe"
$ poe moodle:start
$ poe qpy:install
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

#### Persistent `poe` Alias

Add `poe` alias to your login shell.

```sh
$ echo 'alias poe="poetry run poe"' >> ~/.bash_profile
```

### Todos

- **Manage unified single virtual env**
  - [x] Install repo deps in a unified dev venv
    - [ ] Installing in less pip calls possible? Maybe just use a tempory `requirements.txt`?
  - [ ] "Dependency Merger" (creates list of conflict-free dependencies from all repos)
      - [x] Implement merger
      - [x] Check if repo deps are conflict-free
      - [ ] Consider all (optional) groups
      - [ ] Use `dict[dep.name, tuple[Dep, Pkg]]` for `DependencyMerger._deps`?
      - [ ] Use (version constraint) intersection of conflicting deps
        - Raise error if result is empty
      - [ ] Consider dep extras: use union of conflicting deps extras
      - (Idea: Choose one or the other interactively when a conflict occurs. Can also be done manually/is probably overkill.)
- **Common developer tasks and workflows**
  - [ ] linter/type-checker/tests
    - [ ] tox config to run all all/some/single repository
  - [ ] common git tasks?
    - [ ] git clone
      - [x] all repos
      - [ ] some repos, single repo
    - [ ] git pull
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
    - [ ] Start/stop hooks (mainly need this for creating/removing a Firewall rule to allow the Moodle webserver container to access the QPy server on my host)
  - [ ] Handle QPy server
    - [ ] Tasks
      - [x] start dev server
      - [ ] watch dev server
    - [x] Create `config.ini`
    - [x] Pass env vars
    - [x] Create cache directories
- **Update tooling**
  - [ ] Add ruff (replacing Pylint, Flake8)
    - [ ] Possible to have preset rules (like Eslint sharable config)?  
      - No, not yet. https://github.com/astral-sh/ruff/discussions/3363
        - [ ] Can be mimicked by using [`extend`](https://docs.astral.sh/ruff/settings/#extend)  
          Solution: Have `ruff_defaults.toml` in `qpy-dev` and create command that sync's it into the QPy repos.
        - Look at [hatch default config](https://hatch.pypa.io/latest/config/static-analysis/#default-settings)  
          https://github.com/pypa/hatch/blob/master/ruff_defaults.toml
    - [ ] Add common ruleset to all 3 repos
    - [ ] Add `ruff format --check` to tox
    - [ ] Add `ruff format` task
  - [ ] Add https://github.com/commitizen-tools/commitizen?
  - [ ] Fix this bug and create PR: https://github.com/nat-n/poethepoet/issues/198

### Non-Goal

- Not addressing the PR waterfall issue that occurs when commiting changes that
  involve multiple QuestionPy packages. No idea how to do this (unless
  migrating ot a monorepo)...
