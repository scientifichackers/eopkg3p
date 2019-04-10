# eopkg3p

**A drop-in replacement for `eopkg` that supports Solus 3rd party packages!**

Also ships with a Python API, as a bonus.

## Install

Just download, make executable and run!

```
$ wget https://github.com/pycampers/eopkg3p/releases/download/v0.0.6/eopkg3p
$ chmod +x ./eopkg3p
$ ./eopkg3p
```

[Releases](https://github.com/pycampers/eopkg3p/releases)

---

Or, install using `pip`

```
$ pip3 install eopkg3p
```

Python 3.6+ only    
MIT Lisence

## Dependenices

- `python3.6`
- `git`
- `eopkg`
- `pkexec`


## Usage

If you know `eopkg`, you _already_ know `eopkg3p`.

```
$ eopkg3p 
Usage: eopkg3p [OPTIONS] COMMAND [ARGS]...

Options:
  --cache  Output the cache dir.
  --help   Show this message and exit.

Commands:
  delete-cache    (dc) Delete cache files
  install         (it) Install packages
  list-available  (la) List all packages available in the local repository.
  list-installed  (li) List all 3rd party packages that are currently...
  remove          (rm) Alias for `eopkg rm`
  update-repo     (ur) Update the local repository
  upgrade         (up) Upgrade 3rd party packages
```

## Why?

Installing and updating 3rd party packages is a real pain from the Software center. 
This package elimitates that problem.

---

## API
`eopkg3p` has a Python API as a bonus and can be imported like so:
`import eopkg3p`


#### `build_pspec(pspecfile: Path)`
Build eopkg package of a 3rd party app based on the app's pspec file from the `Path` object in the `pspecfile` argument.
`pspecfile` has to be a `Path` object.

&nbsp;
#### `check_local_repo()`
Check that the local repository directory (`$HOME/.cache/eopkg3p/3rd-party`) exists and that it's not empty.

&nbsp;
#### `extract_description(pspecfile: Path)`
Return the description of a 3rd party app as a string based on the app's pspec file from the `Path` object in the `pspecfile` argument.

&nbsp;
#### `extract_latest_release(pspecfile: Path)`
Return the release number of a 3rd party app as an integer based on the app's pspec file from the `Path` object in the `pspecfile` argument.

&nbsp;
#### `filter_installed(available: Dict[str, Path]) -> Dict[str, Path]*`
If given the argument `available` as a `dict` object with string as first argument and a `Path` object as the second argument, the function will return a dict object with only the installed 3rd party apps.

&nbsp;
#### `filter_outdated(available: Dict[str, Path]) -> Dict[str, Path])`
If given the argument `available` as a `dict` object with string as first argument and a `Path` object as the second argument, the function will return a dict object with only the outdated 3rd party apps.

&nbsp;
#### `get_available() -> Dict[str, Path]`
Return a `dict` with the name of the available 3rd party apps as a string as the key and the POSIX-path to their pspec.xml file as the value.

&nbsp;
#### `get_installed_all() -> Generator[Tuple[str, int], None, None]`
Return all installed apps and their release number as a generator object.

&nbsp;
#### `install_eopkg(eopkgfile: Path)`
Install eopkgfile with `eopkg` based on the app's pspec file from the `Path` object in the `pspecfile` argument.

&nbsp;
#### `update_local_repo()`
Install eopkgfile from `file` with eopkg based on the pspec file.


[🐍🏕](http://www.pycampers.com/)
