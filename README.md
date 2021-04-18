# cocomo-python

## How to run

Start poetry env

```bash
pip install poetry # if don't have poetry installed
poetry install
poetry shell
```

In the poetry environment, execute the module to download and generate the value of coconut 
```bash
python -m src json packages.json  # estimate cocomo from json
python -m src package_history <lib>  # download all versions and estimate cocomo
python dashboard.py # start dashboard
```

## Dependencies
To calculate cococo we are using SCC, so make sure you have it installed on your system
https://github.com/boyter/scc

## Database

We have two models, one for the package history and the other for the packages downloaded in their latest versions via json.


### Package history
```Python
from src.database import Package
```
| arg         | type     | comment |
| ---         | ----     | ------- |
| name        | str      | Package name. "Flask", "Django", "NumPy" .... |
| license     | str      | Package license "GPL", "MIT", ...             |
| url         | str      | Pypi URL                                      |

### PackageHistory
```python
from src.database import PackageHistory
```
| arg         | type        | comment |
| ---         | ----        | ------- |
| name        | FK(Package) |         |
| version     | str         | Package version "1.1.0" ....         | 
| total_cost  | int         | scc cocomo value                     |
| total_lines | int         | scc total lines of package           |
| package_url | str         | url to download this package version | 
| package_name| str         | real package name: "mypy-1.1a.1.whl" |
| downloaded  | bool        |                                      | 
| date        | datetime    | date the package was uploaded        | 
| label       |             |                                      |
| packge_type | str         | wheel, tar, eggs ...                 |

### LastPackage
```Python
from src.database import LastPackage
```
| arg         | type        |
|------       | -----       |
| name        | FK(Package) |
| version     | str         |
| total_cost  | int         |
| total_lines | int         |
| group       | str         |
