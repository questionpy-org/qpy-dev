import contextlib
import logging
import os
import sys
from operator import attrgetter
from pathlib import Path

from poetry.core.factory import Factory
from poetry.core.packages.dependency import Dependency
from poetry.core.packages.dependency_group import MAIN_GROUP
from poetry.core.packages.package import Package

poe_root_str = os.environ.get("POE_ROOT", "")
if not poe_root_str:
    msg = "POE_ROOT is not set"
    raise ValueError(msg)
poe_root = Path(poe_root_str)

logging_level = os.environ.get("QPY_DEV_LOG_LEVEL", "INFO")
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


class VersionConstraintError(Exception):
    pass


class DependencyMerger:
    PACKAGE_DIRS = ("common", "sdk", "server")
    GROUPS = (MAIN_GROUP, "dev", "test", "linter", "type-checker")

    def __init__(self, root_dir: Path) -> None:
        self._root_dir = root_dir
        self._deps: dict[str, tuple[Dependency, Package]] = {}

    def merge(self) -> None:
        for pkg_dir in DependencyMerger.PACKAGE_DIRS:
            poetry = Factory().create_poetry(Path(self._root_dir) / "questionpy" / pkg_dir)
            pkg = poetry.package.with_dependency_groups(DependencyMerger.GROUPS, only=True)
            for dep in pkg.all_requires:
                if not dep.name.startswith("questionpy-"):
                    self._add(dep, pkg)

    @property
    def deps(self) -> list[Dependency]:
        return sorted((dep for dep, _ in self._deps.values()), key=attrgetter("name"))

    def _add(self, dep: Dependency, pkg: Package) -> None:
        other_dep, other_pkg = None, None

        # do we have this dep already?
        with contextlib.suppress(KeyError):
            other_dep, other_pkg = self._deps[dep.name]

        # merge deps
        if other_dep:
            # version constraint
            dep.constraint = dep.constraint.intersect(other_dep.constraint)

            if dep.constraint.is_empty():
                msg = (
                    "Conflicting dependencies detected (no common versions):\n"
                    f"  {dep} [{pkg.name}]\n"
                    f"  {other_dep} [{other_pkg}]"
                )
                raise VersionConstraintError(msg)

            # handle extras
            dep = dep.with_features(dep.extras.union(other_dep.extras))

        self._deps[dep.name] = dep, pkg


manager = DependencyMerger(poe_root)


def create_requirements() -> None:
    """Merge QuestionPy package dependencies and save as requirements file."""
    try:
        manager.merge()
        with open(poe_root / "requirements-dev.txt", "w", encoding="utf-8") as f:
            for dep in manager.deps:
                f.write(f"{dep}\n")
    except VersionConstraintError:
        logger.exception("You need to resolve the conflicting requirement specifiers")
        sys.exit(-1)


def check() -> None:
    """Check QuestionPy package dependencies."""
    try:
        manager.merge()
        for dep in manager.deps:
            logger.info("%s", dep)
    except VersionConstraintError:
        logger.exception("You need to resolve the conflicting requirement specifiers")
        sys.exit(-1)
