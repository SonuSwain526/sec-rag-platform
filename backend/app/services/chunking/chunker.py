import uuid

from docling_core.types.doc.labels import DocItemLabel

from app.services.chunking.models import Chunk
from app.services.chunking.token_counter import count_tokens
from app.services.metadata.section_tagger import Section

MAX_CHUNK_TOKENS = 400
MIN_CHUNK_TOKENS = 50


class Chunker:
    """
    Splits section content into retrievable chunks.

    Text: paragraphs are grouped up to MAX_CHUNK_TOKENS, and any
    resulting chunk smaller than MIN_CHUNK_TOKENS gets merged into
    the next one — avoiding both oversized blurry chunks and tiny
    context-less fragments.

    Tables: always kept as one single, unsplit chunk — a partial
    table is close to useless for financial fact retrieval.
    """

    def chunk_all_sections(
        self,
        content_by_section: dict[str, list],
        sections: list[Section],
        company: str,
        fiscal_year: int,
    ) -> list[Chunk]:
        """Chunks every section in the document, returning one flat list of Chunks."""
        section_lookup = {s.item_code: s for s in sections}
        all_chunks: list[Chunk] = []

        for item_code, items in content_by_section.items():
            section = section_lookup[item_code]
            section_chunks = self._chunk_section(items, section, company, fiscal_year)
            all_chunks.extend(section_chunks)

        return all_chunks

    def _chunk_section(
        self, items: list, section: Section, company: str, fiscal_year: int
    ) -> list[Chunk]:
        chunks: list[Chunk] = []
        text_buffer: list[str] = []
        buffer_tokens = 0

        def flush_text_buffer():
            """Turns whatever's currently in text_buffer into one Chunk, if non-empty."""
            nonlocal buffer_tokens
            if text_buffer:
                content = "\n".join(text_buffer)
                chunks.append(
                    self._make_chunk(content, "text", section, company, fiscal_year)
                )
                text_buffer.clear()
                buffer_tokens = 0

        for item in items:
            if item.label == DocItemLabel.TABLE:
                # Tables always break the current text buffer and become
                # their own standalone chunk.
                flush_text_buffer()
                table_text = self._table_to_text(item)
                if table_text.strip():
                    chunks.append(
                        self._make_chunk(table_text, "table", section, company, fiscal_year)
                    )

            elif item.label == DocItemLabel.TEXT:
                text = item.text.strip() if item.text else ""
                if not text:
                    continue

                item_tokens = count_tokens(text)

                if buffer_tokens + item_tokens > MAX_CHUNK_TOKENS and buffer_tokens > 0:
                    flush_text_buffer()

                text_buffer.append(text)
                buffer_tokens += item_tokens

        flush_text_buffer()

        # Merge any resulting chunk that's too small into its neighbor,
        # so we don't end up with tiny, context-less fragments.
        return self._merge_small_chunks(chunks)

    def _merge_small_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Merges any text chunk under MIN_CHUNK_TOKENS into the next chunk (tables are never merged)."""
        if not chunks:
            return chunks

        merged: list[Chunk] = []
        i = 0
        while i < len(chunks):
            current = chunks[i]

            is_small_text = current.chunk_type == "text" and current.token_count < MIN_CHUNK_TOKENS
            has_next = i + 1 < len(chunks)
            next_is_text = has_next and chunks[i + 1].chunk_type == "text"

            if is_small_text and has_next and next_is_text:
                combined_content = current.content + "\n" + chunks[i + 1].content
                combined = self._make_chunk(
                    combined_content,
                    "text",
                    Section(item_code=current.item_code, title=current.item_title, start_ref=""),
                    current.company,
                    current.fiscal_year,
                )
                merged.append(combined)
                i += 2  # skip the next chunk since we just merged it in
            else:
                merged.append(current)
                i += 1

        return merged

    def _table_to_text(self, table_item) -> str:
            """
            Converts a table into readable text for embedding, one line per row.
            De-duplicates consecutive identical cell values within each row —
            done here at read-time (never by mutating the source document),
            since some filers' HTML causes Docling to reuse the same cell
            object across multiple spanned grid positions.
            """
            rows_text = []
            for row in table_item.data.grid:
                cell_values = [cell.text.strip() for cell in row if cell.text and cell.text.strip()]

                deduped = []
                for value in cell_values:
                    if not deduped or deduped[-1] != value:
                        deduped.append(value)

                if deduped:
                    rows_text.append(" | ".join(deduped))
            return "\n".join(rows_text)
    def _make_chunk(
        self, content: str, chunk_type: str, section: Section, company: str, fiscal_year: int
    ) -> Chunk:
        return Chunk(
            chunk_id=str(uuid.uuid4()),
            company=company,
            fiscal_year=fiscal_year,
            item_code=section.item_code,
            item_title=section.title,
            chunk_type=chunk_type,
            content=content,
            token_count=count_tokens(content),
        )