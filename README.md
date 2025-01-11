<p align="center">
  <a href="https://github.com/mouraworks/docowling">
    <img loading="lazy" alt="Docowling" src="https://github.com/mouraworks/docowling/raw/main/docs/assets/docowling.png" width="80%"/>
  </a>
</p>

# Docowling

[![Docs](https://img.shields.io/badge/docs-live-brightgreen)](https://github.com/mouraworks/docowling/)
[![PyPI version](https://img.shields.io/pypi/v/docowling)](https://pypi.org/project/docowling/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/docowling)](https://pypi.org/project/docowling/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

**Docowling**  is a fork of the [Docling](https://github.com/DS4SD/docling), an IBM project, developed to enhance functionalities and add new document processing capabilities.

## Why Docowling?
Like an owl watching for all prey, docowling is a fork intended to attack all types of documents.

<p align="center">
  <a href="https://github.com/mouraworks/docowling">
    <img loading="lazy" alt="Docowling" src="https://github.com/mouraworks/docowling/raw/main/docs/assets/docowling_csv.png" width="80%"/>
  </a>
</p>

## Features

* 📄 Converts popular formats (CSV, PDF, DOCX, PPTX, XLSX, Images, HTML, AsciiDoc & Markdown) to HTML, Markdown and JSON with embedded/referenced images
* 🧩 Unified DoclingDocument format for standardized representation
* 🤖 Ready-to-use integrations with LangChain, LlamaIndex, Crew AI & Haystack
* 💻 Intuitive CLI for efficient batch processing with customizable export parameters

## Coming Soon

* 📄 More formats compatibility
* 🤖 Optimize integrations with LangChain, Crew AI & Weaviate

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
print(result.document.export_to_markdown())  # output: "## Docowling Technical Report[...]"
```
```python
from docowling.document_converter import DocumentConverter

source = "/content/drive/MyDrive/TESLA.csv"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  
# output: "| Date     |      Open |      High [...]"
```

## License

The Docowling codebase is under MIT license.
For individual model usage, please refer to the model licenses found in the original packages.

## IBM ❤️ Thanks
Thank you IBM for creating Docling, the base of Docowling.