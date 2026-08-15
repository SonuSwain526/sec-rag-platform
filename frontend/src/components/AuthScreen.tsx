import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api, saveToken } from "@/lib/api";
import { FileText } from "lucide-react";

interface AuthScreenProps {
  onLoginSuccess: () => void;
}

export function AuthScreen({ onLoginSuccess }: AuthScreenProps) {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      if (isSignup) await api.signup(email, password);
      const result = await api.login(email, password);
      saveToken(result.access_token);
      onLoginSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 justify-center mb-8">
          <FileText size={20} className="text-blue-600" />
          <span className="font-semibold text-zinc-900">SEC Filings Q&A</span>
        </div>

        <div className="bg-white border rounded-lg shadow-sm p-6">
          <h1 className="text-lg font-semibold text-zinc-900 mb-1">
            {isSignup ? "Create an account" : "Welcome back"}
          </h1>
          <p className="text-sm text-zinc-500 mb-6">
            {isSignup ? "Get started with verified filing answers" : "Sign in to continue"}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-xs text-zinc-600">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="password" className="text-xs text-zinc-600">Password</Label>
              <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>

            {error && (
              <div className="bg-red-50 text-red-700 text-sm rounded-md px-3 py-2">{error}</div>
            )}

            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={loading}>
              {loading ? "Please wait..." : isSignup ? "Sign up" : "Sign in"}
            </Button>
          </form>

          <button
            type="button"
            onClick={() => setIsSignup(!isSignup)}
            className="text-sm text-zinc-500 hover:text-zinc-900 w-full text-center mt-5"
          >
            {isSignup ? "Already have an account? " : "Need an account? "}
            <span className="text-blue-600 font-medium">{isSignup ? "Sign in" : "Sign up"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}