import re
from dataclasses import dataclass

from docling_core.types.doc.document import DoclingDocument
from docling_core.types.doc.labels import DocItemLabel

ITEM_PATTERN = re.compile(r"^Item\s+(\d{1,2})([A-Z]?)\.?\s*(.*)$", re.IGNORECASE)


@dataclass
class Section:
    """One detected section of the filing, e.g. 'Item 7. Management's Discussion...'."""
    item_code: str
    title: str
    start_ref: str


class SectionTagger:
    """
    Detects SEC 10-K "Item X" section boundaries in a Docling document,
    and slices document content into those sections.
    """

    def find_sections(self, doc: DoclingDocument) -> list[Section]:
        candidates = self._find_item_markers(doc)
        return self._filter_toc_entries(candidates)

    def get_section_content(self, doc: DoclingDocument, sections: list[Section]) -> dict[str, list]:
        """
        Slices the document into content grouped by section.
        Returns a dict mapping item_code -> list of Docling items belonging
        to that section (everything between this section's start and the
        next section's start; the last section runs to the end of doc).
        """
        section_starts = {section.start_ref: section.item_code for section in sections}
        content_by_section: dict[str, list] = {section.item_code: [] for section in sections}

        current_section_code: str | None = None

        for item, _level in doc.iterate_items():
            if item.self_ref in section_starts:
                current_section_code = section_starts[item.self_ref]

            if current_section_code is not None:
                content_by_section[current_section_code].append(item)

        return content_by_section

    def _find_item_markers(self, doc: DoclingDocument) -> list[tuple]:
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
        real_sections = []
        for item_code, inline_title, item in candidates:
            if not inline_title:
                continue
            real_sections.append(
                Section(item_code=item_code, title=inline_title, start_ref=item.self_ref)
            )
        return real_sections