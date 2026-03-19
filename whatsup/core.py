"""Core re-exports for the whatsup package."""

from whatsup.config import get_all_projects, get_project, load_config
from whatsup.transport import Transport
from whatsup.transport.telegram import TelegramTransport

__all__ = [
    "load_config",
    "get_project",
    "get_all_projects",
    "Transport",
    "TelegramTransport",
]
