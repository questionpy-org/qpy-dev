import contextlib
import logging
import os
import sys
from collections.abc import Iterable
from pathlib import Path

from poetry.core.packages.dependency import Dependency
from poetry.core.packages.package import Package
from poetry.inspection.info import PackageInfo

PACKAGE_DIRS = ("common", "sdk", "server")

poe_root = os.environ.get("POE_ROOT")
if poe_root is None:
    msg = "POE_ROOT is not set"
    raise ValueError(msg)
logging_level = os.environ.get("QPY_DEV_LOG_LEVEL")
if logging_level is None:
    msg = "QPY_DEV_LOG_LEVEL is not set"
    raise ValueError(msg)

logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


class PackageConflictError(Exception):
    pass


class DependencyMerger:
    def __init__(self, root_dir: str) -> None:
        self._logger = logging.getLogger(DependencyMerger.__name__)
        self._root_dir = root_dir
        self._deps: list[tuple[Dependency, Package]] = []

    def merge(self) -> None:
        for pkg_dir in PACKAGE_DIRS:
            pkg_info = PackageInfo.from_directory(
                Path(self._root_dir) / "questionpy" / pkg_dir,
                disable_build=True,
            )
            pkg = pkg_info.to_package()
            for dep in pkg.all_requires:
                if not dep.name.startswith("questionpy-"):
                    self._add(dep, pkg)

    @property
    def deps(self) -> Iterable[Dependency]:
        return (dep for dep, _ in self._deps)

    def _add(self, dep: Dependency, pkg: Package) -> None:
        with contextlib.suppress(StopIteration):
            # check for dependency conflict
            other_dep, other_pkg = next((d, p) for d, p in self._deps if d.name == dep.name)
            if other_dep != dep:
                msg = f"Conflicting dependencies detected:\n  {dep} [{pkg.name}]\n  {other_dep} [{other_pkg}]"
                raise PackageConflictError(msg)
            return  # identical dep -> fine!
        self._deps.append((dep, pkg))


manager = DependencyMerger(poe_root)


def merge() -> None:
    """Merge QuestionPy package dependencies and print as semicolon separated string."""
    try:
        manager.merge()
        print(";".join(str(dep) for dep in manager.deps))
    except PackageConflictError:
        logger.exception("You need to resolve the conflicting requirement specifiers")
        sys.exit(-1)


def check() -> None:
    """Check QuestionPy package dependencies."""
    try:
        manager.merge()
        for dep in manager.deps:
            logger.info("%s", dep)
        logger.info("=> Dependencies are sync'ed.")
    except PackageConflictError:
        logger.exception("You need to resolve the conflicting requirement specifiers")
        sys.exit(-1)
