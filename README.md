# pyrd

**pyrd** is a library providing bindings for the Real-Debrid API. Premium account required for most endpoints.

# Usage

## Installation

```console
$ pip install pyrd
```

## Using the API

```python
from realdebrid import RealDebrid

rd = RealDebrid("TOKEN HERE")
print(rd.user.get().json())
```

# Credits

This project is inspired by [s-krilla/rd_api_py](https://github.com/s-krilla/rd_api_py). pyrd is intended to be a maintained, modern recreation of rd_api_py.
