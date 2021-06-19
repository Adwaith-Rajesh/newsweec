import logging
import os
from pathlib import Path

from rich.logging import RichHandler

logging.getLogger("urllib3.connectionpool").disabled = True
logging.getLogger("schedule").disabled = True
logging.getLogger("filelock").disabled = True


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    handlers=[RichHandler()],
)

LOG_FILE_FOLDER = os.path.join(Path(__file__).parent.parent, "logs")


class Logger:
    def __init__(
        self,
        logger: logging.Logger,
        base_level: int,
        filename: str,
        _format: str = "%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    ) -> None:

        self._file_path = os.path.join(LOG_FILE_FOLDER, filename)

        self.logger = logger
        self.logger.setLevel(level=base_level)

        if filename:
            self.file_handler = logging.FileHandler(filename=self._file_path)
            self.formatter = logging.Formatter(_format)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

    def log(self, level: int, message: str) -> None:
        self.logger.log(level=level, msg=message)
