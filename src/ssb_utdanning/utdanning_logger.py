from __future__ import annotations

import logging
import sys
from typing import Any

from colorama import Back
from colorama import Fore
from colorama import Style


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(
        self,
        *args: Any,
        colors: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the formatter with specified format strings."""
        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text."""
        record.color = self.colors.get(record.levelname, "")
        record.reset = Style.RESET_ALL

        return super().format(record)


formatter = ColoredFormatter(
    "{color} {levelname:8} {reset}| {message}",
    style="{",
    colors={
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.MAGENTA,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
    },
)



# Delete Jupyter notebook root logger handler
logger = logging.getLogger()
logger.handlers = []

# Create own logger
logger = logging.getLogger(__name__)
logger.handlers = []
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# prevent log messages from propagating to the root logger, which might add the unwanted double output.
logger.propagate = False

# Combine datadocs loggers into ours
dependent_loggers = [logging.getLogger('datadoc.config'), 
                     logging.getLogger('datadoc.config'),
                     logging.getLogger("datadoc.backend.datadoc_metadata"),
                     logging.getLogger("datadoc.backend.statistic_subject_mapping")]
for logr in dependent_loggers:
    logr.setLevel(logging.INFO)
    logr.handlers = []
    logr.addHandler(handler)
    logr.propagate = False

logger.setLevel(logging.INFO)
