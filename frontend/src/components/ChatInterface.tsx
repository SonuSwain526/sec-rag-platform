import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import type { Message } from "@/lib/types";

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const question = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const result = await api.query(question, true);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
          sources: result.sources,
          verification: result.verification,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto">
      <div className="border-b p-4">
        <h1 className="text-lg font-semibold">SEC Filings Q&A</h1>
        <p className="text-sm text-slate-500">Ask about Apple, Microsoft, Google, Amazon, or Meta's 10-K filings</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <p className="text-slate-400 text-sm text-center mt-8">
            Try: "What was Apple's total revenue in fiscal year 2025?"
          </p>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={msg.role === "user" ? "text-right" : "text-left"}>
            <div
              className={`inline-block max-w-[85%] rounded-lg px-4 py-2 text-sm ${
                msg.role === "user"
                  ? "bg-slate-900 text-white"
                  : "bg-slate-100 text-slate-900"
              }`}
            >
              {msg.content}
            </div>

            {msg.role === "assistant" && msg.verification && msg.verification.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {msg.verification.map((v, vi) => (
                  <Badge
                    key={vi}
                    variant={v.status === "verified" ? "default" : "destructive"}
                  >
                    {v.status === "verified" ? "✅ Verified" : v.status === "discrepancy" ? "⚠️ Discrepancy" : "❓ Unverifiable"}
                    {v.metric ? `: ${v.metric}` : ""}
                  </Badge>
                ))}
              </div>
            )}

            {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {[...new Set(msg.sources.map((s) => `${s.company} FY${s.fiscal_year} Item ${s.item_code}`))].map(
                  (src, si) => (
                    <Badge key={si} variant="outline" className="text-xs">
                      {src}
                    </Badge>
                  )
                )}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="text-left">
            <div className="inline-block bg-slate-100 rounded-lg px-4 py-2 text-sm text-slate-500">
              Thinking...
            </div>
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      <form onSubmit={handleSend} className="border-t p-4 flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about a 10-K filing..."
          disabled={loading}
        />
        <Button type="submit" disabled={loading || !input.trim()}>
          Send
        </Button>
      </form>
    </div>
  );
}