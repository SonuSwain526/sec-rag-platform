import { useState, useEffect } from "react";

const STAGES = [
  "Searching filings...",
  "Ranking relevant sections...",
  "Drafting an answer...",
  "Checking figures against SEC data...",
];

export function ThinkingIndicator() {
  const [stageIndex, setStageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStageIndex((i) => Math.min(i + 1, STAGES.length - 1));
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="inline-flex items-center gap-2 bg-zinc-100 rounded-lg px-4 py-2.5 text-sm text-zinc-500">
      <span className="flex gap-1">
        <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce [animation-delay:-0.3s]" />
        <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce [animation-delay:-0.15s]" />
        <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 animate-bounce" />
      </span>
      {STAGES[stageIndex]}
    </div>
  );
}