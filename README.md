# AVM

![Build and test package](https://github.com/SevanSSP/avm/actions/workflows/test.yml/badge.svg?branch=master)
![Publish Python package to Packagr](https://github.com/SevanSSP/avm/workflows/Publish%20Python%20package%20to%20Packagr/badge.svg)

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
