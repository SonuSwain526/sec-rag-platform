import re
from dataclasses import dataclass

from docling_core.types.doc.document import DoclingDocument
from docling_core.types.doc.labels import DocItemLabel

ITEM_PATTERN = re.compile(r"^Item\s+(\d{1,2})([A-Z]?)\.?\s*(.*)$", re.IGNORECASE)
PAGE_NUMBER_PATTERN = re.compile(r"^\d{1,4}$")


@dataclass
class Section:
    item_code: str
    title: str
    start_ref: str


class SectionTagger:
    """
    Detects SEC 10-K "Item X" section boundaries. Different filers format
    headings differently:
      - Apple-style: headings are plain text, with the title inline on
        the same text item. Table of Contents entries are bare markers
        with no inline title.
      - Amazon-style: headings live inside table cells instead. Each
        REAL section gets its own dedicated table containing only that
        one Item. The Table of Contents is one single table containing
        ALL Items together, each row also carrying a page number.
    We detect both patterns and merge the results.
    """

    def find_sections(self, doc: DoclingDocument) -> list[Section]:
        text_sections = self._find_text_based_sections(doc)
        table_sections = self._find_table_based_sections(doc)
        return self._merge_and_order(doc, text_sections + table_sections)

    def get_section_content(self, doc: DoclingDocument, sections: list[Section]) -> dict[str, list]:
        section_starts = {section.start_ref: section.item_code for section in sections}
        content_by_section: dict[str, list] = {section.item_code: [] for section in sections}
        current_section_code: str | None = None

        for item, _level in doc.iterate_items():
            if item.self_ref in section_starts:
                current_section_code = section_starts[item.self_ref]
            if current_section_code is not None:
                content_by_section[current_section_code].append(item)

        return content_by_section

    # ---- Apple-style: plain text headings ----

    def _find_text_based_sections(self, doc: DoclingDocument) -> list[Section]:
        real_sections = []
        for item, _level in doc.iterate_items():
            if item.label != DocItemLabel.TEXT:
                continue
            text = item.text.strip() if item.text else ""
            match = ITEM_PATTERN.match(text)
            if not match:
                continue
            item_code = match.group(1) + match.group(2)
            inline_title = match.group(3).strip()
            if inline_title:  # bare marker with no title = Table of Contents entry, skip
                real_sections.append(Section(item_code=item_code, title=inline_title, start_ref=item.self_ref))
        return real_sections

    # ---- Amazon-style: headings inside dedicated tables ----

    def _find_table_based_sections(self, doc: DoclingDocument) -> list[Section]:
        real_sections = []
        for table in doc.tables:
            matches_in_table = self._item_matches_in_table(table)
            distinct_codes = {code for code, _title in matches_in_table}

            # A table listing MORE than one distinct Item is a Table of
            # Contents — real sections always get their own dedicated table.
            if len(distinct_codes) != 1:
                continue

            item_code, title = matches_in_table[0]
            if title:
                real_sections.append(Section(item_code=item_code, title=title, start_ref=table.self_ref))

        return real_sections

    def _item_matches_in_table(self, table) -> list[tuple[str, str]]:
        """Scans a table's rows for 'Item X' markers, pairing each with its title (the next non-blank, non-page-number cell in the same row)."""
        matches = []
        for row in table.data.grid:
            cell_texts = [cell.text.strip() if cell.text else "" for cell in row]
            non_blank = [t for t in cell_texts if t]
            if not non_blank:
                continue

            first_cell = non_blank[0]
            match = ITEM_PATTERN.match(first_cell)
            if not match:
                continue

            item_code = match.group(1) + match.group(2)
            title = ""
            for cell_text in non_blank[1:]:
                if PAGE_NUMBER_PATTERN.match(cell_text) or cell_text == first_cell:
                    continue  # skip page numbers and duplicate repeats of the marker itself
                title = cell_text
                break

            matches.append((item_code, title))
        return matches

    # ---- Merge both sources, ordered by real document position ----

    def _merge_and_order(self, doc: DoclingDocument, sections: list[Section]) -> list[Section]:
        """Orders sections by their real position in the document, and
        removes duplicates (keeping the first occurrence) in case both
        detection methods somehow matched the same section."""
        position_by_ref = {}
        for position, (item, _level) in enumerate(doc.iterate_items()):
            position_by_ref[item.self_ref] = position

        sections_with_position = [
            (position_by_ref.get(s.start_ref, float("inf")), s) for s in sections
        ]
        sections_with_position.sort(key=lambda pair: pair[0])

        seen_codes = set()
        ordered_unique = []
        for _position, section in sections_with_position:
            if section.item_code in seen_codes:
                continue
            seen_codes.add(section.item_code)
            ordered_unique.append(section)

        return ordered_unique