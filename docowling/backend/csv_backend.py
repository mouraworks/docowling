import csv
import logging
from io import BytesIO, StringIO
from pathlib import Path
from typing import Dict, List, Set, Union

import chardet
from docling_core.types.doc import (
    DoclingDocument,
    DocumentOrigin,
    GroupLabel,
    TableCell,
    TableData,
)

from docowling.backend.abstract_backend import DeclarativeDocumentBackend
from docowling.datamodel.base_models import InputFormat
from docowling.datamodel.document import InputDocument

_log = logging.getLogger(__name__)


class CsvDocumentBackend(DeclarativeDocumentBackend):
    def __init__(self, in_doc: "InputDocument", path_or_stream: Union[BytesIO, Path]):
        super().__init__(in_doc, path_or_stream)
        self.rows = []
        self.valid = False
        self.file = path_or_stream if isinstance(path_or_stream, Path) else None
        self.encoding = "utf-8"

        try:
            # Load and detect CSV dialect
            if isinstance(self.path_or_stream, Path):
                # First detect the encoding
                with self.path_or_stream.open(mode="rb") as file:
                    raw_content = file.read()
                    self.encoding = self._detect_encoding(raw_content)

                # Now read with proper encoding
                with self.path_or_stream.open(mode="r", encoding=self.encoding) as file:
                    content = file.read()
                    if not content.strip():
                        self.valid = True
                        return

                    dialect = self._detect_dialect(content)
                    self.rows = self._parse_csv(content, dialect)

            elif isinstance(self.path_or_stream, BytesIO):
                # Convert BytesIO to StringIO for CSV reading
                raw_content = self.path_or_stream.read()
                self.encoding = self._detect_encoding(raw_content)
                content = raw_content.decode(self.encoding)

                if not content.strip():
                    self.valid = True
                    return

                dialect = self._detect_dialect(content)
                self.rows = self._parse_csv(content, dialect)

            # Add debug logging
            _log.info(
                f"Loaded {len(self.rows)} rows from CSV file using {self.encoding} encoding"
            )
            self.valid = True
        except Exception as e:
            self.valid = False
            raise RuntimeError(
                f"CsvDocumentBackend could not load document with hash {self.document_hash}"
            ) from e

    def _detect_encoding(self, raw_content: bytes) -> str:
        """
        Detect the file encoding.
        Falls back to utf-8 if detection fails.
        """
        try:
            # Remove BOM if present
            if raw_content.startswith(b"\xef\xbb\xbf"):
                raw_content = raw_content[3:]
                return "utf-8"

            result = chardet.detect(raw_content)
            if result["confidence"] > 0.7:
                return result["encoding"]
            return "utf-8"
        except Exception as e:
            _log.warning(f"Failed to detect encoding: {e}. Falling back to UTF-8.")
            return "utf-8"

    def _detect_dialect(self, content: str) -> csv.Dialect:
        """
        Detect the CSV dialect including the delimiter.
        Falls back to comma if detection fails.
        """
        try:
            if not content.strip():
                return csv.excel

            # Try to detect the dialect using a larger sample for files with long headers
            sample_size = min(len(content), 4096)  # Use up to 4KB as sample
            sample = content[:sample_size]
            sniffer = csv.Sniffer()

            # Try with common delimiters first
            dialect = sniffer.sniff(sample, delimiters=",;\t|")
            _log.info(f"Detected delimiter: {dialect.delimiter}")
            return dialect
        except Exception as e:
            _log.warning(
                f"Failed to detect CSV dialect: {e}. Falling back to comma delimiter."
            )
            return csv.excel

    def _parse_csv(self, content: str, dialect: csv.Dialect) -> List[List[str]]:
        """
        Parse CSV content handling various edge cases.
        """
        rows = []
        reader = csv.reader(StringIO(content), dialect=dialect)
        max_cols = 0

        for row in reader:
            # Skip completely empty rows
            if not any(cell.strip() for cell in row):
                continue

            # Track maximum number of columns
            max_cols = max(max_cols, len(row))
            rows.append(row)

        # Normalize row lengths
        for i, row in enumerate(rows):
            if len(row) < max_cols:
                # Pad shorter rows with empty strings
                rows[i] = row + [""] * (max_cols - len(row))
                _log.warning(
                    f"Row {i} had {len(row)} columns, expected {max_cols}. Padded with empty values."
                )

        return rows

    def is_valid(self) -> bool:
        return self.valid

    @classmethod
    def supports_pagination(cls) -> bool:
        return False  # CSV files do not support pagination

    def unload(self):
        if isinstance(self.path_or_stream, BytesIO):
            self.path_or_stream.close()
        self.path_or_stream = None

    @classmethod
    def supported_formats(cls) -> Set[InputFormat]:
        return {InputFormat.CSV}

    def convert(self) -> DoclingDocument:
        # Handle the filename for both Path and BytesIO cases
        if isinstance(self.path_or_stream, Path):
            filename = self.path_or_stream.name
            stem = self.path_or_stream.stem
        else:
            filename = "file.csv"
            stem = "file"

        origin = DocumentOrigin(
            filename=filename,
            mimetype="text/csv",
            binary_hash=self.document_hash,
        )
        doc = DoclingDocument(name=stem, origin=origin)

        if self.is_valid():
            if not self.rows:
                return doc

            # Create a table from the CSV data
            num_rows = len(self.rows)
            num_cols = len(self.rows[0]) if self.rows else 0

            table_data = TableData(
                num_rows=num_rows,
                num_cols=num_cols,
                table_cells=[],
            )

            # Convert each cell to a TableCell
            for row_idx, row in enumerate(self.rows):
                for col_idx, cell_value in enumerate(row):
                    cell = TableCell(
                        text=str(cell_value).strip(),
                        row_span=1,
                        col_span=1,
                        start_row_offset_idx=row_idx,
                        end_row_offset_idx=row_idx + 1,
                        start_col_offset_idx=col_idx,
                        end_col_offset_idx=col_idx + 1,
                        col_header=(row_idx == 0),  # First row is header
                        row_header=False,
                    )
                    table_data.table_cells.append(cell)

            # Add the table to the document
            doc.add_table(data=table_data, parent=None)
        else:
            raise RuntimeError(
                f"Cannot convert doc with {self.document_hash} because the backend failed to init."
            )

        return doc
