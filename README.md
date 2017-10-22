mtcli is a command line tool to access the [MeisterTask](http://www.meistertask.com) API.

It is licensed under the GPL, version 2.

# Installation

```
pip install -r requirements.txt
```

alternatively, use it with virtualenv:
```
virtualenv mtcli
cd mtcli
Scripts/activate
pip install -r requirements.txt
```

The tool is self-describing. `--help` is your friend. Basic syntax is (so far):
```
mtcli.py project [list|show|set]
mtcli.py section [list]
```

You have to supply an API key, either via the `--apikey` option:
```
mtcli.py --apikey foo123 project list
```
...or by putting it into `mtcli.conf` (in the current directory) or `~/.mtcli.conf` (in your homedirectory).
A sample mtcli.conf file is included.


