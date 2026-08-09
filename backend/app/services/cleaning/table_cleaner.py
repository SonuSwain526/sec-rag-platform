from docling_core.types.doc.document import DoclingDocument, TableItem


class TableCleaner:
    """
    Removes fully-empty layout tables from a parsed document, using
    Docling's own delete_items() method (safe — repairs internal
    document references correctly).

    NOTE: We deliberately do NOT mutate cell content here (e.g. to
    de-duplicate repeated spanned-cell text). Some filers' HTML causes
    Docling to represent a single spanned cell as the SAME object
    repeated across multiple grid positions — mutating one occurrence
    silently corrupts the only real copy of that data. De-duplication
    is instead handled at read-time (see Chunker._table_to_text),
    which is always safe since it never modifies the source document.
    """

    def clean(self, doc: DoclingDocument) -> DoclingDocument:
        empty_tables = [table for table in doc.tables if self._is_empty_table(table)]
        if empty_tables:
            doc.delete_items(node_items=empty_tables)
        return doc

    def _is_empty_table(self, table: TableItem) -> bool:
        for cell in table.data.table_cells:
            if cell.text and cell.text.strip():
                return False
        return True