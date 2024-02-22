import logging
import os
import sys

from qpy_dev.dependency_manager import DependencyManager
from qpy_dev.exceptions import QPyDevError


def run() -> None:
    poe_root = os.environ.get("POE_ROOT")
    if poe_root is None:
        raise ValueError("POE_ROOT is not set")
    logging_level = os.environ.get("QPY_DEV_LOG_LEVEL")
    if logging_level is None:
        raise ValueError("QPY_DEV_LOG_LEVEL is not set")

    logging.basicConfig(level=logging_level)
    logger = logging.getLogger(__name__)

    manager = DependencyManager(poe_root)
    try:
        manager.run()
    except QPyDevError as exc:
        logger.error(exc)
        logger.error("You need to resolve the conflicting requirement specifiers")
        sys.exit(-1)
