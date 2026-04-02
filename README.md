# PyKasm

[![PyPI Version](https://badge.fury.io/py/kasm.svg)](https://badge.fury.io/py/kasm)
![Tests](https://github.com/Codoc-os/pykasm/workflows/Tests/badge.svg)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](#)
[![License MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/Codoc-os/pykasm/blob/main/LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/Codoc-os/pykasm/badge)](https://www.codefactor.io/repository/github/Codoc-os/pykasm)

**PyKasm** is an unofficial Python client for the [Kasm API](https://docs.kasm.com/docs/latest/developers/developer_api/index.html). It lets you manage users and Kasm sessions, as well
as retrieve information about images.

## Features

* Provide a high-level interface to create / update and delete users.
* Provide a high-level interface request, manage and destroy Kasm sessions.
* Provide low-level clients to directly interact with the Kasm API.
* Support both synchronous and asynchronous HTTP requests.

## Requirements

**Pykasm** needs an officially [supported versions](https://devguide.python.org/versions/) of
Python (mainstream & LTS).

## Installation

Install via `pip`:

```bash
pip install kasm
```

## Versioning

**PyKasm** follows a `major.minor.patch.revision` versioning scheme. The `major.minor.patch` parts
corresponds to the Kasm API version, while `revision` is incremented for bugfixes and new features.

So if you want to use Kasm API 1.18.0, you should install `kasm>=1.18.0, <1.18.1`. Older version
**PyKasm** might work with a newer API version, but this is not guaranteed.
