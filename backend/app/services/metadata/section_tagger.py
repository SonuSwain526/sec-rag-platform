import re
from dataclasses import dataclass

from docling_core.types.doc.document import DoclingDocument
from docling_core.types.doc.labels import DocItemLabel

# Matches "Item 7.", "Item 7A.", "Item 7.    Management's Discussion..."
# Group 3 captures anything after the item code on the SAME text item —
# a real section header has its title inline; a Table of Contents entry
# is just the bare "Item 7." with nothing else, so group 3 is blank there.
ITEM_PATTERN = re.compile(r"^Item\s+(\d{1,2})([A-Z]?)\.?\s*(.*)$", re.IGNORECASE)


@dataclass
class Section:
    """One detected section of the filing, e.g. 'Item 7. Management's Discussion...'."""
    item_code: str
    title: str
    start_ref: str


class SectionTagger:
    """
    Detects SEC 10-K "Item X" section boundaries in a Docling document.
    SEC's HTML has no real heading tags, so every 'Item X' marker is
    just plain text. A real section header carries its title inline on
    the same text item; a Table of Contents entry is a bare marker with
    nothing else — confirmed against real filing data with no exceptions.
    """

    def find_sections(self, doc: DoclingDocument) -> list[Section]:
        candidates = self._find_item_markers(doc)
        return self._filter_toc_entries(candidates)

    def _find_item_markers(self, doc: DoclingDocument) -> list[tuple]:
        """Returns (item_code, inline_title, docling_item) for every 'Item X' match, in document order."""
        matches = []
        for item, _level in doc.iterate_items():
            if item.label != DocItemLabel.TEXT:
                continue
            text = item.text.strip() if item.text else ""
            match = ITEM_PATTERN.match(text)
            if match:
                item_code = match.group(1) + match.group(2)
                inline_title = match.group(3).strip()
                matches.append((item_code, inline_title, item))
        return matches

    def _filter_toc_entries(self, candidates: list) -> list[Section]:
        """
        Keeps only markers with a non-blank inline title.
        TOC entries are bare markers with nothing else on the line —
        always blank inline title. Real section headers always carry
        their title inline. Verified with zero exceptions on real data.
        """
        real_sections = []
        for item_code, inline_title, item in candidates:
            if not inline_title:
                continue
            real_sections.append(
                Section(item_code=item_code, title=inline_title, start_ref=item.self_ref)
            )
        return real_sections