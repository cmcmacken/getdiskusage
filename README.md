# getdiskusage.py

[![Build Status](https://travis-ci.org/cmcmacken/getdiskusage.svg?branch=master)](https://travis-ci.org/cmcmacken/getdiskusage)



Print the disk usage for all the files at a given path

## Installation

1. Install Python 3.6+ in your $PATH
2. Requires GNU version of `du`
    1. On Mac OSX this can be installed as `gdu` via the homebrew `coreutils` package
2. Clone repository or download getdiskusage.py [here](https://raw.githubusercontent.com/cmcmacken/getdiskusage/master/getdiskusage.py)
3. Ensure `getdiskusage.py` is executable by executing the following command `chmod +x getdiskusage.py`
4. Run via `getdiskusage.py` or `python3 getdiskusage.py`

## Usage information

```
usage: getdiskusage.py [-h] [-u {b,m,g}] path

positional arguments:
  path                  The Path we use to report disk usage on

optional arguments:
  -h, --help            show this help message and exit
  -u {b,m,g}, --unit {b,m,g}
                        Unit used to report file size. b: byte, m: Mbyte, g:
                        Gbyte
  ```

## Running Unit tests

1. `git clone https://github.com/cmcmacken/getdiskusage.git`
2. `cd getdiskusage`
3. `python3 -m unittest`

## Integration tests

Ideally we would execute `getdiskusage.py` on the various linux distributions we care about and assert that it has sane output.

## Further considerations

### Authentication

I'm assuming that the endpoint which calls this would be behind some sort of sane API gateway which handles authentication and rate limiting. Ideally it would also handle limiting which directories user's can list if that's deemed necessary, otherwise that would need to be added.

### Logging

You would want to log all errors to a log file and ingest them somewhere to assist with debugging. Additionally you would want some kind of execution time report so you would watch for performance issues.