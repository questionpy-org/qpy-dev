## QuestionPy Development Environment

### Requirements

- [Poetry](https://python-poetry.org/docs/#installation)

### Quick Start

```sh
$ git clone git@github.com:questionpy-org/qpy-dev.git
$ cd qpy-dev
$ poetry install
$ alias poe="poetry run poe"
$ poe qpy:start
```

### Usage

See the online help for a list of available commands and their descriptions.

```
$ poe --help
```

### Goals & Non-Goals

#### Goals

- **Aggregate common developer tasks and work flows in a central place.**  
  When developers can share a common workflow, DX, general productivity as well
  as reproducibility should improve. A friendly place called `./scratch/` invites
  developers to share unfinished/experimental code and data.

- **Provide a single virtual environment for developing.**  
  Managing a separate virtual env for each project manually is tedious and
  repetitive. Instead *a single* development environment is used that is managed
  automatically and can be used by tools such as type checkers, linters and
  IDEs.

- **Manage dependencies across multiple `pyproject.toml` Python projects.**  
  Manually sync'ing dependencies across a number of Python projects can quickly
  become cumbersome and error-prone. An automated strategy is implemented that
  helps to carry out this task in a safe and reproducible manner.

- **Handle package interdependencies during development.**  
  Unfortunately Poetry does not yet support overriding dependencies to use
  a local path package during development or other advanced techniques (such
  as *workspaces*): python-poetry/poetry#1168  
  Therefore we handle those dependencies from within the dev environment by
  altering Poetry behaviour, leaving the actual packages fully intact with fixed non-path dependency specs.

#### Non-Goals

- **Handle package interdependencies during release.**  
  This project **does not** solve the PR waterfall issue that occurs when
  commiting changes that involve multiple QuestionPy packages.  
  Developers have to take care to create and merge PRs in the correct order,
  so inter-project dependencies don't cause failed CI pipelines or defunct code.

### Persistent `poe` Alias

```sh
$ echo 'alias poe="poetry run poe"' >> ~/.bash_profile
```
