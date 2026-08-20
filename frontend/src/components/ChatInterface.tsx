// import { useState, useRef, useEffect } from "react";
// import { Button } from "@/components/ui/button";
// import { Input } from "@/components/ui/input";
// import { api } from "@/lib/api";
// import type { Message } from "@/lib/types";
// import { ThinkingIndicator } from "@/components/ThinkingIndicator";
// import { Send } from "lucide-react";

// export function ChatInterface() {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const scrollRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     scrollRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages, loading]);

//   async function handleSend(e: React.FormEvent) {
//     e.preventDefault();
//     if (!input.trim() || loading) return;

//     const question = input.trim();
//     setInput("");
//     setMessages((prev) => [...prev, { role: "user", content: question }]);
//     setLoading(true);

//     try {
//       const result = await api.query(question, true);
//       setMessages((prev) => [
//         ...prev,
//         { role: "assistant", content: result.answer, sources: result.sources, verification: result.verification },
//       ]);
//     } catch (err) {
//       const message = err instanceof Error ? err.message : "Something went wrong";
//       setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${message}` }]);
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="flex flex-col h-[calc(100vh-56px)] max-w-3xl mx-auto">
//       <div className="flex-1 overflow-y-auto px-4 py-6 space-y-5">
//         {messages.length === 0 && (
//           <div className="text-center mt-16">
//             <p className="text-zinc-400 text-sm mb-3">Ask about a 10-K filing to get started</p>
//             <div className="flex flex-wrap gap-2 justify-center max-w-md mx-auto">
//               {[
//                 "What was Apple's total revenue in fiscal year 2025?",
//                 "Compare Apple and Microsoft's risk factors",
//                 "Microsoft's cybersecurity measures",
//               ].map((q) => (
//                 <button
//                   key={q}
//                   onClick={() => setInput(q)}
//                   className="text-xs text-zinc-600 bg-zinc-50 border rounded-full px-3 py-1.5 hover:bg-zinc-100 transition-colors"
//                 >
//                   {q}
//                 </button>
//               ))}
//             </div>
//           </div>
//         )}

//         {messages.map((msg, i) => (
//           <div key={i} className={msg.role === "user" ? "flex justify-end" : "flex justify-start"}>
//             <div className="max-w-[85%]">
//               <div
//                 className={`rounded-lg px-4 py-2.5 text-[14px] leading-relaxed ${
//                   msg.role === "user" ? "bg-zinc-900 text-white" : "bg-white border text-zinc-800"
//                 }`}
//               >
//                 {msg.content}
//               </div>

//               {msg.role === "assistant" && (
//                 <div className="mt-2 flex flex-wrap gap-1.5">
//                   {msg.verification && msg.verification.length > 0 ? (
//                     msg.verification.map((v, vi) => (
//                       <span
//                         key={vi}
//                         className={`text-xs font-medium px-2 py-1 rounded-md ${
//                           v.status === "verified"
//                             ? "bg-green-50 text-green-700"
//                             : v.status === "discrepancy"
//                             ? "bg-orange-50 text-orange-700"
//                             : "bg-zinc-100 text-zinc-500"
//                         }`}
//                       >
//                         {v.status === "verified" ? "✓ Verified" : v.status === "discrepancy" ? "⚠ Discrepancy" : "? Unverifiable"}
//                         {v.metric ? ` · ${v.metric}` : ""}
//                       </span>
//                     ))
//                   ) : (
//                     <span className="text-[11px] text-zinc-400 italic">No verifiable figures in this answer</span>
//                   )}
//                 </div>
//               )}

//               {msg.role === "assistant" && !!msg.sources?.length && (
//                 <div className="mt-1.5 flex flex-wrap gap-1">
//                   {[...new Set(msg.sources.map((s) => `${s.company} FY${s.fiscal_year} · Item ${s.item_code}`))].map(
//                     (src, si) => (
//                       <span key={si} className="text-[11px] text-zinc-400 border rounded px-1.5 py-0.5">
//                         {src}
//                       </span>
//                     )
//                   )}
//                 </div>
//               )}
//             </div>
//           </div>
//         ))}

//         {loading && (
//           <div className="flex justify-start">
//             <ThinkingIndicator />
//           </div>
//         )}

//         <div ref={scrollRef} />
//       </div>

//       <form onSubmit={handleSend} className="border-t bg-white p-3 flex gap-2">
//         <Input
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="Ask about a 10-K filing..."
//           disabled={loading}
//           className="text-sm"
//         />
//         <Button type="submit" disabled={loading || !input.trim()} className="bg-blue-600 hover:bg-blue-700 px-3">
//           <Send size={16} />
//         </Button>
//       </form>
//     </div>
//   );
// }

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import type { Message } from "@/lib/types";
import { ThinkingIndicator } from "@/components/ThinkingIndicator";
import { Send } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Shared markdown renderer for assistant messages — keeps table/list/heading
// styling consistent with the rest of the chat UI (zinc/blue palette).
const markdownComponents = {
  p: ({ children }: { children?: React.ReactNode }) => <p className="mb-2 last:mb-0">{children}</p>,
  strong: ({ children }: { children?: React.ReactNode }) => (
    <strong className="font-semibold text-zinc-900">{children}</strong>
  ),
  ul: ({ children }: { children?: React.ReactNode }) => (
    <ul className="list-disc pl-5 mb-2 space-y-1">{children}</ul>
  ),
  ol: ({ children }: { children?: React.ReactNode }) => (
    <ol className="list-decimal pl-5 mb-2 space-y-1">{children}</ol>
  ),
  li: ({ children }: { children?: React.ReactNode }) => <li className="leading-relaxed">{children}</li>,
  h1: ({ children }: { children?: React.ReactNode }) => (
    <h1 className="text-base font-semibold text-zinc-900 mt-3 mb-1.5 first:mt-0">{children}</h1>
  ),
  h2: ({ children }: { children?: React.ReactNode }) => (
    <h2 className="text-[15px] font-semibold text-zinc-900 mt-3 mb-1.5 first:mt-0">{children}</h2>
  ),
  h3: ({ children }: { children?: React.ReactNode }) => (
    <h3 className="text-sm font-semibold text-zinc-900 mt-2.5 mb-1 first:mt-0">{children}</h3>
  ),
  table: ({ children }: { children?: React.ReactNode }) => (
    <div className="overflow-x-auto mb-2 rounded-md border">
      <table className="w-full text-left border-collapse text-[13px]">{children}</table>
    </div>
  ),
  thead: ({ children }: { children?: React.ReactNode }) => <thead className="bg-zinc-50">{children}</thead>,
  th: ({ children }: { children?: React.ReactNode }) => (
    <th className="px-3 py-1.5 font-medium text-zinc-700 border-b">{children}</th>
  ),
  td: ({ children }: { children?: React.ReactNode }) => (
    <td className="px-3 py-1.5 border-b border-zinc-100 align-top">{children}</td>
  ),
  code: ({ children }: { children?: React.ReactNode }) => (
    <code className="bg-zinc-100 text-zinc-800 rounded px-1 py-0.5 text-[13px]">{children}</code>
  ),
  a: ({ children, href }: { children?: React.ReactNode; href?: string }) => (
    <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
      {children}
    </a>
  ),
};

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
                {msg.role === "assistant" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
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