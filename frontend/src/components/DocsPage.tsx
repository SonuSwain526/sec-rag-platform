export function DocsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-semibold text-zinc-900 mb-2">About this project</h1>
      <p className="text-zinc-500 mb-10 text-[15px]">
        A retrieval-augmented Q&A system for SEC 10-K filings, built with verified,
        cited answers — not just plausible-sounding ones.
      </p>

      <div className="space-y-8">
        <Section title="What it does">
          Ask a plain-English question about Apple, Microsoft, Alphabet, Amazon, or
          Meta's annual reports (10-Ks), and get a direct answer — with the exact
          section it came from, instead of reading a 100+ page filing yourself.
        </Section>

        <Section title="How answers are verified">
          Every numeric answer is cross-checked against SEC's own official XBRL
          structured data — an independent source, separate from the document text.
          A <Badge label="✅ Verified" tone="success" /> badge means the figure matches
          SEC's official records; <Badge label="⚠️ Discrepancy" tone="warning" /> flags
          a mismatch worth double-checking.
        </Section>

        <Section title="How retrieval works">
          Filings are parsed with structure-aware extraction (preserving tables and
          section headings), split into focused chunks, and searched using a hybrid
          of semantic search and keyword matching, then re-ranked for precision
          before being sent to the language model.
        </Section>

        <Section title="Coverage">
          5 companies × the last 3 fiscal years each — Apple, Microsoft, Alphabet,
          Amazon, and Meta.
        </Section>

        <Section title="Try asking">
          <ul className="list-disc list-inside space-y-1 text-zinc-600">
            <li>"What was Apple's total revenue in fiscal year 2025?"</li>
            <li>"Compare Apple and Microsoft's approach to risk factors."</li>
            <li>"What cybersecurity measures has Microsoft implemented?"</li>
          </ul>
        </Section>
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h2 className="text-sm font-medium text-zinc-900 mb-2 uppercase tracking-wide">{title}</h2>
      <div className="text-[15px] text-zinc-600 leading-relaxed">{children}</div>
    </div>
  );
}

function Badge({ label, tone }: { label: string; tone: "success" | "warning" }) {
  const cls = tone === "success" ? "bg-green-50 text-green-700" : "bg-orange-50 text-orange-700";
  return <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${cls} mx-0.5`}>{label}</span>;
}