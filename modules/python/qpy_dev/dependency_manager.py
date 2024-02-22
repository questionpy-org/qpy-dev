import contextlib
import logging
from pathlib import Path

from poetry.core.packages.dependency import Dependency
from poetry.core.packages.package import Package
from poetry.inspection.info import PackageInfo

from qpy_dev.exceptions import QPyDevError

PACKAGE_DIRS = ("common", "sdk", "server")


class DependencyManager:
    def __init__(self, root_dir: str) -> None:
        self._logger = logging.getLogger(DependencyManager.__name__)
        self._root_dir = root_dir
        self._deps: list[tuple[Dependency, Package]] = []

    def run(self) -> None:
        for pkg_dir in PACKAGE_DIRS:
            pkg_info = PackageInfo.from_directory(
                Path(self._root_dir) / "questionpy" / pkg_dir,
                disable_build=True,
            )
            pkg = pkg_info.to_package()
            for dep in pkg.requires:
                if not dep.name.startswith("questionpy-"):
                    self._add(dep, pkg)

        print(";".join(str(d) for d, _ in self._deps))

    def _add(self, dep: Dependency, pkg: Package) -> None:
        with contextlib.suppress(StopIteration):
            # check for dependency conflict
            other_dep, other_pkg = next((d, p) for d, p in self._deps if d.name == dep.name)
            if other_dep:
                if other_dep != dep:
                    msg = f"Conflicting dependencies detected:\n  {dep} [{pkg.name}]\n  {other_dep} [{other_pkg}]"
                    raise QPyDevError(msg)
                return  # identical dep -> fine!
        self._deps.append((dep, pkg))
