import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import type { Message } from "@/lib/types";
import { ThinkingIndicator } from "@/components/ThinkingIndicator";
import { Send } from "lucide-react";

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

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
        { role: "assistant", content: result.answer, sources: result.sources, verification: result.verification },
      ]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong";
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${message}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-56px)] max-w-3xl mx-auto">
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-5">
        {messages.length === 0 && (
          <div className="text-center mt-16">
            <p className="text-zinc-400 text-sm mb-3">Ask about a 10-K filing to get started</p>
            <div className="flex flex-wrap gap-2 justify-center max-w-md mx-auto">
              {[
                "What was Apple's total revenue in fiscal year 2025?",
                "Compare Apple and Microsoft's risk factors",
                "Microsoft's cybersecurity measures",
              ].map((q) => (
                <button
                  key={q}
                  onClick={() => setInput(q)}
                  className="text-xs text-zinc-600 bg-zinc-50 border rounded-full px-3 py-1.5 hover:bg-zinc-100 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={msg.role === "user" ? "flex justify-end" : "flex justify-start"}>
            <div className="max-w-[85%]">
              <div
                className={`rounded-lg px-4 py-2.5 text-[14px] leading-relaxed ${
                  msg.role === "user" ? "bg-zinc-900 text-white" : "bg-white border text-zinc-800"
                }`}
              >
                {msg.content}
              </div>

              {msg.role === "assistant" && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {msg.verification && msg.verification.length > 0 ? (
                    msg.verification.map((v, vi) => (
                      <span
                        key={vi}
                        className={`text-xs font-medium px-2 py-1 rounded-md ${
                          v.status === "verified"
                            ? "bg-green-50 text-green-700"
                            : v.status === "discrepancy"
                            ? "bg-orange-50 text-orange-700"
                            : "bg-zinc-100 text-zinc-500"
                        }`}
                      >
                        {v.status === "verified" ? "✓ Verified" : v.status === "discrepancy" ? "⚠ Discrepancy" : "? Unverifiable"}
                        {v.metric ? ` · ${v.metric}` : ""}
                      </span>
                    ))
                  ) : (
                    <span className="text-[11px] text-zinc-400 italic">No verifiable figures in this answer</span>
                  )}
                </div>
              )}

              {msg.role === "assistant" && !!msg.sources?.length && (
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {[...new Set(msg.sources.map((s) => `${s.company} FY${s.fiscal_year} · Item ${s.item_code}`))].map(
                    (src, si) => (
                      <span key={si} className="text-[11px] text-zinc-400 border rounded px-1.5 py-0.5">
                        {src}
                      </span>
                    )
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <ThinkingIndicator />
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      <form onSubmit={handleSend} className="border-t bg-white p-3 flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about a 10-K filing..."
          disabled={loading}
          className="text-sm"
        />
        <Button type="submit" disabled={loading || !input.trim()} className="bg-blue-600 hover:bg-blue-700 px-3">
          <Send size={16} />
        </Button>
      </form>
    </div>
  );
}