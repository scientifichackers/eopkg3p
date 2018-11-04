#!/usr/bin/env bash

# clean old build
rm -r dist shiv_build
mkdir shiv_build dist

pip install -r  <(pipenv lock -r) --target dist/

# specify which files to be included in the build
# You probably want to specify what goes here
cp -r \
-t dist \
eopkg3p

# finally, build!
shiv --site-packages dist --compressed -p '/usr/bin/env python3.6' -o shiv_build/eopkg3p -e eopkg3p.cli:cli