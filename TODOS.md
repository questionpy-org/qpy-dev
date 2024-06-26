## Todos

- **Manage unified single virtual env**
  - [x] Install repo deps in a unified dev venv
    - [x] Installing in less pip calls possible? Maybe just use a temporary `requirements.txt`?
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
  - post-checkout hook that sets up venv automatically?
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
        - [x] PHP_CodeSniffer (https://docs.moodle.org/dev/Linting)
      - [x] Format (check)
      - [x] Type-check
      - [x] Test
        - [x] pytest
        - [x] coverage/report
        - [x] phpunit (https://moodledev.io/general/development/process/testing)
    - [x] Bump versions in `pyproject.toml`
    - [ ] git tasks
      - [x] git clone
        - [x] all repos
        - [x] some repos, single repo
        - [x] .github repo
      - [ ] git pull/fetch (to see if there have been pushes)
    - [x] tox task
      - [x] make sure dev repos are used in tox
      - [x] add pyenv to requirements/add pyenv instructions
    - [ ] Run GH actions locally using [act](https://github.com/nektos/act)?
    - [ ] Sync tooling config into QPy repos
      - [x] `ruff_defaults.toml`
      - [ ] Use tomlkit to sync tooling config (`pyproject.toml`)
        - [ ] dependencies: check pylint, flake8, tox is not present
        - [ ] check `tool.tox` is not presence
        - [ ] check no `tool.pylint*` are present
        - [ ] mypy, check keys/values from qpy-dev config are present and match
        - [ ] `tool.pytest.ini_options`
          - `asyncio_mode = "auto"`, ignore others
          - `tool.coverage.run`
            - `branch = true`
            - `source = [MODULE_NAME]`
        - [ ] ruff
          - check `extend = "ruff_defaults.toml"` option is present
          - check that `extend-*` variants are used
  - Docs
    - [x] Build docs using mkdocs
    - [x] Watch docs
    - [x] ~~Publish docs~~ ([solved using GitHub actions](https://github.com/questionpy-org/questionpy-docs/pull/8/commits/b7ebd6b38e2d66887b7b052da7e462ad674677f4))
- **Update tooling**
  - [x] Add ruff (replacing Pylint, Flake8)
    - Possible to have preset rules (like Eslint sharable config)?  
      - No, not yet. https://github.com/astral-sh/ruff/discussions/3363
        - [x] Can be mimicked by using [`extend`](https://docs.astral.sh/ruff/settings/#extend)  
          Solution: Have `ruff_defaults.toml` in `qpy-dev` and create command that sync's it into the QPy repos.  
          Look at [hatch default config](https://hatch.pypa.io/latest/config/static-analysis/#default-settings)  
          https://github.com/pypa/hatch/blob/master/ruff_defaults.toml
    - Ruff import formatting not configurable  
      https://github.com/astral-sh/ruff/issues/2600
  - [x] Remove tox config from individual repos
  - [X] Update GH actions
  - Other less important
    - [ ] Add https://github.com/commitizen-tools/commitizen?
    - [ ] Fix this bug and create PR: https://github.com/nat-n/poethepoet/issues/198
    - [ ] pre-commit-hook
      - lint/test/...
      - lint conventional commit messages
