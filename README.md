# AVM
[![Build Status](https://travis-ci.com/SevanSSP/avm.svg?token=3uQ4z5yHC2AVPsxguFuR&branch=master)](https://travis-ci.com/SevanSSP/avm)
## Description
Python package for interacting with DNV GL Software's Application Version Manager.

* List installed applications
* See which application version is marked as default
* Get path to application executables

Based on parsing the Application Version Manager XML file with application details.

## Installation
Install the package from PyPri using pip

```bash
pip install --extra-index-url  https://api.python-private-package-index.com/EYvhW6SyL/ avm
```

**Note that the PyPri account is not yet active and the package is therefore not available for download.**

## Usage
### Import package
Import *avm* and start using it.

```python
import avm
```  

Get the executable path of the 'wadam' application. Default version.

```python
from avm import get_exe_path

path = get_exe_path('wadam')
```  

Get the executable path of the 'wadam' application. Default version.

```python
path = get_exe_path('wadam', version='9.4.3')
```  

### Console entry point
List details about the applications and versions registered in Application Version Manager.

Only default application versions.

```bash
avm-list
```

All versions

```bash
avm-list --all-versions
```

Toggle logger level so that debug-level info is piped to console.

```bash
avm-list --all-versions --logging-level debug
```

## Documentation
No documentation yet. Sorry!