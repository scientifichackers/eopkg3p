from distutils.spawn import find_executable
from pathlib import Path


def _excecutable_not_found(name: str):
    exit(
        f"`{name}` executable not found. "
        f"Please make sure you have `{name}` installed on your system."
    )


def _find_executable(name: str) -> str:
    exc = find_executable(name)
    if exc is None:
        _excecutable_not_found(name)
    return exc


EOPKG = _find_executable("eopkg")
GIT = _find_executable("git")
PKEXEC = _find_executable("pkexec")

REPO_URL = "https://github.com/getsolus/3rd-party.git"
PSPEC_FILENAME = "pspec.xml"

CACHE_DIR = Path.home() / ".cache" / "eopkg3p"
REPO_DIR = CACHE_DIR / "3rd-party"
BUILD_DIR = CACHE_DIR / "builds"
