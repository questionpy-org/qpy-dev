import logging
import os
from pathlib import Path
from typing import Literal

import tomlkit
from poetry.core.factory import Factory
from poetry.core.packages.dependency_group import MAIN_GROUP

poe_root_str = os.environ.get("POE_ROOT", "")
if not poe_root_str:
    msg = "POE_ROOT is not set"
    raise ValueError(msg)
poe_root = Path(poe_root_str)

logging_level = os.environ.get("QPY_DEV_LOG_LEVEL", "INFO")
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


PkgName = Literal["common", "sdk", "server"]


class CheckToolingConfig:
    PACKAGE_DIRS = ("common", "sdk", "server")
    GROUPS = (MAIN_GROUP, "dev", "test", "linter", "type-checker")
    BANNED_DEPS = ("pylint", "flake8", "tox")

    def __init__(self, root_dir: Path, pkg_name: PkgName) -> None:
        self._pkg_dir = root_dir / "questionpy" / pkg_name
        self._issues: list[str] = []
        self._pyproject = self._load_pyproject()

    def check(self) -> list[str]:
        self._check_deps()
        self._check_tox_config()
        return self._issues

    def _check_deps(self) -> None:
        poetry = Factory().create_poetry(self._pkg_dir)
        pkg = poetry.package.with_dependency_groups(CheckToolingConfig.GROUPS, only=True)
        for dep in pkg.all_requires:
            for banned_dep in CheckToolingConfig.BANNED_DEPS:
                if dep.name == banned_dep:
                    self._issues.append(f"Found {dep.name} in dependencies")

    def _check_tox_config(self) -> None:
        if self._pyproject["tool.tox"]:
            self._issues.append("Found tool.tox table")

    def _load_pyproject(self) -> tomlkit.TOMLDocument:
        with open(self._pkg_dir / "pyproject.toml", encoding="utf-8") as f:
            return tomlkit.load(f)


def check_config(pkg_name: PkgName) -> None:
    """Check repo pyproject.toml for tooling issues."""
    check_tooling_config = CheckToolingConfig(poe_root, pkg_name)
    check_tooling_config.check()
