import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from textwrap import dedent
from typing import Dict, Tuple
from typing import Generator

from crayons import red, green

from .consts import (
    REPO_DIR,
    GIT,
    REPO_URL,
    PSPEC_FILENAME,
    BUILD_DIR,
    PKEXEC,
    EOPKG,
    CACHE_DIR,
)

if not CACHE_DIR.exists():
    CACHE_DIR.mkdir(parents=True)
if not BUILD_DIR.exists():
    BUILD_DIR.mkdir()


def get_installed_all() -> Generator[Tuple[str, int], None, None]:
    eopkg_process = subprocess.Popen(
        [EOPKG, "li", "-iN"], stdout=subprocess.PIPE, encoding="utf-8"
    )
    it = iter(eopkg_process.stdout)
    try:
        next(it)
    except StopIteration:
        return
    for line in it:
        parts = line.split("|")
        try:
            yield parts[0].strip(), int(parts[3])
        except IndexError:
            pass


def is_empty_dir(d: Path) -> bool:
    try:
        next(d.iterdir())
    except StopIteration:
        return True
    else:
        return False


def check_local_repo():
    return REPO_DIR.exists() and not is_empty_dir(REPO_DIR)


def update_local_repo():
    if REPO_DIR.exists():
        subprocess.check_call([GIT, "pull"], cwd=REPO_DIR)
    else:
        subprocess.check_call([GIT, "clone", REPO_URL, REPO_DIR])


def get_available() -> Dict[str, Path]:
    return {i.parent.name: i for i in REPO_DIR.rglob(PSPEC_FILENAME)}


def extract_latest_release(pspecfile: Path) -> int:
    relstr = ET.parse(pspecfile).find("History").find("Update").attrib["release"]
    try:
        return int(relstr)
    except ValueError as e:
        exit(
            dedent(
                f"""
                {red('Encountered', bold=True)} {repr(e)} 
                {red('while parsing the pspec file at:', bold=True)} {green(str(pspecfile))}.
                {red('Please report this issue, with a copy of this file.', bold=True)}
                """
            )
        )


def extract_description(pspecfile: Path) -> str:
    return ET.parse(pspecfile).find("Source").find("Description").text.strip()


def build_pspec(pspecfile: Path):
    dest = BUILD_DIR / pspecfile.parent.name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    subprocess.check_call(
        [PKEXEC, EOPKG, "bi", "--ignore-safety", pspecfile, "-O", dest]
    )
    return next(dest.iterdir())


def install_eopkg(eopkgfile: Path):
    subprocess.check_call([PKEXEC, EOPKG, "it", eopkgfile])


def filter_installed(available: Dict[str, Path]) -> Dict[str, Path]:
    return {
        name: available[name] for name, _ in get_installed_all() if name in available
    }


def filter_outdated(available: Dict[str, Path]) -> Dict[str, Path]:
    def _():
        for name, release in get_installed_all():
            try:
                pspecfile = available[name]
            except KeyError:
                continue
            if extract_latest_release(pspecfile) > release:
                yield name, pspecfile

    return dict(_())
