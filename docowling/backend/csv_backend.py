import csv
from io import BytesIO, StringIO
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

from docling_core.types.doc import GroupItem  # Add this import
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


class CsvDocumentBackend(DeclarativeDocumentBackend):
    def __init__(self, in_doc: "InputDocument", path_or_stream: Union[BytesIO, Path]):
        super().__init__(in_doc, path_or_stream)
        self.rows = []
        self.parents: Dict[int, GroupItem] = {}  # Update type hint to GroupItem

        try:
            # Load the CSV data
            if isinstance(self.path_or_stream, Path):
                with self.path_or_stream.open(mode="r", encoding="utf-8") as file:
                    self.rows = list(csv.reader(file))
            elif isinstance(self.path_or_stream, BytesIO):
                # Convert BytesIO to StringIO for CSV reading
                text_content = self.path_or_stream.read().decode("utf-8")
                self.rows = list(csv.reader(StringIO(text_content)))

            self.valid = True
        except Exception as e:
            self.valid = False
            raise RuntimeError(
                f"CsvDocumentBackend could not load document with hash {self.document_hash}"
            ) from e

    def is_valid(self) -> bool:
        return self.valid

    @classmethod
    def supports_pagination(cls) -> bool:
        return False  # Typically, CSV files do not support pagination.

    def unload(self):
        self.path_or_stream = None

    @classmethod
    def supported_formats(cls) -> Set[InputFormat]:
        return {InputFormat.CSV}

    def convert(self) -> DoclingDocument:
        origin = DocumentOrigin(
            filename=self.file.name or "file.csv",
            mimetype="text/csv",
            binary_hash=self.document_hash,
        )
        doc = DoclingDocument(name=self.file.stem or "file.csv", origin=origin)

        if self.is_valid():
            doc = self._convert_csv_to_document(doc)
        else:
            raise RuntimeError(
                f"Cannot convert doc with {self.document_hash} because the backend failed to init."
            )

        return doc

    def _convert_csv_to_document(self, doc: DoclingDocument) -> DoclingDocument:
        if not self.rows:
            return doc  # No data to process

        # Create a section for the CSV data
        group_item = doc.add_group(
            parent=None,
            label=GroupLabel.SECTION,
            name="CSV Data",
        )
        self.parents[0] = group_item

        # Convert rows into table data
        num_rows = len(self.rows)
        num_cols = max(len(row) for row in self.rows)

        table_data = TableData(
            num_rows=num_rows,
            num_cols=num_cols,
            table_cells=[],
        )

        for row_idx, row in enumerate(self.rows):
            for col_idx, cell in enumerate(row):
                table_cell = TableCell(
                    text=cell,
                    row_span=1,
                    col_span=1,
                    start_row_offset_idx=row_idx,
                    end_row_offset_idx=row_idx + 1,
                    start_col_offset_idx=col_idx,
                    end_col_offset_idx=col_idx + 1,
                    col_header=False,
                    row_header=False,
                )
                table_data.table_cells.append(table_cell)

        doc.add_table(data=table_data, parent=self.parents[0])
        return doc
