import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { clearToken } from "@/lib/api";
import { FileText, MessageSquare, LogOut } from "lucide-react";

export function Navbar({ onLogout }: { onLogout: () => void }) {
  const location = useLocation();

  function handleLogout() {
    clearToken();
    onLogout();
  }

  const linkClass = (path: string) =>
    `flex items-center gap-1.5 text-sm px-3 py-1.5 rounded-md transition-colors ${
      location.pathname === path
        ? "bg-zinc-100 text-zinc-900 font-medium"
        : "text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50"
    }`;

  return (
    <nav className="border-b bg-white sticky top-0 z-10">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <span className="font-semibold text-zinc-900 text-[15px]">SEC Filings Q&A</span>
          <div className="flex items-center gap-1">
            <Link to="/" className={linkClass("/")}>
              <MessageSquare size={15} /> Chat
            </Link>
            <Link to="/docs" className={linkClass("/docs")}>
              <FileText size={15} /> Docs
            </Link>
          </div>
        </div>
        <Button variant="ghost" size="sm" onClick={handleLogout} className="text-zinc-500 hover:text-zinc-900">
          <LogOut size={15} className="mr-1.5" /> Log out
        </Button>
      </div>
    </nav>
  );
}