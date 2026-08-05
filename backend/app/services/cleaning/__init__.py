"""
Cleaning package for sec-rag.

Fixes known distortions in Docling's parsed output before chunking —
specifically, empty layout-only tables and duplicated spanned cells
that SEC EDGAR's HTML markup causes.
"""
from app.services.cleaning.table_cleaner import TableCleaner

__all__ = ["TableCleaner"]