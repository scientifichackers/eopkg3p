# eopkg3p

**A drop-in replacement for `eopkg` that supports Solus 3rd party packages!**

Also ships with a Python API, as a bonus.

## Install

```
$ pip3 install eopkg3p
```

Or, head over to [releases](https://github.com/pycampers/eopkg3p/releases) and download latest `eopkg3p` binary.

Python 3.6+ only    
MIT Lisence

## Dependenices

- Python 3.6+
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

[🐍🏕](http://www.pycampers.com/)
