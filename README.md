<p align="center">
  <a href="https://github.com/mouraworks/docowling">
    <img loading="lazy" alt="Docowling" src="https://github.com/mouraworks/docowling/raw/main/docs/assets/docowling.png" width="80%"/>
  </a>
</p>

# Docowling

[![Docs](https://img.shields.io/badge/docs-live-brightgreen)](https://github.com/mouraworks/docowling/)
[![PyPI version](https://img.shields.io/pypi/v/docling)](https://pypi.org/project/docowling/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/docling)](https://pypi.org/project/docling/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License MIT](https://img.shields.io/github/license/mouraworks/docowling/)](https://opensource.org/licenses/MIT)

**Docowling**  is a fork of the [Docling](https://github.com/DS4SD/docling), an IBM project, developed to enhance functionalities and add new document processing capabilities.

## Installation

To use Docowling, simply install `docowling` from your package manager, e.g. pip or uv:
```bash
pip install docowling
```

```bash
uv pip install docowling
```

Works on macOS, Linux and Windows environments. Both x86_64 and arm64 architectures.

## Getting started

To convert individual documents, use `convert()`, for example:

```python
from docowling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"
```

## License

The Docowling codebase is under MIT license.
For individual model usage, please refer to the model licenses found in the original packages.
