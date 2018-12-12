import shutil
import subprocess
from pathlib import Path
from textwrap import fill, indent
from typing import Iterable, Dict

import click
from crayons import yellow, green, red, cyan

from . import core
from .__version__ import __version__
from .consts import REPO_DIR, REPO_URL, EOPKG, PKEXEC, CACHE_DIR


@click.command()
def update_repo():
    """(ur) Update the local repository"""
    print(f"Updating repository: {green(REPO_URL)}...")
    core.update_local_repo()


def parse_package_names(packages: Iterable[str], available: Dict[str, Path]):
    try:
        return {name: available[name] for name in map(str.strip, packages)}
    except KeyError as e:
        exit(
            f"{red('Repo item', bold=True)} {cyan(e.args[0])} {red('not found!', bold=True)}"
        )


@click.command()
@click.argument("packages", nargs=-1)
@click.option("--reinstall", is_flag=True)
@click.option("--yes", "-y", help="Don't ask for confirmation.", is_flag=True)
def install(packages, reinstall, yes):
    """(it) Install packages"""
    if not packages:
        print("Nothing to do...")
        return

    available = core.get_available()
    try:
        packages = parse_package_names(packages, available)
    except KeyError as e:
        print(
            f"{red('Repo item', bold=True)} {cyan(e.args[0])} {red('not found!', bold=True)}"
        )
        return

    to_install_set = set(packages)
    if not reinstall:
        all_installed_set = set(core.filter_installed(available))
        installed_set = to_install_set.intersection(all_installed_set)
        to_install_set = to_install_set - installed_set

        if installed_set:
            print(
                yellow(
                    "The following packages(s) are already installed and are not going to be installed again:"
                )
            )
            for i in installed_set:
                print(i)
    print("The following packages are going to be installed:")
    for i in to_install_set:
        print(cyan(i))

    if not (yes or click.confirm("Continue?", default=True)):
        return

    for name in to_install_set:
        pspec = available[name]
        eopkg = core.build_pspec(pspec)
        core.install_eopkg(eopkg)


@click.command()
@click.argument("packages", nargs=-1)
def remove(packages):
    """(rm) Alias for `eopkg rm`"""
    subprocess.run([PKEXEC, EOPKG, "rm", *packages])


@click.command()
def list_available():
    """(la) List all packages available in the local repository."""
    available = core.get_available()
    installed = core.filter_installed(available).keys()

    head_width = max(map(len, available)) + 1
    descrip_indent = head_width + 3
    descrip_width = shutil.get_terminal_size().columns - descrip_indent

    for name, pspec in available.items():
        head = name.rjust(head_width)
        if name in installed:
            head = green(head)
        descrip = core.extract_description(pspec)
        descrip = indent(fill(descrip, descrip_width), " " * descrip_indent)

        print(head, "-", descrip[descrip_indent:])


@click.command()
def list_installed():
    """(li) List all 3rd party packages that are currently installed."""
    available = core.get_available()
    installed = core.filter_installed(available)

    head_width = max(map(len, installed)) + 1
    descrip_indent = head_width + 3
    descrip_width = shutil.get_terminal_size().columns - descrip_indent

    for name, pspec in installed.items():
        head = name.rjust(head_width)
        descrip = core.extract_description(pspec)
        descrip = indent(fill(descrip, descrip_width), " " * descrip_indent)

        print(head, "-", descrip[descrip_indent:])


@click.command()
def delete_cache():
    """(dc) Delete cache files"""
    print(f"Deleting all caches ({green(CACHE_DIR)})...")
    shutil.rmtree(CACHE_DIR)
    print("Done!")


@click.command()
@click.argument("packages", nargs=-1)
@click.option("--yes", "-y", help="Don't ask for confirmation.", is_flag=True)
@click.pass_context
def upgrade(ctx: click.Context, packages, yes):
    """(up) Upgrade 3rd party packages"""
    ctx.invoke(update_repo)

    available = core.get_available()
    if packages:
        packages = parse_package_names(packages, available)
    else:
        packages = available

    outdated = core.filter_outdated(packages)
    if not outdated:
        print("No packages to upgrade.")
        return

    print("The following packages are going to be upgraded:")
    for i in outdated:
        print(cyan(i))

    if not (yes or click.confirm("Continue?", default=True)):
        return

    for name, pspec in outdated.items():
        eopkg = core.build_pspec(pspec)
        core.install_eopkg(eopkg)


class AliasedGroup(click.Group):
    invoke_without_command = True

    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


@click.command(cls=AliasedGroup, invoke_without_command=True, no_args_is_help=True)
@click.option("--cache", help="Output the cache dir.", is_flag=True)
@click.option("--version", help="Output version information.", is_flag=True)
def cli(cache, version):
    if cache:
        print(CACHE_DIR)
        exit()
    if version:
        print(__version__)
        exit()
    if not core.check_local_repo():
        print(red("Local repo not found!", bold=True))
        try:
            REPO_DIR.rmdir()
        except FileNotFoundError:
            pass
        core.update_local_repo()


cli.add_command(install)
cli.add_command(remove)
cli.add_command(update_repo)
cli.add_command(list_available)
cli.add_command(list_installed)
cli.add_command(delete_cache)
cli.add_command(upgrade)

ALIASES = {
    "ur": update_repo,
    "it": install,
    "rm": remove,
    "la": list_available,
    "li": list_installed,
    "dc": delete_cache,
    "up": upgrade,
}

if __name__ == "__main__":
    cli()
