# AVM
[![Build Status](https://travis-ci.com/SevanSSP/avm.svg?token=3uQ4z5yHC2AVPsxguFuR&branch=master)](https://travis-ci.com/SevanSSP/avm)
## Description
Python package for interacting with DNV GL Software's Application Version Manager.

* List installed applications
* See which application version is marked as default
* Get path to application executables

Based on parsing the Application Version Manager XML file with application details.

## Installation
Install the package from Packagr using pip

```bash
pip install avm --extra-index-url https://api.packagr.app/EYvhW6SyL/ --disable-pip-version-check
```

## Usage
### Import package
Import *avm* and start using it.

```python
import avm
```  

Get the executable path of the 'wadam' application. Default version.

```python
from avm import exe_path

path = exe_path('wadam')
```  

Get the executable path of the 'wadam' application. Default version.

```python
from avm import exe_path

path = exe_path('wadam', version='9.4.3')
```  

### Command Line Interface (CLI)
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
