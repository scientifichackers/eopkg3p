import shutil
import subprocess
from textwrap import fill, indent

import click
from crayons import yellow, green, red, cyan

from . import core
from .consts import REPO_DIR, REPO_URL, EOPKG, PKEXEC, CACHE_DIR


@click.command()
def update_repo():
    """(ur) Update the local repository"""
    print(f"Updating repository: {green(REPO_URL)}...")
    core.update_local_repo()
    print("Done!")


@click.command()
@click.argument("packages", nargs=-1)
@click.option("--reinstall", is_flag=True)
def install(packages, reinstall):
    """(it) Install packages"""
    if not packages:
        print("Nothing to do...")
        return

    available = core.get_available()
    try:
        packages = {name: available[name] for name in map(str.strip, packages)}
    except KeyError as e:
        print(
            f"{red('Repo item', bold=True)} {cyan(e.args[0])} {red('not found!', bold=True)}"
        )
        return

    package_set = set(packages)
    if not reinstall:
        all_installed_set = set(core.get_installed(available))
        installed_set = package_set.intersection(all_installed_set)
        package_set = package_set - installed_set

        if installed_set:
            print(
                yellow(
                    "The following packages(s) are already installed and are not going to be installed again:"
                )
            )
            for i in installed_set:
                print(i)

    for name in package_set:
        eopkg = core.build_pspec(available[name])
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
    installed = core.get_installed(available).keys()

    maxsize = max(map(len, available)) + 1
    des_indent = maxsize + 3
    des_width = shutil.get_terminal_size().columns - des_indent

    for name, pspec in available.items():
        head = f"%-{maxsize}s" % name
        if name in installed:
            head = green(head)
        des = core.get_description(pspec)
        des = indent(fill(des, des_width), " " * des_indent)

        print(head, "-", des[des_indent:])


@click.command()
def list_installed():
    """(li) List all 3rd party packages that are currently installed."""
    available = core.get_available()
    installed = core.get_installed(available)

    maxsize = max(map(len, installed)) + 1
    des_indent = maxsize + 3
    des_width = shutil.get_terminal_size().columns - des_indent

    for name, pspec in installed.items():
        head = f"%-{maxsize}s" % name
        des = core.get_description(pspec)
        des = indent(fill(des, des_width), " " * des_indent)

        print(head, "-", des[des_indent:])


@click.command()
def delete_cache():
    """(dc) Delete cache files"""
    print(f"Deleting all caches ({green(CACHE_DIR)})...")
    shutil.rmtree(CACHE_DIR)
    print("Done!")


@click.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def upgrade(ctx: click.Context, packages):
    """(up) Upgrade 3rd party packages"""
    ctx.invoke(update_repo)

    available = core.get_available()
    if packages:
        try:
            packages = {name: available[name] for name in map(str.strip, packages)}
        except KeyError as e:
            print(
                f"{red('Repo item', bold=True)} {cyan(e.args[0])} {red('not found!', bold=True)}"
            )
            return
    else:
        packages = available

    packages = core.get_outdated(packages)

    if not packages:
        print("No packages to upgrade.")
        return

    print("The following packages are going to be upgraded:")
    for i in packages:
        print(i)
    if click.confirm("Continue?"):
        for name, pspec in packages.items():
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
def cli(cache):
    if cache:
        print(CACHE_DIR)
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
