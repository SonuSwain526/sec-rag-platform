from docling_core.types.doc.document import DoclingDocument, TableItem


class TableCleaner:
    """
    Cleans known Docling artifacts from parsed SEC 10-K tables:

    1. Fully-empty layout tables — removed entirely via Docling's
       delete_items(), which safely repairs internal document references.

    2. Duplicated spanned cells — collapsed back to a single value.

    NOTE: We deliberately do NOT remove "mostly empty" tables based on
    a fill-ratio threshold. Real financial tables (e.g., the Statement
    of Operations) also have mostly-blank cells, used as spacing/
    alignment columns around a few real values — a fill-ratio filter
    would delete real financial data along with genuine junk. Only
    100%-empty tables are safe to remove automatically.
    """

    def clean(self, doc: DoclingDocument) -> DoclingDocument:
        empty_tables = [table for table in doc.tables if self._is_empty_table(table)]
        if empty_tables:
            doc.delete_items(node_items=empty_tables)

        for table in doc.tables:
            self._deduplicate_cells(table)

        return doc

    def _is_empty_table(self, table: TableItem) -> bool:
        """True if every cell in the table is blank or whitespace-only."""
        for cell in table.data.table_cells:
            if cell.text and cell.text.strip():
                return False
        return True

    def _deduplicate_cells(self, table: TableItem) -> None:
        for row in table.data.grid:
            seen_text: str | None = None
            for cell in row:
                current = cell.text.strip() if cell.text else ""
                if current and current == seen_text:
                    cell.text = ""
                else:
                    seen_text = current if current else seen_text