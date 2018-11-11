# AVM
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

## Documentation
NO documentation yet. Sorry!