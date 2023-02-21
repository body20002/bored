from enum import Enum
import logging


class Colors(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


FORMAT = (
    f"{Colors.RED.value}%(levelname)s{Colors.RESET.value}: {Colors.BLUE.value}%(name)s{Colors.RESET.value} "
    f"at {Colors.YELLOW.value}%(asctime)s "
    f"{Colors.GREEN.value}%(filename)s{Colors.BLUE.value}@{Colors.MAGENTA.value}"
    f"%(lineno)d{Colors.CYAN.value} %(message)s"
)


formatter = logging.Formatter(FORMAT)

logger = logging.getLogger("client")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()

ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
