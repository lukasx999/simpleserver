from .simple_client import main as client_main
from .simple_server import main

VERSION = "0.1.0"

__exports__ = [main, client_main]
